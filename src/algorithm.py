import copy
import random
from helper import return_cycle_time
import time


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


def get_green_light(intersection, current_time):
    """Get the currently green street and its remaining duration at the given current time.

    Args:
        intersection (list): List of streets at the intersection, each represented as a dictionary with 'street' and 'duration' keys.
        current_time (int): Current time in the simulation.

    Returns:
        tuple: A tuple containing the currently green street and its remaining duration.
            - If no street is currently green, returns (None, 0).
            - Otherwise, returns (green_street, green_duration) where green_street is the name of the green street
              and green_duration is the remaining duration for which the street is green.

    """
    cycle_time = sum(street['duration'] for street in intersection)

    # Check if cycle_time is zero (no valid streets with non-zero duration)
    if cycle_time == 0:
        return None, 0

    num_streets = len(intersection)
    if num_streets == 1:
        # If only one street, it is always green
        street = intersection[0]['street']
        return street, intersection[0]['duration']

    normalized_time = current_time % cycle_time

    elapsed_time = 0
    for i, street in enumerate(intersection):
        elapsed_time += street['duration']
        if normalized_time < elapsed_time:
            green_street = street['street']
            green_duration = min(
                street['duration'], elapsed_time - normalized_time)
            return green_street, green_duration

        if i == num_streets - 1:
            # If we reached the last street, go back to the first street in the next cycle
            elapsed_time = 0

    return None, 0


def evaluate_solution(input_data, solution):
    """Evaluate a solution based on the given input data.

    Args:
        input_data (dict): Input data dictionary containing 'bonus', 'streets', 'cars', and 'duration'.
        solution (dict): Solution dictionary containing the intersection schedules.

    Returns:
        int: Score obtained by the solution.

    """
    bonus = input_data['bonus']
    streets = input_data['streets']
    cars = input_data['cars']
    duration = input_data['duration']

    score = 0
    for car in cars:
        current_time = 0
        current_street_index = 0
        car_finished = False
        final_time = 0
        while current_time < duration:
            street_name = car['path'][current_street_index]
            intersection = solution[streets[street_name]['end']
                                    ] if streets[street_name]['end'] < len(solution) else False
            if intersection:
                street_exists = True if street_name in [
                    street['street'] for street in intersection] else False
                if not street_exists:
                    break
                green_street, green_duration = get_green_light(
                    intersection, current_time)

                if green_street is None:
                    break

                if green_street == street_name:
                    current_street_index = (
                        current_street_index + 1) % len(car['path'])
                    street_length = streets[car['path']
                                            [current_street_index]]['length']
                    final_intersection = solution[streets[car['final']]['end']
                                                  ] if streets[car['final']]['end'] < len(solution) else False
                    current_time += street_length
                    if final_intersection:
                        if current_street_index == len(car['path']) - 1 and current_time < duration and car['final'] in [street['street'] for street in final_intersection]:
                            car_finished = True
                            final_time = current_time
                            break
                    else:
                        break
                else:
                    current_time += green_duration
                    continue  # Skip to the next iteration
            else:
                break

        if car_finished:
            remaining_time = max(0, duration - final_time)
            car_score = bonus + remaining_time
            score += car_score

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
    bonus = input_data['bonus']
    streets = input_data['streets']
    cars = input_data['cars']
    duration = input_data['duration']

    score_diff = 0

    for car in cars:
        pass_through_mutated_intersection = False
        for street in car['path']:
            if streets[street]['end'] == mutated_intersection:
                pass_through_mutated_intersection = True
                break

        if not pass_through_mutated_intersection:
            continue

        current_time = 0
        current_street_index = 0
        car_finished = False
        final_time = 0

        while current_time < duration:
            street_name = car['path'][current_street_index]
            intersection = new_solution[streets[street_name]['end']] if streets[street_name]['end'] < len(
                new_solution) else False
            if intersection:
                street_exists = True if street_name in [
                    street['street'] for street in intersection] else False
                if not street_exists:
                    break
                green_street, green_duration = get_green_light(
                    intersection, current_time)

                if green_street is None:
                    break

                if green_street == street_name:
                    current_street_index = (
                        current_street_index + 1) % len(car['path'])
                    street_length = streets[car['path']
                                            [current_street_index]]['length']
                    final_intersection = new_solution[streets[car['final']]['end']] if streets[car['final']]['end'] < len(
                        new_solution) else False
                    current_time += street_length
                    if final_intersection:
                        if current_street_index == len(car['path']) - 1 and current_time < duration and car[
                                'final'] in [street['street'] for street in final_intersection]:
                            car_finished = True
                            final_time = current_time
                            break
                    else:
                        break
                else:
                    current_time += green_duration
                    continue  # Skip to the next iteration
            else:
                break

        if car_finished:
            remaining_time = max(0, duration - final_time)
            car_score = bonus + remaining_time
            score_diff += car_score

    new_score = old_score - score_diff

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
    start_time = time.time()
    population_size, num_mutations, mutation_rate, inversion_rate, tournament = parameters

    streets = input_data['streets']
    number_of_intersections = input_data['number_of_intersections']

    population = []
    for i in range(population_size):
        solution = init_solution(
            streets, number_of_intersections, input_data['duration'])
        population.append(solution)

    best_solution = population[0]
    print('Initial Solution: ', evaluate_solution(input_data, best_solution))

    generation = 0
    fitness_scores = []

    while time.time() - start_time < 5*60:
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

        # Store the fitness scores of this generation
        fitness_scores.append([])
        for i in range(len(new_population)):
            score = evaluate_solution(input_data, new_population[i])
            fitness_scores[generation].append((new_population[i], score))
        fitness_scores[generation].sort(key=lambda x: x[1], reverse=True)

        population = [x[0]
                      for x in fitness_scores[generation][:population_size]]

        # Print the fitness score of the best solution in this generation
        best_fitness_score = fitness_scores[generation][0][1]

        # print('Generation {}: Fitness score of the best solution = {}'.format(
        #     generation + 1, best_fitness_score))

        if evaluate_solution(input_data, best_solution) < fitness_scores[generation][0][1]:
            best_solution = fitness_scores[generation][0][0]

        generation += 1

    print('Best Solution: ', evaluate_solution(input_data, best_solution))
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
