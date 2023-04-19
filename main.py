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
        f.write(f'{str(len(intersactions))}\n')
        for i in range(len(intersactions)):
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
                         1]['duration'] = cycle_time - sum_per_intersaction

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

def selection(input_data, population, elite_size):
    """Select the parents for crossover based on the fitness score.

    Args:
        input_data (Dict): Input data.
        population (List): List of solutions in the current population.
        elite_size (int): Number of solutions to select as elite.

    Returns:
        List: List of parent solutions.
    """
    fitness_scores = []
    for i in range(len(population)):
        score = evaluate_solution(input_data, population[i])
        fitness_scores.append((population[i], score))
    fitness_scores.sort(key=lambda x: x[1], reverse=True)

    elite = [x[0] for x in fitness_scores[:elite_size]]
    parents = [elite[i] for i in range(len(elite))]

    # Add non-elite parents through tournament selection
    while len(parents) < len(population):
        tournament = random.sample(population, 2)
        tournament_scores = [evaluate_solution(input_data, tournament[i])
                             for i in range(2)]
        winner = tournament[0] if tournament_scores[0] > tournament_scores[1] else tournament[1]
        parents.append(winner)

    return parents

def crossover(parents, number_of_intersactions):
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
        solution = [[] for _ in range(number_of_intersactions)]
        for j in range(number_of_intersactions):
            if j < len(parent1):
                for k in range(len(parent1[j])):
                    if random.uniform(0, 1) < 0.5:
                        solution[j].append(parent1[j][k])
                    else:
                        solution[j].append(parent2[j][k])
            else:
                solution.append(parent2[j])

        offspring.append(solution)

    return offspring

def mutate(solution, cars, streets):
    """Randomly change the order of streets a car passes in the given solution.

    Args:
        solution (List): List of intersactions and their assigned streets and durations.
        cars (List): List of cars with their paths.
        streets (Dict): Dictionary of street information.

    Returns:
        List: New solution after changing the order of streets a car passes.
    """
    # Select a random car
    car_idx = random.randint(0, len(cars)-1)
    car = cars[car_idx]

    # Select two random positions in the car's path (excluding the first and last streets)
    street_idx1 = random.randint(1, len(car['path'])-2)
    street_idx2 = random.randint(1, len(car['path'])-2)

    # Swap the two selected streets in the car's path
    street1 = car['path'][street_idx1]
    street2 = car['path'][street_idx2]
    if street1 in car['path'] and street2 in car['path']:
        car['path'][street_idx1], car['path'][street_idx2] = car['path'][street_idx2], car['path'][street_idx1]
    else:
        mutate()

    for i in range(len(solution)):
        for j in range(len(solution[i])):
            if solution[i][j]['street'] == car['path'][street_idx1]:
                solution[i][j]['street'] = car['path'][street_idx2]
            elif solution[i][j]['street'] == car['path'][street_idx2]:
                solution[i][j]['street'] = car['path'][street_idx1]

    return solution

def genetic_algorithm(input_data):
    """Runs the genetic algorithm to find a solution to the traffic signaling problem.
    Args: input_data (Dict): Input data.
    Returns:
        List: intersaction/Solution data
    """
    streets = input_data['streets']
    number_of_intersactions = input_data['number_of_intersactions']
    duration = input_data['duration']
    cycle_time = return_cycle_time(duration)
    print('Cycle in Seconds: ', cycle_time)

    population_size = 20
    elite_size = 5

    # Generate initial population
    population = []
    for i in range(population_size):
        solution = init_solution(streets, number_of_intersactions, cycle_time)
        population.append(solution)

    best_score = 0
    best_solution = None
    # Evolve the population
    for generation in range(20):
        # Select parents
        parents = selection(input_data, population, elite_size)

        # Generate offspring through crossover
        offspring = crossover(parents, number_of_intersactions)

        # Mutate offspring
        for i in range(len(offspring)): 
            for j in range(NUM_MUTATIONS):
                mutate(offspring[i], input_data['cars'], streets)

        # Add parents to offspring
        offspring.extend(parents)

        # Evaluate fitness of offspring
        fitness_scores = []
        for i in range(len(offspring)):
            score = evaluate_solution(input_data, offspring[i])
            fitness_scores.append((offspring[i], score))
        fitness_scores.sort(key=lambda x: x[1], reverse=True)

        # Select the best solutions as the next generation
        population = [x[0] for x in fitness_scores[:population_size]]

        # Print the fitness score of the best solution in this generation
        best_fitness_score = fitness_scores[0][1]
        print('Generation {}: Fitness score of the best solution = {}'.format(
            generation+1, best_fitness_score))
        
        if fitness_scores[0][1] >= best_score:
            best_score = fitness_scores[0][1]
            best_solution = fitness_scores[0][0]
    
    # Return the best solution in the final population
    return best_solution

def main():
    input_data = read_file()
    best_solution = genetic_algorithm(input_data)

    print('Validation: ')
    print(validate_solution(best_solution, input_data['duration'], return_cycle_time(input_data['duration'])))
    write_file(best_solution)

if __name__ == '__main__':
    main()