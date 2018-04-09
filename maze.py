import numpy as np
from copy import deepcopy
from datetime import datetime as dt
from collections import OrderedDict, deque
from matplotlib import pyplot as plt
from matplotlib import colors

def incr_search(maze, target, start_point=(1,1), max_its=1000,
                directed=False, ret_paths=False, _debug=False):

    # Create main structure - ordered dict of paths.  
    paths = OrderedDict();

    # Initialise with one path, that has one point at 1,1
    paths[0] = [start_point]

    # Make some other useful containers
    tiles_seen = {start_point}
    last_tiles_seen = deque(maxlen=5)
    last_tiles_seen.append(start_point)
    dead_paths = OrderedDict();

    # Counters and such
    pad = 34
    its = 0
    path_count = 1
    start_time = dt.now()

    # Before beginning, check target is valid - remember False means it's open
    if maze[target]:
        print("Target invalid - it's a wall")
        return

    # Main functionality: go thru path dict repeatedly
    while its < max_its:

        # lists to put things while iterating over the paths (rather than changing the dict)
        temp_paths = []
        dead_keys = []

        # check path not totally blocked
        if len(paths) == 0:
            print("no paths left - can't find target")
            return

        # pure debuggery
        if _debug:
            print("\n\n" +  "-"*pad + "ITERATION", its, "-"*pad)
            print("\nLive paths:".ljust(pad), "{}".format(len(paths)).rjust(3))
            for p in paths: 
                print("--> {}".format(str(p+100)[-2:]).ljust(3), end=" ")
                if len(paths[p]) > 5: print("...", end="")
                print(paths[p][-5:])
            print("\nDead paths:".ljust(pad), "{}".format(len(dead_paths)).rjust(3))
            for p in dead_paths: 
                print("--> {}".format(str(p+100)[-2:]).ljust(3), end=" ")
                if len(dead_paths[p]) > 5: print("...", end="")
                print(dead_paths[p][-5:])
            print("\nTiles seen: ".ljust(pad), "{}".format(len(tiles_seen)).rjust(3))
            print("Latest:".ljust(pad), list(last_tiles_seen), "\n")
            print_maze(maze, target, tiles_seen, paths)


        # Now the real work - iterate over the paths

        # if directed, then reduce paths to the nearest and work only on that
        if directed:
            nearest = min(paths, key=lambda x: get_proximity(paths[x][-1], target))
            temp_var = paths
            paths =  {nearest:temp_var[nearest]}
            if _debug:
                print("\nDirected search. Closest path:".ljust(pad), end="")
                print("{}".format(str(nearest+100)[-2:]).ljust(3))
                if len(temp_var[nearest]) > 5: print("...", end="")
                print(temp_var[nearest][-5:])

        for path in paths:

            # rename to make easier
            p = paths[path]

            if _debug:
                print("\n\nEntering path".ljust(pad), "{}".format(str(path+100)[-2:]).rjust(3))

            # get the head of the path
            head = p[-1]
            if _debug: print("Selecting head: ".ljust(pad), head)

            # check for success
            if head == target:
                time_elapsed = (dt.now() - start_time).total_seconds()
                print("-"*12, "TARGET FOUND","-"*12)
                print("Path length:".ljust(pad), str(its).rjust(7))
                print("Successful path number:".ljust(pad), str(path).rjust(7))
                print("Number of paths tried:".ljust(pad), str(len(paths) + len(dead_paths)).rjust(7))
                print("Number of dead ends:".ljust(pad), str(len(dead_paths)).rjust(7))
                print("Total tiles visited:".ljust(pad), str(len(tiles_seen)).rjust(7))
                print("Time taken (ms):".ljust(pad), "{:0.2f}".format(time_elapsed*1000).rjust(7))
                print("-"*38)

                if not ret_paths:
                    return p

                else: return paths

            # otherwise get neighbouring open tiles
            neighbours = [n for n in get_neighbours(head, maze) if n not in tiles_seen]
            if _debug: print("-> Neighbours found: ".ljust(pad), neighbours)

            # if no neighbours flag the path for removal
            if not len(neighbours):
                if _debug: print("Dead path")
                dead_keys.append(path)

            # if there are neighbours, add the first of them to the current path
            else:
                p.append(neighbours[0])
                if _debug:
                    print("\n-> Extending current path with ".ljust(pad), neighbours[0])
                    print("-> Current path now:".ljust(pad), end=" ")
                    if len(p) > 5: print("...", end="")
                    print(p[-5:])

            #  if there's more than 1, make branches with the others
            if len(neighbours) > 1:
                for branch in neighbours[1:]:
                    if _debug: print("\n--> Creating branch for ".ljust(pad), branch)
                    new_path = deepcopy(p)[:-1]
                    new_path.append(branch)
                    temp_paths.append(new_path)

                #if _debug: print("--> Temp paths list:".ljust(pad), temp_paths)

            # add all neighbours to the log of seen tiles
            tiles_seen.update(neighbours)
            if _debug: last_tiles_seen.extend(neighbours)

        # switch the vars back if directed search
        if directed:
            paths = temp_var

        its += 1
        # Now the iteration is over can update the paths dictionary
        # - add new branches to the rest, and delete dead paths 

        for p in temp_paths:
            paths[path_count] = p
            path_count += 1

        for p in dead_keys:
            dead_paths[p] = deepcopy(paths[p])
            del paths[p]


