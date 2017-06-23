import time
import pika
import datetime
import json


def _retrymessage(channel,anzahl,exchange,severity,message,directory_root,prio, directory_ewf=None,directory_partion=None, offset=None):
    for i in range(anzahl):
        timestamp = time.time()
        now = datetime.datetime.now()
        expire = 1000 * int((now.replace(hour=23, minute=59, second=59, microsecond=999999) - now).total_seconds())
        headers = {  # example how headers can be used
            'hello': 'world',
            'created': int(timestamp)
        }
        data = {  # example hot to transfer objects rather than string using json.dumps and json.loads
            'keyword': 'Wie_geil',
            'domain': 'Windows',
            'count': i,
            'message': message,
            'directory_ewf' : directory_ewf,
            'directory_root' : directory_root,
            'directory_partion' : directory_partion,
            'offset' : offset,
            'created': int(timestamp),
            'expire': expire
        }
        channel.basic_publish(
            exchange=exchange,
            routing_key=severity,
            body=json.dumps(data),  # must be string
            properties=pika.BasicProperties(
                delivery_mode=2,  # makes persistent job
                priority=prio,  # default priority
                timestamp=int(timestamp),  # timestamp of job creation
                expiration=str(expire),  # job expiration (milliseconds from now), must be string, handled by rabbitmq
                headers=headers
            ))
        print("[>] Sent %r" % message)


def _bind():
    reconnect_interval = 1
    connection=None
    credentials = pika.PlainCredentials(
        'myuser',
        'mypassword')

    parameters = pika.ConnectionParameters(
        host='192.168.178.7',
        port=5672,
        virtual_host='myvhost',
        credentials=credentials,
        retry_delay=5,
        connection_attempts=3)

    while (connection is None):
        try:
            connection = pika.BlockingConnection(
                parameters)  # Verbindung zu rabbitmq

            # Reset reconnect_interval after a successful connection
            reconnect_interval = 1
            return connection
        except Exception as exception:
            if reconnect_interval >= 1024:
                break
            if reconnect_interval < 1024:
                reconnect_interval = reconnect_interval * 2
            print(reconnect_interval)
            time.sleep(reconnect_interval)
