from difflib import SequenceMatcher


class EmparejadorPartidos:
    """
    Empareja partidos entre Sofascore y Bplay basándose en similitud de nombres.
    """

    def __init__(self, umbral_similitud=0.7):
        """
        Args:
            umbral_similitud: Valor entre 0 y 1 que indica cuán similares deben ser
                             los nombres para considerarlos un match (0.7 = 70% similar)
        """
        self.umbral_similitud = umbral_similitud

    def emparejar_partidos(self, partidos_sofascore, partidos_bplay):
        """
        Encuentra los partidos que están en ambas plataformas.

        Args:
            partidos_sofascore: Lista de partidos de Sofascore
            partidos_bplay: Lista de partidos de Bplay

        Returns:
            list: Lista de tuplas (partido_sofascore, partido_bplay) que coinciden
        """
        emparejamientos = []
        bplay_usados = set()  # Para no emparejar el mismo partido de Bplay dos veces

        print(f"\n{'='*60}")
        print("EMPAREJANDO PARTIDOS ENTRE PLATAFORMAS")
        print(f"{'='*60}")
        print(f"Partidos en Sofascore: {len(partidos_sofascore)}")
        print(f"Partidos en Bplay: {len(partidos_bplay)}")

        for partido_ss in partidos_sofascore:
            mejor_match = None
            mejor_similitud = 0

            for idx, partido_bp in enumerate(partidos_bplay):
                if idx in bplay_usados:
                    continue

                # Calculamos la similitud entre ambos partidos
                similitud = self._calcular_similitud_partido(partido_ss, partido_bp)

                if similitud > mejor_similitud and similitud >= self.umbral_similitud:
                    mejor_similitud = similitud
                    mejor_match = (idx, partido_bp)

            if mejor_match:
                idx_match, partido_bp = mejor_match
                bplay_usados.add(idx_match)
                emparejamientos.append((partido_ss, partido_bp))

                print(f"\n✓ MATCH encontrado ({mejor_similitud:.0%} similitud):")
                print(
                    f"  Sofascore: {partido_ss['equipo_local']} vs {partido_ss['equipo_visitante']}"
                )
                print(
                    f"  Bplay:     {partido_bp['equipo_local']} vs {partido_bp['equipo_visitante']}"
                )

        print(f"\n{'='*60}")
        print(f"TOTAL DE EMPAREJAMIENTOS: {len(emparejamientos)}")
        print(f"{'='*60}\n")

        return emparejamientos

    def _calcular_similitud_partido(self, partido_ss, partido_bp):
        """
        Calcula qué tan similar es un partido entre ambas plataformas.

        Compara los nombres de ambos equipos (local y visitante) y retorna
        la similitud promedio.
        """
        # Usamos los nombres normalizados que ya calculamos en los scrapers
        local_ss = partido_ss.get("equipo_local_normalizado", "")
        visit_ss = partido_ss.get("equipo_visitante_normalizado", "")

        local_bp = partido_bp.get("equipo_local_normalizado", "")
        visit_bp = partido_bp.get("equipo_visitante_normalizado", "")

        # Calculamos similitud de equipos locales
        similitud_local = self._similitud_texto(local_ss, local_bp)

        # Calculamos similitud de equipos visitantes
        similitud_visitante = self._similitud_texto(visit_ss, visit_bp)

        # También consideramos la posibilidad de que los equipos estén invertidos
        # (local de SS = visitante de BP y viceversa)
        similitud_local_invertida = self._similitud_texto(local_ss, visit_bp)
        similitud_visitante_invertida = self._similitud_texto(visit_ss, local_bp)

        # Calculamos el promedio de las similitudes en orden normal
        similitud_normal = (similitud_local + similitud_visitante) / 2

        # Calculamos el promedio de las similitudes en orden invertido
        similitud_invertida = (
            similitud_local_invertida + similitud_visitante_invertida
        ) / 2

        # Retornamos la mayor de las dos
        return max(similitud_normal, similitud_invertida)

    def _similitud_texto(self, texto1, texto2):
        """
        Calcula la similitud entre dos strings usando SequenceMatcher.

        Returns:
            float: Valor entre 0 y 1, donde 1 es idéntico
        """
        if not texto1 or not texto2:
            return 0.0

        # SequenceMatcher usa el algoritmo de Ratcliff/Obershelp
        # que es muy bueno para encontrar similitudes en strings
        return SequenceMatcher(None, texto1, texto2).ratio()
