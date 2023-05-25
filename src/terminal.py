import argparse
import csv

from experiments import experiment


def read_csv():
    """Read the parameter values from a CSV file.

    Returns:
        dict: A dictionary containing the parameter values read from the CSV file. MOMENTARILY ONLY RETURNS THE FIRST ROW.
    """
    with open('../data/config/config.csv', 'r') as file:
        reader = csv.DictReader(file)
        parameters = next(reader)
        return parameters


def read_terminal():
    """Read command-line arguments or parameters using argparse.

    Returns:
        tuple: A tuple containing the extracted values in the following order:
            - population_size (int): Population size
            - num_mutations (int): Number of mutations
            - mutation_rate (float): Mutation rate
            - inversion_rate (float): Inversion rate
            - tournament (bool): Flag indicating whether tournament is enabled
            - file_name (str): Input file name
    """
    parser = argparse.ArgumentParser(
        description='Process command-line arguments or parameters.')

    # Add arguments
    parser.add_argument(
        '--mode', choices=['experimental', 'standard'], default='standard', help='Execution mode')

    # Standard mode arguments
    parser.add_argument('--population_size', type=int,
                        default=0, help='Population size')
    parser.add_argument('--num_mutations', type=int,
                        default=0, help='Number of mutations')
    parser.add_argument('--mutation_rate', type=float,
                        default=0.0, help='Mutation rate')
    parser.add_argument('--inversion_rate', type=float,
                        default=0.0, help='Inversion rate')
    parser.add_argument('--tournament', action='store_true',
                        help='Enable tournament')
    parser.add_argument('--file_name', type=str,
                        default='', help='Input file name')
    parser.add_argument('--config', type=str,
                        default='', help='Config file name')

    args = parser.parse_args()

    mode = args.mode

    if mode == 'standard':
        population_size = args.population_size
        num_mutations = args.num_mutations
        mutation_rate = args.mutation_rate
        inversion_rate = args.inversion_rate
        file_name = args.file_name
        tournament = args.tournament

        if not population_size:
            parser.error(
                "Population Size should be set.")

        if not num_mutations:
            parser.error('Number of Mutations should be set.')

        if not mutation_rate:
            parser.error('Mutation Rate should be set.')

        if not inversion_rate:
            parser.error('Inversion Rate should be set.')

        if not file_name:
            parser.error('File Name should be set.')

        print("Population Size:", population_size)
        print("Number of Mutations:", num_mutations)
        print("Mutation Rate:", mutation_rate)
        print("Inversion Rate:", inversion_rate)
        print("File Name:", file_name)
        print("Tournament:", tournament)

        return population_size, num_mutations, mutation_rate, inversion_rate, tournament, file_name

    elif mode == 'experimental':
        print("Execution Mode: Standard")
        experiment(args.config)
        return 'experimental'

    else:
        parser.error(
            "Invalid mode. Supported modes are 'experimental' and 'standard'.")
