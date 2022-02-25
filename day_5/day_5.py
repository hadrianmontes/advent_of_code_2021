from enum import Enum
from typing import Dict, List, Tuple

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

class Segment:
    class Direction(Enum):
        Horizontal = (1, 0)
        Vertical = (0, 1)
        DiagonalUp = (1, 1)
        DiagonalDown = (1, -1)
        
        @classmethod
        def find_direction_from_delta(cls, delta):
            if delta == (1, 0):
                return cls.Horizontal
            elif delta == (0, 1):
                return cls.Vertical
            elif delta == (1, 1):
                return cls.DiagonalUp
            elif delta == (1, -1):
                return cls.DiagonalDown
            else:
                raise ValueError(f"Unknown direction {delta}") 
            
    
    def __init__(self, point_1: Tuple[int, int], point_2: Tuple[int, int]):
        self.start, self.end = sorted([point_1, point_2])
        
        delta = (sign(self.end[0]-self.start[0]), sign(self.end[1]-self.start[1]))
        self.direction = self.Direction.find_direction_from_delta(delta)
        self.npoints = max((abs(self.end[0]-self.start[0]), abs(self.end[1]-self.start[1])))
        
        self.points: List[Tuple[int, int]] = []
        self._calculate_points()
        
    def _calculate_points(self):
        current_point = self.start
        self.points = [self.start]
        
        for _ in range(self.npoints):
            current_point = (current_point[0] + self.direction.value[0],
                             current_point[1] + self.direction.value[1])
            self.points.append(current_point)
        if current_point != self.end:
            raise ValueError("Cannot reach end point with specified direction")  
    @property
    def is_diagonal(self) -> bool:
        return self.direction in (self.direction.DiagonalUp, self.direction.DiagonalDown)
        
def parse_input(filename: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:               
    points = []
    with open(filename) as file:
        for line in file:
            start, end = line.strip().split("->")
            start_point = tuple(int(i) for i in start.split(","))
            end_point = tuple(int(i) for i in end.split(","))
            points.append((start_point, end_point))
    return points

def part_one(filename: str):
    lines = parse_input(filename)
    segments = [Segment(*edges) for edges in lines]
    
    segments = [segment for segment in segments if not segment.is_diagonal]
    
    points: List[Tuple[int, int]] = sum((segment.points for segment in segments), [])
    counter: Dict[Tuple[int, int], int] = {}
    for point in points:
        if point not in counter:
            counter[point] = 0
        counter[point] += 1
    return sum(1 for count in counter.values() if count > 1)

def part_two(filename: str):
    lines = parse_input(filename)
    segments = [Segment(*edges) for edges in lines]
    
    points: List[Tuple[int, int]] = sum((segment.points for segment in segments), [])
    counter: Dict[Tuple[int, int], int] = {}
    for point in points:
        if point not in counter:
            counter[point] = 0
        counter[point] += 1
    return sum(1 for count in counter.values() if count > 1)


if __name__ == "__main__":
    out = part_one("day_5/input")
    print(out)
    out = part_two("day_5/input")
    print(out)