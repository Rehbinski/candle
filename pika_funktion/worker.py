import sys
import sys
sys.path.append("/home/work/NAS/Pythoncode/candle")
if r'C:\Users\root\PycharmProjects\candle' not in sys.path:
    sys.path.append(r'C:\Users\root\PycharmProjects\candle')
    print('Add')

from .function_Worker import ConsumerThread_retry
import time


if __name__ == "__main__":
    # * vor one word
    # # vor more words

    queue = 'testanlegen2'  # Zu welcher Warteschlange dann gerutet werden soll
    severities = ['info.*', 'test.*']  # Nach welchen Kritereien zu Warteschlange geroutet wird
    exchange = 'topic_logs'  # Wie man mag
    type = 'topic'  # Type auf welche Art der Worker hört

    threads = []
    for i in range(1):
        t = ConsumerThread_retry(queue, exchange, type, severities, 3)
        threads.append(t)

    queue = 'test'  # Zu welcher Warteschlange dann gerutet werden soll
    severities = ['error', 'info', 'warning']
    exchange = 'direct_logs'  # Wie man mag
    type = 'direct'  # Type auf welche Art der Worker hört

    for i in range(1):
        t = ConsumerThread_retry(queue, exchange, type, severities, 3)
        threads.append(t)


    for thread in threads:
        #thread.demon = True
        thread.start()
    #Ende sollte nicht erreicht werden, da Worker immer auf Arbeit warten
    #thread.join()
    #print('ende')



    while len(threads) > 0:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print ("Ctrl-c received! Sending kill to threads TODO...")
            #for thread in threads:
            #    thread.stop()
            #    threads.remove(thread)