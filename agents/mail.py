#! venv/bin/python3

import smtplib #smtp -> Protocolo para enviar correos
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from jinja2 import Template

EMAIL_TEMPLATE = "vigilant-ai-correo.html"

def read_html_file(filename="index.html"):
    with open(filename, "r") as f:
        return f.read()

def get_email_list(filename="email_list.txt"):
    with open(filename, "r") as f:
        lines = f.readlines()

    ans = []
    for email in lines:
        ans.append(email[:-1])

    return ans

def build_mail(username: str, content: str, session_url: str) -> str:
    html_template = read_html_file(EMAIL_TEMPLATE)
    template = Template(html_template)
    html = template.render(username=username, content=content, session_url=session_url)
    return html

def send_mail(to, content, content_type, asunto):
    smtp_server = 'smtp.gmail.com'  # SMTP server
    smtp_port = 587  # SMTP port

    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = to
    msg['Subject'] = asunto
    html_content = MIMEText(content, content_type)
    msg.attach(html_content)
    logo_filename = "logo.png"

    with open("logo.png", "rb") as img:
        data = img.read()
        mime_img = MIMEImage(data)
        mime_img.add_header("Content-ID", "<logo>")
        mime_img.add_header("Content-Disposition", "inline", filename=logo_filename)
        msg.attach(mime_img)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)
        text = msg.as_string()
        server.sendmail(msg["From"], msg["To"], text)
        server.quit()  # Disconnect from the SMTP server
        destinatario = msg['To']
        print(f'Correo enviado con exito a {destinatario}!')

    except Exception as e:
        print(f'Failed to send email: {e}')


#if __name__ == '__main__':
#    # Define a sample HTML template
#    pass
