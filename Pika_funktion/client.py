from Pika_funktion.function_Client import _bind
from Pika_funktion.function_Client import _retrymessage
from global_variable import *

if __name__ == "__main__":

# Variablen für Nachricht belegen senden topic
    severity = 'info.Windows'                          # Nach welchen Kritereien zu Warteschlange geroutet wird
    exchange = 'topic_logs'                             # Wie man mag
    type = 'topic'                                      # Type auf welche Art der Worker hört
# Wird Nachricht benötigt???
    prio = 0                                            # Priorität festlegen

#Connection aufbauen
    connection=_bind()                                  # Verbindung zu Rabbitmq
    channel = connection.channel()                      # Channel erzeugen
    channel.exchange_declare(exchange=exchange,         # Exchange erstellen
                             type=type)

#Retry NAchricht senden
    _retrymessage(channel,2,exchange,severity,0,DATA)

#Connection beenden
    connection.close()