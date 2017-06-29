import logging
import sys
import time

from Forensic_function.Windows.mount import mount
from Pika_funktion.check import Consumer
from Pika_funktion.check import printer

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

# Konfiguration zum starten
retries = 2
threads = []
pcangaben = '.Windows.PC2.thread'

def main():
    #logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    global threads
    workerlist('MountDisk', 'Programme_EWF.MountDisk', mount)
    workerlist('Ende', 'Ende', printer)

    for thread in threads:
        thread.start()
        print('Started: ' + thread.QUEUE)
    print('Started: all')
    unterbrechen()


def unterbrechen():
    global threads
    while len(threads) > 0:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            for t in threads:
                try:
                    t.stop()
                except:
                    print('Fehler: ' + str(sys.exc_info()[0]))
            break

def workerlist(queue, routing_key, function, retriesFunction=1, anzahlWorker=1, doppelt=False):
    # Trigger koennte von Mount kommen
    global threads
    for i in range(anzahlWorker):
        info = ''
        if doppelt:
            info = str(i)
        consumer = Consumer(retriesFunction, queue + info, routing_key + pcangaben, function)
        consumer.daemon = True
        threads.append(consumer)

if __name__ == "__main__":
    # * vor one word
    # # vor more words
    main()