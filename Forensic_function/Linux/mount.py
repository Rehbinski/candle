import subprocess
import re
import os
import time

from global_variable import *
from start_client_linux import sendMessageTopic
from Forensic_function.global_function import *

def mount(data):
    #sudo mount /home/work/NAS/Kunde/mount/ewf1 /home/work/NAS/Kunde/usb -o loop,ro,show_sys_files,offset=1562835456
    #sudo mount /home/work/NAS/Kunde/mount/ewf1 /home/work/NAS/Kunde/usb -o loop,ro,show_sys_files,offset=1562835456
    directory = data.get('directory_root')
    directory = data.get('directory_partion_mount')
    target = data.get('directory_ewf') + '/ewf1'
    offset = data.get('offset')
    sizelimit = data.get('sizelimit')

    #target = '/dev/loop0'

    #Ordner erstellen
    if not os.path.exists(directory):
        os.makedirs(directory)

#mount /home/work/NAS/Kunde/mount/ewf1 /home/work/NAS/Kunde/Partion1/Partion1 -o loop,ro,show_sys_files,offset=1044610560,sizelimit=2056319488 -t auto
    command = 'mount ' + target + ' ' + directory + ' -o loop,ro,show_sys_files,offset=' + str(offset) + ',sizelimit=' + str(sizelimit)
    command = 'echo password | sudo -S ' + command
    sudo = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)

    for i in (sudo.stdout):
        string = i.decode('UTF-8')
        print(string)


def mountDisk(data):
    print('dritter Schritt begonnen')
    mount(data)
    print('dritter Schritt fertig')

    routing_key = 'Programme'  # Nach welchen Kritereien zu Warteschlange geroutet wird
    message = 'Nachricht fuer jedermann'  # Nachricht zum senden erzeugen
    # Wird Nachricht benötigt???
    sendMessageTopic(routing_key, data)


if __name__ == "__main__" :
    mountDisk(DATA)
