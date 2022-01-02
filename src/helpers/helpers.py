import pygame
from src.helpers.config import *
from src.helpers.node import Node


def draw_grid():
    """
    Draw grid lines
    :return: None
    """
    for row in range(GRID_SIZE):
        pygame.draw.line(WINDOW, GREY, (0, row * NODE_SIZE), (WINDOW_WIDTH, row * NODE_SIZE))

    for col in range(GRID_SIZE):
        pygame.draw.line(WINDOW, GREY, (col * NODE_SIZE, 0), (col * NODE_SIZE, WINDOW_WIDTH))

def draw(grid):
    """
    Redraw all nodes in grid with updated color
    :param grid: <array> 2-D array representing the grid of nodes
    :return None
    """
    WINDOW.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw()

    draw_grid()
    pygame.display.update()

def reconstruct_path(came_from, current, grid, start):
        """
        Draw shortest path
        :param came_from: <dict> key -> nodeA : value -> node used to reach nodeA
        :param current: <Node> Node currently being considered
        :param grid: <array> 2-D array representing the grid of nodes
        :param end: <Node> Ending node
        :return None
        """
        end = current
        
        while current in came_from:
            current = came_from[current]
            if current == start:
                break
            current.make_path()
            end.make_end()
            draw(grid)
