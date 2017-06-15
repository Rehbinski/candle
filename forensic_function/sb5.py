import subprocess
import psutil
import re
import os

sudo_command = 'echo password | sudo -S '

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
    global sudo_command
    command = sudo_command + "md5sum " + directory

    sudo = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)

    for i in (sudo.stdout):
        str=i.decode('UTF-8').split()
        return str[0]

def ewfacquire(destination, target):
    global sudo_command
    #success = False
    command = sudo_command + 'sudo ewfacquire '+ destination + ' -t ' + target + '/image' + ' -u'

    sudo = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)

    for i in (sudo.stdout):
        str = i.decode("UTF-8")
        #if str.find('SUCCESS') > 0:
        #    success = True
        if str.find('calculated') > 0:
            checksum = str.rsplit(None, 1)[-1]
        print (str)
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
        hashsum = (ewfacquire(directory, target))
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




