import consts
import math
import BubblesGrid


def create(center_x, center_y, color):
    return {"color": color,
            "center_x": center_x,
            "center_y": center_y,
            "radius": consts.BUBBLE_RADIUS}


def calc_center_x(col, row, row_start):
    bubble_x = row_start + col * (
            consts.BUBBLE_RADIUS * 2 + consts.SPACE_BETWEEN_COLS) + consts.BUBBLE_RADIUS

    # Uneven rows has an offset
    if row % 2 != 0:
        bubble_x += consts.BUBBLE_RADIUS

    return bubble_x


def calc_center_y(row):
    return row * (consts.BUBBLE_RADIUS * 2 - consts.ROWS_OVERLAP) + \
           consts.BUBBLE_RADIUS


def move_in_direction(bubble, direction):
    bubble["center_x"] += direction[0]
    bubble["center_y"] += direction[1]


def is_colliding_with_wall(bullet_bubble):
    return bullet_bubble["center_x"] - consts.BUBBLE_RADIUS <= 0 or \
           bullet_bubble[
               "center_x"] + consts.BUBBLE_RADIUS >= consts.WINDOW_WIDTH


def calc_direction(angle):
    # y/x = tan(angle)
    y_movement = 2
    x_movement = y_movement / math.tan(math.radians(angle))
    return x_movement, -y_movement


def pop(bubbles_grid, bubble_location):
    bubble_popped = bubbles_grid[bubble_location[0]][bubble_location[1]].copy()
    bubbles_grid[bubble_location[0]][bubble_location[1]][
        "color"] = consts.NO_BUBBLE
    return bubble_popped


def is_isolated(bubbles_grid, bubble_location):
    return is_isolated_inner(bubbles_grid, bubble_location, [])


def is_isolated_inner(bubbles_grid, bubble_location, locations_checked):
    start_row, start_col = bubble_location
    locations_checked.append(bubble_location)

    # Bubbles on first row are considered not isolated
    if start_row == 0:
        return False

    neighbors_directions = BubblesGrid.get_neighbors_directions(start_row)

    for direction in neighbors_directions:
        new_row = start_row + direction[0]
        new_col = start_col + direction[1]
        new_location = (new_row, new_col)

        if 0 <= new_row < len(bubbles_grid) and \
                0 <= new_col < consts.BUBBLE_GRID_COLS and \
                new_location not in locations_checked and \
                bubbles_grid[new_row][new_col]["color"] != consts.NO_BUBBLE and \
                not is_isolated_inner(bubbles_grid, new_location,
                                      locations_checked):
            return False

    return True


# -----------------------------------------------------------------------------
# ---------------------------------your code-----------------------------------
# -----------------------------------------------------------------------------

def distance_middles(bubble, bullet_bubble):
    distance_y = (float(bubble["center_y"]) - float(bullet_bubble["center_y"])) ** 2
    distance_x = (float(bubble["center_x"]) - float(bullet_bubble["center_x"])) ** 2
    distance = float((distance_y + distance_x) ** 0.5)
    return distance

def hit_top(bullet):
    if bullet['center_y'] <= consts.BUBBLE_RADIUS:
        return True

def should_stop(bubbles_grid,bullet_bubble):
    for row in range(BubblesGrid.get_length()):
        for col in range(consts.BUBBLE_GRID_COLS):
            bubble = BubblesGrid.get_bubble(row, col)
            if BubblesGrid.get_bubble(row,col)['color'] != consts.NO_BUBBLE:
                dist = distance_middles(bubble, bullet_bubble)
                if dist <= 2 * consts.BUBBLE_RADIUS:
                    return True
            elif hit_top(bullet_bubble):
                return True
    return False

'''

def should_stop(bubbles_grid, bullet_bubble):
    for row in range(len(bubbles_grid)-1):
        for col in range(len(bubbles_grid[row])):
            if bubbles_grid[row][col]["color"] != "EMPTY":
                distance = distance_middles(bubbles_grid[row][col], bullet_bubble)
                if distance <= float(2 * consts.BUBBLE_RADIUS):
                    return True
                elif float(bullet_bubble["center_y"]) == consts.BUBBLE_RADIUS:
                    return True
    return False

'''
