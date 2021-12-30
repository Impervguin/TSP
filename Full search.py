from Graph import Graph
from itertools import permutations

def solve(graph, start_point):
    points = graph.get_points()
    paths = permutations([i for i in range(graph.get_n_points()) if i != start_point])
    min_path = (-1, -1)
    for path in paths:
        dist = graph.calculate_distance(start_point, path[0])
        for i in range(1, len(path)):
            dist += graph.calculate_distance(path[i - 1], path[i])
        if min_path[0] == -1:
            min_path = (dist, path)
        elif min_path[0] > dist:
            min_path = (dist, path)
    return [start_point] + [*min_path[1]], min_path[0]



points = [(10, 10), (9, 1), (3, 5), (5, 5), (9, 9)]
graph = Graph(*points)
start = 1 # 9, 1
path, dist = solve(graph, start)

print(" -> ".join([str(i) for i in path]))
print(dist)

graph.visualize_path_plotly(path)
