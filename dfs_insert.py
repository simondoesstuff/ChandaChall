import io_utils


def dfs_insert(graph, node):
    visited = set()
    frontier = [tuple()]
    
    if node not in graph:
        graph[node] = set()
    
    while frontier != []:
        parent = frontier.pop()
        visited.add(parent)       
        children = graph[parent]
        
        if len(children) == 0:
            # we have reached a leaf
            graph[parent].add(node)
            continue
        
        for child in children - visited:
            if set(child).issubset(node):
                frontier.append(child)
            elif set(parent).issubset(node) and set(node).issubset(child):
                # we have found an edge split
                graph[node].add(child)
                graph[parent].remove(child)
                graph[parent].add(node)
            else:
                graph[parent].add(node)


def build_graph(S):
    graph = {}
    graph[tuple()] = set()
    
    for node in S:
        # insert the node into the graph
        dfs_insert(graph, node)
    
    graph.pop(tuple())
    graph = {k: v for k, v in graph.items() if len(v) > 0}
    
    return graph


def solve(inPath, outPath):
    S = io_utils.import_data(inPath)
    graph = build_graph(S)
    io_utils.export_soln(graph, outPath)



data = [(2,), (1, 2), (2, 3), (1, 2, 3), (1, 2, 3, 4), (1, 2, 3, 4, 5)]
data.reverse()
graph = build_graph(data)
print(graph)