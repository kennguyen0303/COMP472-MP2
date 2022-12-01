"""
Module for handling the search tree
"""
from input_parser import MovingDirection, StateExtractor, Vehicle

DEFAULT_MESSAGE = ""


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
    ]
    for cond in cannot_move_rules:
        if cond:
            return ("", "", DEFAULT_MESSAGE)  # not doing anything and stop here

    if curr_board_str[target_row * extractor.size + vehicle.last_point_loc[1]] != ".":
        # not available
        return ("", "", DEFAULT_MESSAGE)

    # if possible to move
    for i in range(distance):
        curr_row_target = target_row + i  # move down from the top cell
        curr_row_src = vehicle.last_point_loc[0] - i
        target_loc = curr_row_target * extractor.size + vehicle.last_point_loc[1]
        source_loc = curr_row_src * extractor.size + vehicle.last_point_loc[1]
        if new_move_str[target_loc] == "." and new_move_str[source_loc] == ".":
            continue  # no need to switch
        if new_move_str[target_loc] != "." or new_move_str[source_loc] != vehicle.name:
            return ("", "", DEFAULT_MESSAGE)
        new_move_str[target_loc] = vehicle.name
        new_move_str[source_loc] = "."

    fuel_update = vehicle.name + str(vehicle.fuel - distance)
    message = vehicle_name + " up " + str(distance)
    return ("".join(new_move_str), fuel_update, message)


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
        target_row >= extractor.size,
    ]
    for cond in cannot_move_rules:
        if cond:
            return ("", "", DEFAULT_MESSAGE)  # not doing anything and stop here

    if extractor.input[target_row * extractor.size + vehicle.last_point_loc[1]] != ".":
        # not available
        return ("", "", DEFAULT_MESSAGE)

    # if possible to move
    for i in range(distance):
        curr_row_target = target_row - i  # move up from the lowest cell
        curr_row_src = vehicle.last_point_loc[0] + i - (vehicle.size - 1)  #
        target_loc = curr_row_target * extractor.size + vehicle.last_point_loc[1]
        source_loc = curr_row_src * extractor.size + vehicle.last_point_loc[1]
        if new_move_str[target_loc] == "." and new_move_str[source_loc] == ".":
            continue  # no need to switch
        if new_move_str[target_loc] != "." or new_move_str[source_loc] != vehicle.name:
            return ("", "", DEFAULT_MESSAGE)
        new_move_str[target_loc] = vehicle.name
        new_move_str[source_loc] = "."

    fuel_update = vehicle.name + str(vehicle.fuel - distance)
    message = vehicle_name + " down " + str(distance)
    return ("".join(new_move_str), fuel_update, message)


def move_horizontal(extractor: StateExtractor, vehicle_name: str, distance: int):
    """
    moving horizontally by a given distance. Return the new str representing the new state.
    If distance > 0: go to the right. Else, distance <0, move to the left
    """
    is_go_left = distance < 0
    vehicle: Vehicle = extractor.vehicles[vehicle_name]
    new_move_str = list(extractor.input[:36])
    fuel_update = ""
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
    ]
    for cond in cannot_move_rules:
        if cond:
            return ("", "", DEFAULT_MESSAGE)  # not doing anything and stop here

    if extractor.input[target_col + extractor.size * vehicle.last_point_loc[0]] != ".":
        # not available
        return ("", "", DEFAULT_MESSAGE)

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
        if new_move_str[target_loc] == "." and new_move_str[source_loc] == ".":
            continue  # no need to switch
        if new_move_str[target_loc] != "." or new_move_str[source_loc] != vehicle.name:
            return ("", "", DEFAULT_MESSAGE)  # invalid case detected
        new_move_str[target_loc] = vehicle.name
        new_move_str[source_loc] = "."

    fuel_update = vehicle.name + str(vehicle.fuel - abs(distance))
    message = (
        vehicle_name + " left " + str(abs(distance))
        if is_go_left
        else vehicle_name + " right " + str(distance)
    )
    return ("".join(new_move_str), fuel_update, message)


def remove_vehicle(extractor: StateExtractor, vehicle_name: str):
    """
    Remove a horizontal vehicle only if it's at the exit. Return the new string representation
    """
    vehicle: Vehicle = extractor.vehicles[vehicle_name]
    if (
        vehicle_name == "A"
        or vehicle.mov_dir == MovingDirection.VERTICAL
        or not vehicle.can_be_removed()
    ):
        raise ValueError("Invalid vehicle to be removed..")

    curr_board = list(extractor.input[:36])

    for i in range(vehicle.size):
        source_loc = (
            vehicle.last_point_loc[1] - i + extractor.size * vehicle.last_point_loc[0]
        )
        curr_board[source_loc] = "."

    return "".join(curr_board)
