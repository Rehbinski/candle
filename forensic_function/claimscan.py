#clamscan /home/work/NAS/usb -r -i --move=/home/work/NAS/clamscan

import subprocess
import os
import time

def comandList(command):
    sudo = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)
    list=[]
    for i in (sudo.stdout):
        str = i.decode('UTF-8')
        list.append(str)
    return list

def comandListSudo(command):
    command = 'echo password | sudo -S ' + command
    return comandList(command)

def clamscan(directory):
    comandName = 'clamscan'
    pfad = directory + '/' + comandName

    # Startzzeitpunkt festhalten
    start = time.strftime("%d.%m.%Y %H:%M:%S")
    #pfad =  directory.rsplit('/', 1)[0]

    #Ordner anlegen
    if not os.path.exists(pfad):
        os.makedirs(pfad)

    #Beginn beschritten
    fh = open(os.path.join(pfad+'/' + comandName + '_Info.txt'), 'a')
    fh.writelines('Beginn der Funktion '+ comandName +': ' + start + '\n')

    #Version festlegen
    version = comandList(comandName + ' -V')
    fh.write('Aktuelle Version: ')
    fh.writelines(version )
    fh.write('\n')

    #Befehl ausfuehren
    #clamscan /home/work/NAS/Kunde/usb -r -i --copy=/home/work/NAS/Kunde/clamscan
    command = comandName + directory + '/usb' + ' -r -i --copy='  +  pfad
    list = comandListSudo(command)

    #Ergebnis dokumentieren
    fh.writelines('Dies ist ein Test Enddatum:' + time.strftime("%d.%m.%Y %H:%M:%S") + '\n\n')
    fh.writelines(list)
    fh.close

if __name__ == "__main__" :

    directory = '/home/work/NAS/Kunde'
    t = clamscan(directory)

    print('dritter Schritt fertig')