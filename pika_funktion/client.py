from pika_funktion.function_Client import _bind
from pika_funktion.function_Client import _retrymessage
#from pika_funktion.globale_Variable import *

if __name__ == "__main__":

    queue = 'test'
    exchange = 'direct_logs'
    type = 'direct'
    severities = ['error', 'info', 'warning']

    severity = 'error'
    message = 'Hello World'
    prio = 0

#Connection aufbauen
    connection=_bind()
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.exchange_declare(exchange=exchange,
                             type=type)

#Nachrichten senden direct
#    _message(channel,1,exchange,severity,message)

# Nachrichten senden topic

    queue='blubb'
    exchange='topic_logs'
    severity = 'test.critical'
    type = 'topic'
    channel.exchange_declare(exchange=exchange, type=type)
    
#    _message(channel, 1, exchange, routing_key, message)

# Nachrichten senden queue
#    channel.queue_declare(queue='test', durable=True)
#    _message(channel,1,exchange,severity,message)
###

#Retry NAchricht senden
    _retrymessage(channel,200000,exchange,severity,message,prio)


#Connection beenden
    connection.close()