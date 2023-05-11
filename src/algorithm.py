import copy
import random
from helper import return_cycle_time


def init_solution(streets, number_of_intersections, duration):
    """Get initial solution

    Args:
        streets (dict): Street object
        number_of_intersections (int): Number of intersections
        duration (int): Duration of simulation

    Returns:
        list: Intersection/solution data
    """
    intersections = [[] for _ in range(number_of_intersections)]
    for i in range(0, len(intersections)):
        cycle_time = return_cycle_time(duration)
        # How much of the time has been allocated per intersection
        sum_per_intersection = 0
        for key, value in streets.items():
            # How much of the time has been allocated per intersection up until the particular street
            sum_per_street = 0
            if value['end'] == i:
                exists = False
                for j in range(0, len(intersections[i])):
                    exists = True if intersections[i][j]['street'] == key else False
                    sum_per_street += intersections[i][j]['duration']

                if not exists:
                    # Allocate random time based on how much time is left
                    duration_per_street = random.randint(
                        0, cycle_time - sum_per_street)
                    intersections[i].append({
                        'street': key,
                        'duration': duration_per_street
                    })
            sum_per_intersection += sum_per_street

        # If any time has been left allocate all the time left to the last street in the intersection
        intersections[i][-1]['duration'] = max(
            cycle_time - sum_per_intersection, 0)

    return intersections


def evaluate_solution(input_data, solution):
    """Evaluate solution.

    Args:
        input_data (Dict): Input data.
        solution (List): Solution.

    Returns:
        float: Solution score.
    """
    bonus = input_data['bonus']
    streets = input_data['streets']
    cars = input_data['cars']
    duration = input_data['duration']

    # Calculate how many times a street is used
    usage = {street: 0 for street in streets}
    for car in cars:
        for street in car['path']:
            usage[street] += 1

    # Calculate the total waiting time
    total_waiting_time = 0
    for car in cars:
        time_left = duration
        for street in car['path']:
            time_left -= streets[street]['length']
            if time_left < 0:
                time_left = 0
            else:
                intersection = solution[streets[street]['end']]
                street_duration = next(
                    (street['duration'] for street in intersection if street['street'] == street), 0)
                total_waiting_time += street_duration

    # If the total waiting time is greater than or equal to the duration of the simulation, return a score of zero
    if total_waiting_time >= duration:
        return 0

    # Calculate the solution score
    score = bonus * len(cars) + (duration - total_waiting_time)

    return score


def evaluate_solution_delta(input_data, old_solution, new_solution, old_score, mutated_intersection):
    """Evaluate solution using delta evaluation method

    Args:
        input_data (Dict): Input data
        old_solution (List): Old Solution
        new_solution (List): New Solution
        old_score (float): Old solution score
        mutated_intersection (int): The mutated intersection index

    Returns:
        float: New solution score
    """
    streets = input_data['streets']
    cars = input_data['cars']
    duration = input_data['duration']

    # calculate how many times a street is used
    usage = {key: 0 for key in streets}
    for car in cars:
        for street in car['path']:
            usage[street] += 1

    # calculate the total waiting time
    total_waiting_time_diff = 0
    for car in cars:
        time_left = duration
        for street in car['path']:
            time_left -= streets[street]['length']
            if time_left < 0:
                time_left = 0
            else:
                intersection = streets[street]['end']
                if intersection == mutated_intersection:
                    old_duration = old_solution[intersection][next((index for index, item in enumerate(
                        old_solution[intersection]) if item['street'] == street), 0)]['duration']
                    new_duration = new_solution[intersection][next((index for index, item in enumerate(
                        new_solution[intersection]) if item['street'] == street), 0)]['duration']
                    total_waiting_time_diff += new_duration - old_duration

    new_score = old_score - total_waiting_time_diff

    return new_score


