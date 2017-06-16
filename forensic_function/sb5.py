import subprocess
import psutil
import re
import os
import time

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

def copy_disk(pfad):
    #Anzahl an durchlaeufen
    i=1
    directory = get_directory()

    target = pfad + '/image'

    #Ordner anlegen
    if not os.path.exists(target):
        os.makedirs(target)

    while i != 0:
        i = i - 1
        hash_checksum = checksum(directory)
        print('Hashsum md5sum:' + hash_checksum)
        hashsum = (ewfacquire(directory, pfad))
        print('Hashsum ewfacquire:' + hashsum)
        print('Hashsum md5sum:' + hash_checksum)

        if checksum == hash_checksum:
            print('erfolgreich')
            break


if __name__ == "__main__" :
    target = '/home/work/NAS/Kunde'
    # Ziel noch errechnen
    copy_disk(target)
    print('erster Schritt fertig')




