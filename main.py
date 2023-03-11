from email.message import EmailMessage
import ssl
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()


email_sender = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_PASSWORD")
email_receiver = os.getenv("EMAIL_RECEIVER")
subject = 'Python Email Sender (Test Mail)'

body = """
Test Mail 
"""


em = EmailMessage()

em["From"] = email_sender
em["To"] = email_receiver
em["Subject"] = subject
em.set_content(body)


context = ssl.create_default_context()


with open('sample.pdf', 'rb') as content_file:
    content = content_file.read()
    em.add_attachment(content, maintype='application', subtype='pdf', filename='sample.pdf')



with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
    smtp.login(email_sender,email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
    print("Success!")



