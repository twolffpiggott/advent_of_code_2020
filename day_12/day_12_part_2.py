import argparse
import numpy as np


DEGREES_TO_RADIANS = np.pi / 180


class ShipNavigator:
    def __init__(self, instructions: str):
        self.instructions = instructions
        # start at coordinate (0, 0)
        self.x: float = 0
        self.y: float = 0
        # start waypoint at coordinate (10, 1) relative to ship
        self.waypoint_x = 10
        self.waypoint_y = 1

    def apply_instructions(self):
        for instruction in self.instructions.split("\n"):
            self.apply_instruction(instruction)

    def apply_instruction(self, instruction: str):
        action = instruction[0]
        value = float(instruction[1:])
        if action == "N":
            self.waypoint_y += value
        elif action == "S":
            self.waypoint_y -= value
        elif action == "E":
            self.waypoint_x += value
        elif action == "W":
            self.waypoint_x -= value
        elif action == "L":
            self.rotate_waypoint(value)
        elif action == "R":
            self.rotate_waypoint(-value)
        elif action == "F":
            self.x += value * self.waypoint_x
            self.y += value * self.waypoint_y
        else:
            raise ValueError(f"Invalid action: {action}")

    def rotate_waypoint(self, value: float):
        # first find the updated angle to the waypoint
        updated_angle_to_waypoint = self.angle_to_waypoint + value
        if updated_angle_to_waypoint < 0:
            updated_angle_to_waypoint = 360 + updated_angle_to_waypoint
        if updated_angle_to_waypoint >= 360:
            updated_angle_to_waypoint = updated_angle_to_waypoint % 360

        if 0 <= updated_angle_to_waypoint < 90:
            reduced_angle_to_waypoint = updated_angle_to_waypoint
            x_sign = 1
            y_sign = 1
        elif 90 <= updated_angle_to_waypoint < 180:
            reduced_angle_to_waypoint = 180 - updated_angle_to_waypoint
            x_sign = -1
            y_sign = 1
        elif 180 <= updated_angle_to_waypoint < 270:
            reduced_angle_to_waypoint = updated_angle_to_waypoint - 180
            x_sign = -1
            y_sign = -1
        elif 270 <= updated_angle_to_waypoint < 360:
            reduced_angle_to_waypoint = 360 - updated_angle_to_waypoint
            x_sign = 1
            y_sign = -1
        else:
            raise ValueError(f"Invalid heading: {self.heading}")
        reduced_angle_to_waypoint_radians = (
            DEGREES_TO_RADIANS * reduced_angle_to_waypoint
        )
        previous_distance_to_waypoint = self.distance_to_waypoint
        self.waypoint_x = (
            x_sign
            * previous_distance_to_waypoint
            * np.cos(reduced_angle_to_waypoint_radians)
        )
        self.waypoint_y = (
            y_sign
            * previous_distance_to_waypoint
            * np.sin(reduced_angle_to_waypoint_radians)
        )

    @property
    def angle_to_waypoint(self):
        if self.waypoint_x >= 0 and self.waypoint_y >= 0:
            x_multiple = 1
            arccos_multiple = 1
            radian_constant = 0
        elif self.waypoint_x < 0 and self.waypoint_y >= 0:
            x_multiple = -1
            arccos_multiple = -1
            radian_constant = 180 * DEGREES_TO_RADIANS
        elif self.waypoint_x < 0 and self.waypoint_y < 0:
            x_multiple = -1
            arccos_multiple = 1
            radian_constant = 180 * DEGREES_TO_RADIANS
        elif self.waypoint_x >= 0 and self.waypoint_y < 0:
            x_multiple = 1
            arccos_multiple = -1
            radian_constant = 360 * DEGREES_TO_RADIANS
        else:
            raise ValueError(
                f"Invalid waypoint location: {(self.waypoint_x, self.waypoint_y)}"
            )
        return (
            (
                radian_constant
                + arccos_multiple
                * np.arccos(x_multiple * self.waypoint_x / self.distance_to_waypoint)
            )
            * 1
            / DEGREES_TO_RADIANS
        )

    @property
    def distance_to_waypoint(self):
        return np.sqrt(self.waypoint_x ** 2 + self.waypoint_y ** 2)

    def manhattan_distance(self):
        return np.abs(self.x) + np.abs(self.y)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_txt_file", type=str)
    args = parser.parse_args()
    with open(args.input_txt_file, "r") as f:
        input_string = f.read()
    navigator = ShipNavigator(input_string)
    navigator.apply_instructions()
    print(navigator.x, navigator.y)
    print(navigator.manhattan_distance())
