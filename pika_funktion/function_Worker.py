#!/usr/bin/env python
import datetime
import json
import sys
import threading
import time

import pika
from pyrabbit.api import Client

from pika_funktion.function_Worker import *



def queue_count(channel,queuetmp):
    result = channel.queue_declare(
        queue=queuetmp,
        durable=True,
        exclusive=False,
        auto_delete=False,
        passive=True
    )
    print("Anzahl an verbleibenden Aufgaben: " + str(result.method.message_count))

def get_criterias(exchange):
    username = 'test'
    password = 'test'
    cl = Client('192.168.178.7:15672', username, password)
    queues = [q['name'] for q in cl.get_queues()]
    exchanges = cl.get_bindings()
    list=[]
    for e in exchanges:
        if e.get('source') == exchange:
            list.append(e.get('routing_key')+ ' -> ' + e.get('destination') + '\n')
    return list



class ConsumerThread_retry(threading.Thread):


    def __init__(self, queue, exchange, type, severities, max_retries, mainfunction, *args, **kwargs):
        super(ConsumerThread_retry, self).__init__(*args, **kwargs)
        self.queue = queue
        self.test = True
        self.exchange = exchange
        self.type = type
        self.severities = severities
        self.max_retries = max_retries
        self.connection = pika.BlockingConnection(pika.URLParameters('amqp://myuser:mypassword@192.168.178.7:5672/myvhost'))
        self.mainfunction = mainfunction
        self.channel = self.connection.channel()

        try:
            test = self.channel.queue_declare(queue=self.queue, passive=True)
        except:
            print(1)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue, durable=True)

        self.channel.exchange_declare(exchange=self.exchange,
                                 type=self.type)

    # Not necessarily a method.
    def callback_func(self, ch, method, properties, body):
        #print("{} received '{}' '{}'".format(self.name, 'Anfang',body.decode("utf-8")))
        #Daten anzeigen und daten in varaible laden
        #print (properties.headers.get('hello'))
        data = json.loads(body.decode("utf-8"))
        #print ("[>] Received '%s' (try: %d)" % (data.get('keyword'), 1 + int(properties.priority)))

        if properties.priority >= self.max_retries - 1: # example handling retries
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print ("[!] '%s' rejected after %d retries" % (data.get('keyword'), 1 + int(properties.priority)))
        else:
            try:
                #Wieviel sind Aufgaben sind noch in der Warteschlange
                #queue_count(self.channel,self.queue)
                ch.basic_ack(delivery_tag=method.delivery_tag)
                #DOSOMETHING HIERE!!!!!!!!
                self.mainfunction()
                print (self.name+"[+] Done")
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

    def run(self):
        if self.test == False:
            self.channel.stop_consuming()
            self.connection.close()
            return True

        for severity in self.severities:
            self.channel.queue_bind(exchange=self.exchange,
                               queue=self.queue,
                               routing_key=severity)

        self.channel.basic_consume(self.callback_func,
                              queue=self.queue,
                              consumer_tag=self.name + '-Worker')

        list=get_criterias(self.exchange)
        print(self.name + '\n Queue: \"' + self.queue + '\" \n Kriterien hinzugefügt: ' + ', '.join(self.severities) + '\n Kiterien von Exchange "' + self.exchange + '":\n ' +
        ' '.join(list) + ' [*] Waiting for logs. To exit press CTRL+C' + '\n')


        self.channel.start_consuming()

    def stop(self):
        print ("Trying to stop thread ")
        print(self.name + 'Ende')
        self.test = False
        self.run()
        print('b')
