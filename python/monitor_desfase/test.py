from scrapers.bplay_scraper import BplayScraper
from scrapers.sofascore_scraper import SofaScoreScraper

scraper_sofa = SofaScoreScraper()
tiempo = scraper_sofa.obtener_tiempo_partido(
    13638739
)  # Usá el ID real de un partido en vivo
print(f"Tiempo en Sofascore: {tiempo} minutos")


scraper_bplay = BplayScraper()
tiempo = scraper_bplay.obtener_tiempo_partido(
    "https://deportespba.bplay.bet.ar/live/10406341-athletic-club-mg-ferroviaria"
)  # Usá el ID real de un partido en vivo
print(f"Tiempo en Bplay: {tiempo} minutos")