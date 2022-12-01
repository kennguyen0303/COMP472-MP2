"""
Module for search algorithms
"""
import heapq
from input_parser import StateExtractor
from search_tree import move_down, move_up, move_horizontal, remove_vehicle


class UCS:
    """
    Class for universal cost search
    """

    def __init__(self) -> None:
        self.closed_list = (
            {}
        )  # a normal list, can be a map for fast check, only need the key = "state_string"
        self.open_list = (
            []
        )  # the max-heap / sorted queue, storing the tuples (cost, state_string, fuel_update)
        heapq.heapify(self.open_list)
        self.is_final_state_reached = False
        self.final_state = StateExtractor("")
        self.state_count = 0
        self.ori_input = ""

    def search_ucs(self, input_str: str):
        """
        Universal Cost Search
        """
        if input_str.strip() == "":  # invalid input
            return

        fuel_update = ""
        parent_state = ""
        curr_cost = 0
        self.ori_input = input_str
        # add root
        self.open_list.append((curr_cost, input_str, fuel_update, parent_state, ""))

        # loop
        while len(self.open_list) > 0:
            # Stop conditions:
            if self.is_final_state_reached:
                print("FOUND")
                break

            next_state = heapq.heappop(self.open_list)
            curr_cost, input_str, parent_state = (
                next_state[0],
                next_state[1],
                next_state[3],
            )

            fuel_update = (
                next_state[2] if len(next_state[1]) < 38 else next_state[1][37:]
            )  # only the first node

            if self.closed_list.get(input_str) is not None:  # a visited state
                continue

            if input_str == "..IJ.LBBIJ.LGAA...GHDDK.GHEEK.FF..K.":
                print("Here")

            self.state_count += 1
            extractor = StateExtractor(input_str, fuel_update)

            # Step 0: Add curr_state to the closed_list
            self.closed_list[input_str] = (
                parent_state,
                next_state[4],
            )  # store parent state and move_details

            # step 1: Check for vehicle at the exit
            for vehicle in extractor.vehicles.values():
                if not vehicle.can_be_removed():
                    continue

                if vehicle.name == "A":  # goal state reached
                    self.is_final_state_reached = True
                    self.final_state = extractor  # store for key search in closed_list
                    extractor.print_curr_layout()
                    print("\n-------\n")
                    print(extractor.get_fuels())
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
                                heapq.heappush(
                                    self.open_list,
                                    (
                                        curr_cost + 1,
                                        new_move[0],
                                        new_move[1] + " " + fuel_update,
                                        input_str,
                                        new_move[2],
                                    ),
                                )  # new_move <state_string, fuel_update for this move, message for search path>

                    distance += 1
