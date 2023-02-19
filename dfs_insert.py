import io_utils


def dfs_insert(graph, node):
    visited = set()
    frontier = [frozenset()]
    
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
            if child.issubset(node):
                frontier.append(child)
                stuck = False
            elif node.issubset(child):
                # we have found an edge split
                graph[node].add(child)
                graph[parent].remove(child)
                graph[parent].add(node)
                stuck = False
        
        if stuck:
            graph[parent].add(node)


# runs in O(|S|^2) time
def build_graph(S):
    graph = {}
    graph[frozenset()] = set()
    
    # runs in O(|S|^2) time
    for node in sorted(S, key=len):
        # insert the node into the graph
        dfs_insert(graph, node) # DFS runs in O(|V| + |E|) time
        # this graph in particular has |V| ~ |E|, so this is O(|V|) time
    
    graph.pop(frozenset())
    graph = {k: v for k, v in graph.items() if len(v) > 0}
    
    return graph


def solve(inPath, outPath):
    S = io_utils.import_data_sets(inPath)
    graph = build_graph(S)
    io_utils.export_soln(graph, outPath)
    
    



solve('./data/3515.txt', './data/solutions/3515_dfs_insert.txt')