import argparse
import numpy as np


class ShipNavigator:
    def __init__(self, instructions: str):
        self.instructions = instructions
        # start at coordinate (0, 0)
        self.x: float = 0
        self.y: float = 0
        # start facing east; i.e. with heading 0 degrees
        self.heading: float = 0

    def apply_instructions(self):
        for instruction in self.instructions.split("\n"):
            self.apply_instruction(instruction)

    def apply_instruction(self, instruction: str):
        action = instruction[0]
        value = float(instruction[1:])
        if action == "N":
            self.y += value
        elif action == "S":
            self.y -= value
        elif action == "E":
            self.x += value
        elif action == "W":
            self.x -= value
        elif action == "L":
            self.update_heading(value)
        elif action == "R":
            self.update_heading(-value)
        elif action == "F":
            x_increment, y_increment = self.decompose_forward_movement(value)
            self.x += x_increment
            self.y += y_increment
        else:
            raise ValueError(f"Invalid action: {action}")

    def update_heading(self, value: float):
        updated_heading = self.heading + value
        if updated_heading < 0:
            self.heading = 360 + updated_heading
        elif updated_heading >= 360:
            self.heading = updated_heading % 360
        else:
            self.heading = updated_heading

    def decompose_forward_movement(self, value: float):
        if 0 <= self.heading < 90:
            # if due east, x_increment = 1 * value * 1
            # and y_increment = 1 * value * 0
            reduced_heading = self.heading
            x_sign = 1
            y_sign = 1
        elif 90 <= self.heading < 180:
            # if due north, x_increment = -1 * value * 0
            # and y_increment = 1 * value * 1
            reduced_heading = 180 - self.heading
            x_sign = -1
            y_sign = 1
        elif 180 <= self.heading < 270:
            # if due west, x_increment = -1 * value * 1
            # and y_increment = -1 * value * 0
            reduced_heading = self.heading - 180
            x_sign = -1
            y_sign = -1
        elif 270 <= self.heading < 360:
            # if due south, x_increment = 1 * value * 0
            # and y_increment = -1 * value * 1
            reduced_heading = 360 - self.heading
            x_sign = 1
            y_sign = -1
        else:
            raise ValueError(f"Invalid heading: {self.heading}")
        reduced_heading_radians = (np.pi / 180) * reduced_heading
        x_increment = x_sign * value * np.cos(reduced_heading_radians)
        y_increment = y_sign * value * np.sin(reduced_heading_radians)
        return x_increment, y_increment

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
