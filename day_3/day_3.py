from typing import Optional, List


def part_one(filename) -> int:
    input_data = parse_input(filename)
    nbits = len(input_data[0])
    more_commom_bit = find_more_commom_bit(input_data)

    answer = []
    for bit in more_commom_bit:
        if bit == 1:
            answer.append("1")
        elif bit == 0:
            answer.append("0")
        else:
            raise ValueError("Same number of 1 and 0 found")
    gamma = int("".join(answer), base=2)
    epsilon = (2**nbits - 1) ^ gamma
    return epsilon*gamma

def part_two(filename: str) ->int:
    input_data = parse_input(filename)
    nbits = len(input_data[0])
    oxygen = input_data[:]
    co2 = input_data[:]
    for bit_index in range(nbits):
        if len(oxygen) > 1:
            most_common_ox = find_more_commom_bit(oxygen)[bit_index]
            most_common_ox = str(most_common_ox) if most_common_ox is not None else "1"
            oxygen = [bitline for bitline in oxygen if bitline[bit_index] == most_common_ox]
        
        if len(co2) > 1:
            most_common_co2 = find_more_commom_bit(co2)[bit_index]
            most_common_co2 = str(most_common_co2) if most_common_co2 is not None else "1"
            co2 = [bitline for bitline in co2 if bitline[bit_index] != most_common_co2]
    assert len(co2) == 1
    assert len(oxygen) == 1
    co2_num = int(co2[0], base=2)
    oxygen_num = int(oxygen[0], base=2)
    return co2_num*oxygen_num

def find_more_commom_bit(bit_lines: List[str]) -> List[Optional[bool]]:
    bit_counter = [0] * len(bit_lines[0])
    for bitline in bit_lines:
        for index, bit in enumerate(bitline):
            if bit == "1":
                bit_counter[index] += 1
            elif bit == "0":
                bit_counter[index] -= 1
            else:
                raise ValueError(f"Unknown bit specification {bit}")
    more_commom = []
    for bit in bit_counter:
        if bit > 0:
            more_commom.append(1)
        elif bit < 0:
            more_commom.append(0)
        else:
            more_commom.append(None)
    return more_commom
def parse_input(filename):
    with open(filename) as file:
        info = [line.strip() for line in file]
    return info

if __name__ == "__main__":
    out = part_one("day_3/input")
    print(out)
    
    out = part_two("day_3/input")
    print(out)