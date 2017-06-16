#clamscan /home/work/NAS/usb -r -i --move=/home/work/NAS/clamscan

import subprocess
import os
import time

from forensic_function.global_function import *

def clamscan(directory):
    commandName = 'clamscan'
    pfad = directory + '/' + commandName
    #clamscan /home/work/NAS/Kunde/usb -r -i --copy=/home/work/NAS/Kunde/clamscan
    command = commandName + ' ' + directory + '/usb' + ' -r -i --copy='  +  pfad

    commandListSudoDokumentation(command, directory)



if __name__ == "__main__" :

    directory = '/home/work/NAS/Kunde'
    t = clamscan(directory)

    print('dritter Schritt fertig')