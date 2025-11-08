from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time
import re
import unicodedata


class BplayScraper:
    def __init__(self, use_firefox=True):
        """
        Inicializa el scraper de Bplay.

        Args:
            use_firefox: Si es True, usa Firefox. Si es False, usa Chrome.
        """
        self.driver = None
        self.use_firefox = use_firefox
        self.setup_driver()

    def obtener_partidos_en_vivo(self):
        """
        Obtiene una lista de todos los partidos en vivo disponibles en Bplay.

        Returns:
            list: Lista de diccionarios con información de cada partido.
                  Cada diccionario contiene: url, equipo_local, equipo_visitante, etc.
            None: Si hay algún error
        """
        try:
            # URL de la sección de deportes en vivo de Bplay
            url_live = "https://deportespba.bplay.bet.ar/en-vivo"

            print(f"Accediendo a la página de eventos en vivo de Bplay...")
            self.driver.get(url_live)

            # Esperamos a que la página cargue
            wait = WebDriverWait(self.driver, 20)
            time.sleep(5)  # Tiempo adicional para que cargue el contenido dinámico

            print("Buscando partidos de fútbol en vivo...")

            # Bplay organiza los partidos por deporte y torneo
            # Buscamos todos los links que apuntan a partidos individuales
            # Estos links generalmente tienen un formato específico
            enlaces_partidos = self.driver.find_elements(
                By.XPATH, "//a[contains(@href, '/live/')]"
            )

            partidos = []
            urls_procesadas = set()  # Para evitar duplicados

            for enlace in enlaces_partidos:
                try:
                    href = enlace.get_attribute("href")

                    # Filtramos solo los que parecen ser partidos individuales
                    # La URL tiene formato: /live/ID-equipo1-equipo2
                    if not href or href in urls_procesadas:
                        continue

                    # Extraemos el texto del enlace que podría contener los nombres de los equipos
                    texto_enlace = enlace.text.strip()

                    if not texto_enlace or len(texto_enlace) < 5:
                        continue

                    # Intentamos extraer los nombres de los equipos del href
                    partido_info = self._extraer_info_desde_url(href, texto_enlace)

                    if partido_info:
                        urls_procesadas.add(href)
                        partidos.append(partido_info)

                except Exception as e:
                    continue

            print(f"✓ Se encontraron {len(partidos)} partidos en vivo en Bplay")
            return partidos

        except Exception as e:
            print(f"Error al obtener partidos en vivo de Bplay: {e}")
            import traceback

            traceback.print_exc()
            return None

    def _extraer_info_desde_url(self, url, texto):
        """
        Extrae información del partido desde la URL y el texto del enlace.

        La URL de Bplay tiene formato: /live/12345-equipo-local-equipo-visitante
        """
        try:
            # Extraemos la última parte de la URL
            partes = url.split("/live/")
            if len(partes) < 2:
                return None

            slug = partes[1]

            # El slug tiene formato: ID-equipo1-equipo2
            # Separamos por guiones
            componentes = slug.split("-")

            if len(componentes) < 3:
                return None

            # El primer componente es el ID
            partido_id = componentes[0]

            # El resto son los nombres de equipos separados por guiones
            # Necesitamos encontrar dónde termina un equipo y empieza el otro
            # Esto es complicado porque los nombres pueden tener guiones

            # Estrategia: buscar "vs" en el texto o asumir que es mitad y mitad
            resto = "-".join(componentes[1:])

            # Intentamos dividir por "vs" primero
            if " vs " in texto.lower():
                equipos = texto.split(" vs ")
                if len(equipos) == 2:
                    equipo_local = equipos[0].strip()
                    equipo_visitante = equipos[1].strip()
                else:
                    # Fallback: dividir el slug en dos mitades
                    palabras = resto.split("-")
                    mitad = len(palabras) // 2
                    equipo_local = " ".join(palabras[:mitad])
                    equipo_visitante = " ".join(palabras[mitad:])
            else:
                # Usar el slug para extraer nombres
                palabras = resto.split("-")
                mitad = len(palabras) // 2
                equipo_local = " ".join(palabras[:mitad])
                equipo_visitante = " ".join(palabras[mitad:])

            return {
                "id": partido_id,
                "url": url,
                "equipo_local": equipo_local.title(),
                "equipo_visitante": equipo_visitante.title(),
                "equipo_local_normalizado": self._normalizar_nombre_equipo(
                    equipo_local
                ),
                "equipo_visitante_normalizado": self._normalizar_nombre_equipo(
                    equipo_visitante
                ),
                "texto_original": texto,
            }

        except Exception as e:
            return None

    def _normalizar_nombre_equipo(self, nombre):
        """
        Normaliza el nombre de un equipo para facilitar la comparación.
        Debe ser idéntico al método en SofaScoreScraper.
        """
        # Convertir a minúsculas
        nombre = nombre.lower()

        # Eliminar acentos y diacríticos
        nombre = "".join(
            c
            for c in unicodedata.normalize("NFD", nombre)
            if unicodedata.category(c) != "Mn"
        )

        # Eliminar caracteres especiales excepto espacios y guiones
        nombre = "".join(c if c.isalnum() or c in " -" else "" for c in nombre)

        # Reducir espacios múltiples a uno solo y eliminar espacios al inicio/final
        nombre = " ".join(nombre.split())

        return nombre

    def setup_driver(self):
        """
        Configura el driver del navegador con las opciones necesarias.
        Intenta usar Firefox por defecto (mejor compatibilidad con Linux).
        Si Firefox no está disponible, intenta con Chrome.
        """
        if self.use_firefox:
            try:
                self._setup_firefox()
                print("Firefox driver iniciado correctamente")
                return
            except Exception as e:
                print(f"No se pudo iniciar Firefox: {e}")
                print("Intentando con Chrome...")
                self.use_firefox = False

        # Si llegamos acá, intentamos con Chrome
        try:
            self._setup_chrome()
            print("Chrome driver iniciado correctamente")
        except Exception as e:
            print(f"Error al iniciar Chrome driver: {e}")
            print("\nAsegúrate de tener instalado uno de estos navegadores:")
            print("  - Para Firefox: sudo dnf install firefox")
            print("  - Para Chrome/Chromium: sudo dnf install chromium")
            raise

    def _setup_firefox(self):
        """Configura Firefox como navegador."""
        options = webdriver.FirefoxOptions()

        # Ejecutar sin interfaz gráfica (en segundo plano)
        options.add_argument("--headless")

        # Simular un navegador real
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        options.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        )

        # Usar webdriver-manager para descargar geckodriver automáticamente
        service = FirefoxService(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service, options=options)

    def _setup_chrome(self):
        """Configura Chrome como navegador."""
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager

        options = webdriver.ChromeOptions()

        # Ejecutar sin interfaz gráfica (en segundo plano)
        options.add_argument("--headless")

        # Opciones para mejorar el rendimiento y evitar problemas
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        # Simular un navegador real para evitar detección de bots
        options.add_argument("--window-size=1920,1080")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        # Buscar el binario de Chrome/Chromium en ubicaciones comunes de Linux
        chrome_paths = [
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium",
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
        ]

        import os

        for path in chrome_paths:
            if os.path.exists(path):
                options.binary_location = path
                break

        # Usar webdriver-manager para descargar chromedriver automáticamente
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def obtener_tiempo_partido(self, url_partido):
        """
        Obtiene el minuto actual de un partido en Bplay.

        Args:
            url_partido: La URL completa del partido en Bplay

        Returns:
            float: El minuto actual del partido
            None: Si hay algún error o el partido no está en vivo
        """
        try:
            print(f"Accediendo a Bplay: {url_partido}")
            self.driver.get(url_partido)

            # Usamos una espera inteligente: esperamos hasta que aparezca el elemento
            # que contiene el tiempo, con un máximo de 30 segundos
            print("Esperando a que la página cargue...")
            wait = WebDriverWait(self.driver, 30)

            try:
                # Esperamos específicamente a que aparezca un elemento con clase "time"
                # que además tenga contenido visible (no esté vacío)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "time")))
                print("✓ Elemento de tiempo detectado")

                # Damos un segundo adicional para que termine de renderizarse completamente
                time.sleep(1)

            except TimeoutException:
                print("⚠️  Timeout: El elemento de tiempo no apareció en 30 segundos")
                print("Esto puede significar que:")
                print("  - El partido no está en vivo")
                print("  - Bplay suspendió temporalmente los mercados")
                print("  - La página tiene una estructura diferente")
                # Guardamos evidencia para debugging
                self._guardar_debug_info()
                return None

            # Ahora intentamos encontrar el tiempo del partido
            # Probamos múltiples estrategias porque la estructura puede variar

            # Estrategia 1: Buscar por la estructura que vimos antes
            minuto_total = self._buscar_por_estructura_original()
            if minuto_total is not None:
                return minuto_total

            # Estrategia 2: Buscar cualquier elemento que parezca un reloj de partido
            minuto_total = self._buscar_reloj_alternativo()
            if minuto_total is not None:
                return minuto_total

            print("No se pudo encontrar el tiempo del partido con ninguna estrategia")
            self._guardar_debug_info()
            return None

        except Exception as e:
            print(f"Error al obtener tiempo de Bplay: {e}")
            import traceback

            traceback.print_exc()
            return None

    def _guardar_debug_info(self):
        """Guarda captura de pantalla y HTML para debugging."""
        try:
            self.driver.save_screenshot("bplay_debug.png")
            print("📸 Captura guardada en: bplay_debug.png")
        except:
            pass

        try:
            with open("bplay_debug.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            print("📄 HTML guardado en: bplay_debug.html")
        except:
            pass

    def _buscar_por_estructura_original(self):
        """
        Intenta encontrar el tiempo usando la estructura HTML original que encontramos.
        """
        try:
            print("Estrategia 1: Buscando estructura original...")

            # Buscamos el contenedor con clase "time"
            time_containers = self.driver.find_elements(By.CLASS_NAME, "time")

            if not time_containers:
                print("  No se encontró ningún elemento con clase 'time'")
                return None

            print(f"  Se encontraron {len(time_containers)} elementos con clase 'time'")

            # Probamos con cada contenedor que encontremos
            for idx, time_container in enumerate(time_containers):
                print(f"  Analizando contenedor {idx + 1}...")

                # Buscamos "first-info" dentro de este contenedor
                try:
                    first_info = time_container.find_element(
                        By.CLASS_NAME, "first-info"
                    )
                except NoSuchElementException:
                    print(f"    No tiene 'first-info', probando siguiente...")
                    continue

                # Buscamos los spans dentro de first-info
                spans = first_info.find_elements(By.TAG_NAME, "span")

                if len(spans) < 2:
                    print(f"    Solo tiene {len(spans)} spans, necesitamos al menos 2")
                    continue

                # Extraemos el texto de los spans
                periodo = spans[0].text.strip()
                minutos_str = spans[1].text.strip()

                print(
                    f"    Encontrado - Período: '{periodo}', Minutos: '{minutos_str}'"
                )

                # Si ambos tienen contenido, intentamos parsear
                if periodo and minutos_str:
                    minuto_total = self._parsear_tiempo(periodo, minutos_str)
                    if minuto_total is not None:
                        print(f"✓ Minuto actual en Bplay: {minuto_total}'")
                        return minuto_total

            print("  Ningún contenedor 'time' tenía datos válidos")
            return None

        except Exception as e:
            print(f"  Error en estrategia 1: {e}")
            return None

    def _buscar_reloj_alternativo(self):
        """
        Busca el reloj del partido usando patrones alternativos comunes.
        """
        try:
            print("Estrategia 2: Buscando patrones alternativos...")

            # Buscamos elementos que contengan texto con formato de tiempo de partido
            # como "45'", "17'", "1T", "2T", etc.
            all_text_elements = self.driver.find_elements(By.XPATH, "//*[text()]")

            import re

            time_pattern = re.compile(
                r"(\d+)'"
            )  # Patrón: uno o más dígitos seguidos de '

            for element in all_text_elements:
                text = element.text.strip()
                if time_pattern.match(text):
                    print(f"  Encontrado posible tiempo: '{text}'")

                    # Intentamos extraer el número
                    match = time_pattern.match(text)
                    if match:
                        minutos = int(match.group(1))
                        print(f"✓ Minuto extraído: {minutos}'")
                        return float(minutos)

            print("  No se encontraron elementos con formato de tiempo")
            return None

        except Exception as e:
            print(f"  Error en estrategia 2: {e}")
            return None

    def _parsear_tiempo(self, periodo, minutos_str):
        """
        Convierte el período y los minutos en un número total de minutos.

        Args:
            periodo: String como "1T" (primer tiempo) o "2T" (segundo tiempo)
            minutos_str: String como "17'" o "45+2'"

        Returns:
            float: El minuto total del partido (ej: 62.0 para minuto 17 del segundo tiempo)
        """
        try:
            # Limpiamos el string de minutos, quitando el apóstrofe y espacios
            minutos_str = minutos_str.replace("'", "").strip()

            # Buscamos si hay tiempo adicional (ej: "45+3")
            if "+" in minutos_str:
                # Dividimos por el signo +
                partes = minutos_str.split("+")
                minutos_base = int(partes[0])
                minutos_adicionales = int(partes[1])
                minutos_periodo = minutos_base + minutos_adicionales
            else:
                # No hay tiempo adicional, es un número simple
                minutos_periodo = int(minutos_str)

            # Determinamos si estamos en primer o segundo tiempo
            # "1T" o "1º" significa primer tiempo
            # "2T" o "2º" significa segundo tiempo
            if "2" in periodo:
                # Segundo tiempo: sumamos 45 minutos del primer tiempo
                minuto_total = minutos_periodo
            else:
                # Primer tiempo
                minuto_total = float(minutos_periodo)

            return minuto_total

        except (ValueError, IndexError) as e:
            print(f"Error al parsear tiempo '{minutos_str}': {e}")
            return None

    def verificar_partido_en_vivo(self):
        """
        Verifica si hay algún indicador de que el partido está en vivo.
        Busca elementos como badges de "EN VIVO" o "LIVE".
        """
        try:
            # Buscamos el badge de "live" que viste en el HTML
            live_badge = self.driver.find_element(By.CLASS_NAME, "live-badge")
            if live_badge and live_badge.is_displayed():
                return True
        except NoSuchElementException:
            pass

        return False

    def cerrar(self):
        """
        Cierra el navegador y libera recursos.
        Importante llamar a esto cuando termines de usar el scraper.
        """
        if self.driver:
            self.driver.quit()
            print("Chrome driver cerrado")
