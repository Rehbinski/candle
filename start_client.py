from pika_funktion.function_Client import _bind
from pika_funktion.function_Client import _retrymessage
from global_variable import *


def sendMessageTopic(routing_key, data):
    sendMessage('topic_logs', routing_key, data, 'topic')


def sendMessage(exchange, routing_key, data, type):
    # Connection aufbauen
    connection = _bind()  # Verbindung zu Rabbitmq
    channel = connection.channel()  # Channel erzeugen
    channel.exchange_declare(exchange=exchange,  # Exchange erstellen
                             type=type)
    # Retry NAchricht senden
    _retrymessage(channel, 1, exchange, routing_key, 0, data)
    # Connection beenden
    connection.close()
    print('Ende Nachricht gesendet')



if __name__ == "__main__":
# Ziel fuer zum Speichern


# Variablen für Nachricht belegen senden topic
# Erster Arbeiter - copy Disk
    routing_key = 'Copy.Copydisk'                                   #Sollte Reichen
    #routing_key = 'Mount.Ewfmount'
    #routing_key = 'Mount.Ewfmount'
    exchange = 'topic_logs'                             # Wie man mag
    type = 'topic'                                      # Type auf welche Art der Worker hört
# Wird Nachricht benötigt???
    prio = 0                                            # Priorität festlegen
    sendMessageTopic(routing_key, DATA)
    #sendMessage(exchange, routing_key, DATA, type)
