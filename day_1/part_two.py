from part_one import find_increases

def measure_window(data, window_size=3):
    npoints = len(data) - (window_size - 1)
    data_new = [0 for i in range(npoints)]
    for index, value in enumerate(data):
        for delta in range(window_size):
            if not ( 0 <= index - delta < npoints):
                continue
            data_new[index - delta] += value

    return data_new

if __name__ == "__main__":
    with open("day_1/part_one.dat") as filename:
        data = [int(i) for i in filename]
    data = measure_window(data)
    out = find_increases(data)
    print(out)