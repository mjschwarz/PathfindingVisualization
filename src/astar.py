import pygame
from queue import PriorityQueue
from src.helpers.config import WINDOW_WIDTH
from src.helpers.node import Node
from src.helpers.helpers import *


class AStar:
    """
    A* Search Algorithm
    """
    def heuristic_distance(self, p1, p2):
        """
        Calculate Manhattan distance between two points
        :param p1: <array> Point consisting of x and y coordinates
        :param p2: <array> Point consisting of x and y coordinates
        :return: Manhattan distance
        """
        x1, y1 = p1
        x2, y2 = p2
        return abs(x2 - x1) + abs(y2 - y1)

    def path_algorithm(self, grid, start, end):
        """
        Finds the shortest path using A* algorithm
        :param grid: <array> 2-D array representing the grid of nodes
        :param start: <Node> Starting node
        :param end: <Node> Ending node
        :return: True if path found, False if not
        """
        # tiebreaker
        count = 0
        # sort open nodes for heuristically shortest path
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        # store path
        came_from = {}
        # g_score -> current shortest distance to get from start to node
        g_score = { node: float("inf") for row in grid for node in row }
        g_score[start] = 0
        # f_score -> sum of g_score and distance from end node
        f_score = { node: float("inf") for row in grid for node in row }
        f_score[start] = self.heuristic_distance(start.get_pos(), end.get_pos())

        while not open_set.empty():
            # user quit - click red exit button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            # get and remove node at front of priority queue
            current = open_set.get()[2]

            # shortest path found
            if current == end:
                reconstruct_path(came_from, end, grid, start)
                start.make_start()
                return True

            for neighbor in current.neighbors:
                # distance between current and neighbor always 1
                tentative_g_score = g_score[current] + 1 

                # theoretically shorter path found
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic_distance(neighbor.get_pos(), end.get_pos())
                    # neighbor not yet visited
                    if neighbor not in open_set.queue and not neighbor.is_closed():
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        neighbor.make_open()

            draw(grid)

            # mark as closed/explored
            if current != start:
                current.make_closed()

        # no path found
        return False
