import dramatiq
from dramatiq.results.backends.redis import RedisBackend
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
import requests
from requests.exceptions import ReadTimeout

import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from email.mime.application import MIMEApplication

from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

result_backend = RedisBackend()
broker = RedisBroker()
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)

def when_to_retry(number_of_retries: int, exc: Exception) -> bool:
    return isinstance(exc, ReadTimeout)


class BookingRequest(BaseModel):
    email: str
    name: str
    time: str
    num_people: int



@dramatiq.actor(store_results=True)
def book_table(email_receiver:str):
    email_sender = 'spnvva@gmail.com'
    email_password = os.environ.get("EMAIL_PASSWORD")
    subject = 'food'
    body = """just stfu and eat ur food ig
            """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    message = MIMEMultipart()
    message.attach(MIMEText(body, "plain"))  

    message["Subject"] = subject
    message["From"] = email_sender
    message["To"] = email_receiver

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, [email_receiver], message.as_bytes())
    return "email send succesfully"


