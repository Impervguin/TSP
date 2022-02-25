import random
import time

from Algorithm import Algorithm
from Graph import Graph
from Random_path import RandomAlgorithm
from random import choices
import numpy as np

# DISTANCE_COEF = 2
# PHEROMONES_COEF = 3
# PHEROMONES_EVAP = 0.2


DISTANCE_COEF = 0.5
PHEROMONES_COEF = 1.8
PHEROMONES_EVAP = 0.6392857142857143
PHEROMONES_ENCH = 1


class AntAlgorithm(Algorithm):
    def create_pher_dist_matrix(self):
        self.matrix = []
        for i in range(self.graph.get_n_points()):
            self.matrix.append([])
            for j in range(self.graph.get_n_points()):
                if i == j:
                    self.matrix[-1].append(None)
                else:
                    self.matrix[-1].append([self.graph.calculate_distance(i, j), 1])
        # print(*self.matrix, sep="\n")

    def solve(self, start, ants=5, iter=100):
        min_path, min_dist, _ = RandomAlgorithm(self.graph).solve(start)
        self.create_pher_dist_matrix()
        start_time = time.time()
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
                        attr = self.matrix[path[-1]][p][0] ** DISTANCE_COEF + self.matrix[path[-1]][p][1] ** PHEROMONES_COEF
                        weights[p] = attr
                    s_attr = sum(weights.values())
                    # for w in weights.keys():
                    #     weights[w] /= s_attr
                    # try:
                    s = 0
                    r = random.uniform(0, s_attr)
                    for k in dict(sorted(weights.items(), key=lambda item: item[1])).keys():
                        s += weights[k]
                        if s > r:
                            sel_point = k
                            break

                    # sel_point = choices(pos_points, weights, k=1)[0]
                    # except BaseException as e:
                    #     print(path)
                    #     print(pos_points)
                    #     print(weights)
                    #     print(weights.keys())
                    #     print(weights.values())
                    #     exit()
                    # for p in pos_points.keys():
                    #     if pos_points[p] == sel_point:
                    #         sel_point = p
                    #         break
                    # else:
                    #     print(sel_point)
                    #     print(pos_points)
                    dist += self.matrix[path[-1]][sel_point][0]
                    path.append(sel_point)
                    del pos_points[sel_point]
                path.append(start)
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
                    self.matrix[ap[0][j]][ap[0][j + 1]][1] += pheromones
            # if i % 10 == 9:
            #     print(f"{i + 1} Итерация пройдена")
        # print(*self.matrix, sep="\n")
        end_time = time.time()
        return min_path, min_dist, end_time - start_time


if __name__ == "__main__":
    points = [(10, 10, 10), (9, 1, 10), (3, 5, 10), (5, 5, 10), (9, 9, 2), (1, 1, 5), (5, 9, 6), (8, 15, 8), (9, 5, 2)]
    graph = Graph(*points)
    algorithm = AntAlgorithm(graph)
    start = 1  # 9, 1
    path, dist, time = algorithm.solve(start)
    print(" -> ".join([str(i) for i in path]))
    print(dist)
    # print(tot_time)
    graph.visualize_path_plotly(path)
    # #1 -> 5 -> 3 -> 2 -> 4 -> 8 -> 6 -> 0 -> 7
    # #43.00899537064003

    # points = [[(16, 2), (44, 11), (43, 25), (35, 22), (14, 21), (49, 13), (8, 19), (43, 30)],
    #           [(43, 63), (91, 11), (85, 87), (102, 82), (97, 3), (17, 83), (105, 55), (78, 36), (55, 110), (52, 36),
    #            (74, 117)],
    #           [(173, 483), (2, 63), (395, 149), (148, 208), (168, 213), (179, 108), (12, 436), (491, 350), (332, 242),
    #            (329, 77), (160, 336)],
    #           [(92, 313), (447, 94), (410, 409), (419, 12), (231, 418), (20, 198), (439, 393), (50, 290), (454, 301),
    #            (67, 333), (166, 423), (492, 385)],
    #           [(474, 16), (125, 185), (147, 104), (208, 407), (587, 112), (207, 365), (585, 385), (219, 226), (130, 364),
    #            (535, 128), (222, 248)], [(388, 704), (652, 254), (60, 447), (525, 460), (616, 469), (187, 762)],
    #           [(96, 478), (203, 396), (299, 208), (314, 418), (95, 250), (76, 150), (141, 13), (357, 324), (311, 340),
    #            (275, 148), (25, 129), (499, 462), (123, 404), (385, 135)],
    #           [(866, 689), (253, 759), (753, 330), (652, 623), (564, 134), (775, 846), (46, 30), (585, 892), (54, 405),
    #            (705, 149), (605, 862), (586, 307)],
    #           [(318, 533), (555, 484), (514, 657), (433, 245), (280, 643), (651, 145), (120, 256), (417, 302), (713, 628)],
    #           [(5375, 9525), (8185, 9104), (6297, 8263), (4784, 1158), (1595, 7732), (6567, 1326), (9932, 459), (401, 5714),
    #            (1959, 4038), (5202, 4721), (3320, 204), (4380, 5887), (9121, 8389), (9792, 5669)],
    #           [(97132, 58762), (10327, 55605), (81846, 63793), (15918, 80285), (5799, 51326), (17271, 78701), (6439, 79407),
    #            (17364, 18446), (14472, 473)],
    #           [(21607, 4018), (4282, 44098), (43993, 2959), (21009, 1075), (1251, 23229), (2365, 8349), (15543, 5115),
    #            (46985, 27441), (36373, 7250), (28810, 8124), (3786, 45491), (20123, 19978), (42637, 20224), (5951, 25896),
    #            (13310, 38973)],
    #           [(27, 393), (268, 393), (224, 439), (652, 486), (618, 491), (242, 926), (145, 603), (451, 339), (837, 488),
    #            (187, 505), (616, 242), (729, 889), (863, 994), (558, 928)]]
    #
    # min_consts = (100000000000,)

    # for DISTANCE_COEF in np.linspace(0.5, 3, 26):
    #     for PHEROMONES_COEF in np.linspace(0.5, 3, 26):
    #         for PHEROMONES_EVAP in np.linspace(0.05, 0.8, 15):
    #             s = 0
    #             for p in points:
    #                 algo = AntAlgorithm(Graph(*p))
    #                 s += algo.solve(1)[1]
    #             for p in points:
    #                 algo = AntAlgorithm(Graph(*p))
    #                 s += algo.solve(1)[1]
    #             for p in points:
    #                 algo = AntAlgorithm(Graph(*p))
    #                 s += algo.solve(1)[1]
    #             if s < min_consts[0]:
    #                 min_consts = (s, DISTANCE_COEF, PHEROMONES_COEF, PHEROMONES_EVAP)
    #                 print(f"PATH:{s} DISTANCE_COEF:{DISTANCE_COEF} PHEROMONES_COEF:{PHEROMONES_COEF} PHEROMONES_EVAP:{PHEROMONES_EVAP}")
    #     print(DISTANCE_COEF)
