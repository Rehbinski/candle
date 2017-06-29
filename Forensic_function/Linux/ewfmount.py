from Forensic_function.global_function import *
from global_variable import *
from start_client_linux import sendMessageTopic


def ewfmount(data):
    directory_root = data.get('directory_root')
    directory_ewf = data.get('directory_ewf')
    image = directory_root + '/image/image.E01'
    # Ordner erstellen
    if 'mount' not in os.listdir(directory_root):
        os.makedirs(directory_ewf)
    # ewfmount /home/work/NAS/Kunde/image/image.E01 /home/work/NAS/Kunde/mount
    command = "ewfmount " + image + ' ' + directory_ewf
    list = commandListSudoDokumentation(command, directory_root)
    routing_key = routingkeysNachbedingung.get('Ewfmount')  # Nach welchen Kritereien zu Warteschlange geroutet wird
    sendMessageTopic(routing_key, data)


def getEwf(data):
    print('zweiter Schritt begonnen')
    ewfmount(data)
    print('zweiter Schritt fertig')
    # routing_key = 'Programme.clamscannDisk'  # Nach welchen Kritereien zu Warteschlange geroutet wird


if __name__ == "__main__":
    getEwf(DATA)
