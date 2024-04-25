import os
import platform
import time
import asyncio
from zaber_motion.ascii import Connection
from zaber_motion import Units

CYCLES = 10000
THREAD_COUNT = 12

def main():
    loop = asyncio.get_event_loop()

    for thread_count in range(1, THREAD_COUNT + 1):
        loop.run_until_complete(speed_test_tasks(thread_count))

async def speed_test_tasks(thread_count):
    fibers = []

    for id in range(thread_count):
        fibers.append(speed_test())

    results = await asyncio.gather(*fibers)

    total_avg = sum(results) / thread_count
    print("{}: {}".format(thread_count, total_avg))

async def speed_test():
    values = []

    conn = await Connection.open_tcp_async("127.0.0.1", 11234)
    try:
        for _i in range(CYCLES):
            t = time.perf_counter()

            await conn.generic_command_async("")

            elapsed_time = time.perf_counter() - t
            values.append(elapsed_time * 1000)

    finally:
        await conn.close_async()

    avg = sum(values) / CYCLES
    return avg

# run main function on program start
if __name__ == '__main__':
    main()
