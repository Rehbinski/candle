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

