"""
Class InputParser for parsing input file
"""
from enum import Enum
from math import pow


class InputParser:
    """
    Class InputParser for parsing input file
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def parse(filepath: str):
        """
        parse the input txt, return the list of input configurations
        """
        outputs = []
        with open(filepath, mode="r", encoding="utf-8") as file:
            while True:
                line = file.readline()
                if line == "":
                    break  # reach EoF

                if line == "\n" or "#" == line[0]:
                    continue  # skip comments

                # if here, it's the input
                outputs.append(line.strip())

        return outputs


class MovingDirection(Enum):
    """
    Enum class for the direction
    """

    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class Vehicle:
    """
    A vehicle
    """

    def __init__(
        self,
        name: str,
        last_point_loc: tuple,
        size=1,
        mov_dir=MovingDirection.HORIZONTAL,
        fuel=100,
    ) -> None:
        self.name = name
        self.size = size
        self.last_point_loc = last_point_loc
        self.mov_dir = mov_dir
        self.fuel = fuel

    def add_new_part(self, new_part_loc: tuple):
        """
        Add a new part of the vehicle
        """
        if (
            new_part_loc[0] != self.last_point_loc[0]
            and self.mov_dir != MovingDirection.VERTICAL
        ):  # same row
            self.mov_dir = MovingDirection.VERTICAL

        self.size += 1
        self.last_point_loc = new_part_loc

    def __str__(self):
        return (
            "vehicle name: "
            + self.name
            + " , size ="
            + str(self.size)
            + ", direction: "
            + str(self.mov_dir.value)
            + ", curr_fuel_level: "
            + str(self.fuel)
            + ", last_position: "
            + str(self.last_point_loc)
        )


class StateExtractor:
    """
    Class for extracting the information from a string
    """

    def __init__(self, str_input: str, fuel_update="", size=6) -> None:
        self.input = str_input
        self.vehicles = {}
        self.size = size
        self.has_custom_fuel = False
        self.board = []

        # collect vehicles
        self.collect_vehicles()
        if len(str_input) > 37:
            self.set_fuel_for_vehicles(self.input[37:])

        if len(fuel_update) > 2:
            self.set_fuel_for_vehicles(fuel_update)

    def convert_to_array(self):
        """
        Convert the str input into a 2-d array
        """
        curr_board = [0] * self.size  # initiate the 2-d array
        curr = 0
        for i in range(self.size):
            row = [0] * self.size
            for j in range(self.size):
                row[j] = self.input[curr]
                curr += 1
            curr_board[i] = row

        self.board = curr_board
        return curr_board

    def collect_vehicles(self):
        """
        Collect the vehicles info
        """
        vehicles = {}
        for idx, char in enumerate(self.input[:36]):
            if char == ".":
                continue  # no need

            # define curr location
            row_pos = idx // self.size
            col_pos = idx - row_pos * self.size
            curr_loc = (row_pos, col_pos)

            if vehicles.get(char) is None:
                # initiate the new vehicle
                vehicles[char] = Vehicle(char, curr_loc)
            else:
                # if the vehicle is defined, update its part
                vehicle: Vehicle = vehicles[char]
                vehicle.add_new_part(curr_loc)

        self.vehicles = vehicles
        return list(vehicles.values())

    def print_curr_layout(self):
        """
        print the current layout of the board
        """
        for i in range(self.size):
            start = i * self.size
            end = start + self.size
            print(self.input[start:end])

    def set_fuel_for_vehicles(self, fuel_info: str):
        """
        Method for setting the fuel for all vehicles in the current state

        fuel_info: the string represent the fuel information for all vehicles
        """
        if len(self.vehicles) == 0 or len(fuel_info) < 2:
            return

        # if there is some vehicles and some fuel info
        slow, fast = 0, 1
        while fast < len(fuel_info):
            veh_name = fuel_info[slow]
            vehicle: Vehicle = self.vehicles[veh_name]

            # collect fuel for this vehicle
            tmp_fuel = [""]
            while fuel_info[fast] != " ":
                tmp_fuel.append(fuel_info[fast])
                fast += 1
                if fast >= len(fuel_info):
                    break

            new_fuel = "".join(tmp_fuel)
            vehicle.fuel = int(new_fuel)

            # update pointers
            slow = fast + 1  # next vehicle name if exists
            fast = slow + 1

    def get_fuels(self):
        """
        Return the string representing the fuel
        """
        to_print = []
        for veh in self.vehicles.values():
            to_print.append(veh.name)
            to_print.append(str(veh.fuel))
            to_print.append(" ")

        return "".join(to_print)

    def get_curr_layout_str(self):
        """
        Return current layout as a string
        """
        end = pow(self.size, 2)
        return self.input[:end]
