import random


def return_cycle_time(duration, min=10, max=120):
    """Given the simulation duration come up with a divisible cycle time

    Args:
        duration (int): simulation duration
        min (int, optional): Minimum cycle time. Defaults to 10.
        max (int, optional): Maximim cycle time. Defaults to 120.

    Returns:
        int: Cycle time in seconds
    """
    divisors = []
    for i in range(min, max+1):
        if duration % i == 0:
            divisors.append(i)
    choose = random.randint(0, len(divisors)-1)
    cycle_time = divisors[choose]
    return cycle_time


def write_file(intersections, fname='fiek.out.txt'):
    """Write solution in file.

    Args:
        intersections (List): Solution
        fname (str, optional): Output filename. Defaults to 'fiek.out.txt'.
    """
    with open(fname, 'w') as f:
        f.write(f'{str(len(intersections))}\n')
        for i in range(len(intersections)):
            f.write(f'{str(i)}\n')
            sum_streets = 0
            for value in intersections[i]:
                if value['duration'] > 0:
                    sum_streets += 1
            f.write(f'{str(sum_streets)}\n')
            for value in intersections[i]:
                if value['duration'] > 0:
                    f.write(
                        f"{str(value['street'])} {str(value['duration'])}\n")


def read_file(fname="fiek.in.txt"):
    """Read input from file

    Args:
        fname (str, optional): Input filename. Defaults to "fiek.in.txt".

    Returns:
        Dict: Input data representation
    """
    with open(fname, "r+") as example_file:
        file = example_file.read()
        first_line = file.split('\n')[0].split(' ')
        duration, number_of_intersactions, number_of_streets, number_of_cars, bonus = list(
            map(int, first_line))
        streets = get_streets(file, number_of_streets)
        cars = get_cars(file, streets, number_of_streets, number_of_cars)
        example_file.close()
        input_data = {
            'duration': duration,
            'number_of_intersactions': number_of_intersactions,
            'number_of_streets': number_of_streets,
            'number_of_cars': number_of_cars,
            'bonus': bonus,
            'streets': streets,
            'cars': cars
        }
        return input_data


def get_streets(file, number_of_streets):
    """Given input data get streets.

    Args:
        file (file): File
        number_of_streets (int): Number of streets

    Returns:
        Dict: Key: street name, Value: length, start, end
    """
    streets = {}
    for line in file.split('\n')[1: number_of_streets + 1]:
        start, end, name, length = line.split(' ')
        streets[name] = {'length': int(
            length), 'start': int(start), 'end': int(end)}
    return streets


def get_cars(file, streets, number_of_streets, number_of_cars):
    """Given input data get cars.

    Args:
        file (file): file
        streets (Dict): Street object
        number_of_streets (int): Number of streets
        number_of_cars (int): Number of cars

    Returns:
        List: List of car information data
    """
    cars = [[] for car in range(number_of_cars)]
    number = 0
    for line in file.split('\n')[number_of_streets+1: number_of_streets + 1 + number_of_cars]:
        path = [street for street in line.split(' ')[1:]]
        cars[number] = {
            'path': path,
            'current': path[0],
            'left_in_current': streets[path[0]]['length'],
            'final': path[-1]
        }
        number += 1
    return cars


def init_solution(streets, number_of_intersactions, cycle_time):
    """Get initial solution

    Args:
        streets (Dict): Street object
        number_of_intersactions (int): Number of intersactions  
        cycle_time (int): Cycle time in seconds

    Returns:
        List: Intersaction/Solution data
    """
    intersactions = [[] for _ in range(number_of_intersactions)]
    for i in range(0, len(intersactions)):
        # How much of the time has been allocated per intersaction
        sum_per_intersaction = 0
        for key, value in streets.items():
            # How much of the time has been allocated per intersaction up until the particular street
            sum_per_street = 0
            if value['end'] == i:
                exists = False
                for j in range(0, len(intersactions[i])):
                    exists = True if intersactions[i][j]['street'] == key else False
                    sum_per_street += intersactions[i][j]['duration']
                if not exists:
                    # Allocate random time based on how much time is left
                    duration1 = random.randint(
                        0, cycle_time - sum_per_street)
                    intersactions[i].append({
                        'street': key,
                        'duration': duration1
                    })
            sum_per_intersaction += sum_per_street
        # If any time has been left allocate all the time left to the last street in the intersaction
        intersactions[i][len(intersactions[i]) -
                         1]['duration'] = cycle_time - sum_per_intersaction

    return intersactions


def main():
    input_data = read_file()
    streets = input_data['streets']
    number_of_intersactions = input_data['number_of_intersactions']
    cycle_time = return_cycle_time(input_data['duration'])
    print('Cycle in Seconds: ', cycle_time)

    intersactions = init_solution(
        streets, number_of_intersactions, cycle_time)
    print(intersactions)
    write_file(intersactions)


if __name__ == '__main__':
    main()
