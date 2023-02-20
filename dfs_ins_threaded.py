import futureproof # threadpool


def import_data(path=f'./data/{3515}.txt'):
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
        line = ""
        
        for k, v in graph.items():
            formattedKey = ','.join(str(x) for x in from_bitwise(k))
            
            for vv in v:
                line += formattedKey
                line += "->"
                line += ','.join(str(x) for x in from_bitwise(vv))
                line += "\n"
        
        f.write(line)


def issubset(a, b):
    return (a & b) == a


def analyze(graph, node):
    visited = set()
    frontier = [0]
    
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
                yield node, parent, child
        
        if stuck:
            yield node, parent, None


def apply_insert(graph, node, parent, child):
    parentAdj = graph[parent]
    graph.setdefault(node, set())
    
    if child is None:
        parentAdj.add(node)
    else:
        graph[node].add(child)
        parentAdj.remove(child)
        parentAdj.add(node)


# runs in O(|S|^2) time
def build_graph(S, max_threads):
    graph = {}
    graph[0] = set()
    dataBySize = {}
    
    # sorting nodes by size
    for node in S:
        length = bin(node).count('1')
        dataBySize.setdefault(length, []).append(node)
    
    for k in sorted(dataBySize.keys()):
        threadPool = futureproof.ThreadPoolExecutor(max_workers=max_threads)
        
        with futureproof.TaskManager(threadPool) as tm:
            for node in dataBySize[k]:
                tm.submit(analyze, graph, node)

        for task in tm.results:
            for result in task:
                apply_insert(graph, *result)
    
    graph.pop(0)
    graph = {k: v for k, v in graph.items() if len(v) > 0}
    
    return graph


def solve(inPath, outPath, max_threads):
    S = import_data(inPath)
    graph = build_graph(S, max_threads)
    export_soln(graph, outPath)




import time
t0 = time.time()
p = 3515
solve(f'./data/{p}.txt', f'./data/solutions/{p}_dfsi_thread.txt', 10)
print(f"Time: {time.time() - t0} seconds")