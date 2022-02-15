from Algorithm import Algorithm
from Graph import Graph
from Random_path import RandomAlgorithm
import numpy as np
DISTANCE_COEF = 2
PHEROMONES_COEF = 3
PHEROMONES_EVAP = 0.2
PHEROMONES_ENCH = 10

class AntAlgorithm(Algorithm):
    def create_pher_dist_matrix(self):
        self.matrix = []
        for i in range(self.graph.get_n_points()):
            self.matrix.append([])
            for j in range(self.graph.get_n_points()):
                if i == j:
                    self.matrix[-1].append(None)
                else:
                    self.matrix[-1].append([self.graph.calculate_distance(i, j), 0])
        # print(*self.matrix, sep="\n")
    def solve(self, start, ants=10, iter=100):
        min_path, min_dist, _ = RandomAlgorithm(self.graph).solve(start)
        self.create_pher_dist_matrix()
        for i in range(iter):
            ant_paths = []
            for a in range(ants):
                path = [start]
                dist = 0
                pos_points = self.graph.get_points().copy()
                del pos_points[start]
                for _ in range(self.graph.get_n_points() - 1):
                    weights = dict()
                    for p in pos_points.keys():
                        attr = self.matrix[path[-1]][p][0] ** DISTANCE_COEF +  self.matrix[path[-1]][p][1] ** PHEROMONES_COEF
                        weights[p] = attr
                    s_attr = sum(weights.values())
                    for w in weights.keys():
                        weights[w] /= s_attr
                    # try:
                    sel_point = 1 # Выбор точки по весам
                    # except BaseException as e:
                    #     print(path)
                    #     print(pos_points)
                    #     print(weights)
                    #     print(weights.keys())
                    #     print(weights.values())
                    #     exit()
                    for p in pos_points.keys():
                        if pos_points[p] == sel_point:
                            sel_point = p
                            break
                    else:
                        print(sel_point)
                        print(pos_points)
                    dist += self.matrix[path[-1]][sel_point][0]
                    path.append(sel_point)
                    del pos_points[sel_point]
                ant_paths.append((path, dist))
                if dist < min_dist:
                    min_path, min_dist = path, dist

            for j in range(len(self.matrix)):
                for k in range(len(self.matrix[j])):
                    if k != j:
                        self.matrix[j][k][1] *= (1 - PHEROMONES_EVAP)
            for ap in ant_paths:
                pheromones = PHEROMONES_ENCH / ap[1]
                for j in range(len(ap[0]) - 1):
                    self.matrix[ap[j]][ap[j + 1]][1] += pheromones
            if i % 10 == 9:
                print(f"{i + 1} Итерация пройдена")
        return min_path, min_dist













points = [(10, 10), (9, 1), (3, 5), (5, 5), (9, 9), (1, 1), (5, 9), (8, 15), (9, 5)]
graph = Graph(*points)
algorithm = AntAlgorithm(graph)
start = 1 # 9, 1
path, dist = algorithm.solve(start)
# print(" -> ".join([str(i) for i in path]))
# print(dist)
# print(tot_time)
# graph.visualize_path_plotly(path)
