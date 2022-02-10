from Graph import Graph
import time

def solve(graph, start_point):
    path = [start_point]
    total_dist = 0
    n = graph.number_of_points
    now = start_point
    start_time = time.time()
    for i in range(n - 1):
        possible_moves = graph.get_adjoining_points(now)
        min_dist_point = (-1, -1)
        for move in possible_moves:
            if move[0] not in path:
                if min_dist_point[0] == -1:
                    min_dist_point = move
                elif min_dist_point[1] > move[1]:
                    min_dist_point = move
        total_dist += min_dist_point[1]
        now = min_dist_point[0]
        path.append(min_dist_point[0])
    end_time = time.time()
    totat_time = end_time - start_time
    return path, total_dist, totat_time
# 1644498579.8804176


points = [(10, 10), (9, 1), (3, 5), (5, 5), (9, 9), (1, 1), (5, 9), (8, 15), (9, 5)]
graph = Graph(*points)
start = 1 # 9, 1
path, dist, tot_time = solve(graph, start)

print(" -> ".join([str(i) for i in path]))
print(dist)
print(tot_time)

graph.visualize_path_plotly(path)