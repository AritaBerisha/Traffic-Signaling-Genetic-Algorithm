from representation import get_cars, get_streets


def read_file(fname="../data/input/fiek.in.txt"):
    """Read input from file

    Args:
        fname (str, optional): Input filename. Defaults to "../data/fiek.in.txt".

    Returns:
        Dict: Input data representation
    """
    with open(fname, "r+") as example_file:
        content = example_file.read().splitlines()

        duration, number_of_intersections, number_of_streets, number_of_cars, bonus = map(
            int, content[0].split())

        streets = get_streets(content, number_of_streets)
        cars = get_cars(content, streets, number_of_streets, number_of_cars)

        input_data = {
            'duration': duration,
            'number_of_intersections': number_of_intersections,
            'number_of_streets': number_of_streets,
            'number_of_cars': number_of_cars,
            'bonus': bonus,
            'streets': streets,
            'cars': cars
        }

    return input_data


def write_file(intersections, fname='../data/output/fiek.out.txt'):
    """Write solution to a file.

    Args:
        intersections (list): Solution list of intersections
        fname (str, optional): Output filename. Defaults to '../data/fiek.out.txt'.
    """
    with open(fname, 'w') as submission_file:
        intersections_done = 0
        for i in range(len(intersections)):
            sum_duration_per_intersection = sum(
                value['duration'] for value in intersections[i])
            if sum_duration_per_intersection > 0:
                intersections_done += 1

        submission_file.write(f'{intersections_done}\n')

        for i in range(len(intersections)):
            sum_duration = sum(value['duration'] for value in intersections[i])
            if sum_duration > 0:
                submission_file.write(f'{i}\n')
                sum_streets = sum(value['duration'] >
                                  0 for value in intersections[i])
                submission_file.write(f'{sum_streets}\n')
                for value in intersections[i]:
                    if value['duration'] > 0:
                        submission_file.write(
                            f"{value['street']} {value['duration']}\n")


def parse_submission_file(filename):
    """
    Parse the submission file for the Google Hash Code's Traffic Signaling Problem.

    Args:
    filename (str): The path to the submission file.

    Returns:
    list: A list where each index represents an intersection ID and each element is a list of dictionaries
    mapping street names to the duration the traffic light is green.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
    num_intersections = int(lines[0])
    intersections = [None] * num_intersections  # initialize list with None
    line_idx = 1
    while line_idx < len(lines):
        intersection_id = int(lines[line_idx])
        num_incoming = int(lines[line_idx+1])
        schedule = []
        for j in range(num_incoming):
            street, duration = lines[line_idx+2+j].strip().split()
            schedule.append({'street': street, 'duration': int(duration)})

        # Ensure our intersections list is long enough
        if intersection_id >= len(intersections):
            intersections.extend(
                [None] * (intersection_id - len(intersections) + 1))

        intersections[intersection_id] = schedule
        line_idx += 2 + num_incoming  # move to the next intersection

    # Fill skipped intersections with default values
    for i in range(len(intersections)):
        if intersections[i] is None:
            intersections[i] = [{'street': 'default', 'duration': 0}]

    return intersections
