#clamscan /home/work/NAS/usb -r -i --move=/home/work/NAS/clamscan

import subprocess
import os
import time

from start_client import sendMessage


from forensic_function.global_function import *

def clamscan(directory):
    commandName = 'clamscan'
    pfad = directory + '/' + commandName
    #clamscan /home/work/NAS/Kunde/usb -r -i --copy=/home/work/NAS/Kunde/clamscan
    command = commandName + ' ' + directory + '/usb' + ' -r -i --copy='  +  pfad
    commandListSudoDokumentation(command, directory)


def clamscanDisk(directory):
    print('dritter Schritt begonnen')
    clamscan(directory)
    print('dritter Schritt fertig')

    severity = 'info.Windows'  # Nach welchen Kritereien zu Warteschlange geroutet wird
    exchange = 'topic_logs'  # Wie man mag
    type = 'topic'  # Type auf welche Art der Worker hört
    message = 'Hello World'  # Nachricht zum senden erzeugen
    directory = '/home/work/NAS/Kunde'  # Pfad angabe
    # Wird Nachricht benötigt???
    prio = 0  # Priorität festlegen

    sendMessage(exchange, severity, message, directory, prio, type)


    print('jaa so gehts')





if __name__ == "__main__" :

    directory = '/home/work/NAS/Kunde'
    clamscanDisk(directory)