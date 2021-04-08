#!/usr/bin/env python3
from math import floor

WIDTH = 10
HEIGHT = 10
MAZE = "3 0 0 0 0 1 0 0 3 3 3 0 3 0 0 0 0 0 3 3 3 0 3 0 0 0 0 0 3 3 3 0 3 0 0 0 0 0 3 3 3 0 3 0 0 0 0 0 3 3 3 0 3 0 0 0 0 2 3 3 3 0 3 0 0 0 0 3 3 3 3 0 3 0 0 0 0 3 3 3 3 0 3 2 2 0 0 3 3 3 3 3 3 3 3 2 0 3 3 3".split(" ")
EMPTY = "0"
START = "1"
GOAL = "2"
WALL = "3"

up = lambda p: (p[0],p[1]-1)
down = lambda p: (p[0],p[1]+1)
left = lambda p: (p[0]-1, p[1])
right = lambda p: (p[0]+1, p[1])


def is_out_of_bounds(p, width=WIDTH, height=HEIGHT):
    x = p[0]
    y = p[1]
    return x >= width or x < 0 or y >= height or y < 0

def is_obstical(maze, p):
    return maze[xy_to_index(p)] == WALL


def is_goal(maze, p):
    return maze[xy_to_index(p)] == GOAL


def xy_to_index(p, width=WIDTH, height=HEIGHT):
    x = p[0]
    y = p[1]
    if is_out_of_bounds(p):
        raise IndexError

    return y*width + x


def index_to_xy(i):
    return i%WIDTH, floor(i/HEIGHT)


def draw_maze(maze, width=WIDTH, height=HEIGHT):
    for y in range(width):
        for x in range(height):
            print(maze[xy_to_index((x,y))], end=" ")
        print("")


def find_start(maze):
    for i, v in enumerate(maze):
        if v == START:
            return index_to_xy(i)

    raise ValueError("Could not find start")


def _dfs(maze, pos, path, visited, results):
    if is_out_of_bounds(pos) or pos in path:
        return path

    if maze[xy_to_index(pos)] == WALL or visited.get(pos, False):
        return path

    path.append(pos)
    visited[pos] = True

    if maze[xy_to_index(pos)] == GOAL:
        results.append(path[:])
        return path[:-1]

    path = _dfs(maze, up(pos), path[:], visited, results)
    path = _dfs(maze, left(pos), path[:], visited, results)
    path = _dfs(maze, down(pos), path[:], visited, results)
    path = _dfs(maze, right(pos), path[:], visited, results)

    return path[:-1]


def dfs():
    results = []
    _dfs(MAZE, find_start(MAZE), [], {}, results)
    return results


def bfs(maze, width=WIDTH, height=HEIGHT):
    maze = list(maze)
    paths = [[find_start(maze)]]

    while paths:
        paths = sorted(paths, key=lambda x: len(x), reverse=True)
        path = paths.pop()
        node = path[-1]

        if is_goal(maze, node):
            return list(path)

        for d in (up(node), down(node), left(node), right(node)):
            if not is_out_of_bounds(d) and not is_obstical(maze, d) and d not in path:
                l = list(path)
                l.append(d)
                paths.append(l)

    return []


def bfs_find_all(maze, width=WIDTH, height=HEIGHT):
    all_paths = []
    found = []
    maze = list(maze)

    found = bfs(maze)
    while found:
        if found:
            all_paths.append(found)
            node = found[-1]
            maze[xy_to_index(node)] = EMPTY
            draw_maze(maze)
            print("\n")
            found = []
        found = bfs(maze)

    return all_paths


def main():
    draw_maze(MAZE)
    print(dfs())
    print("\n\n\n\n")
    print(bfs_find_all(MAZE))


if __name__ == "__main__":
    main()
