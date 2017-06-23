from pika_funktion.function_Client import _bind
from pika_funktion.function_Client import _retrymessage



def sendMessageTopic(routing_key, message, directory):
    sendMessage('topic_logs', routing_key, message, directory, 0, 'topic')


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
    print('Ende Nachricht gesendet')



if __name__ == "__main__":
# Ziel fuer zum Speichern


# Variablen für Nachricht belegen senden topic
# Erster Arbeiter - copy Disk
    severity = 'Copydisk.Kopieren.Linux.*.*'            # Nach welchen Kritereien zu Warteschlange geroutet wird
    severity = 'Programme.clamscannDisk'                #Fuer Testzwecke angelegt
    severity = 'Copy'                                   #Sollte Reichen
    exchange = 'topic_logs'                             # Wie man mag
    type = 'topic'                                      # Type auf welche Art der Worker hört
    message = 'Nachricht fuer jedermann'                # Nachricht zum senden erzeugen
    directory = '/home/work/NAS/Kunde'
# Wird Nachricht benötigt???
    prio = 0                                            # Priorität festlegen
    sendMessage(exchange, severity, message, directory, prio, type)