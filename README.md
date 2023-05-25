# Traffic-Signaling-Genetic-Algorithm

This project provides an implementation of a genetic algorithm for traffic signal optimization, in accordance with University of Prishtina, Computer Engineering (https://fiek.uni-pr.edu/)

## Running the Genetic Algorithm

To run the genetic algorithm, you can use one of the following commands based on your desired execution mode.

### Standard Mode

Standard mode allows you to play and adjust with the parameters. 

```shell
cd src

python main.py --mode standard --population_size <population_size> --num_mutations <num_mutations> --mutation_rate <mutation_rate> --inversion_rate <inversion_rate> --tournament --file_name ../data/input/<input_file>

```

- mode: This should be standard.
- population_size: The size of the population for the genetic algorithm.
- num_mutations: The number of mutations.
- mutation_rate: The mutation rate.
- inversion_rate: The inversion rate.
- tournament: Pass this option to enable tournament selection.
- file_name: The name of the input file.

### Experimental mode

The command runs the genetic algorithm in the experimental mode. The algorithm will read the parameters from a CSV file named parameters.csv 

```shell
cd src

python main.py --mode experimental --config ../data/config/<config_file>

```

The CSV File contains:

- population_size: Population size.
- num_generations: Number of generations.
- num_mutations: Number of mutations.
- mutation_rate: Mutation rate.
- inversion_rate: Inversion rate.
- tournament: tournament select flag
- file_name: Input file name.
