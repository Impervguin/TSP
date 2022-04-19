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


# DISTANCE_COEF = 0.5
# PHEROMONES_COEF = 1.8
# PHEROMONES_EVAP = 0.6392857142857143
# PHEROMONES_ENCH = 1

DISTANCE_COEF = 2
PHEROMONES_COEF = 2.1386363636363637
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

    def solve(self, start=0, ants=30, iter=1500):
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
                        attr = 1 / self.matrix[path[-1]][p][0] ** DISTANCE_COEF + self.matrix[path[-1]][p][1] ** PHEROMONES_COEF
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
                dist += self.matrix[path[-2]][path[-1]][0]
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
        total_time = end_time - start_time
        return min_path, min_dist, total_time


if __name__ == "__main__":
    #points = [(10, 10, 10), (9, 1, 10), (3, 5, 10), (5, 5, 10), (9, 9, 2), (1, 1, 5), (5, 9, 6), (8, 15, 8), (9, 5, 2)]
    #points = [(91.7311459346491, 15.342820268851298, 77.53479746150663), (62.595798272237445, 94.58617578743547, 99.76370379060849), (74.32021743917898, 56.6362601791274, 29.58346499534801), (36.12229467034849, 47.75829366597794, 84.95218127238945), (0.9613939628796975, 40.81584061580516, 77.34242626106106), (87.16464560697416, 12.903054589685581, 13.084325187436862), (70.18511661550662, 71.42918835363741, 57.97018380425412), (16.159047192582587, 93.80791835406649, 51.77476525745684), (75.68100170077795, 83.46932150606358, 35.24274070868005), (76.49678612764977, 79.33331499612642, 85.75161288966933), (9.128753146533208, 86.22003390470118, 28.039898275495723), (45.86776165196835, 32.588278037569864, 50.02916622882233), (12.58025051971785, 25.61088225221776, 0.9660423520892469), (80.37192050955042, 90.20015699100932, 6.168015966092987), (55.65352854222125, 61.072486581627636, 95.20969582429714), (67.2337845583764, 4.82705217854511, 13.367546244563389), (24.26393457790823, 35.93678283168128, 50.99531022401784), (52.013751258468425, 36.61358585648403, 40.51360995569455), (81.72858167732934, 73.98030635033679, 84.35847992012513), (9.373415583680867, 92.35302614484439, 42.951974600052786), (65.73355891122839, 19.09766766823121, 3.6378746628049075), (84.18672557499427, 41.17215198314664, 7.864123283782032), (45.922489302436546, 88.70769938729741, 19.137911376170603), (18.246282347494436, 10.10243270408795, 22.34060404278113), (63.52286031137283, 4.842791078971153, 69.72630454510089), (21.353827980658522, 10.979107156744494, 98.42176479763371), (42.064685225405675, 26.059234649235552, 60.392123963783526), (12.624596891592788, 14.371580899234893, 81.15915767830056), (26.684769194697864, 16.51702279504391, 46.2655877031674), (32.83621222526592, 3.759246766932034, 77.82822806911935), (19.58741806516725, 58.398418907367486, 83.30120538805402), (35.5590273452646, 11.305304047980492, 2.9175746004953207), (52.94645066291373, 89.02542101901997, 90.70155263130502), (31.820067796642004, 60.196244125375344, 64.71304819339824), (72.99489843193115, 44.34248331032842, 7.45812465825254), (6.358766342434096, 63.83955241344738, 7.8963548650051285), (2.056932280996193, 28.43510634094779, 34.84738850974377), (98.26392818443607, 29.35541575144799, 46.59418235980066), (53.40201691411819, 36.33661538807981, 29.135273868591284), (33.50986881993408, 53.04054129071377, 54.30528385740385), (9.96477401653334, 29.256770850166625, 20.876531458924962), (83.34886780793163, 30.105812959314616, 71.06605926064599), (98.88608728909477, 73.16913694337688, 49.79807914224976), (87.89200760228317, 73.62082341406177, 1.4393478344569166), (23.3083609558999, 97.04783605583948, 60.314720194402426), (18.16948409500496, 91.42043119883677, 37.48795578996602), (91.36171496447287, 25.498050296647, 36.19746021573466), (2.793964593699494, 54.303805956236374, 69.19203821504212), (27.458550236345737, 16.70103035870546, 96.24534909179019), (45.22411357243612, 5.9191234849254375, 89.53341625046613)]
    points = [(427, 627, 262), (379, 429, 121), (547, 625, 579), (209, 373, 807), (659, 385, 741), (653, 225, 633), (515, 207, 491), (858, 348, 505), (213, 788, 991), (952, 60, 133), (498, 549, 126), (970, 118, 52), (931, 25, 505), (762, 718, 923), (718, 823, 27)]

    graph = Graph(*points)
    algorithm = AntAlgorithm(graph)
    start = 1  # 9, 1
    path, dist, tot_time = algorithm.solve(start)
    print(" -> ".join([str(i) for i in path]))
    print(dist)
    print(tot_time)
    graph.visualize_path_plotly(path)



    # dis_coefs = []
    # pher_coefs = []
    # dists = []
    # m = (0, 0, 500000000000)
    # points = [[(222, 394, 718), (458, 5, 401), (642, 833, 277), (749, 372, 210), (846, 716, 18), (678, 255, 910), (647, 150, 749), (64, 555, 352), (89, 295, 372), (832, 861, 880), (274, 761, 739), (304, 501, 649), (945, 752, 17), (630, 234, 260), (949, 493, 879), (303, 610, 320), (484, 830, 309), (554, 794, 156), (966, 658, 629), (60, 528, 277)], [(263, 707, 983), (260, 573, 868), (471, 178, 808), (561, 17, 752), (735, 397, 58), (896, 565, 564), (56, 264, 575), (238, 337, 963), (213, 8, 437), (616, 3, 483), (968, 252, 240), (807, 700, 970), (680, 393, 166), (778, 939, 553), (929, 165, 330), (216, 457, 378), (286, 250, 187), (872, 119, 217), (773, 552, 347), (695, 622, 95)], [(888, 76, 142), (257, 656, 641), (711, 424, 583), (155, 127, 293), (76, 381, 929), (704, 17, 59), (872, 884, 822), (929, 619, 356), (439, 188, 756), (663, 711, 835), (48, 122, 566), (85, 398, 859), (186, 490, 483), (18, 40, 554), (665, 571, 873), (827, 766, 894), (836, 198, 802), (41, 661, 840), (372, 478, 486), (570, 318, 786), (609, 844, 823), (679, 168, 463), (771, 508, 216), (528, 224, 879), (47, 814, 687)], [(1000, 984, 510), (829, 603, 212), (444, 14, 15), (378, 495, 160), (962, 20, 387), (18, 929, 224), (812, 214, 236), (234, 314, 834), (246, 682, 38), (813, 834, 787), (5, 140, 114), (179, 34, 723), (418, 729, 581), (126, 919, 31), (327, 592, 338), (892, 463, 591), (617, 346, 665), (829, 815, 86), (378, 899, 841), (906, 674, 759), (630, 918, 61), (916, 24, 256), (258, 222, 466), (573, 651, 336), (38, 359, 243)], [(967, 152, 413), (496, 973, 73), (990, 264, 314), (610, 924, 291), (720, 181, 398), (866, 428, 975), (277, 366, 12), (945, 751, 165), (986, 509, 559), (849, 210, 368), (32, 367, 747), (491, 23, 32), (969, 940, 187), (142, 14, 941), (663, 412, 529), (855, 521, 97), (618, 262, 41), (823, 679, 172), (12, 769, 157), (320, 952, 286), (463, 309, 469), (22, 333, 35), (567, 853, 325), (62, 204, 58), (413, 949, 720), (11, 161, 800), (464, 837, 590), (130, 758, 823), (903, 373, 472), (221, 459, 210)], [(544, 486, 777), (242, 663, 279), (173, 953, 894), (10, 636, 601), (689, 80, 17), (704, 983, 899), (645, 825, 20), (118, 46, 697), (501, 822, 830), (858, 309, 567), (107, 231, 484), (939, 601, 797), (48, 563, 130), (370, 314, 399), (48, 292, 890), (810, 38, 886), (360, 286, 913), (174, 262, 954), (989, 408, 569), (182, 131, 789), (58, 843, 823), (377, 764, 327), (643, 555, 665), (738, 911, 271), (731, 36, 683), (810, 369, 188), (426, 971, 463), (782, 662, 550), (22, 813, 365), (427, 486, 670)], [(703, 519, 212), (539, 616, 938), (290, 65, 951), (709, 904, 966), (7, 31, 984), (408, 620, 537), (490, 481, 742), (954, 727, 976), (33, 95, 841), (92, 52, 176), (608, 839, 181), (866, 873, 326), (874, 916, 473), (457, 970, 960), (832, 862, 942), (295, 774, 600), (446, 89, 835), (166, 943, 954), (106, 522, 464), (154, 724, 260), (729, 653, 960), (554, 867, 268), (944, 884, 148), (806, 169, 895), (183, 294, 696), (619, 435, 796), (66, 874, 902), (393, 792, 202), (540, 206, 159), (847, 574, 115), (816, 945, 85), (100, 915, 926), (182, 358, 375), (710, 894, 507), (377, 371, 45), (518, 672, 846), (871, 158, 151), (458, 66, 32), (464, 174, 25), (163, 789, 446)], [(465, 94, 722), (938, 58, 762), (391, 112, 174), (212, 944, 586), (8, 933, 263), (488, 334, 287), (72, 335, 629), (0, 189, 651), (925, 629, 881), (180, 413, 850), (875, 441, 809), (938, 171, 899), (877, 429, 35), (881, 421, 790), (66, 452, 486), (742, 831, 860), (270, 477, 617), (91, 523, 656), (703, 498, 775), (522, 198, 857), (31, 835, 58), (290, 203, 390), (521, 845, 748), (919, 52, 285), (776, 685, 396), (380, 487, 140), (318, 441, 749), (674, 447, 365), (328, 98, 638), (717, 77, 702), (693, 241, 738), (658, 920, 454), (995, 310, 250), (431, 240, 577), (683, 450, 768), (975, 871, 898), (249, 899, 379), (894, 366, 882), (937, 260, 667), (743, 163, 750)], [(706, 448, 456), (132, 263, 563), (279, 417, 438), (742, 455, 524), (264, 433, 292), (73, 983, 725), (34, 512, 545), (183, 667, 689), (225, 156, 966), (23, 614, 948), (594, 460, 359), (887, 846, 847), (898, 253, 861), (990, 86, 23), (912, 399, 416), (398, 324, 848), (476, 822, 538), (762, 395, 219), (71, 601, 428), (288, 388, 27), (147, 865, 902), (790, 769, 898), (978, 650, 672), (541, 201, 73), (916, 759, 962), (283, 631, 77), (765, 589, 401), (814, 391, 152), (385, 690, 826), (137, 643, 431), (963, 947, 2), (612, 799, 193), (47, 199, 726), (137, 279, 314), (755, 842, 119), (41, 572, 16), (529, 498, 933), (351, 911, 535), (718, 835, 172), (679, 69, 523), (299, 511, 309), (801, 457, 91), (310, 142, 893), (743, 481, 706), (655, 495, 889)], [(665, 444, 744), (674, 682, 182), (591, 847, 189), (370, 609, 203), (949, 315, 269), (211, 128, 81), (289, 864, 842), (476, 595, 766), (387, 234, 611), (611, 446, 627), (157, 701, 326), (664, 953, 919), (4, 232, 906), (560, 70, 686), (686, 541, 273), (306, 454, 95), (164, 894, 186), (521, 38, 571), (477, 331, 557), (250, 226, 361), (979, 187, 433), (432, 99, 239), (225, 986, 167), (471, 713, 451), (417, 448, 540), (660, 272, 398), (337, 349, 775), (960, 308, 469), (774, 584, 764), (905, 794, 629), (12, 220, 305), (20, 800, 431), (874, 762, 164), (272, 150, 902), (580, 902, 842), (234, 195, 222), (714, 854, 157), (653, 196, 519), (570, 661, 602), (255, 59, 276), (873, 161, 85), (268, 994, 421), (235, 744, 484), (951, 644, 723), (23, 984, 151)], [(236, 472, 224), (345, 799, 903), (29, 898, 135), (793, 97, 7), (698, 360, 568), (58, 818, 421), (623, 352, 59), (285, 477, 908), (481, 538, 64), (766, 250, 975), (113, 201, 705), (914, 589, 621), (762, 815, 982), (663, 766, 708), (922, 706, 320), (257, 843, 938), (373, 734, 778), (627, 610, 360), (938, 935, 735), (510, 699, 204), (242, 86, 214), (616, 629, 315), (521, 618, 565), (426, 363, 127), (868, 938, 405), (334, 511, 373), (670, 875, 252), (686, 260, 669), (537, 699, 545), (677, 304, 649), (251, 460, 856), (806, 624, 246), (447, 567, 794), (137, 412, 912), (962, 746, 156), (682, 565, 889), (936, 692, 764), (577, 720, 173), (332, 465, 235), (263, 189, 351), (691, 531, 510), (596, 888, 279), (207, 915, 506), (58, 425, 595), (163, 424, 140), (780, 24, 395), (997, 840, 839), (874, 819, 428), (83, 379, 598), (489, 112, 50)]]
    # t = 0
    # n = len(points)
    # f = open("log.txt", "w")
    # dists_f = open("dists_fail.txt", "w")
    # pher_f = open("phers.txt", "w")
    # disc_f = open("discs.txt", "w")
    # str_time = time.time()
    # for DISTANCE_COEF in np.linspace(0.1, 4, 45):
    #     for PHEROMONES_COEF in np.linspace(0.1, 4, 45):
    #         for p in points:
    #             graph = Graph(*p)
    #             algorithm = AntAlgorithm(graph)
    #             start = 1
    #             path, dist, tot_time = algorithm.solve(start)
    #             t += dist
    #         sr_dist = t / n
    #         if sr_dist < m[2]:
    #             m = (DISTANCE_COEF, PHEROMONES_COEF, sr_dist)
    #             f.write(f"{time.time() - str_time}: PHER = {PHEROMONES_COEF}, DIST = {DISTANCE_COEF}, {sr_dist}\n")
    #         dis_coefs.append(DISTANCE_COEF)
    #         pher_coefs.append(PHEROMONES_COEF)
    #         dists.append(sr_dist)
    #         dists_f.write(str(sr_dist)+ "\n")
    #         disc_f.write(str(DISTANCE_COEF)+ "\n")
    #         pher_f.write(str(PHEROMONES_COEF) + "\n")
    # print(DISTANCE_COEF)
    #
    #


