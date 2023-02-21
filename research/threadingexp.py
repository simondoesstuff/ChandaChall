import concurrent.futures
import dis


def fn(a):
    return a


def main():
    workers = 3
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for size in range(50, 500, 50):
            results = list(executor.map(fn, range(size), chunksize=size // workers))
            print(f"Sum: {sum(results)}")


if __name__ == '__main__':
    graph = {2: 5, 9: 3}
    g = [graph]*4
    dis.dis(lambda x: g)
    main()