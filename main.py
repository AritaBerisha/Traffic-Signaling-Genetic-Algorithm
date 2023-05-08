import random

# Genetic Algorithm Parameters
POPULATION_SIZE = 10
NUM_GENERATIONS = 5
NUM_MUTATIONS = 3


def return_cycle_time(duration):
    """Given the simulation duration come up with a divisible cycle time

    Args:
        duration (int): simulation duration

    Returns:
        int: Cycle time in seconds
    """
    divisors = []
    for i in range(1, duration+1):
        if duration % i == 0:
            divisors.append(i)
    choose = random.randint(0, len(divisors)-1)
    cycle_time = divisors[choose]
    return cycle_time


def write_file(intersactions, fname='fiek.out.txt'):
    """Write solution in file.

    Args:
        intersactions (List): Solution
        fname (str, optional): Output filename. Defaults to 'fiek.out.txt'.
    """
    with open(fname, 'w') as f:
        intersaction_done = 0
        for i in range(len(intersactions)):
            sum_duration_per_intersaction = 0
            for value in intersactions[i]:
                sum_duration_per_intersaction += value['duration']
            if sum_duration_per_intersaction > 0:
                intersaction_done += 1
        f.write(f'{str((intersaction_done))}\n')
        for i in range(len(intersactions)):
            sum_duration = 0
            for value in intersactions[i]:
                sum_duration += value['duration']
            if sum_duration > 0:
                f.write(f'{str(i)}\n')
                sum_streets = 0
                for value in intersactions[i]:
                    if value['duration'] > 0:
                        sum_streets += 1
                f.write(f'{str(sum_streets)}\n')
                for value in intersactions[i]:
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
                         1]['duration'] = cycle_time - sum_per_intersaction if cycle_time - sum_per_intersaction > 0 else 0

    return intersactions


def evaluate_solution(input_data, solution):
    """Evaluate solution
    Args:
        input_data (Dict): Input data
        solution (List): Solution

    Returns:
        float: Solution score
    """
    bonus = input_data['bonus']
    streets = input_data['streets']
    cars = input_data['cars']
    duration = input_data['duration']

    # calculate how many times a street is used
    usage = {key: 0 for key in streets}
    for car in cars:
        for street in car['path']:
            usage[street] += 1

    # calculate the total waiting time
    total_waiting_time = 0
    for car in cars:
        time_left = duration
        for street in car['path']:
            time_left -= streets[street]['length']
            if time_left < 0:
                time_left = 0
            else:
                total_waiting_time += solution[streets[street]['end']][next((index for index, item in enumerate(
                    solution[streets[street]['end']]) if item['street'] == street), 0)]['duration']

    # if the total waiting time is greater than or equal to the duration of the simulation, return a score of zero
    if total_waiting_time >= duration:
        return 0

    # calculate the solution score
    score = bonus * len(cars) + (duration - total_waiting_time)

    return score


def validate_solution(intersactions, total_duration, cycle_time):
    """Validate Given Solution
    Args:
        intersactions (List): Intersaction List
        total_duration (int): Total duration of simulation in seconds
        cycle_time (int): Duration per cycle in seconds

    Returns:
        str: Message
    """
    total_sum = 0
    for i in range(len(intersactions)):
        sum_of_points = 0
        for street in intersactions[i]:
            sum_of_points += street['duration']
        if sum_of_points > cycle_time:
            print(sum_of_points)
            print(cycle_time)
            return 'Duration per cycle for intersaction {} exceeded time.'.format(i)
    for i in range(int(total_duration/cycle_time)):
        sum_of_points = 0
        for i in range(len(intersactions)):
            sum_of_points = 0
            for street in intersactions[i]:
                sum_of_points += street['duration']
        total_sum += sum_of_points
    if total_sum > total_duration:
        print(total_duration)
        print(total_sum)
        return 'Total Duration of simulation exceeded time.'
    else:
        return 'Solution is Valid.'


# def selection(input_data, population, elite_size):
#     """Select the parents for crossover based on the fitness score.

#     Args:
#         input_data (Dict): Input data.
#         population (List): List of solutions in the current population.
#         elite_size (int): Number of solutions to select as elite.

#     Returns:
#         List: List of parent solutions.
#     """
#     fitness_scores = []
#     for i in range(len(population)):
#         score = evaluate_solution(input_data, population[i])
#         fitness_scores.append((population[i], score))
#     fitness_scores.sort(key=lambda x: x[1], reverse=True)

#     elite = [x[0] for x in fitness_scores[:elite_size]]
#     parents = [elite[i] for i in range(len(elite))]

