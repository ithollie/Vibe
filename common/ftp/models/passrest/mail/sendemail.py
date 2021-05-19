import smtplib,imaplib,os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Mail(object):
    def __init__(self,toaddr,message,subject,name="boysthollie",password ="6941442217394311",fromaddr = "boysthollie@ygmail.com",):
        self.message = message
        self.name = name
        self.password = password
        self.fromaddr = fromaddr
        self.sendto =  toaddr
        self.subject = subject

    def send(self):
       msg = MIMEMultipart()
       msg['From'] = self.fromaddr
       msg['To'] = self.sendto
       msg['Subject'] = self.subject
       msg.attach(MIMEText(self.message))
       server = smtplib.SMTP('smtp.gmail.com:587')
       server.ehlo()
       server.starttls()
       server.ehlo()
       server.login(self.name, self.password)
       server.sendmail(self.fromaddr, self.sendto, msg.as_string())
       server.quit()
