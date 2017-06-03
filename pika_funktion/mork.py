while len(threads) > 0:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print("Ctrl-c received! Sending kill to threads...")
        for thread in threads:
            print(threads)
            thread.stop()
            print(threads)

print('Festpatte image machst isolieren der Partitionen Filesystem zu dateien')
print('USB Stick -> '
      'klassische Partitionen'
      'Gwd'
      'FDisk output')

for i in range(5):
    print(i)