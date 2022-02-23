def find_increases(vector):
    previous = vector[0]
    count = 0
    for item in vector[1:]:
        if item > previous:
            count += 1
        previous = item
    return count

if __name__ == "__main__":
    with open("day_1/part_one.dat") as filename:
        data = [int(i) for i in filename]
    
    print(find_increases(data))