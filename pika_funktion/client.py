from .function_Client import _bind
from .function_Client import _retrymessage

if __name__ == "__main__":

# Variablen für Nachricht belegen senden topic
    severity = 'info'                          # Nach welchen Kritereien zu Warteschlange geroutet wird
    exchange = 'direct_logs'                             # Wie man mag
    type = 'direct'                                      # Type auf welche Art der Worker hört
    message = 'Hello World'                             # Nachricht zum senden erzeugen
# Wird Nachricht benötigt???
    prio = 0                                            # Priorität festlegen

#Connection aufbauen
    connection=_bind()                                  # Verbindung zu Rabbitmq
    channel = connection.channel()                      # Channel erzeugen
    channel.exchange_declare(exchange=exchange,         # Exchange erstellen
                             type=type)

#Retry NAchricht senden
    _retrymessage(channel,2,exchange,severity,message,prio)

#Connection beenden
    connection.close()