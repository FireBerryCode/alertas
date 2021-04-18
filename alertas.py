from google.cloud import error_reporting


def report_error(msg):

    client = error_reporting.Client()
    client.report(msg)


class Alertas(ndb.Model):
    usuario = ndb.StringProperty()
    id_dispositivo = ndb.IntegerProperty()
    temp = ndb.IntegerProperty()
    hum = ndb.IntegerProperty()
    luz = ndb.IntegerProperty()
    rinf = ndb.IntegerProperty()
    lux = ndb.IntegerProperty()
    gas = ndb.IntegerProperty()
    co2 = ndb.IntegerProperty()

def alerts(event, callback):
    
    pubsub_message = json.loads(events.data)
    alerts = get_device_by(pubsub_message["device_id"])

    for item in alerts:
        
        if pubsub_message["temp"] > item.temp:
            msg = f"ALERTA!!! TEMPERATURA DE {pubsub_message["temp"]}ºC, EXCEDIDO UMBRAL DE {item.temp} PARA O USUARIO {item.usuario} NO DISPOSITIVO {item.id_dispositivo}"
            report_error(msg)

        if pubsub_message["hum"] > item.temp:
            msg = f"ALERTA!!! HUMIDADE DE {pubsub_message["hum"]}ºC, EXCEDIDO UMBRAL DE {item.hum} PARA O USUARIO {item.usuario} NO DISPOSITIVO {item.id_dispositivo}"
            report_error(msg)

        if pubsub_message["luz"] > item.temp:
            msg = f"ALERTA!!! LUZ DE {pubsub_message["luz"]}ºC, EXCEDIDO UMBRAL DE {item.luz} PARA O USUARIO {item.usuario} NO DISPOSITIVO {item.id_dispositivo}"
            report_error(msg)

        if pubsub_message["rinf"] > item.temp:
            msg = f"ALERTA!!! RADIACIÓN INFRAVERMELLA DE {pubsub_message["rinf"]}ºC, EXCEDIDO UMBRAL DE {item.rinf} PARA O USUARIO {item.usuario} NO DISPOSITIVO {item.id_dispositivo}"
            report_error(msg)

        if pubsub_message["lux"] > item.temp:
            msg = f"ALERTA!!! LUX DE {pubsub_message["lux"]}ºC, EXCEDIDO UMBRAL DE {item.lux} PARA O USUARIO {item.usuario} NO DISPOSITIVO {item.id_dispositivo}"
            report_error(msg)

        if pubsub_message["gas"] > item.temp:
            msg = f"ALERTA!!! CONCENTRACIÓN DE GASES DE {pubsub_message["gas"]}ºC, EXCEDIDO UMBRAL DE {item.gas} PARA O USUARIO {item.usuario} NO DISPOSITIVO {item.id_dispositivo}"
            report_error(msg)

        if pubsub_message["co2"] > item.temp:
            msg = f"ALERTA!!! CONCENTRACIÓN DE CO2 DE {pubsub_message["co2"]}ºC, EXCEDIDO UMBRAL DE {item.co2} PARA O USUARIO {item.usuario} NO DISPOSITIVO {item.id_dispositivo}"
            report_error(msg)




def get_device_by(device_id):
    with datastore_client.context():
        alerts = Alertas.query().filter(Alertas.id_dispositivo==device_id).fetch()
        return alerts

