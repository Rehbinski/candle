from pika_funktion.function_Worker import ConsumerThread_retry

if __name__ == "__main__":
    # * vor one word
    # # vor more words

    queue = 'blubb'  # Zu welcher Warteschlange dann gerutet werden soll
    severities = ['info.*', 'test.*']  # Nach welchen Kritereien zu Warteschlange geroutet wird
    exchange = 'topic_logs'  # Wie man mag
    type = 'topic'  # Type auf welche Art der Worker hört

    threads = []
    for i in range(1):
        t = ConsumerThread_retry(queue, exchange, type, severities, 3)
        threads.append(t)


    for thread in threads:
        thread.start()
    #Ende sollte nicht erreicht werden, da Worker immer auf Arbeit warten
    #thread.join()
    #print('ende')
