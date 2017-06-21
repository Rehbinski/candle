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
        print(str)
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


    # Version festlegen
    version = comandList(commandName + ' -V')
    # Befehl ausfuehren
    list = comandListSudo(command)
    # Ergebnis dokumentieren
    # Beginn beschritten
    fh = open(os.path.join(pfad + '/' + commandName + '_Info.txt'), 'a')
    fh.write('Beginn der Funktion ' + commandName + ': ' + start + '\n')
    fh.write('Ende der Funktion ' + commandName + ': ' + time.strftime("%d.%m.%Y %H:%M:%S") + '\n')
    fh.write('Aktuelle Version: ')
    fh.writelines(version)
    fh.write('\n\n')
    fh.writelines(list)
    fh.write('---------------------- END PROGRAMM ----------------------\n\n')
    fh.close
    return list
