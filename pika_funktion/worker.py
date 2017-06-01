
from pika_funktion.function_Worker import ConsumerThread_retry




if __name__ == "__main__":
    #normaler worker
    #_worker(queue,exchange,type,severities)

    #normaler worker topic
    # * vor one word
    # # vor more words
    """"
    exchange = 'topic_logs'
    type = 'topic'
    binding_keys = ['info.*', 'test.*']
    _worker(queue,exchange,type,binding_keys)
    """

    #_workerRetry(queue,exchange,type,severities,3)

    """
    threads = []
    for i in range(2):
        t = ConsumerThread(queue, exchange, type, severities)
        threads.append(t)


    for thread in threads:
        thread.start()
    """

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
    thread.join()
    print('ende')
