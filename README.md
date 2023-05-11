# Traffic-Signaling-Genetic-Algorithm

## Running the Genetic Algorithm

To run the genetic algorithm, you can use one of the following commands based on your desired execution mode.

### Experimental Mode

Experimental mode allows you to play and adjust with the parameters. 

```shell
cd src

python main.py --mode experimental --population_size <population_size> --num_generations <num_generations> --num_mutations <num_mutations> --mutation_rate <mutation_rate> --inversion_rate <inversion_rate> --file_name <input_file> --tournament
```

- mode experimental: Sets the execution mode to "experimental".
- population_size <population_size>: Specifies the population size.
- num_generations <num_generations>: Specifies the number of generations.
- num_mutations <num_mutations>: Specifies the number of mutations.
- mutation_rate <mutation_rate>: Specifies the mutation rate.
- inversion_rate <inversion_rate>: Specifies the inversion rate.
- file_name <input_file>: Specifies the input file name.
- tournament: Enables the tournament selection.

### Standard mode

The command runs the genetic algorithm in the standard mode. The algorithm will read the parameters from a CSV file named parameters.csv 

```shell
cd src

python main.py --mode standard
```

The CSV File contains:

- population_size: Population size.
- num_generations: Number of generations.
- num_mutations: Number of mutations.
- mutation_rate: Mutation rate.
- inversion_rate: Inversion rate.
- tournament: tournament select flag
- file_name: Input file name.
