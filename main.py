from email.message import EmailMessage
import ssl
import smtplib
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

logging.basicConfig(filename='logFile.log', encoding='utf-8', level=logging.DEBUG)

load_dotenv()
em = EmailMessage()

attachment_path = os.getenv("ATTACHMENT_PATH")
email_sender = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_PASSWORD")
email_receiver = os.getenv("EMAIL_RECEIVER")
subject = 'Python Email Sender (Test Mail)'

body = """
Test Mail 
"""


def mailMessage():
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body)





def attachmentReader():
    for fileName in os.listdir(attachment_path):
        with open(attachment_path + f"{fileName}", 'rb') as f:
            content = f.read()
            name, fileType  = os.path.splitext(fileName)
            em.add_attachment(content, maintype='application', subtype=fileType.replace(".",""), filename=name)

def mailSender():
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            logging.info(f"Email Sent Done! -- Time: {datetime.now()} -- Receiver: {email_receiver}")

    except Exception as e:
        logging.error("Exception occurred", exc_info=True)



if __name__ == '__main__':
    mailMessage()
    attachmentReader()
    mailSender()

