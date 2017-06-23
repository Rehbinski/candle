from forensic_function.claimscan import clamscanDisk
from forensic_function.mmls import mountDisk
from forensic_function.sb5 import copyDisk

from pika_funktion.function_Worker import ConsumerThread_retry
from pika_funktion.check import Consumer
import time
import sys
import logging
from pika_funktion.check import printer

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


def main():
    #logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    threads = []
# Erster Arbeiter - copy Disk

    for i in range(1):
        t = Consumer(1, 'Copydisk', 'Copy.Copydisk.Linux.PC1.thread' + str(i), copyDisk)
        t.demon = True
        threads.append(t)

# Zweiter Arbeiter - mount Disk
    for i in range(1):
        t = Consumer(2, 'MountDisk', 'Mount.MountDisk.Linux.PC1.thread' + str(i), mountDisk)
        t.daemon = True
        threads.append(t)

# Dritter Arbeiter - mount Disk
    for i in range(1):
        #Queuenamen namen hochzahelen wenn 2 die gleiche arbeit machen sollen
        #t = Consumer(1, 'clamscannDisk'+str(i), 'Programme.clamscannDisk.Linux.PC1.thread' + str(i), clamscanDisk)
        #Queuenamen gleich lassen wenn mehrere Anfragen kommen koennen und diese Parallel bearbeitet werden sollen
        t = Consumer(1, 'clamscannDisk', 'Programme.clamscannDisk.Linux.PC1.thread' + str(i), clamscanDisk)

        t.daemon = True
        threads.append(t)

# Ende Arbeiter - mount Disk
        for i in range(3):
            t = Consumer(1, 'End'+str(i), 'Ende', printer)
            t.daemon = True
            threads.append(t)

    for thread in threads:
        thread.start()

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


if __name__ == "__main__":
    # * vor one word
    # # vor more words
    main()