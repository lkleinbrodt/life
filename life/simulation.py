from config import *
import parameters
import world
import selection
import population

class Simulation:
    def __init__(self, params: parameters.Parameters) -> None:
        self.params = params
        
        self.world = world.World(params.world_size)
        print(params.selector_params)
        self.selector = selection.SELECTOR_MAP[params.selector](*params.selector_params)
        
        self.population = population.Population(
            world = self.world, 
            params=params
        )
        
        if params.selector == 'disease':
            import random
            for _ in range(10):
                patient_zero = random.randint(0, params.population_size-1)
                self.population.population[patient_zero].contract()
    
    def step(self):
        self.population.step(self.world, self.selector)

        if (self.population.step_count % (self.params.generation_length * 10)) == 0:
            # prev_gen = population.generation_count
            # print('Generation:', self.population.generation_count)
            self.population.save()
            self.population.save_generation_data()