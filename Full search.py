from Graph import Graph
from itertools import permutations
import time

def solve(graph, start_point):

    points = graph.get_points()
    paths = permutations([i for i in range(graph.get_n_points()) if i != start_point])
    min_path = (-1, -1)
    start_time = time.time()
    for path in paths:
        dist = graph.calculate_distance(start_point, path[0])
        for i in range(1, len(path)):
            dist += graph.calculate_distance(path[i - 1], path[i])
        if min_path[0] == -1:
            min_path = (dist, path)
        elif min_path[0] > dist:
            min_path = (dist, path)
    end_time = time.time()
    total_time = end_time - start_time
    return [start_point] + [*min_path[1]], min_path[0], total_time



points = [(10, 10), (9, 1), (3, 5), (5, 5), (9, 9), (1, 1), (5, 9), (8, 15), (9, 5)]
graph = Graph(*points)
start = 1 # 9, 1
path, dist, tot_time = solve(graph, start)

print(" -> ".join([str(i) for i in path]))
print(dist)
print(tot_time)
graph.visualize_path_plotly(path)
