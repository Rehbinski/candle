from global_variable import *
list = ['Dies ist NTFS', 'affs k', 'Dies nicht', 'adfss', 'ext', 'lalala','affs']
#if any(word in test for word in list):
#    print('test')

for string in (list):
    for partion_format in partion_formate:
        partion_format_low = partion_format.lower()
        string_low = string.lower()
        if partion_format_low in string_low:
            print(partion_format)#Dies wird gebraucht
            #Uebergabe in Funktion Parameter

