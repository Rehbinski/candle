import time

from forensic_function.claimscan import clamscanDisk
from forensic_function.mmls import mountDisk
from forensic_function.sb5 import copyDisk

from pika_funktion.function_Worker import ConsumerThread_retry


if __name__ == "__main__":
    # * vor one word
    # # vor more words
    threads = []
    exchange = 'topic_logs'  # Wie man mag
    type = 'topic'  # Type auf welche Art der Worker hört




# Erster Arbeiter - copy Disk
    queue = 'Copydisk'  # Zu welcher Warteschlange dann gerutet werden soll
    severities = ['Linux.Copydisk.*']  # Nach welchen Kritereien zu Warteschlange geroutet wird


    for i in range(1):
        t = ConsumerThread_retry(queue, exchange, type, severities, 3, copyDisk)
        t.demon=True
        threads.append(t)

# Zweiter Arbeiter - mount Disk
    queue = 'MountDisk'  # Zu welcher Warteschlange dann gerutet werden soll
    severities = ['Linux.MountDisk.*']  # Nach welchen Kritereien zu Warteschlange geroutet wird

    for i in range(1):
        t = ConsumerThread_retry(queue, exchange, type, severities, 3, mountDisk)
        t.daemon = True
        threads.append(t)

        # Dritter Arbeiter - mount Disk
    queue = 'clamscannDisk'  # Zu welcher Warteschlange dann gerutet werden soll
    severities = ['Linux.clamscannDisk.*']  # Nach welchen Kritereien zu Warteschlange geroutet wird
#TODO clamcannDisk ist eine Funktion ander betiteln
    for i in range(2):
        t = ConsumerThread_retry(queue, exchange, type, severities, 3, clamscanDisk)
        t.daemon = True
        threads.append(t)



 # Alle Arbeiter Anstossen
    for thread in threads:
        thread.start()



    while len(threads) > 0:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print ("Ctrl-c received! Sending kill to threads TODO...")
            for t in threads:
                t.stop()
            break
    print('Ende')