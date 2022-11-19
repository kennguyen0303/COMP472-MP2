"""
Module for handling the search tree
"""
from input_parser import MovingDirection, StateExtractor, Vehicle


def move_up(extractor: StateExtractor, vehicle: Vehicle, distance: int):
    """
    moving up by a given distance. Return the new str representing the new state
    """
    curr_board_str = extractor.input
    new_move_str = list(curr_board_str[:36])
    target_row = (
        vehicle.last_point_loc[0] - distance - (vehicle.size - 1)
    )  # -1 because location is based 0, but size starts at 1
    cannot_move_rules = [
        distance == 0,
        vehicle.fuel < distance,
        vehicle.mov_dir == MovingDirection.HORIZONTAL,
        target_row < 0,
        curr_board_str[target_row * extractor.size + vehicle.last_point_loc[1]] != ".",
    ]
    for cond in cannot_move_rules:
        if cond:
            return ""  # not doing anything and stop here

    # if possible to move
    for i in range(distance):
        curr_row_target = target_row + i  # move down from the top cell
        curr_row_src = vehicle.last_point_loc[0] - i
        target_loc = curr_row_target * extractor.size + vehicle.last_point_loc[1]
        source_loc = curr_row_src * extractor.size + vehicle.last_point_loc[1]
        new_move_str[target_loc] = vehicle.name
        new_move_str[source_loc] = "."

    return "".join(new_move_str)


def move_down(extractor: StateExtractor, vehicle: Vehicle, distance: int):
    """
    moving down by a given distance. Return the new str representing the new state
    """
    new_move_str = list(extractor.input[:36])
    target_row = vehicle.last_point_loc[0] + distance
    cannot_move_rules = [
        distance == 0,
        vehicle.fuel < distance,
        vehicle.mov_dir == MovingDirection.HORIZONTAL,
        target_row < 0,
        target_row > extractor.size,
        extractor.input[target_row * extractor.size + vehicle.last_point_loc[1]] != ".",
    ]
    for cond in cannot_move_rules:
        if cond:
            return ""  # not doing anything and stop here

    # if possible to move
    for i in range(distance):
        curr_row_target = target_row - i  # move up from the lowest cell
        curr_row_src = vehicle.last_point_loc[0] + i - (vehicle.size - 1)  #
        target_loc = curr_row_target * extractor.size + vehicle.last_point_loc[1]
        source_loc = curr_row_src * extractor.size + vehicle.last_point_loc[1]
        new_move_str[target_loc] = vehicle.name
        new_move_str[source_loc] = "."

    return "".join(new_move_str)
