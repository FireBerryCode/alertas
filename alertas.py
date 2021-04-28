from google.cloud import ndb
import google.cloud.logging

import base64
import json

import logging

from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



client_logging = google.cloud.logging.Client()
client_logging.get_default_handler()
client_logging.setup_logging()



def send_mail(msg, mail):
    message = Mail(
        from_email='fberry125@gmail.com',
        to_emails='pablosanchez.aveiga@gmail.com',
        subject='ALERTA!! UNHA DAS SÚAS ALARMAS FOI EXECUTADA!!!',
        html_content=f'<strong>{msg}</strong>')
    try:
        sg = SendGridAPIClient("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")
        response = sg.send(message)
    except Exception as e:
        logging.warning(e.message)



def send_sms(msg, phone):

    client = Client("AC7d3aea8289a8a833ad1f16a68e49086b", "03c954838e78eedfeb6dce6b625fdb2a")

    # change the "from_" number to your Twilio number and the "to" number
    # to the phone number you signed up for Twilio with, or upgrade your
    # account to send SMS to any phone number
    message = client.messages.create(to="+34" + phone, 
                        from_="+19386665305", 
                        body=msg)

def get_device_by(device_id):
    datastore_client = ndb.Client()
    with datastore_client.context():
        alerts = Alertas.query().filter(Alertas.id_dispositivo==device_id).fetch()
        return alerts


class Alertas(ndb.Model):
    usuario = ndb.StringProperty(),
    email = ndb.StringProperty(),
    telefono = ndb.StringProperty(),
    id_dispositivo = ndb.IntegerProperty()
    temp = ndb.IntegerProperty()
    hum = ndb.IntegerProperty()
    luz = ndb.IntegerProperty()
    rinf = ndb.IntegerProperty()
    flame = ndb.IntegerProperty()
    gas = ndb.IntegerProperty()
    activa = ndb.BooleanProperty()

def alerts(event, context):
    
    pubsub_message = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    alerts = get_device_by(pubsub_message["device_id"])

    for item in alerts:
        
        if pubsub_message["temp"] > item.temp and item.activa:
            temp = pubsub_message["temp"]
            msg = f"ALERTA!!! TEMPERATURA DE {temp}ºC, EXCEDIDO UMBRAL DE {item.temp} PARA O USUARIO {item.usuario} NO DISPOSITIVO {item.id_dispositivo}"
            logging.warning(msg)
            send_sms(msg, item.telefono)
            send_mail(msg, item.email)
            item.activa = False
            item.put()

        if pubsub_message["hum"] > item.temp and item.activa:
            hum = pubsub_message["hum"]
            msg = f"ALERTA!!! HUMIDADE DE {hum}ºC, EXCEDIDO UMBRAL DE {item.hum} PARA O USUARIO {item.usuario} NO DISPOSITIVO {item.id_dispositivo}"
            logging.warning(msg)
            send_sms(msg, item.telefono)
            send_mail(msg, item.email)
            item.activa = False
            item.put()

        if pubsub_message["luz"] > item.temp and item.activa:
            luz = pubsub_message["luz"]
            msg = f"ALERTA!!! LUZ DE {luz}ºC, EXCEDIDO UMBRAL DE {item.luz} PARA O USUARIO {item.usuario} NO DISPOSITIVO {item.id_dispositivo}"
            logging.warning(msg)
            send_sms(msg, item.telefono)
            send_mail(msg, item.email)
            item.activa = False
            item.put()

        if pubsub_message["rinf"] > item.temp and item.activa:
            rinf = pubsub_message["rinf"]
            msg = f"ALERTA!!! RADIACIÓN INFRAVERMELLA DE {rinf}ºC, EXCEDIDO UMBRAL DE {item.rinf} PARA O USUARIO {item.usuario} NO DISPOSITIVO {item.id_dispositivo}"
            logging.warning(msg)
            send_sms(msg, item.telefono)
            send_mail(msg, item.email)
            item.activa = False
            item.put()

        if pubsub_message["flame"] > item.temp and item.activa:
            flame = pubsub_message["flame"]
            msg = f"ALERTA!!! SENSOR DE CHAMA DE {flame}ºC, EXCEDIDO UMBRAL DE {item.flame} PARA O USUARIO {item.usuario} NO DISPOSITIVO {item.id_dispositivo}"
            logging.warning(msg)
            send_sms(msg, item.telefono)
            send_mail(msg, item.email)
            item.activa = False
            item.put()

        if pubsub_message["gas"] > item.temp and item.activa:
            gas = pubsub_message["gas"]
            msg = f"ALERTA!!! CONCENTRACIÓN DE GASES DE {gas}ºC, EXCEDIDO UMBRAL DE {item.gas} PARA O USUARIO {item.usuario} NO DISPOSITIVO {item.id_dispositivo}"
            logging.warning(msg)
            send_sms(msg, item.telefono)
            send_mail(msg, item.email)
            item.activa = False
            item.put()

