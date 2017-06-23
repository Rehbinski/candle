#clamscan /home/work/NAS/usb -r -i --move=/home/work/NAS/clamscan

import subprocess
import os
import time

from global_variable import *
from start_client import sendMessageTopic


from forensic_function.global_function import *

def clamscan(data):
    directory = data.get('directory_root')
    commandName = 'clamscan'
    pfad = directory + '/' + commandName
    #clamscan /home/work/NAS/Kunde/usb -r -i --copy=/home/work/NAS/Kunde/clamscan
    command = commandName + ' ' + directory + '/usb' + ' -r -i --copy='  +  pfad
    commandListSudoDokumentation(command, directory)


def clamscanDisk(directory):
    print('dritter Schritt begonnen')
    clamscan(directory)
    print('dritter Schritt fertig')

    routing_key = 'Ende'  # Nach welchen Kritereien zu Warteschlange geroutet wird
    message = 'Nachricht fuer jedermann'  # Nachricht zum senden erzeugen
    # Wird Nachricht benötigt???
    sendMessageTopic(routing_key, message, directory)


    print('jaa so gehts')





if __name__ == "__main__" :
    clamscanDisk(DATA)