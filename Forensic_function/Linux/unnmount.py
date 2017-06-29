from Forensic_function.global_function import *
from global_variable import *


def umount_partition(data):
    directory = data.get('directory_partion') + '/' + data.get('directory_partion').split('/')[-1]
    command = 'echo password | sudo -S ' + "umount " + directory
    comandList(command)


def umount_ewf(data):
    directory = data.get('directory_ewf')
    command = 'echo password | sudo -S ' + "umount " + directory
    comandList(command)

    # def unmount_losetup(directory):
    #losetup -d / dev/loop0
    command = "losetup -d " + directory
    command = 'echo password | sudo -S ' + command
    sudo = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)

    for i in (sudo.stdout):
        a=i.decode('UTF-8')
        print(a)

if __name__ == "__main__" :
    data = DATA

    directory = data.get('directory_root')
    target = '/dev/loop0'
    i = 1

#unmounten
    for i in range(4):
        i = str(i)
        partition = '/Partition' + i
        data['directory_partion'] = directory + partition
        umount_partition(data)
        # unmount_losetup(target)
    umount_ewf(data)

    print('zweiter Schritt fertig')