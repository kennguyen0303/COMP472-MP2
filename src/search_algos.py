"""
Module for search algorithms
"""
import heapq
from constants import SIZE
from input_parser import StateExtractor
from search_tree import move_down, move_up, move_horizontal, remove_vehicle


class GenericSearch:
    """
    Class for universal cost search
    """

    def __init__(self, function_g, function_h, name="", heuristic_name="NA") -> None:
        self.name = name
        self.heuristic_name = heuristic_name
        self.function_g = function_g
        self.function_h = function_h
        self.search_path = []
        self.closed_list = (
            {}
        )  # a normal list, can be a map for fast check, only need the key = "state_string"
        self.open_list = (
            []
        )  # the max-heap / sorted queue, storing the tuples (cost, state_string, fuel_update)
        heapq.heapify(self.open_list)
        self.is_final_state_reached = False
        self.final_state = StateExtractor("")
        self.ori_input = ""

    def search(self, input_str: str):
        """
        Run search algo
        """
        if input_str.strip() == "":  # invalid input
            return

        fuel_update = " "
        parent_state = ""
        curr_cost = 0
        self.ori_input = input_str
        init_h = self.function_h(input_str[:36])
        # add root
        self.open_list.append(
            (
                curr_cost + init_h,
                input_str,
                fuel_update,
                parent_state,
                "",
                (curr_cost, init_h),
            )
        )

        # loop
        while len(self.open_list) > 0:
            # Stop conditions:
            if self.is_final_state_reached:
                break

            next_state = heapq.heappop(self.open_list)
            curr_cost, input_str, parent_state = (
                next_state[5][0],
                next_state[1],
                next_state[3],
            )

            fuel_update = (
                next_state[2] if len(next_state[1]) < 38 else next_state[1][37:]
            )  # only the first node

            if self.closed_list.get(input_str) is not None:  # a visited state
                continue

            extractor = StateExtractor(input_str, fuel_update)

            # Step 0: Add curr_state to the closed_list
            self.closed_list[input_str] = (
                parent_state,
                next_state[4],
                fuel_update[len(fuel_update) - 3 : len(fuel_update)][1:],
            )  # store <parent_state, move_details, new_fuel_for_vehicle_moved
            # search path update
            self.search_path.append(next_state)

            # step 1: Check for vehicle at the exit
            for vehicle in extractor.vehicles.values():
                if not vehicle.can_be_removed():
                    continue

                if vehicle.name == "A":  # goal state reached
                    self.is_final_state_reached = True
                    self.final_state = extractor  # store for key search in closed_list
                    # extractor.print_curr_layout()
                    # print(len(self.closed_list))
                    # print("\n-------\n")
                    # print(extractor.get_fuels(only_consumed=True))
                    return

                # remove the vehicle at exit
                new_state = remove_vehicle(extractor, vehicle.name)
                extractor.set_new_input(
                    new_state, fuel_update
                )  # update new state and vehicles data
                break  # Each time, there will be only one vehicle at the exit

            # step 2: Explore all possible states for each vehicles
            vehicles = extractor.vehicles.values()
            for vehicle in vehicles:
                no_more_move = False
                distance = 1

                while not no_more_move:
                    possible_moves = [
                        move_horizontal(extractor, vehicle.name, -distance),
                        move_horizontal(extractor, vehicle.name, distance),
                        move_up(extractor, vehicle.name, distance),
                        move_down(extractor, vehicle.name, distance),
                    ]

                    # 1. check new states in CLOSED list
                    # 2. if a new state is found, add to open_list
                    no_more_move = True
                    for new_move in possible_moves:
                        if new_move[0] != "":
                            if (
                                self.closed_list.get(new_move[0]) is None
                            ):  # not in closed list
                                no_more_move = False
                                cost_g = self.function_g(curr_cost)
                                cost_h = self.function_h(new_move[0])
                                # curr_cost +1
                                # new_move <state_string, fuel_update for
                                # this move, message for search path>
                                heapq.heappush(
                                    self.open_list,
                                    (
                                        cost_g + cost_h,
                                        new_move[0],
                                        fuel_update + " " + new_move[1],
                                        input_str,
                                        new_move[2],
                                        (cost_g, cost_h),
                                    ),
                                )

                    distance += 1


