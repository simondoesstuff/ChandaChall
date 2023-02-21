def import_data(path=f'./data/{3515}.txt'):
    with open(path) as f:
        S = []
        
        for line in f:
            split = tuple(sorted(int(x) for x in line.strip().split(' ')))
            S.append(split)
        
    return S


def import_data_sets(path=f'./data/{3515}.txt'):
    with open(path) as f:
        S = set()
        
        for line in f:
            split = frozenset(int(x) for x in line.strip().split(' '))
            S.add(split)
        
    return S


def import_solution(path=f'./data/solutions/{3515}_naive.txt'):
    m = {}
    
    with open(path) as f:
        for line in f.readlines():
            split = line.split('->')
            clean = lambda x: tuple(sorted(int(x) for x in x.strip().split(',')))
            
            parent = clean(split[0])
            child = clean(split[1])
            
            if parent not in m:
                m[parent] = set()
            
            m[parent].add(child)
    
    return m


def import_soln_sets(path=f'./data/solutions/{3515}_naive.txt'):
    m = {}
    
    with open(path) as f:
        for line in f.readlines():
            split = line.split('->')
            clean = lambda x: frozenset(int(x) for x in x.strip().split(','))
            
            parent = clean(split[0])
            child = clean(split[1])
            
            if parent not in m:
                m[parent] = set()
            
            m[parent].add(child)
    
    return m


def export_soln(graph, path):
    # the graph is a list of sets
    with open(path, 'w') as f:
        formatted = ""
        
        for k, v in graph.items():
            for vv in v:
                formatted += ','.join(str(x) for x in sorted(list(k)))
                formatted += "->"
                formatted += ','.join(str(x) for x in sorted(vv))
                formatted += "\n"
        
        f.write(formatted)