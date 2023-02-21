import concurrent.futures # thread pool


_silent = False
def _log(message):
    global _silent
    if not _silent:
        print(message)


def import_data(path):
    """Imports data from a file. The file should be a list of integers separated by spaces on each line.
    Nodes are represented as a bitwise integer where each bit represents an attribute.

    Args:
        path (str): Input file path

    Yields:
        int: extracted node
    """
    
    with open(path) as f:
        for line in f:
            value = 0
        
            for j in (int(x) for x in line.strip().split(' ')):
                j = j - 1
                value = value | (1 << j)
            
            yield value


def export_soln(graph, path):
    """Exports the solution to a file. The file is a list of edges separated by newlines.
    Takes in a graph of nodes represented as a bitwise integer and converts it to a list of integers.

    Args:
        path (str): Output file path
    """
    
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


def _issubset(a, b):
    return (a & b) == a


def _apply_insert(graph, node, parent, child):
    """Apply an insert operation to the graph.
    If child is None, then the node is inserted as new a child of parent.
    Otherwise, the edge is split and the node is inserted as a child of parent and child is inserted as a child of node.
    """
    
    parentAdj = graph[parent]
    graph.setdefault(node, set())
    
    if child is None:
        parentAdj.add(node)
    else:
        graph[node].add(child)
        parentAdj.remove(child)
        parentAdj.add(node)


def _analyze(graph, node):
    """Analyze the graph in the context of a single node.

    Returns:
        (int, int, int): (node, parent, child) representing the edge split; the change to the graph
    """
    
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
            # if the child is a subset of the node, we continue along the path
            if _issubset(child, node):
                frontier.append(child)
                stuck = False
            # if the node is a subset of the child, we have found an edge split
            elif _issubset(node, child):
                # we have found an edge split
                stuck = False
                results.append((node, parent, child))
        
        if stuck:
            # dead end; append a new branch
            results.append((node, parent, None))
    
    return results


# runs in O(|S|^2) time
def build_graph(S, workers):
    """Analyze the graph and build the solution.

    Args:
        workers (int): Workers to use for parallelization

    Returns:
        Dictionary: Graph in the form of a dictionary of edges
    """
    
    S = list(S)
    dataSize = len(S)
    graph = {0: set()}
    dataBySize = {}

    # sorting nodes by size
    for node in S:
        length = bin(node).count('1')
        dataBySize.setdefault(length, []).append(node)
    
    _log(f"- Analyzing {len(S)} nodes with {workers} workers.")
    _log(f"- Beginning with {len(dataBySize)} layers.")

    completedNodes = 0

    with concurrent.futures.ProcessPoolExecutor() as pool:
        # analysis must be done in layers; nodes of the same size must be analyzed together
        for k in sorted(dataBySize.keys()):
            nextLayer = dataBySize[k]
            layerSize = len(nextLayer)
            chunkSize = max(1, layerSize // workers)
            
            # parallelize the analysis
            results = list(pool.map(_analyze, [graph] * layerSize, nextLayer, chunksize=chunkSize))

            # apply the results in sync to avoid race conditions
            for result in results:
                for action in result:
                    _apply_insert(graph, *action)
            
            completedNodes += layerSize
            _log(f"\t- ~{completedNodes/dataSize * 100:.1f}% done.\tCompleted layer {k + 1} with {len(nextLayer)} nodes.")
    
    # root node is not part of the solution
    graph.pop(0)
    # remove nodes with no children
    graph = {k: v for k, v in graph.items() if len(v) > 0}
    
    return graph


def solve(inPath: str, outPath: str, workers: int):
    """Solve the DNA subset problem.
     
    Args:
        inPath (str): Data input path
        outPath (str): Data output path
        workers (int): Amount of workers to use for parallelization
    """
    
    S = import_data(inPath)
    graph = build_graph(S, workers)
    _log("- Completed analysis.")
    export_soln(graph, outPath)


if __name__ == '__main__':
    # these imports are only used for the command line interface
    # the API does not require them
    import argparse
    import time
    import os
    
    parser = argparse.ArgumentParser("DFSIns")
    parser.add_argument('inPath', type=str, help='Path to input file')
    parser.add_argument('-o', '--outPath', type=str, help='Path to output file')
    parser.add_argument('-w', '--workers', type=int, help='Number of workers to use', default=4)
    parser.add_argument('-s', '--silent', action=argparse.BooleanOptionalAction, help='Turn off logging', default=False)
    args = parser.parse_args()
    
    args.outPath = args.outPath or args.inPath.replace('.txt', '.soln')
    
    # check if the output file's directory exists
    if not os.path.exists(os.path.dirname(args.outPath)):
        print(f"Output directory {os.path.dirname(args.outPath)} does not exist.")
        raise SystemExit
    
    _silent = args.silent
    
    t0 = time.time()
    solve(args.inPath, args.outPath, args.workers)
    _log(f"Time elapsed: {time.time() - t0} seconds")
