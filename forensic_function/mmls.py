import subprocess
import re
import os
import time

from forensic_function.global_function import *
# 3 mal austauschen

def ewfmount(directory):
    pfad=directory+'/mount'
    image= directory + '/image/image.E01'
    #Ordner erstellen
    if not (os.path.exists(pfad) or os.path.isfile(image)):
        os.makedirs(pfad)
    #Ordner erstellen
    #if not os.path.exists(directory):
    #    os.makedirs(directory)
    #ewfmount /home/work/NAS/Kunde/image/image.E01 /home/work/NAS/Kunde/mount
    command = "ewfmount " + image + ' ' + pfad
    #comandListSudo(command)
    list = commandListSudoDokumentation(command,directory)


def umount(directory):
    command = 'echo password | sudo -S ' + "umount " + directory
    comandList(command)

def mmls(directory):
    path = directory+ '/mount/ewf1'

    command = "mmls " + path
    #command = 'echo password | sudo -S ' + command
    #sudo = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)
    list = commandListSudoDokumentation(command,directory)

    for i in (list):
        #str = i.decode('UTF-8')
        str = i
        #print(str)
        if str.find('NTFS') > 0:
            start = int(str.split()[2])
        if str.find('sectors') > 0:
            sector = int(re.findall('\d+', str)[0])
            # Anstossen von naesten arbeiter uebergabe von Start mal sector
    return sector * start

def losetup(directory):
    #sudo losetup -o16384 -r /dev/loop0 /mnt/ewf/ewf1
    path =directory + '/mount'
    target = '/dev/loop0'
    #Ordner erstellen
    #if not os.path.exists(directory):
    #    os.makedirs(directory)


    #losetup -o16384 -r /dev/Kunde /home/work/NAS/Kunde/mount/ewf1
    #offset = '16384'
    offset = mmls(directory)
    command = "losetup -o" + str(offset) +' -r '+ target + ' ' + path + '/ewf1'
    #command = 'echo password | sudo -S ' + command
    #sudo = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)
    list = commandListSudoDokumentation(command,directory)


def unmount_losetup(directory):
    #losetup -d / dev/loop0
    command = "losetup -d " + directory
    command = 'echo password | sudo -S ' + command
    sudo = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)

    for i in (sudo.stdout):
        a=i.decode('UTF-8')
        print(a)

def mount(directory):
    #sudo mount /dev/loop0 /mnt/usb -o loop,ro,show_sys_files
    directory = directory + '/usb'
    target = '/dev/loop0'

    #Ordner erstellen
    if not os.path.exists(directory):
        os.makedirs(directory)

    command = 'mount ' + target + ' ' + directory + ' -o loop,ro,show_sys_files'
    command = 'echo password | sudo -S ' + command
    sudo = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)

    for i in (sudo.stdout):
        str = i.decode('UTF-8')
        print(str)

if __name__ == "__main__" :



    #directory = '/home/work/NAS/Testimage/'
    #directory = '/mnt/ewf/'
    directory = '/home/work/NAS/Kunde'
    target = '/dev/loop0'
    #ziel = '/mnt/usb'
    i = 0
    if i ==0:
        ewfmount(directory)
        #offset = mmls(directory+'ewf1')

        #sudo losetup -o16384 -r /dev/loop0 /mnt/ewf/ewf1
        losetup(directory)

        #sudo mount /dev/loop0 /mnt/usb -o loop,ro,show_sys_files
        mount(directory)

#unmounten
    if i ==1 :
        umount(directory + '/usb')
        unmount_losetup(target)
        umount(directory+'/mount/')

    print('zweiter Schritt fertig')