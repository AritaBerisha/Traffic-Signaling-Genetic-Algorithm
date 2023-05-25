from file_management import read_file, write_file, parse_submission_file
from helper import get_output_filename
from algorithm import genetic_algorithm, evaluate_solution
from validation import validate_solution
from terminal import read_terminal
from experiments import experiment


def main():
    parameters = read_terminal()
    file_name = parameters[-1]
    input_data = read_file(file_name)

    best_solution = genetic_algorithm(input_data, parameters[:6])
    write_file(best_solution, get_output_filename(file_name))


if __name__ == '__main__':
    submission_result = parse_submission_file('../data/output/fiek1.out.txt')
    input_data = read_file('../data/input/fiek.in.txt')
    submission_score = evaluate_solution(input_data, submission_result)
    print('Score: ', submission_score)
    # experiment()
    # main()
