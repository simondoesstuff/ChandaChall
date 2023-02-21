import concurrent.futures # thread pool
import argparse
import time


def import_data(path):
    with open(path) as f:
        for line in f:
            value = 0
        
            for j in (int(x) for x in line.strip().split(' ')):
                j = j - 1
                value = value | (1 << j)
            
            yield value


def export_soln(graph, path):
    def from_bitwise(value):
        index = 1
    
        for i in bin(value)[2:][::-1]:
            if i == '1':
                yield index
            index += 1
    
    # the graph is a list of sets
    with open(path, 'w') as f:
        contents = []
        
        for k, v in graph.items():
            formattedKey = ','.join(str(x) for x in from_bitwise(k))
            
            for vv in v:
                formattedValue = ','.join(str(x) for x in from_bitwise(vv))
                contents.append(f"{formattedKey}->{formattedValue}")
        
        strContents = '\n'.join(contents)
        f.write(strContents)


def issubset(a, b):
    return (a & b) == a


def apply_insert(graph, node, parent, child):
    parentAdj = graph[parent]
    graph.setdefault(node, set())
    
    if child is None:
        parentAdj.add(node)
    else:
        graph[node].add(child)
        parentAdj.remove(child)
        parentAdj.add(node)


def analyze(graph, node):
    visited = set()
    frontier = [0]
    results = []
    
    while frontier != []:
        parent = frontier.pop()
        
        if parent in visited:
            continue
        
        visited.add(parent)       
        children = graph[parent]
        
        stuck = True

        for child in children:
            if child in visited:
                stuck = False
            if issubset(child, node):
                frontier.append(child)
                stuck = False
            elif issubset(node, child):
                # we have found an edge split
                stuck = False
                results.append((node, parent, child))
        
        if stuck:
            results.append((node, parent, None))
    
    return results


# runs in O(|S|^2) time
def build_graph(S, workers):
    graph = {0: set()}
    dataBySize = {}
    
    # sorting nodes by size
    for node in S:
        length = bin(node).count('1')
        dataBySize.setdefault(length, []).append(node)

    with concurrent.futures.ProcessPoolExecutor() as pool:
        for k in sorted(dataBySize.keys()):
            chunkSize = max(1, len(dataBySize[k]) // workers)
            nextNodeSet = dataBySize[k]
            results = list(pool.map(analyze, [graph]*len(nextNodeSet), nextNodeSet, chunksize=chunkSize))

            for result in results:
                for action in result:
                    apply_insert(graph, *action)
    
    graph.pop(0)
    graph = {k: v for k, v in graph.items() if len(v) > 0}
    
    return graph


def solve(inPath, outPath, workers):
    S = import_data(inPath)
    graph = build_graph(S, workers)
    export_soln(graph, outPath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("DFSIns")
    parser.add_argument('inPath', type=str, help='Path to input file')
    parser.add_argument('-o', '--outPath', type=str, help='Path to output file')
    parser.add_argument('-w', '--workers', type=int, help='Number of workers to use', default=4)
    args = parser.parse_args()
    
    args.outPath = args.outPath or args.inPath.replace('.txt', '.soln')
    
    t0 = time.time()
    solve(args.inPath, args.outPath, args.workers)
    print(f"Time: {time.time() - t0} seconds")
