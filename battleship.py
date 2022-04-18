import copy
import random


def create_map(length, height):
    nmap = []
    for i in range(height + 1):
        nmap.append([])
        for j in range(length + 1):
            nmap[i].append('o')
    return nmap


def print_map(map_to_print: list):
    for key, item in enumerate(map_to_print):
        print(' '.join(item))


def conditions(nmap, x, y, map_length, map_height, first, direction):
    """
    Is the coordinate checked free of neighbors directly
    Parameters
    ----------
    nmap: map
    x: position on x-axis
    y: position on y-axis
    map_length: length of the map
    map_height: height of the map
    first: We do want to check top or left neighbor only during the first iteration
    direction: Either vertical or horizontal

    Returns
    -------
    True if the boat could be on this coordinate.

    """
    check_left = True
    check_top = True

    if 'V' in direction and not first:
        check_top = False
    if 'H' in direction and not first:
        check_left = False

    if y - 1 >= 0 and check_top:
        # Top
        if nmap[y - 1][x] == 'X':
            return False
    if y + 1 <= map_height:
        # bottom
        if nmap[y + 1][x] == 'X':
            return False
    if x - 1 >= 0 and check_left:
        # left
        if nmap[y][x - 1] == 'X':
            return False
    if x + 1 <= map_length:
        # right
        if nmap[y][x + 1] == 'X':
            return False
    return True


def diag_conditions(nmap, x, y, map_length, map_height):
    """
    Check if coordinate is free of diagonals neighbors.
    Parameters
    ----------
    nmap
    x
    y
    map_length
    map_height

    Returns
    -------
    Bool
    """
    if y - 1 >= 0:
        # diag top right
        if x + 1 <= map_length:
            if nmap[y - 1][x + 1] == 'X':
                return False
        # diag top left
        if x - 1 >= 0:
            if nmap[y - 1][x - 1] == 'X':
                return False
    if y + 1 <= map_height:
        # diag bot right
        if x + 1 <= map_length:
            if nmap[y + 1][x + 1] == 'X':
                return False
        # diag bot left
        if x - 1 >= 0:
            if nmap[y + 1][x - 1] == 'X':
                return False
    return True


def try_to_draw(boat, x, y, direction, nmap, length, height):
    """
    Check if the boat can be placed with this coordinate.
    Parameters
    ----------
    boat
    x
    y
    direction
    nmap
    length
    height

    Returns
    -------
    Bool
    """
    map_copy = nmap.copy()
    if 'V' in direction:
        for i in range(boat):
            try:
                if nmap[y + i][x] == 'o' and diag_conditions(map_copy, x, y + i, length, height) and conditions(map_copy, x, y + i, length, height, i == 0, direction):
                    pass
                else:
                    return False
            except IndexError:
                return False
        return True
    if 'H' in direction:
        for i in range(boat):
            try:
                if nmap[y][x + i] == 'o' and diag_conditions(map_copy, x + i, y, length, height) and conditions(map_copy, x + i, y, length, height, i == 0, direction):
                    pass
                else:
                    return False
            except IndexError:
                return False
        return True


def draw_boat(boat, x, y, direction, nmap):
    """
    Draw the boat on the map.
    Parameters
    ----------
    boat
    x
    y
    direction
    nmap

    Returns
    -------
    map
    """
    if 'V' in direction:
        for i in range(boat):
            nmap[y + i][x] = 'X'
    else:
        for i in range(boat):
            nmap[y][x + i] = 'X'
    return nmap


def main():
    ships_list = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    boat_list = []
    # Keep in mind that length and height start at 0, this is not the number of column or rows
    # Map has to be at least 6x6 to work with the rules
    map_length = 6
    map_height = 6
    dir_list = []
    coord_list = []
    compt = 0
    ultimate_reset = {}
    """
     When we can not draw a boat even after trying all the coordinates we will need to get
     the state of the map before drawting the previous boat. So we will have a queue of map's
     state and just pop the last one each time we change a boat.
    """
    q = []

    if map_height < 6 or map_length < 6:
        print('Not possible')
        return

    nmap = create_map(map_length, map_height)
    boat = max(ships_list)
    start_x = random.randint(0, map_length)
    start_y = random.randint(0, map_height)
    boat_direction = random.choices(['V', 'H'])

    while len(ships_list) != 0:
        worked = try_to_draw(
            boat, start_x, start_y, boat_direction, nmap, map_length, map_height
        )
        # Uncomment next line to have the coordinate tried.
        # print(f'start {boat} + {start_x} + {start_y} + {boat_direction}')
        if worked:
            boat_list.append(boat)
            ships_list.pop(ships_list.index(boat))
            coord_list.clear()
            q.append(copy.deepcopy(nmap))
            nmap = draw_boat(boat, start_x, start_y, boat_direction, nmap)
            if len(ships_list) > 0:
                boat = max(ships_list)
        else:
            # Change the direction of the boat
            if boat_direction not in dir_list:
                dir_list.append(boat_direction)
                boat_direction = ['V'] if boat_direction == ['H'] else ['H']

            # If the 2 directions has been tryied for this boat in this coord
            else:
                dir_list.clear()
                # If every coord has been tried then change the boat
                if len(coord_list) + 1 == (map_length + 1) * (map_height + 1):
                    if len(boat_list) <= 0:
                        print('Not possible')
                        return

                    """ 
                    ships_list correspond to the list of ship that has not been placed
                    Append the last boat placed on the map to this list so it becomes the next
                    tried boat.
                    """
                    ships_list.append(min(boat_list))
                    boat_list.pop(boat_list.index(min(boat_list)))
                    boat = max(ships_list)
                    coord_list.clear()
                    nmap = q.pop()
                    ultimate_reset[boat] = 1 if boat not in ultimate_reset else ultimate_reset[boat] + 1

                    # Sometimes, the map is fucked up so we full reset.
                    if boat in ultimate_reset and ultimate_reset[boat] > 4:
                        ultimate_reset = {}
                        ships_list = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
                        nmap = create_map(map_length, map_height)
                        start_x = random.randint(0, map_length)
                        start_y = random.randint(0, map_height)
                        boat_list.clear()
                        coord_list.clear()

                # Since we use the len of coord_list to know if we tried every coordinate
                # possible we need to make sure that we don't append duplicate in the list.
                while [start_x, start_y] in coord_list:
                    start_x = random.randint(0, map_length)
                    start_y = random.randint(0, map_height)

                if [start_x, start_y] not in coord_list:
                    coord_list.append([start_x, start_y])
                boat_direction = random.choices(['V', 'H'])
        compt += 1

    print(f"Every ships been placed in {compt} tries. \nHere is the map:")
    print_map(nmap)
    return


main()
