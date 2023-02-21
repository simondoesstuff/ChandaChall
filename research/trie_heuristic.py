class Trie:
    def __init__(self):
        self.adjacent = {}
        self.adjacent[tuple()] = set()
    
    def insert(self, node):
        root = tuple()
        
        for i in range(len(node)):
            nextKey = node[i]
            nextNode = root + (nextKey,)
            adjNodes = self.adjacent[root]
            
            if nextNode not in adjNodes:
                self.adjacent[root].add(nextNode)
                self.adjacent[nextNode] = set()

            root = nextNode
    
    def describe(self):
        for node in self.adjacent:
            p = ','.join([str(x) for x in node])
            c = ', '.join([str(x) for x in self.adjacent[node]])
            print(f"{p} -> {c}")


def build_trie(S):
    trie = Trie()
    
    for node in S:
        trie.insert(node)
    
    return trie