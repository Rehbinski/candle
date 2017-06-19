import subprocess
import os
import time

sudo_command = 'echo password | sudo -S '

def comandList(command):
    sudo = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)
    list=[]
    for i in (sudo.stdout):
        str = i.decode('UTF-8')
        list.append(str)
        #Zum Debugen print anmachen
        #print(str)
    return list

def comandListSudo(command):
    command = 'echo password | sudo -S ' + command
    return comandList(command)

def commandListSudoDokumentation(command, directory):
    # Startzzeitpunkt festhalten
    commandName = command.split()[0].lower()
    pfad = directory + '/' + commandName
    start = time.strftime("%d.%m.%Y %H:%M:%S")
    # pfad =  directory.rsplit('/', 1)[0]
    # Ordner anlegen
    if not os.path.exists(pfad):
        os.makedirs(pfad)

    # Beginn beschritten
    fh = open(os.path.join(pfad + '/' + commandName + '_Info.txt'), 'a')
    fh.writelines('Beginn der Funktion ' + commandName + ': ' + start + '\n')
    # Version festlegen
    version = comandList(commandName + ' -V')
    fh.write('Aktuelle Version: ')
    fh.writelines(version)
    fh.write('\n')
    # Befehl ausfuehren
    list = comandListSudo(command)
    # Ergebnis dokumentieren
    fh.writelines('Dies ist ein Test Enddatum:' + time.strftime("%d.%m.%Y %H:%M:%S") + '\n\n')
    fh.writelines(list)
    fh.write('---------------------- END PROGRAMM ----------------------')
    fh.close
    return list
