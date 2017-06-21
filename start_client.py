from pika_funktion.function_Client import _bind
from pika_funktion.function_Client import _retrymessage


def sendMessage(exchange, severity, message, directory, prio, type):
    # Connection aufbauen
    connection = _bind()  # Verbindung zu Rabbitmq
    channel = connection.channel()  # Channel erzeugen
    channel.exchange_declare(exchange=exchange,  # Exchange erstellen
                             type=type)
    # Retry NAchricht senden
    _retrymessage(channel, 1, exchange, severity, message, directory, prio)
    # Connection beenden
    connection.close()
    print('Nachricht gesendet')



if __name__ == "__main__":
# Ziel fuer zum Speichern


# Variablen für Nachricht belegen senden topic
# Erster Arbeiter - copy Disk
    severity = 'Linux.Copydisk.*'                       # Nach welchen Kritereien zu Warteschlange geroutet wird
    severity = 'Linux.clamscannDisk.*'                  #Fuer Testzwecke angelegt
    exchange = 'topic_logs'                             # Wie man mag
    type = 'topic'                                      # Type auf welche Art der Worker hört
    message = 'Nachricht fuer jedermann'                # Nachricht zum senden erzeugen
    directory = '/home/work/NAS/Kunde'
# Wird Nachricht benötigt???
    prio = 0                                            # Priorität festlegen
    sendMessage(exchange, severity, message, directory, prio, type)