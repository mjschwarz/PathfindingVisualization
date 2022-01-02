import pygame
from queue import Queue
from src.helpers.config import WINDOW_WIDTH
from src.helpers.node import Node
from src.helpers.helpers import *


class BFS:
    """
    Breadth-first Search Algorithm
    """
    def path_algorithm(self, grid, start, end):
        """
        Finds the shortest path using BFS algorithm
        :param grid: <array> 2-D array representing the grid of nodes
        :param start: <Node> Starting node
        :param end: <Node> Ending node
        :return: True if path found, False if not
        """
        # store open nodes chronologically as encountered for shortest path
        open_set = Queue()
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

            # shortest path found
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