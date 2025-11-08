# config.py
# Configuración central del monitor de desfases

CONFIG = {
    # Intervalo en segundos entre cada chequeo
    # 10 segundos es bueno para testing, podés aumentarlo a 30-60 para uso normal
    "intervalo_chequeo": 120,
    # Umbral de diferencia en minutos para considerar que hay un desfase significativo
    # 0.5 minutos = 30 segundos
    # Cuando la diferencia supere este valor, se enviará una alerta
    "umbral_desfase": 5.0,
    # Lista de partidos a monitorear
    # Cada partido necesita:
    # - nombre: Identificador del partido (para logs y notificaciones)
    # - sofascore_id: El ID numérico del partido en Sofascore
    #   Lo sacás de la URL del partido, ej: sofascore.com/partido/algo/12345 -> ID es 12345
    # - bplay_url: La URL completa del partido en Bplay
    "partidos_interes": [
        {
            "nombre": "Athletic Club vs Ferroviária",
            "sofascore_id": 13638739,  # Este es el ID del partido que me mostraste
            "bplay_url": "https://deportespba.bplay.bet.ar/live/10406341-athletic-club-mg-ferroviaria",
        },
        # Podés agregar más partidos aquí cuando necesites monitorear varios
        # {
        #     "nombre": "Otro partido",
        #     "sofascore_id": 99999,
        #     "bplay_url": "https://www.bplay.com.ar/..."
        # },
    ],
    # Configuración para notificaciones por email
    "email": {
        "habilitado": False,  # Cambiá a False si no querés recibir emails
        "smtp_server": "smtp.gmail.com",  # Servidor SMTP de Gmail
        "smtp_port": 587,  # Puerto TLS de Gmail
        "remitente": "tu_email@gmail.com",  # Tu email de Gmail
        "password": "tu_app_password_aqui",  # App Password de Gmail (NO tu contraseña normal)
        "destinatario": "tu_email@gmail.com",  # Email donde querés recibir las alertas
    },
    # Guardar historial de desfases detectados
    "guardar_historial": True,
    "archivo_historial": "historial_desfases.json",
}

# IMPORTANTE: Para configurar el email de Gmail:
# 1. Andá a tu cuenta de Google: myaccount.google.com
# 2. En "Seguridad", activá la verificación en 2 pasos
# 3. Después de activarla, buscá "Contraseñas de aplicaciones"
# 4. Generá una nueva contraseña de aplicación para "Correo"
# 5. Usá esa contraseña de 16 caracteres en el campo "password" arriba
# 6. NUNCA uses tu contraseña normal de Gmail aquí
