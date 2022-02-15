from Graph import Graph
from Algorithm import Algorithm
from random import choice
import time

class RandomAlgorithm(Algorithm):
    def solve(self, start_point):
        graph_points = self.graph.get_points()
        points = [(i, graph_points[i])for i in range(len(graph_points))]
        del points[start_point]
        path = [start_point]
        total_dist = 0
        start_time = time.time()
        for _ in range(self.graph.number_of_points - 1):
            point = choice(points)
            total_dist += self.graph.calculate_distance(path[-1], point[0])
            points.remove(point)
            path.append(point[0])
        end_time = time.time()
        total_time = end_time - start_time
        return path, total_dist, total_time

if __name__ == "__main__":
    points = [(10, 10), (9, 1), (3, 5), (5, 5), (9, 9), (1, 1), (5, 9), (8, 15), (9, 5)]
    graph = Graph(*points)
    algorithm = RandomAlgorithm(graph)
    start = 1 # 9, 1
    path, dist, tot_time = algorithm.solve(start)

    print(" -> ".join([str(i) for i in path]))
    print(dist)
    print(tot_time)
    graph.visualize_path_plotly(path)