class UCS(GenericSearch):
    """'
    UCS algo
    """

    def __init__(self) -> None:
        super().__init__(
            function_g=self.calculate_g, function_h=self.calculate_heuristic, name="UCS"
        )

    def calculate_g(self, curr_cost: int):
        """
        find the cost based on number of parents
        """
        return curr_cost + 1

    def calculate_heuristic(self, __state_str__: str):
        """'
        Calculate heruristic based on a string
        """
        return 0


class GBFS(GenericSearch):
    """'
    Greedy best first search algo
    """

    def __init__(self, heuristic_function, heuristic_name: str) -> None:
        super().__init__(
            function_g=self.calculate_g,
            function_h=heuristic_function,
            name="GBFS",
            heuristic_name="h" + heuristic_name,
        )

    def calculate_g(self, __curr_cost__: int):
        """
        find the cost based on number of parents
        """
        return 0


class AlgoA(GenericSearch):
    """'
    Algorithm A
    """

    def __init__(self, heuristic_function, heuristic_name: str) -> None:
        super().__init__(
            function_g=self.calculate_g,
            function_h=heuristic_function,
            name="A/A*",
            heuristic_name="h" + heuristic_name,
        )

    def calculate_g(self, curr_cost: int):
        """
        find the cost based on number of parents
        """
        return curr_cost + 1


def calculate_heuristic_1(state_str: str):
    """'
    Calculate heruristic based on a string

    Heuristic 1: Number of blocking vehicles
    """
    # first, locate A on row 3
    row_loc = 2
    slow = SIZE * row_loc
    fast = slow
    end = slow + (SIZE - 1)
    is_ambulance_found = False
    heuristic = 0
    while fast <= end:
        if state_str[fast] == "A":
            # goal: slow is the first cell of A
            if not is_ambulance_found:
                is_ambulance_found = True
                slow = fast
        elif is_ambulance_found:
            if state_str[fast] != "." and state_str[fast] != state_str[slow]:
                slow = fast
                heuristic += 1

        fast += 1
    return heuristic


def calculate_heuristic_2(state_str: str):
    """'
    Calculate heruristic based on a string

    Heuristic 2: Number of blocked positions
    (position which is not . towards the exit)
    """
    # first, locate A on row 3
    row_loc = 2
    slow = SIZE * row_loc
    fast = slow
    end = slow + (SIZE - 1)
    is_ambulance_found = False
    heuristic = 0
    while fast <= end:
        if state_str[fast] == "A":
            # goal: slow is the first cell of A
            if not is_ambulance_found:
                is_ambulance_found = True
                slow = fast
        elif is_ambulance_found and (state_str[fast] != "."):
            heuristic += 1

        fast += 1
    return heuristic


def calculate_heuristic_3(state_str: str):
    """'
    Calculate heruristic based on a string

    Heuristic 3: Multiply heuristic 1 with a constant = 5
    """
    return calculate_heuristic_1(state_str) * 5


def calculate_heuristic_4(state_str: str):
    """'
    Calculate heruristic based on a string

    Heuristic 4: Measure difference between the distance
    from the ambulance (last cell) to the exit and
    the number of available cells
    """
    row_loc = 2
    slow = SIZE * row_loc
    fast = slow
    end = slow + (SIZE - 1)
    is_ambulance_found = False
    distance = 0
    num_of_empty_spot = 0
    while fast <= end:
        if state_str[fast] == "A":  # first, locate A on row 3
            # goal: slow is the last cell of A
            if not is_ambulance_found:
                is_ambulance_found = True

            slow = fast
        elif is_ambulance_found:  # calculate the distance
            distance = end - slow
            break

        fast += 1

    while fast <= end:
        if state_str[fast] == ".":
            num_of_empty_spot += 1

        fast += 1

    return distance - num_of_empty_spot
