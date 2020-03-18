from collections import defaultdict


def earliest_ancestor(ancestors, starting_node):
    graph = defaultdict(set)
    for (parent, child) in ancestors:
        if not graph[parent]:
            graph[parent] = set()
        graph[parent].add(child)
    return dfs(graph, starting_node, ancestors)


def dfs(graph, starting_node, ancestors):
    visited = set()
    stack = []
    stack.append([starting_node])
    while len(stack) > 0:
        path = stack.pop()
        nodes = set(path) - visited
        for vertex in nodes:
            parents = [parent for (parent, child)
                       in ancestors if child == vertex]
            if len(parents) == 0:
                return -1 if path[-1] == starting_node else path[-1]
            new_path = list(path)
            new_path.append(min(parents))
            stack.append(new_path)
            visited.add(vertex)
