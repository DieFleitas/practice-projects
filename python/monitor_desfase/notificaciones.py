import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

# Configuramos el sistema de logging para ver mensajes en la consola
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Notificador:
    def __init__(self, config_email=None):
        """
        Inicializa el notificador con la configuración de email.

        Args:
            config_email: Diccionario con la configuración del email
        """
        self.logger = logging.getLogger("monitor_desfase")
        self.config_email = config_email
        self.ultima_alerta = {}  # Para evitar spam de notificaciones repetidas

    def enviar_alerta(self, nombre_partido, diferencia, tiempo_bplay, tiempo_sofascore):
        """
        Envía una alerta cuando se detecta un desfase significativo.

        Args:
            nombre_partido: Nombre del partido (ej: "Athletic Club vs Ferroviária")
            diferencia: Diferencia en minutos entre ambas fuentes
            tiempo_bplay: Minuto actual en Bplay
            tiempo_sofascore: Minuto actual en Sofascore
        """
        # Creamos el mensaje de la alerta
        if diferencia > 0:
            adelantado = "Sofascore"
            atrasado = "Bplay"
        else:
            adelantado = "Bplay"
            atrasado = "Sofascore"
            diferencia = abs(diferencia)

        mensaje_corto = f"⚠️ DESFASE DETECTADO: {nombre_partido}"

        mensaje_detallado = f"""
╔══════════════════════════════════════════════════════════╗
║        ⚠️  ALERTA DE DESFASE DETECTADO  ⚠️               ║
╚══════════════════════════════════════════════════════════╝

📺 Partido: {nombre_partido}

⏱️  Tiempos detectados:
   • Bplay:     {tiempo_bplay:.1f} minutos
   • Sofascore: {tiempo_sofascore:.1f} minutos

⚡ Diferencia: {diferencia:.1f} minutos ({diferencia * 60:.0f} segundos)
   {adelantado} va adelantado respecto a {atrasado}

📅 Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

💡 Esto significa que si hacés una apuesta en Bplay, ya sabés
   qué pasó {diferencia:.1f} minutos antes viendo Sofascore.

════════════════════════════════════════════════════════════
"""

        # Mostramos la alerta en la consola
        self.logger.warning(mensaje_corto)
        print(mensaje_detallado)

        # Enviamos email si está configurado
        if self.config_email and self.config_email.get("habilitado"):
            # Evitamos enviar el mismo email muchas veces seguidas
            # Solo enviamos si pasaron al menos 2 minutos desde la última alerta de este partido
            ahora = datetime.now()
            if nombre_partido in self.ultima_alerta:
                tiempo_desde_ultima = (
                    ahora - self.ultima_alerta[nombre_partido]
                ).total_seconds()
                if tiempo_desde_ultima < 120:  # 120 segundos = 2 minutos
                    self.logger.info("Alerta suprimida (muy cercana a la anterior)")
                    return

            self.ultima_alerta[nombre_partido] = ahora
            self.enviar_email(mensaje_corto, mensaje_detallado)

    def enviar_email(self, asunto, cuerpo):
        """
        Envía un email usando Gmail SMTP.

        Args:
            asunto: Asunto del email
            cuerpo: Cuerpo del mensaje
        """
        try:
            # Creamos el mensaje de email
            mensaje = MIMEMultipart()
            mensaje["From"] = self.config_email["remitente"]
            mensaje["To"] = self.config_email["destinatario"]
            mensaje["Subject"] = asunto

            # Adjuntamos el cuerpo del mensaje
            mensaje.attach(MIMEText(cuerpo, "plain", "utf-8"))

            # Nos conectamos al servidor SMTP de Gmail
            self.logger.info("Conectando al servidor SMTP...")
            servidor = smtplib.SMTP(
                self.config_email["smtp_server"], self.config_email["smtp_port"]
            )

            # Iniciamos conexión TLS (encriptada)
            servidor.starttls()

            # Nos autenticamos
            servidor.login(
                self.config_email["remitente"], self.config_email["password"]
            )

            # Enviamos el email
            servidor.send_message(mensaje)
            servidor.quit()

            self.logger.info(
                f"✅ Email enviado exitosamente a {self.config_email['destinatario']}"
            )

        except smtplib.SMTPAuthenticationError:
            self.logger.error("❌ Error de autenticación SMTP. Verificá que:")
            self.logger.error("   1. El email y la contraseña sean correctos")
            self.logger.error(
                "   2. Estés usando una App Password de Gmail, no tu contraseña normal"
            )
            self.logger.error(
                "   3. Tengas activada la verificación en 2 pasos en tu cuenta de Google"
            )
        except smtplib.SMTPException as e:
            self.logger.error(f"❌ Error SMTP al enviar email: {e}")
        except Exception as e:
            self.logger.error(f"❌ Error inesperado al enviar email: {e}")

    def notificar_inicio_monitoreo(self, partidos):
        """
        Envía una notificación informando que el monitoreo comenzó.
        """
        mensaje = f"""
╔══════════════════════════════════════════════════════════╗
║       🚀  MONITOR DE DESFASES INICIADO  🚀               ║
╚══════════════════════════════════════════════════════════╝

📊 Monitoreando {len(partidos)} partido(s):
"""
        for p in partidos:
            mensaje += f"   • {p['nombre']}\n"

        mensaje += f"""
⏰ Fecha de inicio: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

El sistema está funcionando y te notificará cuando detecte desfases.
════════════════════════════════════════════════════════════
"""
        print(mensaje)
        self.logger.info("Monitor de desfases iniciado correctamente")

    def notificar_error_scraping(self, fuente, nombre_partido, error):
        """
        Notifica cuando hay un error al obtener datos de alguna fuente.
        """
        self.logger.error(f"Error en {fuente} para {nombre_partido}: {error}")
