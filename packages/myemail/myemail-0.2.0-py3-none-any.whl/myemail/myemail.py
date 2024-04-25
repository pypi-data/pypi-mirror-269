import smtplib
from email.message import EmailMessage
import email


def send(msg_content, from_email, to_email, subject):
    msg_content = msg_content
    message = EmailMessage()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(msg_content)
    try:
        server = smtplib.SMTP(smtpserver, sslport)
        server.starttls()
        server.login(me, password)
        server.send_message(message)
        print("E-Mail erfolgreich gesendet!")
    except Exception as e:
        print(f"Fehler beim Senden der E-Mail: {e}")
    finally:
        server.quit()
