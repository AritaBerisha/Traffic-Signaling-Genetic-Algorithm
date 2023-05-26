from algorithm import evaluate_solution, genetic_algorithm
from file_management import read_file, write_file

import csv
import os


def experiment(configuration_file):
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
    - Stores the output file path and score of the result for later use.

    After all rows in the CSV file have been processed, the function writes all output file paths and scores to a new 
    CSV file named 'resultA.csv'. The file contains one line per experiment, each line consisting of the original data 
    from the config CSV file, with the 'file_name' column replaced by the 'output_file' column, and a new 'score' column added.

    Args:
        None

    Returns:
        None
    """
    output_counter = {}
    csv_rows = []

    result_file_path = configuration_file.replace('config', 'results')

    with open(configuration_file, 'r') as config_file:
        csv_reader = csv.reader(config_file)
        headers = next(csv_reader)
        headers[0] = 'output_file'
        csv_rows.append(headers + ['score'])
        instance_counter = 1

        for row in csv_reader:
            print('Currently in session Instance ', instance_counter)
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
            score = evaluate_solution(input_data, result)

            # Replace input file name with output file name and append score to the row
            row[0] = output_filename
            row.append(score)
            csv_rows.append(row)
            instance_counter += 1

    # Write output file paths and scores to a new CSV file
    with open(result_file_path, 'w', newline='') as result_file:
        csv_writer = csv.writer(result_file)
        csv_writer.writerows(csv_rows)
