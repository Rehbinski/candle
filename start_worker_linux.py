from Forensic_function.claimscan import clamscanDisk
from Forensic_function.mount import mountDisk
from Forensic_function.copyDisk import copyDisk
from Forensic_function.foremost import foremostScan

from Pika_funktion.check import Consumer
from Pika_funktion.check import printer
from Forensic_function.getPartion import getPartion
from Forensic_function.plaso import timeline
from global_function import workerlist

import time
import sys
import logging

# Konfiguration zum starten
retries = 2
threads = []
pcangaben = '.Linux.PC1.thread'

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


# Queuenamen namen hochzahelen wenn 2 die gleiche arbeit machen sollen
# t = Consumer(1, 'clamscannDisk'+str(i), 'Programme.clamscannDisk.Linux.PC1.thread' + str(i), clamscanDisk)
# Queuenamen gleich lassen wenn mehrere Anfragen kommen koennen und diese Parallel bearbeitet werden sollen


def main():
    #logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    global threads

    workerlist('Copydisk', 'Copy.Copydisk', copyDisk)
    workerlist('Ewfmount', 'Mount.Ewfmount', getPartion)
    workerlist('MountDisk_Linux', 'Mount.MountDisk', mountDisk)
    workerlist('clamscannDisk', 'Programme.clamscannDisk', clamscanDisk)
    workerlist('foremostScan', 'Mount.foremost', foremostScan)
    workerlist('foremostScan', 'Mount.timeline', timeline)
    workerlist('Ende', 'Ende', printer)

    for thread in threads:
        thread.start()

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