from typing import Tuple, List
from dataclasses import dataclass

from setuptools import Command

@dataclass
class Coordinates():
    depth: int
    horizontal: int
    
@dataclass
class AimedCoordinates(Coordinates):
    aim: int
    
    
@dataclass
class Action():
    command: str
    time: int

def part_one(inputfile: str)-> Coordinates:
    actions = read_commands(inputfile)
    position = Coordinates(depth=0, horizontal=0)
    for action in actions:
        perform_action(action, position)
    return position

def part_two(inputfile: str)-> Coordinates:
    actions = read_commands(inputfile)
    position = AimedCoordinates(depth=0, horizontal=0, aim=0)
    for action in actions:
        perform_action_part_2(action, position)
    return position

def perform_action(action: Action, coordinates: Coordinates):
    if action.command == "down":
        coordinates.depth += action.time
    elif action.command == "up":
        coordinates.depth -= action.time
    elif action.command == "forward":
        coordinates.horizontal += action.time
    else:
        raise ValueError(f"Invalid command {action.command}")
    
def perform_action_part_2(action: Action, coordinates: AimedCoordinates):
    if action.command == "down":
        coordinates.aim += action.time
    elif action.command == "up":
        coordinates.aim -= action.time
    elif action.command == "forward":
        coordinates.horizontal += action.time
        coordinates.depth += action.time * coordinates.aim
    else:
        raise ValueError(f"Invalid command {action.command}")

def read_commands(inputfile: str) -> List[Action]:
    out = []
    with open(inputfile) as file:
        for line in file:
            info = line.split()
            out.append(Action(command=info[0], time=int(info[1])))
    return out



if __name__ == "__main__":
    coordinates = part_one("day_2/input")
    print(coordinates)
    print(coordinates.depth * coordinates.horizontal)
    
    coordinates = part_two("day_2/input")
    print(coordinates)
    print(coordinates.depth * coordinates.horizontal)