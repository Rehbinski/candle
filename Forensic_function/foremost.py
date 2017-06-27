#clamscan /home/work/NAS/usb -r -i --move=/home/work/NAS/clamscan

import subprocess
import os
import time

from global_variable import *
from start_client_linux import sendMessageTopic


from Forensic_function.global_function import *

def foremost(data):
    directory_image = data.get('directory_root') + '/image/image.E01'
    directory = data.get('directory_root')

    commandName = 'foremost'
    directory_output = directory + '/' + commandName
    #clamscan /home/work/NAS/Kunde/usb -r -i --copy=/home/work/NAS/Kunde/clamscan
    command = commandName + ' -o ' + directory_output + ' -i '  +  directory_image + ' -T'
    #foremost -o /home/work/Desktop/Tipp -i /home/work/NAS/Kunde/image/image.E01 -T
    commandListSudoDokumentation(command, directory)


def foremostScan(data):
    print('vierter Schritt begonnen')
    foremost(data)
    print('vierter Schritt fertig')

    routing_key = 'Ende'  # Nach welchen Kritereien zu Warteschlange geroutet wird
    # Wird Nachricht benötigt???
    sendMessageTopic(routing_key, data)


    print('jaa so gehts')





if __name__ == "__main__" :
    foremostScan(DATA)