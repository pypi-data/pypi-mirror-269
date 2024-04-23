import numpy as np
import intervalpy as ival
import itertools as it
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.patches import Rectangle
from typing import Dict, List

class AreaCalculator:   
    """
    Class that allows to visualize the solution if the dimensionality is less than 3
    Precalculated areas for 2-RPR and 3-RPR robots are also included in the class
    """ 
    def __init__(self, name, pa_params=None):
        """Constructor

        Args:
            name (string): The name of the robot configuration
            pa_params (dict, optional): Matplotlib parameters to draw the predetermined configuration. Defaults to None.

        Raises:
            NotImplementedError: if the configuration is not supported
        """
        if name is not None and name not in ["2-RPR", "3-RPR"]:
            raise NotImplementedError
        self.name = name
        self.pa_params = pa_params
    
    """
            Make list of boxes in dim dimension from vector grid
            :param grid: vector on which grid is constructed
            :param dim:  the dimensional of grid
            :return: the list of boxes in dim
            """
    def make_boxes_list(grid: List[float], dim: int, uniform=True) -> List[tuple]:
        """Makes the grid boxes for the solver and the drawer

        Args:
            grid (np.array or list): the 1d-grid that will be used for each axis
            dim (int): the number of dimensions of the grid
            uniform (bool, optional): Defines the grid to be uniform on each axis. Defaults to True.

        Returns:
            list of tuples: list of all boxes in the grid
        """
        if uniform == True:
            grid_size = len(grid) - 1
            grid_intervals = []
            grid_variants = []
            for i in range(grid_size):
                grid_intervals.append(ival.Interval([grid[i], grid[i + 1]]))
            for i in range(dim):
                grid_variants.append(grid_intervals)
            grid_n_size = list(it.product(*grid_variants))
        else:
            grid_variants = []
            grid_numbers = np.shape(grid)[0]
            for i in range(grid_numbers):
                grid_intervals = []
                one_grid = grid[i]
                grid_size = len(one_grid) - 1
                for j in range(grid_size):
                    grid_intervals.append(ival.Interval([one_grid[j], one_grid[j + 1]]))
                grid_variants.append(grid_intervals)
            grid_n_size = list(it.product(*grid_variants))
        return grid_n_size
    
    def __plot_area_3RPR(self, ax: plt.axes, x_c: List[float], y_c: List[float]):
        """private function to plot the workspace area of the 3-RPR robot

        Args:
            ax (plt.ax): the axes where to plot the area
            x_c (List): the x-coordinates of the 3 circles' centers
            y_c (List): the y-coordinates of the 3 circles' centers
        """
        for i in range(3):
            circle = plt.Circle((x_c[i], y_c[i]), radius=12, fc='y', fill=False)
            circle1 = plt.Circle((x_c[i], y_c[i]), radius=27, fc='y', fill=False)
            ax.add_patch(circle)
            ax.add_patch(circle1)
        ax.grid()

    def __plot_area_2RPR(self, ax: plt.axes, r1: float=3, r2: float =15, d: float=8):
        """private function to plot the workspace are of the 2-RPR robot

        Args:
            ax (plt.ax): the axes where to plot the area
            r1 (float, optional): minimal length of the bar. Defaults to 3.
            r2 (float, optional): maximal length of the bar. Defaults to 15.
            d (float, optional): the distance between the stationary points. Defaults to 8.
        """
        circle = plt.Circle((-0.5*d, 0), radius=r1, fc='y', fill=False, color="blue")
        ax.add_patch(circle)
        circle = plt.Circle((0.5*d, 0), radius=r1, fc='y', fill=False, color="red")
        ax.add_patch(circle)
        circle = plt.Circle((-0.5*d, 0), radius=r2, fc='y', fill=False, color="blue")
        ax.add_patch(circle)
        circle = plt.Circle((0.5*d, 0), radius=r2, fc='y', fill=False, color="red")
        ax.add_patch(circle)
        ax.set_xlim([-20, 20])
        ax.set_ylim([-20, 20])
        ax.grid()

    def plot_area(self, ax: plt.axes, pa_params: Dict):
        """plots the analytically found area if the configuration is predetermined

        Args:
            ax (plt.axes): matplotlib axes where to plot
            pa_params (_type_): matplotlib parameters for the configurations
        """
        if self.name == "2-RPR":
            self.__plot_area_2RPR(ax, *pa_params)
        elif self.name == "3-RPR":
            self.__plot_area_3RPR(ax, *pa_params)

    def plot_linear_cube(**kwargs):
        """Plots the 3d projection of the solution

        Raises:
            NotImplementedError: 3d is not yet supported
        """
        raise NotImplementedError
    
    def uni_plotter(self, area_points, border_points, ini_box=None, title="", ax=0, size=0, outside_boxes=None, legend=False, 
                plot_area=plot_area, pa_params=None):
        """Plots the solution on the grid with the analytically found area (if the configuration is supported)

        Args:
            area_points (List): the list of all the inside boxes
            border_points (List): the list of all the border boxes
            ini_box (List[List[float]], optional): The initial bounding box. Defaults to None.
            title (str, optional): The title of the visualized solution. Defaults to "".
            ax (int | plt.axes, optional): The matplotlib axes to plot on. Defaults to 0.
            size (int, optional): Number of dimensions. Defaults to 0.
            outside_boxes (List, optional): the list of all the outside boxes. Defaults to None.
            legend (bool, optional): whether to show the legend on graph. Defaults to False.
            plot_area (function, optional): the analytically found area. Defaults to plot_area.
            pa_params (dict, optional): Matplotlib plot parameters. Defaults to None.
        """
        if pa_params is None:
            pa_params = self.pa_params
        plt.rcParams.update({'font.size': 18})
        handles = []
        if size == 1:
            if ax == 0:
                fig, ax = plt.subplots(figsize=(14, 2))
            if ini_box:
                ini_legend = mlines.Line2D([], [], color='blue', label='Initial interval')
                handles.append(ini_legend)
                x_lim = ini_box
                x_min, x_max = x_lim[0] - abs(x_lim[0]) / 10, x_lim[1] + abs(x_lim[1]) / 10
                ax.set_xlim([x_min, x_max])
                ax.set_ylim([-1, 1])
                ax.plot([x_lim[0], x_lim[1]], [0, 0], linewidth = 12, alpha = 0.4, c = "blue")
            for i in range(len(area_points)):
                ax.plot([area_points[i][0][0], area_points[i][0][1]],[0, 0], marker = "|", color = "green")
            for i in range(len(border_points)):
                ax.plot([border_points[i][0][0], border_points[i][0][1]],[0, 0], marker = "|", color = "yellow")
            if np.any(outside_boxes):
                outside_legend = mlines.Line2D([], [], color='black', label='Outside intervals')
                handles.append(outside_legend)
                for i in range(len(outside_boxes)):
                    ax.plot([outside_boxes[i][0][0], outside_boxes[i][0][1]],[0, 0], marker = "|", color = "black")
            inside_legend = mlines.Line2D([], [], color='green', label='Inside intervals')
            border_legend = mlines.Line2D([], [], color='yellow', label='Border intervals')
            handles.append(inside_legend)
            handles.append(border_legend)
        elif size == 2:
            if ax == 0:
                fig, ax = plt.subplots(figsize=(12, 6))
            if ini_box:

                x_lim = ini_box[0]
                y_lim = ini_box[1]
                x_min, y_min, x_max, y_max = x_lim[0] - abs(x_lim[0]) / 10, y_lim[0] - abs(y_lim[0]) / 10, \
                                            x_lim[1] + abs(x_lim[1]) / 10, y_lim[1] + abs(y_lim[1]) / 10
                ax.set_ylim([y_min, y_max])
                ax.set_xlim([x_min, x_max])
                rect1 = Rectangle((x_lim[0], y_lim[0]), x_lim[1] - x_lim[0], y_lim[1] - y_lim[0], fill=False, color='red',
                                linewidth=2.0)
                ax.add_patch(rect1)
                ini_legend = mlines.Line2D([], [], color='red', label='Initial box')
                handles.append(ini_legend)
            ax.axes.set_aspect('equal')
            for i in range(len(area_points)):  # Plot rectangles, which compose workspace area
                rect1 = Rectangle((area_points[i][0][0], area_points[i][1][0]),
                                area_points[i][0][1] - area_points[i][0][0],
                                area_points[i][1][1] - area_points[i][1][0],
                                fill=True, fc='green', color='black', linewidth=0.5, alpha=0.8)
                ax.add_patch(rect1)
            for i in range(len(border_points)):  # Plot rectangles, which compose the border of workspace area
                rect1 = Rectangle((border_points[i][0][0], border_points[i][1][0]),
                                border_points[i][0][1] - border_points[i][0][0],
                                border_points[i][1][1] - border_points[i][1][0],
                                fill=True, fc='yellow', color='black', linewidth=0.5, alpha=0.8)
                ax.add_patch(rect1)
            if np.any(outside_boxes):
                outside_legend = mpatches.Patch(color='black', label='Outside boxes')
                handles.append(outside_legend)
                for i in range(len(outside_boxes)):  # Plot rectangles, which compose the border of workspace area
                    rect1 = Rectangle((outside_boxes[i][0][0], outside_boxes[i][1][0]),
                                    outside_boxes[i][0][1] - outside_boxes[i][0][0],
                                    outside_boxes[i][1][1] - outside_boxes[i][1][0],
                                    fill=True, fc='black', color='black', linewidth=0.5, alpha=0.8)
                    ax.add_patch(rect1)
            inside_legend = mpatches.Patch(color='green', label='Inside boxes')
            border_legend = mpatches.Patch(color='yellow', label='Border boxes')
            handles.append(inside_legend)
            handles.append(border_legend)
        else:
            if ax == 0:
                fig = plt.figure(figsize=(8, 8))
                ax = fig.add_subplot(111, projection='3d')
            if ini_box:
                x_lim = ini_box[0]
                y_lim = ini_box[1]
                z_lim = ini_box[2]
                x_min, y_min, z_min, x_max, y_max, z_max = x_lim[0] - abs(x_lim[0]) / 10, y_lim[0] - abs(y_lim[0]) / 10, z_lim[0] - abs(z_lim[0]) / 10,\
                                            x_lim[1] + abs(x_lim[1]) / 10, y_lim[1] + abs(y_lim[1]) / 10,  z_lim[1] + abs(z_lim[1]) / 10
                ax.set_ylim([y_min, y_max])
                ax.set_xlim([x_min, x_max])
                ax.set_zlim([z_min, z_max])
                plot_linear_cube(ax, x_min, y_min, z_min, abs(x_max - x_min), abs(y_max - y_min), abs(z_max - z_min), color="red")
                ini_legend = mlines.Line2D([], [], color='red', label='Initial box')
                handles.append(ini_legend)
            for i in range(len(area_points)):
                plot_linear_cube(ax, area_points[i][0][0], area_points[i][1][0], area_points[i][2][0],
                                area_points[i][0][1] - area_points[i][0][0], area_points[i][1][1] - area_points[i][1][0],
                                area_points[i][2][1] - area_points[i][2][0], color="green")
            for i in range(len(border_points)):
                plot_linear_cube(ax, border_points[i][0][0], border_points[i][1][0], border_points[i][2][0],
                                border_points[i][0][1] - border_points[i][0][0],
                                border_points[i][1][1] - border_points[i][1][0],
                                border_points[i][2][1] - border_points[i][2][0], color="yellow")
            if np.any(outside_boxes):
                for i in range(len(outside_boxes)):
                    outside_legend = mpatches.Patch(color='black', label='Outside boxes')
                    handles.append(outside_legend)
                    plot_linear_cube(ax, outside_boxes[i][0][0], outside_boxes[i][1][0], outside_boxes[i][2][0],
                                    outside_boxes[i][0][1] - outside_boxes[i][0][0],
                                    outside_boxes[i][1][1] - outside_boxes[i][1][0],
                                    outside_boxes[i][2][1] - outside_boxes[i][2][0], color="black")
            inside_legend = mpatches.Patch(color='green', label='Inside boxes')
            border_legend = mpatches.Patch(color='yellow', label='Border boxes')
            handles.append(inside_legend)
            handles.append(border_legend)
        ax.set_title(title, fontsize=12)
        ax.tick_params(axis='both', which='major', labelsize=10)
        ax.tick_params(axis='both', which='minor', labelsize=8)
        if legend:
            ax.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', handles=handles)
        plt.tight_layout()
        if plot_area != None:
            plot_area(self, ax, pa_params)
        plt.show()
    
    def make_grid2d(left_bottom: tuple, right_top: tuple, N: int) -> list[tuple]:
        """Helper function to make a 2d grid

        Args:
            left_bottom (tuple): the coorindates of the bottom left corner of the grid
            right_top (tuple): the coordinates of the top right corner of the grid
            N (int):the number of boxes in one axis

        Returns:
            list[tuple]: the 2dgrid
        """
        return AreaCalculator.make_boxes_list([np.linspace(left_bottom[0], right_top[0], N + 1), 
                                               np.linspace(left_bottom[1], right_top[1], N + 1)], 2, False)
            
if __name__ == "__main__":
    drawer = AreaCalculator("2-RPR", [3, 15, 8])
    N = 64
    u_x, u_y = [[-20, 20]] * 2
    grid_u1 = np.linspace(u_x[0], u_x[1], N + 1)
    grid_u2 = np.linspace(u_y[0], u_y[1], N + 1)
    grid_u = [grid_u1, grid_u2]
    ini_box = [u_x, u_y]

    boxes = AreaCalculator.make_boxes_list(grid_u, 2, False)
    # Assuming boxes[400] is included in the solution - green color
    # and boxes[1025] is on the border of the solution - yellow color
    drawer.uni_plotter([boxes[400]], [boxes[1025]], size = 2, ini_box = ini_box, title="Method")