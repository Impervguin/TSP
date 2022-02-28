from Algorithm import Algorithm
from Graph import Graph
import time
from random import randint, shuffle, uniform, choice, choices
import plotly as px


class Individual:
    def __init__(self, start_point, graph, perm, mutation_chance):
        self.perm = perm
        self.path = [start_point] + perm + [start_point]
        self.graph = graph
        self.fitness = self.calc_fitness()
        self.mutation_chance = mutation_chance

    def calc_fitness(self):
        fitness = sum(
            [self.graph.get_distance(self.path[i], self.path[i + 1]) for i in range(len(self.path) - 1)])
        return fitness

    def get_child(self, other):
        edges = sorted((randint(0, len(self.perm) - 1), randint(0, len(self.perm) - 1)), reverse=True)
        part = self.perm[edges[0]:edges[1]]
        child_perm = [0] * len(self.perm)
        for i in range(edges[0], edges[0]):
            child_perm[i] = self.perm[i]
        k = 0
        for i in range(len(self.perm)):
            if other.perm[i] not in part:
                while child_perm[k] != 0:
                    k += 1
                child_perm[k] = other.perm[i]
        # mutation
        for i in range(len(child_perm)):
            r = uniform(0, 1)
            if r < self.mutation_chance:
                j = randint(0, len(child_perm) - 1)
                while j == i:
                    j = randint(0, len(child_perm) - 1)
                child_perm[i], child_perm[j] = child_perm[j], child_perm[i]
                break
        return Individual(self.path[0], self.graph, child_perm, self.mutation_chance)


class Generation:
    def __init__(self, start_point,graph, population):
        self.start_point = start_point
        self.graph = graph
        self.population = population

    def get_child(self, n=10):
        inds = choices(self.population, k=n)
        # ind1 = choice(self.population)
        # ind2 = choice(self.population)
        parent1 = min(inds, key=lambda x: x.fitness)

        inds = choices(self.population, k=n)
        # ind1 = choice(self.population)
        # ind2 = choice(self.population)
        parent2 = min(inds, key=lambda x: x.fitness)

        child = parent1.get_child(parent2)
        return child

    def get_next_generation(self, n_contest=10):
        new_population = [self.get_child(n_contest) for _ in range(len(self.population))]

        return Generation(self.start_point,self.graph, new_population)

    def get_best_ind(self):
        return min(self.population, key=lambda x: x.fitness)


class GeneticAlgoritm(Algorithm):
    def __init__(self, graph, population_size=200, generations=1500, mutation=0.5, n_contest=10):
        super(GeneticAlgoritm, self).__init__(graph)
        self.population_size = population_size
        self.generations = generations
        self.mutation = mutation
        self.n_contest = n_contest



    def solve(self, start_point=0):
        best_inds = []
        population = []
        start_time = time.time()
        for _ in range(self.population_size):
            perm = [i for i in range(self.graph.get_n_points()) if i != start_point]
            shuffle(perm)
            population.append(Individual(start_point, self.graph, perm, self.mutation))
        generation = Generation(start_point,self.graph, population)
        best_ind = generation.get_best_ind()
        best_inds.append(best_ind.fitness)
        for _ in range(self.generations - 1):
            generation = generation.get_next_generation()
            best_ind = min(best_ind, generation.get_best_ind(), key=lambda x: x.fitness)
            best_inds.append(generation.get_best_ind().fitness)
        end_time = time.time()
        total_time = end_time - start_time
        return best_ind.path, best_ind.fitness, total_time, best_inds


