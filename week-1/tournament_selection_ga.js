const individuals = 100; 
const listLength = 50; 
const generations = 100; 
const mutationRate = 0.01;

// Creates population with binary data
function getPopulation(individuals, listLength) {
  let list = [];
  for (let index = 0; index < individuals; index++) {
    // Randomly returns binary list data for an individual
    list.push(Array.from(Array(listLength), () => {
      const randomNum = Math.random() + 0.5; 
      return Math.floor(randomNum);
    }));
  }
  return list;
};

// Gets fitnesses of the population
function getFitness(population) {
  let list = [];
  // Loop for each individual
  for (let index = 0; index < population.length; index++) {
    const row = population[index];
    let rowSum = 0;
    // Sums up each individual(row)
    for (let index = 0; index < row.length; index++) {
      rowSum += row[index];      
    }
    list.push(rowSum);
  }
  return list;
}

// Gets two random individuals from the population
function getTwoRandomIndividuals(population, n) {
  const firstIndex = Math.floor(Math.random() * n);
  let secondIndex;
  
  // Loop for ensuring individuals are distinct
  do {
    secondIndex = Math.floor(Math.random() * n);
  } while (secondIndex === firstIndex);
  
  return [ population[firstIndex], population[secondIndex], firstIndex, secondIndex];
}

// Tournament Selection: Selects best fitness of two random individual
function tournamentSelection(population, fitness, n) {
  let list = [];
  for (let index = 0; index < n; index++) {
    // Gets two random individual with their indexes
    const [ individual1, individual2, firstIndex, secondIndex] = 
      getTwoRandomIndividuals(population, population.length); 
    // Checks which individual has the best fitness(sum of the data)
    if (fitness[firstIndex] > fitness[secondIndex]) {
      list.push(individual1);
    } else {
      list.push(individual2);
    }
  }
  return list;
}

// Crossover: Randomly changes genes of two random individual inside the selected parents
function crossover(selectedParents) {
  const numParents = selectedParents.length;
  const stringLength = selectedParents[0].length; 
  // Creates an empty list
  const offspring = Array(numParents).fill(null).map(() => Array(stringLength).fill(0)); 

  for (let i = 0; i < numParents - 1; i += 2) { 
    // Finds a random crossover point inside the genes
    const crossoverPoint = Math.floor(Math.random() * (stringLength - 1)) + 1; 

    // Crossover for first parent
    offspring[i] = [
      ...selectedParents[i].slice(0, crossoverPoint), 
      ...selectedParents[i + 1].slice(crossoverPoint) 
    ];
    
    // Crossover for second parent
    offspring[i + 1] = [
      ...selectedParents[i + 1].slice(0, crossoverPoint), 
      ...selectedParents[i].slice(crossoverPoint) 
    ];
  }

  // If the population number is odd adds the last parent directly to offspring
  if (numParents % 2 === 1) {
    offspring[numParents - 1] = parents[numParents - 1]; 
  }

  return offspring; 
}

// Mutates offspring
function mutate(offspring) {
  let mutatedList = offspring.map(individual => [...individual]); 
  
  // For each data randomly mutates the binary value to the opposite
  for (let i = 0; i < mutatedList.length; i++) {
    for (let j = 0; j < mutatedList[i].length; j++) {
      if (mutationRate > Math.random()) {
        mutatedList[i][j] = mutatedList[i][j] === 0 ? 1 : 0;
      }
    }
  }
  return mutatedList;
}

// Main function for the Genetic Algorithm
function oneMaxGA() {
  let population = getPopulation(individuals, listLength);

  for (let generation = 1; generation <= generations; generation++) {

    const fitness = getFitness(population);

    const bestFitness = Math.max(...fitness);

    if (bestFitness < 35) {
      const selectedParents = tournamentSelection(population, fitness, individuals);
  
      const offspring = crossover(selectedParents);
      console.log(offspring)
      const mutated_offspring = mutate(offspring);
  
      population = mutated_offspring;

      console.log(`Generation ${generation}: Best Fitness = ${bestFitness}`);
    } else {
      console.log(`Generation ${generation}: Best Fitness = ${bestFitness}`);
      console.log(`Best fitness is reached`);
      break;
    }
  }

  const finalFitness = getFitness(population);

  const bestFitness = Math.max(...finalFitness);

  const bestIndex = finalFitness.indexOf(bestFitness);
  
  const bestSolution = population[bestIndex];

  console.log(`Best solution: [${bestSolution.join(', ')}] with fitness ${bestFitness}`);
}

oneMaxGA();