def crossover(parents):
    """Generate offspring from the selected parents through crossover.

    Args:
        parents (List): List of parent solutions.

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
    """Select an individual from the population using fitness-proportionate selection with replacement.

    Args:
        input_data: Input data for evaluating the solutions.
        population: List of solutions.

    Returns:
        The selected solution.
    """
    population_fitnesses = [evaluate_solution(input_data,
                                              solution) for solution in population]

    for i in range(1, len(population_fitnesses)):
        population_fitnesses[i] = population_fitnesses[i] + \
            population_fitnesses[i - 1]

    random_number = random.randint(
        population_fitnesses[0], population_fitnesses[-1])
    for i in range(1, len(population_fitnesses)):
        if population_fitnesses[i - 1] <= random_number and random_number <= population_fitnesses[i]:
            return population[i]


def mutate_street_duration(solution, mutated_intersections):
    """Mutate the street duration within the intersections.

    Args:
        solution (List): The solution containing intersections.
        mutated_intersections (List): List to track mutated intersection indices.

    Returns:
        Tuple: The mutated solution and the updated list of mutated intersection indices.
    """
    intersection_index = random.randint(0, len(solution) - 1)
    for _ in range(len(solution[intersection_index]) - 1):
        street_index = random.randint(
            0, len(solution[intersection_index]) - 1)
        # Avoid swapping the first street's duration with itself
        if street_index != 0:
            solution[intersection_index][street_index]['duration'], \
                solution[intersection_index][street_index - 1]['duration'] = \
                solution[intersection_index][street_index - 1]['duration'], \
                solution[intersection_index][street_index]['duration']
            if intersection_index not in mutated_intersections:
                mutated_intersections.append(intersection_index)
    return solution, mutated_intersections


def mutate(solution, num_mutations):
    """Mutate the solution by swapping the durations of random intersections.

    Args:
        solution: The solution to be mutated.
        num_mutations: The number of mutations to be applied.

    Returns:
        Tuple containing the mutated solution and the list of mutated intersections.

    """
    mutated_intersections = []

    for _ in range(num_mutations):
        solution, mutated_intersections = mutate_street_duration(
            solution, mutated_intersections)

        # solution, mutated_intersections = mutate_intersection_duration(
        #     solution, mutated_intersections)

    return solution, mutated_intersections


def inversion(solution):
    """Apply inversion operator to the solution.

    The inversion operator randomly selects a range of streets within each intersection
    and reverses their order, introducing diversity to the solution.

    Args:
        solution (List): The solution to apply the inversion operator to.

    Returns:
        List: The solution after applying the inversion operation.
    """
    for i in range(len(solution)):
        if len(solution[i]) > 1:
            start = random.randint(0, len(solution[i]) - 2)
            end = random.randint(start + 1, len(solution[i]) - 1)
            solution[i][start:end + 1] = reversed(solution[i][start:end + 1])
    return solution


def tournament_selection(input_data, population, tournament_size):
    """Perform tournament selection on a population to select two individuals as winners.

    Args:
        input_data (dict): Input data for evaluation
        population (List): List of individuals in the population
        tournament_size (int): Size of each tournament

    Returns:
        List: List containing two selected individuals as winners
    """
    selected = []
    for _ in range(2):
        tournament = random.sample(population, tournament_size)
        winner = max(tournament, key=lambda individual: evaluate_solution(
            input_data, individual))
        selected.append(winner)
    return selected


def genetic_algorithm(input_data, parameters):
    """Runs the genetic algorithm to find a solution to the traffic signaling problem.

    Args:
        input_data (dict): Input data.
        parameters (tuple): Genetic algorithm parameters.

    Returns:
        list: Intersection/solution data.
    """
    population_size, num_generations, num_mutations, mutation_rate, inversion_rate, tournament = parameters
    streets = input_data['streets']
    number_of_intersections = input_data['number_of_intersections']

    population = []
    for i in range(population_size):
        solution = init_solution(
            streets, number_of_intersections, input_data['duration'])
        population.append(solution)

    best_solution = population[0]
    print('Initial Solution:', evaluate_solution(input_data, best_solution))

    fitness_scores = [[] for i in range(num_generations)]

    for generation in range(num_generations):
        for solution in population:
            if evaluate_solution(input_data, solution) > evaluate_solution(input_data, best_solution):
                best_solution = solution

        best_solution = copy.deepcopy(best_solution)
        new_population = []

        for _ in range(int(population_size)):

            if tournament:
                tournament_size = random.randint(1, population_size - 1)
                parentA, parentB = tournament_selection(
                    input_data, population, tournament_size)
            else:
                parentA = select_with_replacement(input_data, population)
                parentB = select_with_replacement(input_data, population)

            childA, childB = crossover([parentA, parentB])

            childA_old_score = evaluate_solution(input_data, childA)
            childB_old_score = evaluate_solution(input_data, childB)
            mutated_intersectionA = None
            mutated_intersectionB = None

            if random.randint(0, 1) < mutation_rate:
                childA, mutated_intersectionA = mutate(childA, num_mutations)
                childB, mutated_intersectionB = mutate(childB, num_mutations)
            if random.randint(0, 1) < inversion_rate:
                childA = inversion(childA)
                childB = inversion(childB)

            childA_new_score = evaluate_solution_delta(
                input_data, parentA, childA, childA_old_score, mutated_intersectionA)
            childB_new_score = evaluate_solution_delta(
                input_data, parentB, childB, childB_old_score, mutated_intersectionB)

            # Check if the new scores are better than the old scores and include the child solutions in the new population accordingly
            if childA_new_score > evaluate_solution(input_data, parentA):
                new_population.append(childA)
            else:
                new_population.append(parentA)

            if childB_new_score > evaluate_solution(input_data, parentB):
                new_population.append(childB)
            else:
                new_population.append(parentB)

        for i in range(len(new_population)):
            score = evaluate_solution(input_data, new_population[i])
            fitness_scores[generation].append((new_population[i], score))
        fitness_scores[generation].sort(key=lambda x: x[1], reverse=True)

        population = [x[0]
                      for x in fitness_scores[generation][:population_size]]

        # Print the fitness score of the best solution in this generation
        best_fitness_score = fitness_scores[generation][0][1]

        print('Generation {}: Fitness score of the best solution = {}'.format(
            generation + 1, best_fitness_score))

        if evaluate_solution(input_data, best_solution) < fitness_scores[generation][0][1]:
            best_solution = fitness_scores[generation][0][0]

    print('Best Solution', evaluate_solution(input_data, best_solution))
    return best_solution


def mutate_intersection_duration(solution, mutated_intersections):
    """Mutate the intersection duration within the solution.

    Args:
        solution (List): The solution containing intersections.
        mutated_intersections (List): List to track mutated intersection indices.

    Returns:
        Tuple: The mutated solution and the updated list of mutated intersection indices.
    """
    num_intersections = len(solution)
    if num_intersections < 2:
        return solution, mutated_intersections

    index1 = random.randint(0, num_intersections - 1)
    index2 = random.randint(0, num_intersections - 1)
    while index1 == index2:
        # Make sure the two indices are different
        index2 = random.randint(0, num_intersections - 1)

    # Swap the durations of the two intersections
    intersection1 = solution[index1]
    intersection2 = solution[index2]
    duration1 = sum(street['duration'] for street in intersection1)
    duration2 = sum(street['duration'] for street in intersection2)

    # Update the durations of the streets in each intersection
    remaining_time1 = duration2
    remaining_time2 = duration1

    for street in intersection1:
        duration = round((duration2 / len(intersection1)))
        street['duration'] = duration
        remaining_time1 -= duration

    for street in intersection2:
        duration = round((duration1 / len(intersection2)))
        street['duration'] = duration
        remaining_time2 -= duration

    # Distribute remaining time among the streets
    distribute_remaining_time(intersection1, remaining_time1)
    distribute_remaining_time(intersection2, remaining_time2)

    if index1 not in mutated_intersections:
        mutated_intersections.append(index1)

    if index2 not in mutated_intersections:
        mutated_intersections.append(index2)

    return solution, mutated_intersections


def distribute_remaining_time(intersection, remaining_time):
    """Distribute remaining time among the streets in the intersection.

    Args:
        intersection (List): Intersection data.
        remaining_time (int): Remaining time to distribute.
    """
    if remaining_time > 0:
        streets = sorted(intersection, key=lambda street: street['duration'])
        num_streets = len(streets)
        for i in range(remaining_time):
            street_index = i % num_streets
            streets[street_index]['duration'] += 1
