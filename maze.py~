from copy import deepcopy

def incr_search(maze, target, start_point=(1,1), _debug=False):

    # create the main structure - a list of paths.  Start with one, that has one point at 1,1
    paths = [[start_point]]
    tiles_seen = {start_point}
    # go through paths repeatedly, extending by 1 where paths are open, adding new paths where there are choices

    # iterate over paths
    while True:
        for i, path in enumerate(paths):

            temp_paths = []

            print("seen: ", tiles_seen)
            if _debug:
                print("paths now")
                for p in paths:
                    print(p)

            if _debug: print("\nin path: ", i)
            # get the head of the path
            head = path[-1]
            print("Selecting head: ", head)
            if head == target:
                print("found target")
                return path
            tiles_seen.add(head)

            # get open tiles
            neighbours = [n for n in get_neighbours(head, maze) if n not in tiles_seen]
            if _debug: print("neighbours found: ", neighbours)

            # add to the first
            if len(neighbours):
                if _debug: print("extending current path with ", neighbours[0])
                path.append(neighbours[0])

            if len(neighbours) > 1:
                if _debug: print("found branches")
                for branch in neighbours[1:]:
                    if _debug: print("creating branch for ", branch)
                    new_path = deepcopy(path)[:-1]
                    if _debug: print("made a new path ", new_path)
                    new_path.append(branch)
                    temp_paths.append(new_path)
                    if _debug: 
                        print("appended a path, with head ", branch)
                        print("length of paths list now ", len(paths))
            # branch and add to the rest

        paths.extend(temp_paths)
        print("paths after an iteration") 
        for p in paths:
            print(p)

def get_neighbours(tile, maze):

    # the list to return
    out = []

    # go around the compass, NESW
    #out['N'] = maze[tile[0]-1, tile[0]]
    #out['E'] = maze[tile[0],   tile[0]+1]
    #out['S'] = maze[tile[0]+1, tile[0]]
    #out['W'] = maze[tile[0],   tile[0]-1]

    # remember walls are True
    if not maze[tile[0]-1, tile[0]]:
        out.append((tile[0]-1, tile[0]))

    if not maze[tile[0],   tile[0]+1]:
        out.append((tile[0], tile[0]+1))

    if not maze[tile[0]+1, tile[0]]:
        out.append((tile[0]+1, tile[0]))

    if not maze[tile[0],   tile[0]-1]:
        out.append((tile[0], tile[0]-1))

    return out
