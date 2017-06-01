#!/usr/bin/env python
import datetime
import json
import sys
import threading
import time

import pika

from pika_funktion.function_Client import _bind



def queue_count(channel,queuetmp):
    result = channel.queue_declare(
        queue=queuetmp,
        durable=True,
        exclusive=False,
        auto_delete=False,
        passive=True
    )
    print("Anzahl an verbleibenden Aufgaben: " + str(result.method.message_count))

def _worker(queue, exchange, type, severities):

#Fehlermeldungen abfangen
    if not severities:
        sys.exit(1)

    connection=_bind()
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange,
                             type=type)
#wird des untere gebraucht?
    channel.queue_declare(queue=queue, durable=True)
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

#queue oder queuename??? bzw beides machen musss noch geklärt werden
    for severity in severities:
        channel.queue_bind(exchange=exchange,
                           queue=queue,
                           routing_key=severity)



# mithilfe von lambda übergeben???
    def callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))
# Eventuell noch einen mit selbst erzeugnednen queues
    channel.basic_consume(callback,
                          queue=queue,
                          no_ack=True)


    print(' [*] Waiting for logs. To exit press CTRL+C')
    channel.start_consuming()


def _workerRetry(queue, exchange, type, severities,max_retries):
    max_retries = max_retries

    connection = _bind()
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange,
                             type=type)
    # wird des untere gebraucht?
    channel.queue_declare(queue=queue, durable=True)

    print ('[*] Waiting for messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        #Daten anzeigen und daten in varaible laden
        print (properties.headers.get('hello'))
        data = json.loads(body)
        print ("[>] Received '%s' (try: %d)" % (data.get('keyword'), 1 + int(properties.priority)))

        if properties.priority >= max_retries - 1: # example handling retries
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print ("[!] '%s' rejected after %d retries" % (data.get('keyword'), 1 + int(properties.priority)))
        else:
            try:
                #Wieviel sind Aufgaben sind noch in der Warteschlange
                queue_count(channel,queue)
                ch.basic_ack(delivery_tag=method.delivery_tag)
                #DOSOMETHING HIERE!!!!!!!!
                print ("[+] Done")
            except:
                timestamp = time.time()
                now = datetime.datetime.now()
                expire = 1000 * int((now.replace(hour=23, minute=59, second=59, microsecond=999999) - now).total_seconds())

                # to reject job we create new one with other priority and expiration
                channel.basic_publish(exchange='',
                                      routing_key=severities,
                                      body=json.dumps(data),
                                      properties=pika.BasicProperties(
                                          delivery_mode=2,
                                          priority=int(properties.priority) + 1,
                                          timestamp=timestamp,
                                          expiration=str(expire),
                                          headers=properties.headers))

                # also do not forget to send back acknowledge about job
                ch.basic_ack(delivery_tag=method.delivery_tag)
                print ("[!] Rejected, going to sleep for a while")
                time.sleep(10)


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue=queue)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming();

    connection.close()



class ConsumerThread(threading.Thread):
    def __init__(self, queue, exchange, type, severities, *args, **kwargs):
        super(ConsumerThread, self).__init__(*args, **kwargs)
        self.queue = queue
        self.exchange = exchange
        self.type = type
        self.severities = severities
        self.connection = pika.BlockingConnection(pika.URLParameters('amqp://myuser:mypassword@192.168.178.7:5672/myvhost'))  # Verbindung zu rabbitmq
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue, durable=True)


    # Not necessarily a method.
    def callback_func(self, channel, method, properties, body):
        queue_count(self.channel,self.queue)
        print("{} received '{}' '{}'".format(self.name, 'Anfang',body.decode("utf-8")))


    def run(self):
        queue= self.queue
        exchange= self.exchange
        type = self.type
        severities = self.severities



        for severity in severities:
            self.channel.queue_bind(exchange=self.exchange,
                               queue=self.queue,
                               routing_key=severity)
        #self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.callback_func,
                              queue=self.queue,
                              consumer_tag=self.name + '-Worker')



        print(self.name + ' [*] Waiting for logs. To exit press CTRL+C')
        self.channel.start_consuming()

class ConsumerThread_retry(threading.Thread):
    def __init__(self, queue, exchange, type, severities, max_retries, *args, **kwargs):
        super(ConsumerThread_retry, self).__init__(*args, **kwargs)
        self.queue = queue
        self.exchange = exchange
        self.type = type
        self.severities = severities
        self.max_retries = max_retries
        self.connection = _bind()
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange,
                                 type=type)
        self.channel.queue_declare(queue=self.queue, durable=True)

    # Not necessarily a method.
    def callback_func(self, ch, method, properties, body):
        print("{} received '{}' '{}'".format(self.name, 'Anfang',body.decode("utf-8")))
        #Daten anzeigen und daten in varaible laden
        print (properties.headers.get('hello'))
        data = json.loads(body)
        print ("[>] Received '%s' (try: %d)" % (data.get('keyword'), 1 + int(properties.priority)))

        if properties.priority >= self.max_retries - 1: # example handling retries
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print ("[!] '%s' rejected after %d retries" % (data.get('keyword'), 1 + int(properties.priority)))
        else:
            try:
                #Wieviel sind Aufgaben sind noch in der Warteschlange
                queue_count(self.channel,self.queue)
                ch.basic_ack(delivery_tag=method.delivery_tag)
                #DOSOMETHING HIERE!!!!!!!!
                print ("[+] Done")
            except:
                timestamp = time.time()
                now = datetime.datetime.now()
                expire = 1000 * int((now.replace(hour=23, minute=59, second=59, microsecond=999999) - now).total_seconds())

                # to reject job we create new one with other priority and expiration
                self.channel.basic_publish(exchange=self.exchange,
                                      routing_key=self.severities,
                                      body=json.dumps(data),
                                      properties=pika.BasicProperties(
                                          delivery_mode=2,
                                          priority=int(properties.priority) + 1,
                                          timestamp=timestamp,
                                          expiration=str(expire),
                                          headers=properties.headers))

                # also do not forget to send back acknowledge about job
                ch.basic_ack(delivery_tag=method.delivery_tag)
                print ("[!] Rejected, going to sleep for a while")
                time.sleep(10)
        print('blubb')











    def run(self):



        for severity in self.severities:
            self.channel.queue_bind(exchange=self.exchange,
                               queue=self.queue,
                               routing_key=severity)

        self.channel.basic_consume(self.callback_func,
                              queue=self.queue,
                              consumer_tag=self.name + '-Worker')

        print(self.name + ' [*] Waiting for logs. To exit press CTRL+C')
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            print('LALALALALALALALALLALALAALA')
            self.connection.close();

