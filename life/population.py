import pickle
import json
from config import DATA_DIR
import os
from world import World
import random
from gene import create_genome
from organism import Organism
from parameters import Parameters



class Population:
    def __init__(self, world: World, params: Parameters):
        self.population = []
        self.starting_n = params.population_size
        self.step_count = 0
        self.generation_count = 0
        self.world = world
        self.generation_data = {}
        self.generation_length = params.generation_length
        self.uid = random.getrandbits(48)
        self.directory = DATA_DIR+'/'+str(self.uid)
        self.params = params
        
        os.mkdir(self.directory)
        
        
        for _ in range(self.starting_n):
            
            location = random.sample(range(world.size), 2)
            while world.is_occupied(location):
                location = random.sample(range(world.size), 2)
                
            organism = Organism(
                genome = create_genome(parent=None, params = params),
                starting_loc=location,
                world = world,
                params = params,
            )
            self.population.append(organism)
            
    def scatter(self, organisms = None):
        for organism in self.population:
            location = random.sample(range(self.world.size), 2)
            while self.world.is_occupied(location):
                location = random.sample(range(self.world.size), 2)
            organism.move(location)
            
    def selection(self, selector):
        self.selection_output = selector.select(self)
        
    
    def reproduce(self):
        #TODO: make this more extensible
        target_n = self.starting_n
        n_current = len(self.population)
        # n_needed = starting_n - n_current
        i = 0
        while len(self.population) != target_n:
            new_genome = create_genome(
                self.population[i].genome,
                self.params
            )
            #TODO: birth location should be near parent
            location = random.sample(range(self.world.size), 2)
            while self.world.is_occupied(location):
                location = random.sample(range(self.world.size), 2)
                
            self.population.append(
                Organism(new_genome, location, self.world, self.params)
            )
            if i == n_current:
                i = 0
            else:
                i += 1
        
    def step(self, world: World, selector):
        for organism in self.population:
            organism.act(world)
        
        if self.step_count == self.generation_length:
            self.selection(selector)
            self.reproduce()
            self.scatter()
            self.step_count = 0
            self.generation_count += 1
            self.generation_data[str(self.generation_count)] = self.snapshot()
            # self.save_generation_data()
        else:
            self.step_count += 1
    
    def get_organism(self, idx):
        return self.population[idx]

    def __repr__(self) -> str:
        out = ""
        for i, organism in enumerate(self.population):
            out += f'Organism {i} /n'
            out += str(organism)
        return out
    
    def snapshot(self):
        out = {
            'n_alive': len(self.population),
            'previous selection': self.selection_output
        }
        return out
    
    def save_generation_data(self):
        
        with open(self.directory+'/generation_data.json', 'w') as f:
            json.dump(self.generation_data, f)
    
    def save(self):
        with open(self.directory+'/population.pkl', 'wb') as f:
            pickle.dump(self, f)
        

def load_population(path):
    with open(path, 'rb') as f:
        out = pickle.load(f)
    return out