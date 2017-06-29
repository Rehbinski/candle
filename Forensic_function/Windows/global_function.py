import subprocess
import os
import time

def convert_path(path):
    #plus = r'/home/work/NAS/Kunde/image/image.E01'
    path = path.replace('/', '\\')
    path = path.replace('\\home\\work\\NAS','Z:')
    return path

def searching(ordner):
    path =r'C:\Program Files'
    for root, dirs, filenames in os.walk(path):
        if root.split(os.sep)[-1] == ordner:
            return root
            print(root)

def comandList(command):

    ordner = command.split()[0]
    #inkscape_dir=r"c:\Program Files\OSFMount"
    inkscape_dir = searching(ordner)
    assert os.path.isdir(inkscape_dir)
    os.chdir(inkscape_dir)

    sudo = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)

    list=[]
    for i in (sudo.stdout):
        try:
            str = i.decode('UTF-8')
            list.append(str)
            #Zum Debugen print anmachen
            print(str)
        except:
            try:
                str = i.decode('ISO-8859-1')
                list.append(str)
                #Zum Debugen print anmachen
                print(str)
            except:
                pass


    return list

def commandListDokumentation(command, directory):

    # Startzzeitpunkt festhalten
    commandName = command.split()[0].lower()
    pfad = directory + '\\' + commandName.split('.')[0]
    start = time.strftime("%d.%m.%Y %H:%M:%S")

    # Ordner anlegen
    if not os.path.exists(pfad):
        os.makedirs(pfad)


    # Version festlegen
    #version = comandList(commandName + ' -V')

    # Befehl ausfuehren
    list = comandList(command)



    # Ergebnis dokumentieren
    # Beginn beschritten
    fh = open(os.path.join(pfad + '/' + commandName + '_Info.txt'), 'a')
    fh.write('Beginn der Funktion ' + commandName + ': ' + start + '\n')
    fh.write('Ende der Funktion ' + commandName + ': ' + time.strftime("%d.%m.%Y %H:%M:%S") + '\n')
    fh.write('Aktuelle Version: ')
    #fh.writelines(version)
    fh.write('\n\n')
    fh.writelines(list)
    fh.write('---------------------- END PROGRAMM ----------------------\n\n')
    fh.close
    return list


if __name__ == "__main__":
    print(searching('OSFMount'))
