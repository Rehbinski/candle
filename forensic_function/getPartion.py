import re

from start_client import sendMessageTopic
from forensic_function.global_function import *
from global_variable import *


def ewfmount(data):
    directory_root = data.get('directory_root')
    directory_ewf = data.get('directory_ewf')
    image= directory_root + '/image/image.E01'
    #Ordner erstellen
    if 'mount' not in os.listdir(directory_root):
        os.makedirs(directory_ewf)
    #ewfmount /home/work/NAS/Kunde/image/image.E01 /home/work/NAS/Kunde/mount
    command = "ewfmount " + image + ' ' + directory_ewf
    list = commandListSudoDokumentation(command, directory_root)

def mmls(data):
    directory = data.get('directory_root')
    path = data.get('directory_ewf') + '/ewf1'
    partionNumber = 0

    command = "mmls " + path
    list = commandListSudoDokumentation(command,directory)
    sector = None
    for string in (list):
        if string.find('sectors') > 0:
            sector = int(re.findall('\d+', string)[0])
    for string in (list):
        #if any(word in string.lower for word in format):
        if string.find('NTFS') > 0 or string.find('FAT32') > 0 or string.find('EXT') > 0:
            offset = int(string.split()[2])
            sizelimit = int(string.split()[3])
            routing_key = 'Mount.MountDisk'                                 # Nach welchen Kritereien zu Warteschlange geroutet wird
            directory_partion = directory + '/Partion' + str(partionNumber)
            directory_partion_mount = directory_partion + '/Partion'+ str(partionNumber)
            # Ordner erstellen
            if 'Partion'+ str(partionNumber) not in os.listdir(directory):
                os.makedirs(directory_partion)
            if 'Partion' + str(partionNumber) not in os.listdir(directory_partion):
                os.makedirs(directory_partion_mount)
            data_send = data
            data_send['directory_partion'] = directory_partion
            data_send['directory_partion_mount'] = directory_partion_mount
            data_send['offset'] = offset * sector
            data_send['sizelimit'] =  sizelimit * sector
            sendMessageTopic(routing_key, data_send)
            print('Send Message an: ' + directory_partion)
            partionNumber += 1

    return list

def getPartion(data):
    print('zweiter Schritt begonnen')
    ewfmount(data)
    mmls(data)
    print('zweiter Schritt fertig')
    #routing_key = 'Programme.clamscannDisk'  # Nach welchen Kritereien zu Warteschlange geroutet wird

if __name__ == "__main__" :
    getPartion(DATA)