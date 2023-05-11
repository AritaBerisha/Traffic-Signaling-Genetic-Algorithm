def validate_solution(intersections, total_duration):
    """Validate Given Solution

    Args:
        intersections (list): Intersection list
        total_duration (int): Total duration of simulation in seconds
        cycle_time (int): Duration per cycle in seconds

    Returns:
        str: Validation message
    """
    total_sum = sum(sum(street['duration'] for street in intersection)
                    for intersection in intersections)
    if total_sum > total_duration:
        return "Total duration of simulation exceeded the limit."
    else:
        return "Solution is valid."