#     # Add non-elite parents through tournament selection
#     while len(parents) < len(population):
#         tournament = random.sample(population, 2)
#         tournament_scores = [evaluate_solution(input_data, tournament[i])
#                              for i in range(2)]
#         winner = tournament[0] if tournament_scores[0] > tournament_scores[1] else tournament[1]
#         parents.append(winner)

#     return parents


def crossover(parents):
    """Generate offspring from the selected parents through crossover.

    Args:
        parents (List): List of parent solutions.
        number_of_intersactions (int): Number of intersactions.

    Returns:
        List: List of offspring solutions.
    """
    offspring = []
    offspring_size = len(parents)
    for i in range(offspring_size):
        parent1_index = i % len(parents)
        parent2_index = (i+1) % len(parents)
        parent1 = parents[parent1_index]
        parent2 = parents[parent2_index]
        # Uniform crossover
        solution = [[] for _ in range(len(parent1))]
        for j in range(len(parent1)):
            for k in range(len(parent1[j])):
                if random.uniform(0, 1) < 0.5:
                    solution[j].append(parent1[j][k])
                else:
                    solution[j].append(parent2[j][k])

        offspring.append(solution)

    return offspring


def select_with_replacement(input_data, population):
    population_fitnesses = [evaluate_solution(input_data,
                                              solution) for solution in population]

    for i in range(1, len(population_fitnesses)):
        population_fitnesses[i] = population_fitnesses[i] + \
            population_fitnesses[i-1]

    random_number = random.randint(
        population_fitnesses[0], population_fitnesses[-1])
    for i in range(1, len(population_fitnesses)):
        if population_fitnesses[i-1] <= random_number and random_number <= population_fitnesses[i]:
            return population[i]


def mutate(solution):
    probability = 0.5
    for i in range(len(solution)):
        for j in range(1, len(solution[i])):
            # random_probability = random.uniform(0, 1)
            # if probability > random_probability:
            solution[i][j]['duration'], solution[i][j -
                                                    1]['duration'] = solution[i][j-1]['duration'], solution[i][j]['duration']

    return solution


def genetic_algorithm(input_data, cycle_time):
    """Runs the genetic algorithm to find a solution to the traffic signaling problem.
    Args: input_data (Dict): Input data.
    Returns:
        List: intersaction/Solution data
    """
    streets = input_data['streets']
    number_of_intersactions = input_data['number_of_intersactions']
    print('Cycle in Seconds: ', cycle_time)

    population_size = 20
    population = []
    for i in range(population_size):
        solution = init_solution(
            streets, number_of_intersactions, cycle_time)
        population.append(solution)
    best_solution = population[0]
    print('Initial Solution:', evaluate_solution(input_data, best_solution))

    fitness_scores = [[] for i in range(20)]

    for generation in range(20):
        for solution in population:
            if evaluate_solution(input_data, solution) > evaluate_solution(input_data, best_solution):
                best_solution = solution

        new_population = []
        for i in range(int(population_size)):
            parentA = select_with_replacement(input_data, population)
            parentB = select_with_replacement(input_data, population)
            childA, childB = crossover([parentA, parentB])  # rate
            childA = mutate(childA)  # rate
            childB = mutate(childB)
            new_population.append(childA)
            new_population.append(childB)

        for i in range(len(new_population)):
            score = evaluate_solution(input_data, new_population[i])
            fitness_scores[generation].append((new_population[i], score))
        fitness_scores[generation].sort(key=lambda x: x[1], reverse=True)
        # Select the best solutions as the next generation
        population = [x[0]
                      for x in fitness_scores[generation][:population_size]]

        # Print the fitness score of the best solution in this generation

        best_fitness_score = fitness_scores[generation][0][1]

        print('Generation {}: Fitness score of the best solution = {}'.format(
            generation + 1, best_fitness_score))

        if evaluate_solution(input_data, best_solution) < fitness_scores[generation][0][1]:
            best_solution = fitness_scores[generation][0][0]

    print(evaluate_solution(input_data, best_solution))
    return best_solution


def main():
    input_data = read_file()
    cycle_time = return_cycle_time(input_data['duration'])
    best_solution = genetic_algorithm(input_data, cycle_time)
    print('Validation: ')
    print(validate_solution(best_solution,
          input_data['duration'], cycle_time))
    write_file(best_solution)
    # print(validate_solution(intersactions, input_data['duration'], cycle_time))
    # print('Evaluation: ')
    # print(evaluate_solution(input_data, intersactions))
    # write_file(intersactions)


if __name__ == '__main__':
    main()
