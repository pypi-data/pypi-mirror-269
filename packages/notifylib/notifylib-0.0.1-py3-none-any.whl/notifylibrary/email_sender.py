import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, smtp_server, port, username, password):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password

    def send_mail(self, subject, message, from_email, to_emails):
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP(self.smtp_server, self.port)
        server.starttls()
        server.login(self.username, self.password)
        text = msg.as_string()
        server.sendmail(from_email, to_emails, text)
        server.quit()
