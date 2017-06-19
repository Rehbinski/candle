from forensic_function.claimscan import clamscan
from forensic_function.mmls import *
from forensic_function.sb5 import copy_disk

from pika_funktion.function_Worker import ConsumerThread_retry


if __name__ == "__main__":
    # * vor one word
    # # vor more words
    threads = []


# Erster Arbeiter
    queue = 'testanlegen2'  # Zu welcher Warteschlange dann gerutet werden soll
    severities = ['info.*', 'test.*']  # Nach welchen Kritereien zu Warteschlange geroutet wird
    exchange = 'topic_logs'  # Wie man mag
    type = 'topic'  # Type auf welche Art der Worker hört

    for i in range(1):
        t = ConsumerThread_retry(queue, exchange, type, severities, 3)
        t.demon=True
        threads.append(t)

# Alle Arbeiter Anstossen

    for thread in threads:
        thread.start()




    while len(threads) > 0:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print ("Ctrl-c received! Sending kill to threads TODO...")
            break
    print('Ende')