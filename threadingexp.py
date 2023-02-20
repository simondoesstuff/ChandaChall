import concurrent.futures
import time


def demo_func(num):
    for i in range(num):
        a = i**2


def without_threads():
    for i in range(6):
        demo_func(10000000)


def threads():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(demo_func, [10000000]*3)
        executor.map(demo_func, [10000000]*3)


def main():
    t0 = time.time()
    without_threads()
    print(f'Without threads: {time.time() - t0}')
    t0 = time.time()
    threads()
    print(f'With threads: {time.time() - t0}')


if __name__ == '__main__':
    main()