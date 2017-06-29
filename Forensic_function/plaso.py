#clamscan /home/work/NAS/usb -r -i --move=/home/work/NAS/clamscan

import subprocess
import os
import time

from global_variable import *
from start_client_linux import sendMessageTopic


from Forensic_function.global_function import *

def log2timeline(data):
    directory_image = data.get('directory_root') + '/image/image.E01'
    directory = data.get('directory_root')

    commandName = 'log2timeline.py'
    directory_output = directory + '/' + commandName.split('.')[0] + '/all.plaso'
    command = commandName + ' ' + directory_output  + ' ' +  directory_image + ' --partition all'
    #sudo log2timeline.py /home/work/NAS/Kunde/test.plaso /home/work/NAS/Kunde/mount/ewf1 --partition all

    commandListSudoDokumentation(command, directory)

def plaso(data):
    directory = data.get('directory_root')
    directory_image = directory + '/' + 'log2timeline' + '/all.plaso '

    commandName = 'psort.py'

    directory_output = directory + '/' + commandName.split('.')[0] + '/datei.csv'
    #clamscan /home/work/NAS/Kunde/usb -r -i --copy=/home/work/NAS/Kunde/clamscan
    command = commandName + ' ' +  directory_image + ' -w' + directory_output
    #foremost -o /home/work/Desktop/Tipp -i /home/work/NAS/Kunde/image/image.E01 -T
    #log2timeline /home/work/NAS/Kunde/log2timeline /home/work/NAS/Kunde/image/image.E01log

    commandListSudoDokumentation(command, directory)



def timeline(data):
    print('sechster Schritt begonnen')
    log2timeline(data)
    plaso(data)

    print('sechser Schritt fertig')

    routing_key = 'Ende'  # Nach welchen Kritereien zu Warteschlange geroutet wird
    # Wird Nachricht benötigt???
    sendMessageTopic(routing_key, data)


if __name__ == "__main__" :
    timeline(DATA)