import smtplib
from email.message import EmailMessage
import email


def send(
    msg_content, from_email, to_email, subject, sslport, password, smtpserver, attachment_path=""
):
    msg_content = msg_content
    message = EmailMessage()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(msg_content)
    try:
        with open(attachment_path, "rb") as attachment_file:
            attachment_data = attachment_file.read()
            attachment_filename = attachment_path.split("/")[-1]
        message.add_attachment(
            attachment_data,
            maintype="application",
            subtype="octet-stream",
            filename=attachment_filename,
        )
    except:
        pass
    try:
        server = smtplib.SMTP(smtpserver, sslport)
        server.starttls()
        server.login(from_email, password)
        server.send_message(message)
        print("E-Mail sucsessfully send")
    except Exception as e:
        print(f"Error while sending e-mail: {e}")
    finally:
        server.quit()


if __name__ == "__main__":
    import os, dotenv as dv

    dv.load_dotenv()
    sslport = os.getenv("SSLPORT")  # For SSL
    password = os.getenv("PASSWORD")
    smtpserver = os.getenv("SMTPSERVER")
    emailvar = os.getenv("EMAIL")
    attachment_path = f"{os.getenv('HOME')}/testfile123.txt"
    print(attachment_path)
    send(
        msg_content="test",
        from_email=emailvar,
        to_email=emailvar,
        subject="test",
        sslport=sslport,
        password=password,
        attachment_path=attachment_path,
        smtpserver=smtpserver
    )