if __name__ == "__main__":
    # points = [(10, 10, 10), (9, 1, 10), (3, 5, 10), (5, 5, 10), (9, 9, 2), (1, 1, 5), (5, 9, 6), (8, 15, 8), (9, 5, 2)]
    points = [(91.7311459346491, 15.342820268851298, 77.53479746150663), (62.595798272237445, 94.58617578743547, 99.76370379060849), (74.32021743917898, 56.6362601791274, 29.58346499534801), (36.12229467034849, 47.75829366597794, 84.95218127238945), (0.9613939628796975, 40.81584061580516, 77.34242626106106), (87.16464560697416, 12.903054589685581, 13.084325187436862), (70.18511661550662, 71.42918835363741, 57.97018380425412), (16.159047192582587, 93.80791835406649, 51.77476525745684), (75.68100170077795, 83.46932150606358, 35.24274070868005), (76.49678612764977, 79.33331499612642, 85.75161288966933), (9.128753146533208, 86.22003390470118, 28.039898275495723), (45.86776165196835, 32.588278037569864, 50.02916622882233), (12.58025051971785, 25.61088225221776, 0.9660423520892469), (80.37192050955042, 90.20015699100932, 6.168015966092987), (55.65352854222125, 61.072486581627636, 95.20969582429714), (67.2337845583764, 4.82705217854511, 13.367546244563389), (24.26393457790823, 35.93678283168128, 50.99531022401784), (52.013751258468425, 36.61358585648403, 40.51360995569455), (81.72858167732934, 73.98030635033679, 84.35847992012513), (9.373415583680867, 92.35302614484439, 42.951974600052786), (65.73355891122839, 19.09766766823121, 3.6378746628049075), (84.18672557499427, 41.17215198314664, 7.864123283782032), (45.922489302436546, 88.70769938729741, 19.137911376170603), (18.246282347494436, 10.10243270408795, 22.34060404278113), (63.52286031137283, 4.842791078971153, 69.72630454510089), (21.353827980658522, 10.979107156744494, 98.42176479763371), (42.064685225405675, 26.059234649235552, 60.392123963783526), (12.624596891592788, 14.371580899234893, 81.15915767830056), (26.684769194697864, 16.51702279504391, 46.2655877031674), (32.83621222526592, 3.759246766932034, 77.82822806911935), (19.58741806516725, 58.398418907367486, 83.30120538805402), (35.5590273452646, 11.305304047980492, 2.9175746004953207), (52.94645066291373, 89.02542101901997, 90.70155263130502), (31.820067796642004, 60.196244125375344, 64.71304819339824), (72.99489843193115, 44.34248331032842, 7.45812465825254), (6.358766342434096, 63.83955241344738, 7.8963548650051285), (2.056932280996193, 28.43510634094779, 34.84738850974377), (98.26392818443607, 29.35541575144799, 46.59418235980066), (53.40201691411819, 36.33661538807981, 29.135273868591284), (33.50986881993408, 53.04054129071377, 54.30528385740385), (9.96477401653334, 29.256770850166625, 20.876531458924962), (83.34886780793163, 30.105812959314616, 71.06605926064599), (98.88608728909477, 73.16913694337688, 49.79807914224976), (87.89200760228317, 73.62082341406177, 1.4393478344569166), (23.3083609558999, 97.04783605583948, 60.314720194402426), (18.16948409500496, 91.42043119883677, 37.48795578996602), (91.36171496447287, 25.498050296647, 36.19746021573466), (2.793964593699494, 54.303805956236374, 69.19203821504212), (27.458550236345737, 16.70103035870546, 96.24534909179019), (45.22411357243612, 5.9191234849254375, 89.53341625046613)]
    #points = [(427, 627, 262), (379, 429, 121), (547, 625, 579), (209, 373, 807), (659, 385, 741), (653, 225, 633), (515, 207, 491), (858, 348, 505), (213, 788, 991), (952, 60, 133), (498, 549, 126), (970, 118, 52), (931, 25, 505), (762, 718, 923), (718, 823, 27)]
    graph = Graph(*points)
    algorithm = GeneticAlgoritm(graph)
    start = 1 # 9, 1
    path, dist, tot_time, best_inds = algorithm.solve(start)

    print(" -> ".join([str(i) for i in path]))
    print(dist)
    print(tot_time)
    graph.visualize_path_plotly(path)
    fig = px.graph_objs.Figure()
    fig.add_scatter(x=list(range(1, len(best_inds) + 1)), y=best_inds, mode="markers+lines", name="Лучшие пути")
    fig.update_xaxes(title_text="Поколения")
    fig.update_yaxes(title_text="Лучшее расстояние в поколении")
    fig.show()

