import logging
import sys
import time

from Forensic_function.Linux.claimscan import clamscanDisk
from Forensic_function.Linux.copyDisk import copyDisk
from Forensic_function.Linux.ewfmount import getEwf
from Forensic_function.Linux.foremost import foremostScan
from Forensic_function.Linux.getPartion import getPartion
from Forensic_function.Linux.mount import mountDisk
from Forensic_function.Linux.plaso import timeline
from Pika_funktion.check import Consumer
from Pika_funktion.check import printer
from global_variable import *

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

    workerlist('Copydisk', routingkeysVorbedingung.get('Copydisk'), copyDisk)

    workerlist('Ewfmount', routingkeysVorbedingung.get('Eefmount'), getEwf)
    workerlist('Partition', routingkeysVorbedingung.get('Partition'), getPartion)
    workerlist('MountDisk_Linux', routingkeysVorbedingung.get('MountDisk_Linux'), mountDisk)

    workerlist('Foremostscan', routingkeysVorbedingung.get('Foremostscan'), foremostScan)
    workerlist('Timeline', routingkeysVorbedingung.get('Timeline'), timeline)

    workerlist('Clamscanndisk', routingkeysVorbedingung.get('Clamscanndisk'), clamscanDisk)



    workerlist('Ende', 'Ende', printer)

    for thread in threads:
        # print('Starting: ' + thread.QUEUE)
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