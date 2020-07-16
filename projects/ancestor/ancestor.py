
from util import Queue


def earliest_ancestor(ancestors, starting_node):
    # graph is a connections list of {child: [parents]}
    graph = build_graph(ancestors)
    # paths is all the paths from the starting node to the top of the tree
    # this is a BFS
    paths = find_ancestors(graph, starting_node)
    # we then need to find the longest path or the path with the lowest end ID
    if paths != -1:
        long = None
        end = None
        for path in paths:
            if long is None:
                long = len(path)
                end = path[-1]
            elif long < len(path):
                long = len(path)
                end = path[-1]
            elif long == len(path):
                if end > path[-1]:
                    end = path[-1]
        return end
    else:
        return -1


def build_graph(connections):
    nodes = {}
    for b, a in connections:
        if a in nodes:
            nodes[a].append(b)
        else:
            nodes[a] = [b]
    return nodes


def find_ancestors(graph, start):
    if start not in graph:
        return -1
    paths = {start: [start]}
    ends = []
    q = Queue()
    q.enqueue((start, None))
    while q.size() > 0:
        n, t = q.dequeue()
        if n not in paths:
            if n in graph:
                paths[n] = paths[t] + [n]
                for x in graph[n]:
                    q.enqueue((x, n))
            else:
                ends.append(paths[t]+[n])
        if n == start:
            for x in graph[n]:
                q.enqueue((x, n))
    return ends
