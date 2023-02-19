def issubset(a, b):
    return (a & b) == a


def dfs_insert(graph, node):
    visited = set()
    frontier = [0]
    
    if node not in graph:
        graph[node] = set()
    
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
                graph[node].add(child)
                graph[parent].remove(child)
                graph[parent].add(node)
                stuck = False
        
        if stuck:
            graph[parent].add(node)


def single_from_bitwise(value):
    index = 1
    
    for i in bin(value)[2:][::-1]:
        if i == '1':
            yield index
        index += 1


def import_data(path=f'./data/{3515}.txt'):
    with open(path) as f:
        S = []
        
        for line in f:
            value = 0
        
            for j in (int(x) for x in line.strip().split(' ')):
                j = j - 1
                value = value | (1 << j)
            
            S.append(value)
        
    return S


def export_soln(graph, path):
    # the graph is a list of sets
    with open(path, 'w') as f:
        line = ""
        
        for k, v in graph.items():
            formattedKey = ','.join(str(x) for x in single_from_bitwise(k))
            
            for vv in v:
                line += formattedKey
                line += "->"
                line += ','.join(str(x) for x in single_from_bitwise(vv))
                line += "\n"
        
        f.write(line)


# runs in O(|S|^2) time
def build_graph(S):
    graph = {}
    graph[0] = set()
    
    # runs in O(|S|^2) time
    for node in sorted(S, key=lambda x: bin(x).count('1')):
        # insert the node into the graph
        dfs_insert(graph, node) # DFS runs in O(|V| + |E|) time
        # this graph in particular has |V| ~ |E|, so this is O(|V|) time
    
    graph.pop(0)
    graph = {k: v for k, v in graph.items() if len(v) > 0}
    
    return graph


def solve(inPath, outPath):
    S = import_data(inPath)
    graph = build_graph(S)
    export_soln(graph, outPath)
    
    



solve('./data/3515.txt', './data/solutions/3515_dfs_insert.txt')