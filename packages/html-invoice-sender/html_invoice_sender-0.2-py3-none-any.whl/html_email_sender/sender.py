import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
import os

class EmailSender:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def send_email(self, to_email, subject, template_file, context):
        env = Environment(loader=FileSystemLoader(os.path.join(os.getcwd(), 'templates')))
        template = env.get_template(template_file)
        html_content = template.render(context)

        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(html_content, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.email, self.password)
        server.send_message(msg)
        server.quit()
