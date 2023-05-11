
import os
import random


def return_cycle_time(duration):
    """Given the simulation duration come up with a divisible cycle time

    Args:
        duration (int): simulation duration

    Returns:
        int: Cycle time in seconds
    """
    divisors = []
    for i in range(1, duration + 1):
        if duration % i == 0:
            divisors.append(i)
    choose = random.randint(0, len(divisors) - 1)
    cycle_time = divisors[choose]
    return cycle_time


def get_output_filename(input_filename):
    """Get the output file name based on the input file name.

    Args:
        input_filename (str): Input file name.

    Returns:
        str: Output file name.
    """
    dirname = os.path.dirname(input_filename)
    basename = os.path.basename(input_filename)

    output_dirname = dirname.replace('input', 'output')
    output_basename = basename.replace('.in.', '.out.')

    output_filename = os.path.join(output_dirname, output_basename)

    return output_filename
