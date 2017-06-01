

import time
import pika
import datetime
import json


def _message(channel,anzahl, exchange, severity, message):
    for i in range(anzahl):
        tmpmessage = message + str(i)
        channel.basic_publish(exchange=exchange,
                              routing_key=severity,
                              body=tmpmessage)
        print(" [x] Sent %r:%r" % (severity, tmpmessage))




def _retrymessage(channel,anzahl,exchange,severity,message,prio):
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





#only for test
if __name__ == "__main__":
    rmq_server = None
    queue='test'
    connection=_bind()
    channel = connection.channel()
    channel.queue_declare(queue='test', durable=True)
    severity='error'
    for i in range(1):
        message = '0-Hello World!' + str(i)
        channel.basic_publish(exchange='direct_logs',
                              routing_key=severity,
                              body=message)
        print(" [x] Sent %r:%r" % (severity, message))

    connection.close()
