from typing import List, Dict, Set, Tuple, Optional
import warnings

class BingoCard:
    def __init__(self, number_matrix: List[List[int]]):
        self.validate_input(number_matrix)
        self.numbers = number_matrix[:]
        self.nrows = len(self.numbers)
        self.ncols = len(self.numbers[0])
        
        self._column_count = [0]*self.ncols
        self._row_count = [0]*self.nrows
        self._winner_flag = False

        self.number_location: Dict[int, Tuple[int, int]] = {}
        self.matched = [[False for _ in range(self.ncols)]for _ in range(self.nrows)]
        
        
        self._init_number_location()
        
    def _init_number_location(self):
        for i in range(self.nrows):
            for j in range(self.ncols):
                self.number_location[self.numbers[i][j]] = (i, j)
                
    def mark_number(self, number, raise_errors=True):
        position = self.number_location.get(number, None)
        if (position is None):
            if raise_errors:
                raise ValueError("Number not found in card")
            else:
                return
        if self.matched[position[0]][position[1]]:
            warnings.warn(f"Marking a repeated number {number}")
            return
        self.matched[position[0]][position[1]] = True
        
        self._column_count[position[1]] += 1
        self._row_count[position[0]] += 1
        self._check_winner_after_insertion(position)

        
    def _check_winner_after_insertion(self, position):
        if self._column_count[position[1]] == self.nrows:
            self._winner_flag = True
        if self._row_count[position[0]] == self.ncols:
            self._winner_flag = True
    
    @property
    def winner(self) -> bool:
        return self._winner_flag
        
        
        
    @staticmethod
    def validate_input(matrix):
        nrows = len(matrix)
        ncols = len(matrix[0])
        
        if nrows != ncols:
            warnings.warn("Unmatched number of rows and columns, check your input")
        
        for row in matrix:
            if len(row) != ncols:
                raise ValueError("Bingo Cards must have the same number of columns per row")
            
        numbers = sum(matrix, [])
        if len(numbers) != len(set(numbers)):
            raise ValueError("Numbers in each Bingo Card must be unique")

def part_one(path: str) -> int:
    numbers, bingo_data = parse_input(path)
    cards = [BingoCard(matrix) for matrix in bingo_data]
    winner_data = play_bingo(cards, numbers)
    if winner_data is None:
        raise RuntimeError("No Winner found")
    value = calc_points_winner(*winner_data)
    return value

def part_two(path: str) -> int:
    numbers, bingo_data = parse_input(path)
    cards = [BingoCard(matrix) for matrix in bingo_data]
    winner_data = loose_bingo(cards, numbers)
    if winner_data is None:
        raise RuntimeError("No Winner found")
    value = calc_points_winner(*winner_data)
    return value

def calc_points_winner(card: BingoCard, last_number: int) -> int:
    numbers_in_card = sum(card.numbers, [])
    matched_numbers = sum(card.matched, [])
    non_marked = sum(number for number, mark in zip(numbers_in_card, matched_numbers)
                     if not mark)
    return non_marked*last_number
    

def play_bingo(cards: List[BingoCard], number_list: List[int]) -> Optional[Tuple[BingoCard, int]]:
    # Create reverse index of numbers to cards
    reverse_index = create_reverse_index(cards)
    for number in number_list:
        for card in reverse_index.get(number, ()):
            card.mark_number(number)
            if card.winner:
                return card, number
    return None

def loose_bingo(cards: List[BingoCard], number_list: List[int]) -> Optional[Tuple[BingoCard, int]]:
    reverse_index = create_reverse_index(cards)
    winners: Set[BingoCard] = set()
    last_winner: Optional[BingoCard] = None
    last_number: Optional[int] = None
    for number in number_list:
        for card in reverse_index.get(number, ()):
            if card not in winners:
                card.mark_number(number)
                if card.winner:
                    winners.add(card)
                    last_number = number
                    last_winner = card
                
    if last_winner is None or last_number is None:
        return None
    return last_winner, last_number

def create_reverse_index(cards: List[BingoCard]) -> Dict[int, List[BingoCard]]:
    reverse_index: Dict[int, List[BingoCard]] = {}
    for card in cards:
        numbers = sum(card.numbers, [])
        for number in numbers:
            if number not in reverse_index:
                reverse_index[number] = []
            reverse_index[number].append(card)
    return reverse_index        
    
    
def parse_input(path: str) -> Tuple[List[int], List[List[List[int]]]]:
    with open(path) as file:
        numbers = [int(i) for i in next(file).split(",")]

        bingos = []
        for line in file:
            if not line.strip():
                bingos.append([])
                continue
            bingos[-1].append([int(i) for i in line.split()])
    return numbers, bingos

if __name__ == "__main__":
    out = part_one("day_4/input")
    print(out)
    out = part_two("day_4/input")
    print(out)