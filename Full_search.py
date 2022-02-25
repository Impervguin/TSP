from Graph import Graph
from Algorithm import Algorithm
from itertools import permutations
import time
class FullSearchAlgorithm(Algorithm):
    def solve(self, start_point):
        points = self.graph.get_points()
        paths = [[start_point] + list(p) + [start_point] for p in permutations([i for i in range(self.graph.get_n_points()) if i != start_point])]
        min_path = (-1, -1)
        start_time = time.time()
        for path in paths:
            dist = 0
            for i in range(len(path) - 1):
                dist += self.graph.calculate_distance(path[i], path[i + 1])
            if min_path[0] == -1:
                min_path = (dist, path)
            elif min_path[0] > dist:
                min_path = (dist, path)
        end_time = time.time()
        total_time = end_time - start_time
        return min_path[1], min_path[0], total_time


if __name__ == "__main__":
    points = [(10, 10, 10), (9, 1, 10), (3, 5, 10), (5, 5, 10), (9, 9, 2), (1, 1, 5), (5, 9, 6), (8, 15, 8), (9, 5, 2)]
    graph = Graph(*points)
    algorithm = FullSearchAlgorithm(graph)
    start = 1 # 9, 1
    path, dist, tot_time = algorithm.solve(start)

    print(" -> ".join([str(i) for i in path]))
    print(dist)
    print(tot_time)
    graph.visualize_path_plotly(path)