def print_maze(maze, target, tiles_seen, paths):
    '''Output a maze with paths etc to the terminal
    '''
    # General idea is to built up a copy of the maze 
    # using ints as flags.  Then print according to those ints.

    # First transform maze from bool to ints (walls are 1s)
    maze = maze.copy().astype(int)

    # Now add flags for all tiles traversed
    for p in tiles_seen:
        for point in tiles_seen:
            maze[point] = 2

    # Adding labels for heads of live paths
    # -first get path keys and head points
    heads = {k:paths[k][-1] for k in paths}

    # - now write into maze
    for head in heads:
        # start at 100 to distinguish from other int flags 
        maze[heads[head]] = (head%100) + 100

    # Add a flag for the target itself
    maze[target] = 4

    # Finally print the maze.  Two chars per tile (as terminal chars are twice
    # as high as wide
    for row in maze:
        for cell in row:
            # walls
            if cell == 1: print(u'\u2588'*2, end="")
            # tiles seen
            elif cell == 2: print(u'\u2591'*2, end="")
            # the target
            elif cell == 4: print("<>", end="")
            # heads of live paths
            elif cell > 99: print(str(cell)[-2:], end="")
            # everything else is empty
            else: print(' '*2, end="")
        print("")



def get_neighbours(tile, maze, _debug=False):

    # the list to return
    out = []
    pad = 30

    # remember walls are True
    # Try North
    nbr = tile[0]-1, tile[1]
    if _debug: print("North:".ljust(pad), nbr, maze[nbr])
    if not maze[nbr]: out.append(nbr)

    nbr = tile[0], tile[1]+1
    if not maze[nbr]: out.append(nbr)
    if _debug: print("East:".ljust(pad), nbr, maze[nbr])

    nbr = tile[0]+1, tile[1]
    if not maze[nbr]: out.append(nbr)
    if _debug: print("South:".ljust(pad), nbr, maze[nbr])

    nbr = tile[0], tile[1]-1
    if not maze[nbr]: out.append(nbr)
    if _debug: print("West:".ljust(pad), nbr, maze[nbr])

    if _debug: print(out)

    return out


def maze(width=81, height=51, complexity=.75, density=.75):

    # Only odd shapes`
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)

    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    density    = int(density * ((shape[0] // 2) * (shape[1] // 2)))

    # Build actual maze
    Z = np.zeros(shape, dtype=bool)

    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    # Make aisles

    for i in range(density):
        x, y = np.random.randint(0, shape[1] // 2) * 2, np.random.randint(0, shape[0] // 2) * 2
        Z[y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:             neighbours.append((y, x - 2))
            if x < shape[1] - 2:  neighbours.append((y, x + 2))
            if y > 1:             neighbours.append((y - 2, x))
            if y < shape[0] - 2:  neighbours.append((y + 2, x))
            if len(neighbours):
                y_,x_ = neighbours[np.random.randint(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    return Z



def draw_maze(maze, path=None, paths=None, target=None, ax_in=None, figsize=(8,8)):

    maze = maze.copy().astype(int)

    if paths is not None:
        for p in paths:
            for point in paths[p]:
                maze[point] = 2

    if path is not None:
        for point in path:
            maze[point] = 3

    if target is not None:
        maze[target] = 4

    cmap = colors.ListedColormap(['white', 'grey', 'steelblue', 'yellow', 'red'])

    if ax_in is not None:
        ax_in = plt.imshow(maze, cmap=cmap)

    else:
        fig, ax = plt.subplots(figsize=figsize)
        ax = plt.imshow(maze, cmap=cmap)
        plt.show()





def get_proximity(a, b):
    # distance between points - hypotenuse of right triangle
    return ((a[0]-b[0])**2 + ((a[1]-b[1])**2))**0.5

