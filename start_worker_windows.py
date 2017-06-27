from Forensic_function.Windows.mount import mount
from Pika_funktion.check import Consumer
from Pika_funktion.check import printer

import time
import sys
import logging

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


def main():
    #logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    threads = []
# Erster Arbeiter - copy Disk
    for i in range(1):
        t = Consumer(2, 'MountDisk', 'Mount.MountDisk.Windows.PC2.thread' + str(i), mount)
        t.daemon = True
        threads.append(t)

# Ende Arbeiter - mount Disk
    for i in range(1):
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