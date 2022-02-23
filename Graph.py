from math import sqrt
from random import choice
import plotly as px
import plotly.express


class Graph:
    def __init__(self, *args):
        self.points = dict()
        self.number_of_points = len(args)
        for i in range(len(args)):
            self.points[i] = args[i]

    def get_point_coordinates(self, point_name):
        return self.points[point_name]


    def add_point(self, point):
        self.points[self.number_of_points] = point
        self.number_of_points += 1

    def get_n_points(self):
        return self.number_of_points

    def get_points(self):
        return self.points

    def get_adjoining_points(self, point_name):
        lst = [(i, self.calculate_distance(i, point_name)) for i in range(self.number_of_points) if i != point_name]
        return lst


    def calculate_distance(self, point1, point2):
        pc1 = self.points[point1]
        pc2 = self.points[point2]
        d = sqrt((pc1[0] - pc2[0]) ** 2 + (pc1[1] - pc2[1]) ** 2 + (pc1[2] - pc2[2]) ** 2)
        return d



    def visualize_path_plotly(self, path):
        points = [self.get_point_coordinates(i) for i in path]
        x = [coord[0] for coord in points]
        y = [coord[1] for coord in points]
        z = [coord[2] for coord in points]
        fig = plotly.express.line_3d(x=x, y=y,z=z, markers=True, text=path)
        # fig = plotly.graph_objs.Figure()
        # fig.add_trace(plotly.graph_objs.Scatter(x=x, y=y,z=z, mode="lines+markers+text", text=path,textposition="bottom right"))
        fig.show()

