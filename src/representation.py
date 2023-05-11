def get_streets(lines, number_of_streets):
    """Given input data, get streets.

    Args:
        lines (list): List of lines containing street data
        number_of_streets (int): Number of streets

    Returns:
        dict: Street information with street name as key and length, start, end as values
    """
    streets = {}
    for line in lines[1: number_of_streets + 1]:
        start, end, name, length = line.split(' ')
        streets[name] = {'length': int(
            length), 'start': int(start), 'end': int(end)}
    return streets


def get_cars(lines, streets, number_of_streets, number_of_cars):
    """Given input data, get cars.

    Args:
        lines (list): List of lines containing car data
        streets (dict): Street information
        number_of_streets (int): Number of streets
        number_of_cars (int): Number of cars

    Returns:
        list: List of car information data
    """
    cars = [[] for _ in range(number_of_cars)]
    number = 0
    for line in lines[number_of_streets + 1: number_of_streets + 1 + number_of_cars]:
        path = [street for street in line.split(' ')[1:]]
        cars[number] = {
            'path': path,
            'current': path[0],
            'left_in_current': streets[path[0]]['length'],
            'final': path[-1]
        }
        number += 1
    return cars
