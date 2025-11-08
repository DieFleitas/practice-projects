import requests
from datetime import datetime
import time


class SofaScoreScraper:
    def __init__(self):
        self.session = requests.Session()
        # Headers importantes para que Sofascore nos acepte las peticiones
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Accept-Language": "es-ES,es;q=0.9",
                "Referer": "https://www.sofascore.com/",
            }
        )

    def obtener_partidos_en_vivo(self, deporte="football"):
        """
        Obtiene una lista de todos los partidos en vivo en Sofascore.

        Args:
            deporte: El deporte a consultar. Por defecto "football" (fútbol).
                     Otros valores: "basketball", "tennis", etc.

        Returns:
            list: Lista de diccionarios con información de cada partido en vivo.
                  Cada diccionario contiene: id, equipo_local, equipo_visitante,
                  minuto_actual, torneo, etc.
            None: Si hay algún error
        """
        try:
            # Esta es la URL de la API de Sofascore para obtener eventos en vivo
            # El número 1 al final corresponde al ID del deporte (1 = fútbol)
            deporte_id = self._obtener_id_deporte(deporte)
            url = f"https://www.sofascore.com/api/v1/sport/{deporte}/events/live"

            print(f"Consultando partidos en vivo de {deporte} en Sofascore...")
            response = self.session.get(url, timeout=10)

            if response.status_code != 200:
                print(f"Error: Sofascore respondió con código {response.status_code}")
                return None

            data = response.json()

            # La respuesta contiene un array de eventos organizados por categoría
            # Necesitamos aplanar esta estructura para obtener una lista simple
            partidos = []
            events = data.get("events", [])

            for event in events:
                try:
                    partido_info = self._extraer_info_partido(event)
                    if partido_info:
                        partidos.append(partido_info)
                except Exception as e:
                    print(f"Error al procesar un evento: {e}")
                    continue

            print(f"✓ Se encontraron {len(partidos)} partidos en vivo")
            return partidos

        except requests.exceptions.RequestException as e:
            print(f"Error de red al consultar Sofascore: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado al obtener partidos en vivo: {e}")
            return None

    def _obtener_id_deporte(self, deporte):
        """Mapea nombres de deportes a sus IDs en Sofascore."""
        mapeo = {
            "football": "football",
            "futbol": "football",
            "soccer": "football",
            "basketball": "basketball",
            "basquet": "basketball",
            "tennis": "tennis",
            "tenis": "tennis",
        }
        return mapeo.get(deporte.lower(), "football")

    def _extraer_info_partido(self, event):
        """
        Extrae la información relevante de un evento de Sofascore.

        Args:
            event: Diccionario con datos del evento desde la API

        Returns:
            dict: Información procesada del partido
        """
        # Verificamos que el evento esté realmente en progreso
        status = event.get("status", {})
        if status.get("type") != "inprogress":
            return None

        # Extraemos información básica
        partido_id = event.get("id")
        equipo_local = event.get("homeTeam", {}).get("name", "")
        equipo_visitante = event.get("awayTeam", {}).get("name", "")

        # Extraemos el torneo para poder filtrar o agrupar después
        torneo = event.get("tournament", {}).get("name", "")
        categoria = event.get("tournament", {}).get("category", {}).get("name", "")

        # Calculamos el minuto actual
        time_info = event.get("time", {})
        current_period_start = time_info.get("currentPeriodStartTimestamp")

        minuto_actual = None
        if current_period_start:
            current_timestamp = int(time.time())
            seconds_elapsed = current_timestamp - current_period_start
            minutes_in_period = seconds_elapsed / 60.0

            status_description = status.get("description", "")
            if "2nd" in status_description.lower():
                minuto_actual = round(45.0 + minutes_in_period, 1)
            else:
                minuto_actual = round(minutes_in_period, 1)

        return {
            "id": partido_id,
            "equipo_local": equipo_local,
            "equipo_visitante": equipo_visitante,
            "equipo_local_normalizado": self._normalizar_nombre_equipo(equipo_local),
            "equipo_visitante_normalizado": self._normalizar_nombre_equipo(
                equipo_visitante
            ),
            "minuto_actual": minuto_actual,
            "torneo": torneo,
            "categoria": categoria,
            "estado": status.get("description", ""),
            "url": f"https://www.sofascore.com/partido/{partido_id}",
        }

    def _normalizar_nombre_equipo(self, nombre):
        """
        Normaliza el nombre de un equipo para facilitar la comparación entre plataformas.

        Convierte a minúsculas, elimina acentos, elimina caracteres especiales,
        y reduce espacios múltiples a uno solo.

        Args:
            nombre: Nombre original del equipo

        Returns:
            str: Nombre normalizado
        """
        import unicodedata

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

    def obtener_tiempo_partido(self, partido_id):
        """
        Obtiene el minuto actual de un partido en Sofascore.

        Args:
            partido_id: El ID numérico del partido en Sofascore

        Returns:
            float: El minuto actual del partido (ej: 17.5 para 17 minutos y 30 segundos)
            None: Si hay algún error o el partido no está en vivo
        """
        try:
            # La URL de la API de Sofascore para obtener datos de un evento
            url = f"https://www.sofascore.com/api/v1/event/{partido_id}"

            print(f"Consultando Sofascore para partido ID: {partido_id}")
            response = self.session.get(url, timeout=10)

            # Si la respuesta no es exitosa, retornamos None
            if response.status_code != 200:
                print(f"Error: Sofascore respondió con código {response.status_code}")
                return None

            data = response.json()

            # Extraemos la información del evento
            event = data.get("event")
            if not event:
                print("Error: No se encontró información del evento")
                return None

            # Verificamos que el partido esté en vivo
            status = event.get("status", {})
            status_type = status.get("type")

            if status_type != "inprogress":
                print(f"El partido no está en vivo. Estado: {status_type}")
                return None

            # Obtenemos el período actual (1st half, 2nd half, etc)
            status_description = status.get("description", "")
            print(f"Estado del partido: {status_description}")

            # Extraemos la información de tiempo
            time_info = event.get("time", {})
            current_period_start = time_info.get("currentPeriodStartTimestamp")

            if not current_period_start:
                print("Error: No se encontró el timestamp de inicio del período")
                return None

            # Calculamos cuántos segundos pasaron desde que empezó este período
            current_timestamp = int(time.time())
            seconds_elapsed = current_timestamp - current_period_start

            # Convertimos a minutos (con decimales para mayor precisión)
            minutes_in_period = seconds_elapsed / 60.0

            # Si estamos en el segundo tiempo, sumamos 45 minutos
            # Sofascore usa "2nd half" para el segundo tiempo
            if "2nd" in status_description.lower():
                total_minutes = 45.0 + minutes_in_period
            else:
                total_minutes = minutes_in_period

            print(f"Minuto actual en Sofascore: {total_minutes:.1f}'")
            return round(total_minutes, 1)

        except requests.exceptions.RequestException as e:
            print(f"Error de red al consultar Sofascore: {e}")
            return None
        except (KeyError, ValueError, TypeError) as e:
            print(f"Error al parsear datos de Sofascore: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado en Sofascore: {e}")
            return None

    def obtener_info_partido(self, partido_id):
        """
        Obtiene información completa del partido (equipos, score, estado).
        Útil para logging y debugging.
        """
        try:
            url = f"https://www.sofascore.com/api/v1/event/{partido_id}"
            response = self.session.get(url, timeout=10)

            if response.status_code != 200:
                return None

            data = response.json()
            event = data.get("event", {})

            info = {
                "home_team": event.get("homeTeam", {}).get("name"),
                "away_team": event.get("awayTeam", {}).get("name"),
                "home_score": event.get("homeScore", {}).get("current"),
                "away_score": event.get("awayScore", {}).get("current"),
                "status": event.get("status", {}).get("description"),
            }

            return info

        except Exception as e:
            print(f"Error obteniendo info del partido: {e}")
            return None
