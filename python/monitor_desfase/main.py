import time
import schedule
import json
from datetime import datetime
from scrapers.bplay_scraper import BplayScraper
from scrapers.sofascore_scraper import SofaScoreScraper
from emparejador import EmparejadorPartidos
from comparador import ComparadorTiempos
from notificaciones import Notificador
from config import CONFIG


class MonitorDesfaseAutomatico:
    """
    Monitor automático que detecta partidos en vivo en ambas plataformas
    y los monitorea buscando desfases de tiempo.
    """

    def __init__(self):
        print("Inicializando monitor automático...")

        # Inicializamos los scrapers
        self.bplay_scraper = BplayScraper()
        self.sofascore_scraper = SofaScoreScraper()

        # Inicializamos el emparejador de partidos
        self.emparejador = EmparejadorPartidos(umbral_similitud=0.7)

        # Inicializamos el comparador de tiempos
        self.comparador = ComparadorTiempos()

        # Inicializamos el notificador
        self.notificador = Notificador(CONFIG.get("email"))

        # Guardamos los partidos que estamos monitoreando actualmente
        self.partidos_monitoreados = {}

        print("✅ Monitor automático inicializado\n")

    def descubrir_partidos_en_comun(self):
        """
        Descubre qué partidos están en vivo en ambas plataformas simultáneamente.

        Returns:
            list: Lista de tuplas (partido_sofascore, partido_bplay) emparejados
        """
        print("\n" + "🔍 " + "=" * 58)
        print("   BUSCANDO PARTIDOS EN VIVO EN AMBAS PLATAFORMAS")
        print("=" * 60 + "\n")

        # Obtenemos partidos en vivo de Sofascore
        partidos_sofascore = self.sofascore_scraper.obtener_partidos_en_vivo()
        if not partidos_sofascore:
            print("⚠️  No se pudieron obtener partidos de Sofascore")
            return []

        # Obtenemos partidos en vivo de Bplay
        partidos_bplay = self.bplay_scraper.obtener_partidos_en_vivo()
        if not partidos_bplay:
            print("⚠️  No se pudieron obtener partidos de Bplay")
            return []

        # Emparejamos los partidos entre ambas plataformas
        emparejamientos = self.emparejador.emparejar_partidos(
            partidos_sofascore, partidos_bplay
        )

        return emparejamientos

    def monitorear_partido_emparejado(self, partido_ss, partido_bp):
        """
        Monitorea un partido específico que fue emparejado entre ambas plataformas.

        Args:
            partido_ss: Diccionario con info del partido en Sofascore
            partido_bp: Diccionario con info del partido en Bplay
        """
        nombre_partido = (
            f"{partido_ss['equipo_local']} vs {partido_ss['equipo_visitante']}"
        )

        print(f"\n{'─'*60}")
        print(f"Monitoreando: {nombre_partido}")
        print(f"{'─'*60}")

        # Obtenemos el tiempo de Sofascore
        # Ya lo tenemos en partido_ss si viene de la lista de en vivo,
        # pero lo volvemos a consultar para tener el valor más actualizado
        tiempo_sofascore = self.sofascore_scraper.obtener_tiempo_partido(
            partido_ss["id"]
        )

        # Obtenemos el tiempo de Bplay accediendo a la URL específica del partido
        tiempo_bplay = self.bplay_scraper.obtener_tiempo_partido(partido_bp["url"])

        # Mostramos los resultados
        print(f"\n📊 Tiempos obtenidos:")
        print(
            f"   Sofascore: {tiempo_sofascore if tiempo_sofascore is not None else 'N/A'} min"
        )
        print(
            f"   Bplay:     {tiempo_bplay if tiempo_bplay is not None else 'N/A'} min"
        )

        # Solo comparamos si ambos valores son válidos
        if tiempo_bplay is not None and tiempo_sofascore is not None:
            # Calculamos la diferencia
            diferencia = self.comparador.comparar_tiempos(
                tiempo_bplay, tiempo_sofascore
            )

            # Mostramos la diferencia
            print(f"   Diferencia: {abs(diferencia):.1f} min", end="")
            if diferencia > 0:
                print(" (Sofascore adelantado)")
            elif diferencia < 0:
                print(" (Bplay adelantado)")
            else:
                print(" (Sincronizados)")

            # Verificamos si hay un desfase significativo
            if self.comparador.hay_desfase_significativo(diferencia):
                print(f"\n⚠️  ¡DESFASE SIGNIFICATIVO DETECTADO!")
                self.notificador.enviar_alerta(
                    nombre_partido, diferencia, tiempo_bplay, tiempo_sofascore
                )

                # Guardamos este partido en nuestra lista de desfases detectados
                partido_key = f"{partido_ss['id']}"
                self.partidos_monitoreados[partido_key] = {
                    "nombre": nombre_partido,
                    "ultima_alerta": datetime.now(),
                    "diferencia_maxima": abs(diferencia),
                }
            else:
                print(f"\n✅ Tiempos dentro del rango aceptable")
        else:
            # Si alguno de los dos scrapers falló
            if tiempo_bplay is None:
                print("⚠️  No se pudo obtener el tiempo de Bplay")

            if tiempo_sofascore is None:
                print("⚠️  No se pudo obtener el tiempo de Sofascore")

    def ejecutar_ciclo_monitoreo(self):
        """
        Ejecuta un ciclo completo de monitoreo:
        1. Descubre partidos en ambas plataformas
        2. Los empareja
        3. Monitorea cada pareja buscando desfases
        """
        print(f"\n\n{'#'*60}")
        print(
            f"# CICLO DE MONITOREO AUTOMÁTICO - {datetime.now().strftime('%H:%M:%S')}"
        )
        print(f"{'#'*60}")

        try:
            # Descubrimos partidos en común
            emparejamientos = self.descubrir_partidos_en_comun()

            if not emparejamientos:
                print(
                    "\n⚠️  No se encontraron partidos en común entre ambas plataformas"
                )
                print("Esperando al próximo ciclo...\n")
                return

            # Monitoreamos cada partido emparejado
            print(f"\n{'='*60}")
            print(f"MONITOREANDO {len(emparejamientos)} PARTIDO(S)")
            print(f"{'='*60}")

            for partido_ss, partido_bp in emparejamientos:
                try:
                    self.monitorear_partido_emparejado(partido_ss, partido_bp)

                    # Esperamos un poco entre partidos para no sobrecargar las plataformas
                    time.sleep(2)

                except Exception as e:
                    nombre = f"{partido_ss.get('equipo_local')} vs {partido_ss.get('equipo_visitante')}"
                    print(f"❌ Error al monitorear {nombre}: {e}")

            # Guardamos el historial
            if CONFIG.get("guardar_historial"):
                self.guardar_historial()

            print(f"\n{'='*60}")
            print(f"CICLO COMPLETADO")
            print(f"{'='*60}\n")

        except Exception as e:
            print(f"❌ Error en el ciclo de monitoreo: {e}")
            import traceback

            traceback.print_exc()

    def guardar_historial(self):
        """
        Guarda el historial de comparaciones y desfases detectados.
        """
        try:
            # Historial de todas las comparaciones
            archivo_comparaciones = CONFIG.get(
                "archivo_historial", "historial_desfases.json"
            )

            historial_serializable = []
            for registro in self.comparador.historial:
                historial_serializable.append(
                    {
                        "timestamp": registro["timestamp"].isoformat(),
                        "bplay": registro["bplay"],
                        "sofascore": registro["sofascore"],
                        "diferencia": registro["diferencia"],
                    }
                )

            with open(archivo_comparaciones, "w") as f:
                json.dump(historial_serializable, f, indent=2)

            # Historial de partidos con desfases detectados
            if self.partidos_monitoreados:
                archivo_desfases = "partidos_con_desfase.json"

                desfases_serializable = {}
                for key, info in self.partidos_monitoreados.items():
                    desfases_serializable[key] = {
                        "nombre": info["nombre"],
                        "ultima_alerta": info["ultima_alerta"].isoformat(),
                        "diferencia_maxima": info["diferencia_maxima"],
                    }

                with open(archivo_desfases, "w") as f:
                    json.dump(desfases_serializable, f, indent=2)

        except Exception as e:
            print(f"Error al guardar historial: {e}")

    def iniciar(self):
        """
        Inicia el monitoreo automático continuo.
        """
        print("\n" + "=" * 60)
        print("🚀 INICIANDO MONITOR AUTOMÁTICO DE DESFASES")
        print("=" * 60 + "\n")

        print("ℹ️  Modo: AUTOMÁTICO (descubrimiento de partidos)")
        print(f"⏱️  Intervalo de chequeo: {CONFIG['intervalo_chequeo']} segundos")
        print(f"⚡ Umbral de desfase: {CONFIG['umbral_desfase']} minutos")
        print(
            f"📧 Notificaciones por email: {'Activadas' if CONFIG.get('email', {}).get('habilitado') else 'Desactivadas'}"
        )

        # Ejecutamos el primer ciclo inmediatamente
        print(f"\n🔍 Ejecutando primer ciclo de descubrimiento...")
        self.ejecutar_ciclo_monitoreo()

        # Programamos ejecuciones periódicas
        # Para el modo automático, usamos intervalos más largos porque
        # cada ciclo toma más tiempo (debe descubrir y emparejar partidos)
        intervalo = max(CONFIG["intervalo_chequeo"], 60)  # Mínimo 60 segundos
        print(f"\n⏰ Ciclos programados cada {intervalo} segundos")

        schedule.every(intervalo).seconds.do(self.ejecutar_ciclo_monitoreo)

        print(f"\n✅ Monitor funcionando. Presioná Ctrl+C para detener.\n")

        # Loop principal
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Deteniendo monitor...")
            self.cerrar()

    def cerrar(self):
        """
        Cierra correctamente todos los recursos.
        """
        print("Cerrando navegadores...")
        self.bplay_scraper.cerrar()

        # Guardamos el historial final
        if CONFIG.get("guardar_historial"):
            self.guardar_historial()
            print(f"Historial guardado")

        # Mostramos resumen
        if self.partidos_monitoreados:
            print(f"\n📊 Resumen de la sesión:")
            print(
                f"   Partidos con desfases detectados: {len(self.partidos_monitoreados)}"
            )
            for info in self.partidos_monitoreados.values():
                print(f"   - {info['nombre']}: {info['diferencia_maxima']:.1f} min máx")

        print("\n✅ Monitor detenido correctamente")


if __name__ == "__main__":
    # Creamos una instancia del monitor automático
    monitor = MonitorDesfaseAutomatico()

    # Iniciamos el monitoreo
    monitor.iniciar()
