#clamscan /home/work/NAS/usb -r -i --move=/home/work/NAS/clamscan

from Forensic_function.global_function import *
from global_variable import *
from start_client_linux import sendMessageTopic


def clamscan(data):
    directory = data.get('directory_partion')
    directory_mount = data.get('directory_partion_mount')

    commandName = 'clamscan'
    pfad = directory + '/' + commandName
    #clamscan /home/work/NAS/Kunde/usb -r -i --copy=/home/work/NAS/Kunde/clamscan
    command = commandName + ' ' + directory_mount + ' -r -i --copy='  +  pfad
    commandListSudoDokumentation(command, directory)


def clamscanDisk(data):
    print('vierter Schritt begonnen')
    clamscan(data)
    print('vierter Schritt fertig')

    routing_key = routingkeysNachbedingung.get('ClamscannDisk')
    sendMessageTopic(routing_key, data)



if __name__ == "__main__" :
    clamscanDisk(DATA)