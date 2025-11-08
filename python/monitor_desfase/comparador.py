from datetime import datetime
from config import CONFIG


class ComparadorTiempos:
    """
    Compara los tiempos de dos fuentes y mantiene un historial de las comparaciones.
    """

    def __init__(self):
        self.historial = []
        # Guardamos el último desfase detectado para evitar alertas repetitivas
        self.ultimo_desfase_reportado = None

    def comparar_tiempos(self, tiempo_bplay, tiempo_sofascore):
        """
        Compara dos tiempos y calcula la diferencia.

        Args:
            tiempo_bplay: Minutos actuales según Bplay
            tiempo_sofascore: Minutos actuales según Sofascore

        Returns:
            float: Diferencia en minutos (positivo si Sofascore va adelantado)
            None: Si alguno de los tiempos es None
        """
        # Verificamos que ambos valores sean válidos
        if tiempo_bplay is None or tiempo_sofascore is None:
            return None

        # Calculamos la diferencia
        # Si el resultado es positivo, Sofascore va adelantado
        # Si es negativo, Bplay va adelantado
        diferencia = tiempo_sofascore - tiempo_bplay

        # Creamos un registro de esta comparación
        registro = {
            "timestamp": datetime.now(),
            "bplay": tiempo_bplay,
            "sofascore": tiempo_sofascore,
            "diferencia": diferencia,
        }

        # Agregamos el registro al historial
        self.historial.append(registro)

        # Limitamos el tamaño del historial en memoria para no consumir demasiados recursos
        # Mantenemos solo las últimas 1000 comparaciones
        if len(self.historial) > 1000:
            self.historial = self.historial[-1000:]

        return diferencia

    def hay_desfase_significativo(self, diferencia):
        """
        Determina si una diferencia es lo suficientemente grande como para alertar.

        Args:
            diferencia: Diferencia en minutos entre las dos fuentes

        Returns:
            bool: True si el desfase es significativo, False si no
        """
        if diferencia is None:
            return False

        # Usamos el valor absoluto porque no importa quién va adelante,
        # solo nos interesa la magnitud de la diferencia
        return abs(diferencia) >= CONFIG["umbral_desfase"]

    def obtener_estadisticas(self):
        """
        Calcula estadísticas sobre el historial de comparaciones.
        Útil para análisis y debugging.

        Returns:
            dict: Diccionario con estadísticas del historial
        """
        if not self.historial:
            return {
                "total_comparaciones": 0,
                "diferencia_promedio": 0,
                "diferencia_maxima": 0,
                "diferencia_minima": 0,
            }

        # Extraemos solo las diferencias del historial
        diferencias = [
            r["diferencia"] for r in self.historial if r["diferencia"] is not None
        ]

        if not diferencias:
            return {
                "total_comparaciones": len(self.historial),
                "diferencia_promedio": 0,
                "diferencia_maxima": 0,
                "diferencia_minima": 0,
            }

        return {
            "total_comparaciones": len(diferencias),
            "diferencia_promedio": sum(diferencias) / len(diferencias),
            "diferencia_maxima": max(diferencias),
            "diferencia_minima": min(diferencias),
            "diferencia_absoluta_promedio": sum(abs(d) for d in diferencias)
            / len(diferencias),
        }

    def obtener_ultimas_comparaciones(self, n=10):
        """
        Obtiene las últimas N comparaciones del historial.

        Args:
            n: Cantidad de comparaciones a obtener (default: 10)

        Returns:
            list: Lista con las últimas N comparaciones
        """
        return self.historial[-n:] if len(self.historial) >= n else self.historial
