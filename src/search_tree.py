"""
Module for handling the search tree
"""
from input_parser import MovingDirection, StateExtractor, Vehicle


def move_up(extractor: StateExtractor, vehicle_name: str, distance: int):
    """
    moving up by a given distance. Return the new str representing the new state
    """
    vehicle: Vehicle = extractor.vehicles[vehicle_name]
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


def move_down(extractor: StateExtractor, vehicle_name: str, distance: int):
    """
    moving down by a given distance. Return the new str representing the new state
    """
    vehicle: Vehicle = extractor.vehicles[vehicle_name]
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


def move_horizontal(extractor: StateExtractor, vehicle_name: str, distance: int):
    """
    moving horizontally by a given distance. Return the new str representing the new state.
    If distance > 0: go to the right. Else, distance <0, move to the left
    """
    is_go_left = distance < 0
    vehicle: Vehicle = extractor.vehicles[vehicle_name]
    new_move_str = list(extractor.input[:36])
    target_col = (
        vehicle.last_point_loc[1] + distance
        if not is_go_left
        else vehicle.last_point_loc[1] + distance - (vehicle.size - 1)
    )  # detect the target column
    cannot_move_rules = [
        distance == 0,
        vehicle.fuel < abs(distance),
        vehicle.mov_dir == MovingDirection.VERTICAL,
        target_col < 0,
        target_col >= extractor.size,
        extractor.input[target_col + extractor.size * vehicle.last_point_loc[0]] != ".",
    ]
    for cond in cannot_move_rules:
        if cond:
            return ""  # not doing anything and stop here

    # if possible to move
    for i in range(abs(distance)):
        curr_col_target = (
            target_col + i if is_go_left else target_col - i
        )  # move to the right from the left-most target cell
        curr_col_src = (
            vehicle.last_point_loc[1] - i
            if is_go_left
            else vehicle.last_point_loc[1] + i - (vehicle.size - 1)
        )
        target_loc = curr_col_target + extractor.size * vehicle.last_point_loc[0]
        source_loc = curr_col_src + extractor.size * vehicle.last_point_loc[0]
        new_move_str[target_loc] = vehicle.name
        new_move_str[source_loc] = "."

    return "".join(new_move_str)
