import smtplib, ssl
import email
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


class Emails(object):
    def  __init__(self, send_email=None ,receiver=None):
       self.sender_email = send_email
       self.receiver_email = receiver
       
    def __enter__(self):
        return "You are in a with block"
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        return 
    
    def mailer(self):

        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] =   self.sender_email
        message["To"] =     self.receiver_email
        
        # Create the plain-text and HTML version of your message
        text = """\
        Hi,
        How are you?
        Real Python has many great tutorials:
        www.realpython.com"""
        html = """\
        <html>
          <body>
            <p>Hi,<br>
               How are you?<br>
               <a href="http://www.realpython.com">Real Python</a> 
               has many great tutorials.
            </p>
          </body>
        </html>
        """
        
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        
        # Create secure connection with server and send email
        #context = ssl.create_default_context()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.login("boysthollie@gmail.com", "69414422173943112")
        server.sendmail(self.sender_email, self.receiver_email, message.as_string())
        server.quit()
