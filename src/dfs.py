import pygame
from queue import LifoQueue
from src.helpers.config import WINDOW_WIDTH
from src.helpers.node import Node
from src.helpers.helpers import *


class DFS:
    """
    Depth-first Search Algorithm
    """
    def path_algorithm(self, grid, start, end):
        """
        Finds the a path (not necessarily shortest) using DFS algorithm
        :param grid: <array> 2-D array representing the grid of nodes
        :param start: <Node> Starting node
        :param end: <Node> Ending node
        :return: True if path found, False if not
        """
        # store open nodes in a stack
        open_set = LifoQueue()
        open_set.put(start)
        # store path
        came_from = {}

        while not open_set.empty():
            # user quit - click red exit button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            # get and remove node at front of priority queue
            current = open_set.get()

            # path found
            if current == end:
                reconstruct_path(came_from, end, grid, start)
                start.make_start()
                return True

            for neighbor in current.neighbors:
                # neighbor not yet visited
                if neighbor not in open_set.queue and not (neighbor.is_closed() or neighbor.is_start()):
                    came_from[neighbor] = current
                    open_set.put(neighbor)
                    neighbor.make_open()

            draw(grid)

            # mark as closed/explored
            if current != start:
                current.make_closed()

        # no path found
        return False