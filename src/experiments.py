from algorithm import evaluate_solution, genetic_algorithm
from file_management import read_file, write_file

import csv
import os


def experiment():
    """
    Function to execute a series of genetic algorithm experiments based on a configuration CSV file. 

    This function reads the CSV file located at '../data/config/config.csv'. Each row in the file corresponds 
    to one experiment, specifying the parameters for the genetic algorithm and the input data file.

    The function performs the following steps for each row in the CSV file:
    - Reads the input data from the file specified in the first column.
    - Runs the genetic algorithm with this input data and the specified parameters.
    - Generates a corresponding output file path by replacing 'input' with 'output' in the input file path, and 
      replacing '.in.' with a counter number and '.out.' in the file name.
    - Writes the result of the genetic algorithm to this output file.
    - Stores the score of the result for later use.

    After all rows in the CSV file have been processed, the function writes all scores to a file located at 
    '../data/config/scores.txt'. The file contains one line per output file, each line consisting of the output 
    file path and the corresponding score.

    Args:
        None

    Returns:
        None
    """
    scores_dict = {}
    output_counter = {}

    with open('../data/config/config.csv', 'r') as config_file:
        csv_reader = csv.reader(config_file)
        next(csv_reader)  # Skip the header
        for row in csv_reader:
            input_file = row[0]
            parameters = (int(row[1]), int(row[2]), float(
                row[3]), float(row[4]), row[5] == 'True')

            if not os.path.exists(input_file):
                print(f"Input file {input_file} does not exist. Skipping...")
                continue

            input_data = read_file(input_file)
            result = genetic_algorithm(input_data, parameters)

            # Count how many outputs for this input file
            if input_file in output_counter:
                output_counter[input_file] += 1
            else:
                output_counter[input_file] = 1

            dirname = os.path.dirname(input_file)
            basename = os.path.basename(input_file)

            output_dirname = dirname.replace('input', 'output')
            output_basename = basename.replace(
                '.in.', str(output_counter[input_file]) + '.out.')

            output_filename = os.path.join(output_dirname, output_basename)

            write_file(result, output_filename)

            # Save score for each output file
            scores_dict[output_filename] = evaluate_solution(
                input_data, result)

    # Write scores to a file
    with open('../data/config/scores.txt', 'w') as scores_file:
        for output_file, score in scores_dict.items():
            scores_file.write(f"{output_file}: {score}\n")
