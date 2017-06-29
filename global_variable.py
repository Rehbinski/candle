#Testdaten
# TODO imagenamen mit integrieren
# TODO formate einpflegen
DATA = {
    'directory_root': '/home/work/NAS/Kunde',
    'directory_ewf': '/home/work/NAS/Kunde/mount',
    'directory_partion_mount': '/home/work/NAS/Kunde/Partion0/mount',
    'directory_partion': '/home/work/NAS/Kunde/Partion0',
    # 'directory_image': '/home/work/NAS/Kunde/image',
    # 'image': '/image.E01',
    'laufwerksbuchstabe': 'G:\\',
    'offset': '1',
    'domain': 'Windows',
    'message': 'Dies ist die neue Data Message',
    'priority' : 0,

}

# Formate zum mounten
formate = 'adfs, affs, autofs, cifs, coda, coherent, cramfs, debugfs, devpts, efs, ext, ext2, ext3, ext4, hfs, hfsplus, hpfs, iso9660, jfs, minix, msdos, ncpfs, nfs, nfs4, ntfs, proc, qnx4, ramfs, reiserfs, romfs, squashfs, smbfs, sysv, tmpfs, ubifs, udf, ufs, umsdos, usbfs, vfat, xenix, xfs, xiafs'.split(',')
partion_formate = [x.strip(' ') for x in formate]

# Konfiguration zum starten
retries = 2

# Routingkeys
# routingkeysVorbedingung.get('')
routingkeysNachbedingung = {
    'Copydisk': 'Mount.Ewfmount',
    'Ewfmount': 'Programme_EWF',
    'Partition': 'Partition.MountDisk',
    'Mountdisklinux': 'Programme',
    'ForemostScan': 'Ende',
    'Timeline': 'Ende',
    'ClamscannDisk': 'Ende'
}
routingkeysVorbedingung = {
    'Copydisk': 'Copy.Copydisk',
    'Ewfmount': routingkeysNachbedingung.get('Copydisk'),
    'Partition': routingkeysNachbedingung.get('Ewfmount') + '.Partition',
    'MountDisk_Linux': routingkeysNachbedingung.get('Partition'),
    'ForemostScan': routingkeysNachbedingung.get('Ewfmount') + '.foremost',
    'Timeline': routingkeysNachbedingung.get('Ewfmount') + '.timeline',
    'ClamscannDisk': routingkeysNachbedingung.get('Mountdisklinux') + '.clamscannDisk',
}
