import os
import ssl
import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
from dramatiq.results.backends.redis import RedisBackend
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
result_backend = RedisBackend()
broker = RedisBroker()
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)

class ReservationDetails(BaseModel):
    name: str
    date: str
    time: str
    party_size: int 

@dramatiq.actor(store_results=True)
def send_reservation_confirmation(email_receiver: str, reservation_details: ReservationDetails):
    email_sender = 'spnvva.a@gmail.com'
    email_password = os.getenv("EMAIL_PASSWORD")
    smtp_server = 'smtp.gmail.com'
    port = 465  
    context = ssl.create_default_context()

    subject = 'ayo food'
    body = f"""dearest most gentle reader  {reservation_details.name},
 thanks for your reservation.your reservation details:

Name: {reservation_details.name}
Date: {reservation_details.date}
Time: {reservation_details.time}
Party Size: {reservation_details.party_size}

Reservation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

we look forward to meet u

xoxo, gossip girl
"""
    message = MIMEMultipart()
    message["From"] = email_sender
    message["To"] = email_receiver
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(email_sender, email_password)
            server.sendmail(email_sender, email_receiver, message.as_string())
        return "Reservation confirmation email sent successfully"
    except Exception as e:
        return f"Failed to send email: {e}"