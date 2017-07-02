from Forensic_function.Windows.global_function import commandListDokumentation
from Forensic_function.Windows.global_function import convert_path
from global_variable import *
from start_client_linux import sendMessageTopic


### Unter Benutzereinstellungen Rechte heruntersetzen

def osfmount(data):
    directory_root = convert_path(data.get('directory_root'))
    directory_partition = convert_path(data.get('directory_partion'))

    directory = directory_root + '\\image\\image.E01'
    #plus = r'Z:\Kunde\image\image.E01'
    offset = data.get('offset')
    command = "OSFMount -a -t file -f " + directory + ' -b ' + offset + ' -m #:'
    list = commandListDokumentation(command, directory_partition)

    for string in list:
        if "Created device" in string:
            buchstabe = string.split()
            richtig = buchstabe[3]


def mount(data):
    print('vierter Schritt begonnen')
    buchstabe = osfmount(data)
    print('vierter Schritt fertig')

    data_send = data
    data_send['laufwerksbuchstabe'] = buchstabe
    routing_key = 'Ende'  # Nach welchen Kritereien zu Warteschlange geroutet wird
    sendMessageTopic(routing_key, data_send)

    print('jaa so gehts')



if __name__ == "__main__":
    mount(DATA)
