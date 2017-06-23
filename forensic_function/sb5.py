import subprocess
import psutil
import re
import os
import time

from global_variable import *
from start_client import sendMessageTopic
from forensic_function.global_function import *

def get_directory():
    global disk
    device_list = get_partition()
    for device in device_list:
        if re.search("sd[b-z]", device):
            disk = device
    return  '/dev/' + disk

def get_partition():
    a=psutil.disk_partitions()
    list = []
    for i in a:
        info_device = i[0].split('/')
        device = info_device[2][0:3]
        list.append(device)
        #TODO Ueberpruefen ob hier Code eingeuegt wird zum weiteren uebergeben
    return list

def checksum(directory):
    command =  "md5sum " + directory
    list= comandListSudo(command)
    return list[0]

def ewfacquire(destination, directory):
    global sudo_command
    target = directory + '/image'
    command = 'ewfacquire ' + destination + ' -t ' + target + '/image' + ' -u'

    #sudo = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)
    list = commandListSudoDokumentation(command,directory)

    for i in list:
        str = i         #.decode("UTF-8")
        #if str.find('SUCCESS') > 0:
        #    success = True
        if str.find('calculated') > 0:
            checksum = str.rsplit(None, 1)[-1]
    return checksum

def copyDisk(data):
    directory = data.get('directory_root')
    print('erster Schritt begonnen')
    #Anzahl an durchlaeufen
    i=1
    pfad = get_directory()

    target = directory + '/image'

    #Ordner anlegen
    if not os.path.exists(target):
        os.makedirs(target)

    while i != 0:
        i = i - 1
        hash_checksum = checksum(pfad)
        print('Hashsum md5sum:' + hash_checksum)
        hashsum = (ewfacquire(pfad, directory))
        print('Hashsum ewfacquire:' + hashsum)
        print('Hashsum md5sum:' + hash_checksum)

        if checksum == hash_checksum:
            print('erfolgreich')
            break
    print('erster Schritt fertig')

    routing_key = 'Mount.MountDisk'  # Nach welchen Kritereien zu Warteschlange geroutet wird
    message = 'Nachricht fuer jedermann'  # Nachricht zum senden erzeugen
    # Wird Nachricht benötigt???
    sendMessageTopic(routing_key,message, directory)


if __name__ == "__main__" :
    # Ziel noch errechnen

    copyDisk(DATA)
    print('erster Schritt fertig')




