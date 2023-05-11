from file_management import read_file, write_file
from helper import get_output_filename
from algorithm import genetic_algorithm
from validation import validate_solution
from terminal import read_terminal


def main():
    parameters = read_terminal()
    file_name = parameters[-1]
    input_data = read_file(file_name)

    best_solution = genetic_algorithm(input_data, parameters[:6])
    print('Validation: ')
    print(validate_solution(best_solution,
          input_data['duration']))
    write_file(best_solution, get_output_filename(file_name))


if __name__ == '__main__':
    main()
