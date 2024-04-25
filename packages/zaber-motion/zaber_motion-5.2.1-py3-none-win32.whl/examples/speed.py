import os
import platform
import time
from threading import Thread, Lock
from zaber_motion.ascii import Connection
from zaber_motion import Units

CYCLES = 10000
THREAD_COUNT = 12

results = []
lock = Lock()

def main():
    for thread_count in range(1, THREAD_COUNT + 1):
        speed_test_threads(thread_count)

def speed_test_threads(thread_count):
    threads = []
    results.clear()

    for id in range(thread_count):
        thread = Thread(target = speed_test, args = (id, ))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    total_avg = sum(results) / thread_count
    print("{}: {}".format(thread_count, total_avg))

def speed_test(id):
    conn = Connection.open_tcp("127.0.0.1", 11234)

    values = []
    for _i in range(CYCLES):
        t = time.perf_counter()

        conn.generic_command("")

        elapsed_time = time.perf_counter() - t
        values.append(elapsed_time * 1000)

    conn.close()

    avg = sum(values) / CYCLES
    with lock:
        results.append(avg)

# run main function on program start
if __name__ == '__main__':
    main()
