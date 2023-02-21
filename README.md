## This algorithm can solve the largest dataset in 135 seconds.

# Trickle Algorithm

For a dataset of $N$ nodes, the algorithm performs an insertion into the graph for each node.
The scan/insertion algorithm prunes unnecessary branches so it will almost never scan over all
previous nodes, but at theoretical worst case, it runs in $O(N)$.

**Overall Runtime:**  $\approx O(N^2)$

## Source Code

**Source**: [trickle.py](research/trickle.py)  
**79867.txt solution:** [79867.soln](data/solutions/trickle_threads/79867.soln)  

**Usage:** `py trickle.py 79867.txt`  
Performance can be increased with more workers: `py trickle.py 79867.txt -w 12`  
See all the options: `py trickle.py -h`  

## Explanation

### Insertion procedure

The insertion procedure inserts a single node at a time, `insertionNode`.
It is inserted into the graph using an algorithm similar to a modified DFS.  

The insertion process starts the search at the root of the graph. As it traverses, if
it encounters a branch that is not a subset of the insertionNode, it ignores it.
If it encounters a branch that is a subset, it follows it. If it follows the branch
until it hits a child that the insertionNode is a subset of, it splits the edge
and inserts the node. If it follows the branch to a dead end (that is, a child that the
insertionNode is not a child of or a lack of children),
it inserts the node under the current parent.

### Layered analysis

The insertion process will always produce the correct result if all nodes that the insertionNode
depends on are already within the graph. The insertionNode depends on nodes that *could* be a valid
parent. Since a node cannot have a parent of size greater than itself, all nodes will depend on, *at most*,
the nodes of smaller size.

Each node within the layer cannot depend on any other node in the layer and so their
computation can be done out of order and in parallel as long as they do not write to the graph.
Thus, I break the data up by size and handle each `layer` sequentially.

### Parallelization

All nodes within the `layer` perform their analysis of the graph in parallel.
After the analysis is complete, the results are applied to the graph all at once
in-sync.

Of course, speed will vary with hardware. But the parallelization with allow it to scale better with more CPUs.

### Extra tricks

Nodes are a series of binary attributes. I represent all nodes as a number with each bit corresponding
to an attribute. This allows me to determine $a \subset b$ in about 2 cycles. The bitwise conversion
is done on the dataset during import and export.

---

Simon Walker  
2/20/2022