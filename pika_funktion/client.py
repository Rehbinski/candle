from pika_funktion.function_Client import _bind
from pika_funktion.function_Client import _retrymessage

if __name__ == "__main__":

# Variablen für Nachricht belegen senden topic
    queue = 'blubb'                                     # Zu welcher Warteschlange dann gerutet werden soll
    severity = 'test.critical'                          # Nach welchen Kritereien zu Warteschlange geroutet wird
    exchange = 'topic_logs'                             # Wie man mag
    type = 'topic'                                      # Type auf welche Art der Worker hört
    message = 'Hello World'                             # Nachricht zum senden erzeugen
# Wird Nachricht benötigt???
    prio = 0                                            # Priorität festlegen

#Connection aufbauen
    connection=_bind()                                  # Verbindung zu Rabbitmq
    channel = connection.channel()                      # Channel erzeugen
    channel.queue_declare(queue=queue, durable=True)    # Warteschlange erstellen
    channel.exchange_declare(exchange=exchange,         # Exchange erstellen
                             type=type)

#Retry NAchricht senden
    _retrymessage(channel,2,exchange,severity,message,prio)

#Connection beenden
    connection.close()