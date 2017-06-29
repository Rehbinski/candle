from Forensic_function.global_function import *


# from start_client_linux import sendMessageTopic
# 3 mal austauschen

def umount(directory):
    command = 'echo password | sudo -S ' + "umount " + directory
    comandList(command)

def unmount_losetup(directory):
    #losetup -d / dev/loop0
    command = "losetup -d " + directory
    command = 'echo password | sudo -S ' + command
    sudo = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)

    for i in (sudo.stdout):
        a=i.decode('UTF-8')
        print(a)

if __name__ == "__main__" :

    directory = '/home/work/NAS/Kunde'
    target = '/dev/loop0'
    i = 1

#unmounten
    if i ==1 :
        for i in range(4):
            i = str(i)
            umount(directory + '/Partion'+i+'/Partion'+i)
            unmount_losetup(target)
            umount(directory+'/mount/')

    print('zweiter Schritt fertig')