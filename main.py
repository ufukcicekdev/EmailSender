from email.message import EmailMessage
import ssl
import smtplib
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
import time
import schedule

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
    em = EmailMessage()
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
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as server:
            server.login(email_sender,email_password)
            server.sendmail(email_sender, email_receiver, em.as_string())
            logging.info(f"Email Sent Done! -- Time: {datetime.now()} -- Receiver: {email_receiver}")
            server.quit()
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)



def job():
    mailMessage()
    attachmentReader()
    mailSender()   

schedule.every(10).seconds.do(job)
# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)