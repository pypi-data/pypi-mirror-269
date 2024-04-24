import time
import sys

if sys.platform == "win32":
    timer = time.perf_counter
else:
    timer = time.time


def conv(data, mode="speed"):
    if mode == "speed":
        if data > 1000000:
            result = str(round(data / 1000000, 2)) + " M/S"
        elif data > 1000:
            result = str(round(data / 1000, 2)) + " K/S"
        else:
            result = str(round(data, 2)) + "/s"
    elif mode == "elapsed":
        if data > 0.001:
            result = str(round(data, 3)) + "s"
        elif data > 1e-6:
            result = str(int(data * 1e6)) + "ms"
        else:
            result = str(int(data * 1e9)) + "ns"
    return result


def vfunc(func, args, mode="speed"):
    stat = []

    for i in range(10):
        count = pow(10, i)
        start_time = timer()
        for i in range(count):
            func(*args)
        run_time = timer() - start_time

        if run_time > 0.01:
            if run_time > 1:
                count = 1
            else:
                count = int(1 / run_time * count)
            break

    while True:
        start_time = timer()
        for i in range(count):
            func(*args)

        run_time = timer() - start_time

        if mode == "speed":
            stat.append(count / run_time)
        else:
            stat.append(run_time / count)

        result = conv(sum(stat) / len(stat), mode)

        print(" " * 45, end="\r")
        print(result)
        print("repeat: {}  ".format(len(stat)), "avg = {}".format(result), end="\r")
