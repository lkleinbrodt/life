import pickle
import json
from config import *
from world import World
import random
from gene import create_genome
from organism import Organism



class Population:
    def __init__(self, world: World, n_organisms: int, selector):
        self.population = []
        self.starting_n = n_organisms
        self.step_count = 0
        self.generation_count = 0
        self.world = world
        self.generation_data = {}
        self.selector = selector
        self.uid = random.getrandbits(48)
        self.directory = DATA_DIR+'/'+str(self.uid)
        
        os.mkdir(self.directory)
        
        
        for _ in range(n_organisms):
            
            location = random.sample(range(world.size), 2)
            while world.is_occupied(location):
                location = random.sample(range(world.size), 2)
                
            organism = Organism(
                genome = create_genome(parent=None),
                starting_loc=location,
                world = world
            )
            self.population.append(organism)
            
    def scatter(self):
        for organism in self.population:
            location = random.sample(range(self.world.size), 2)
            while self.world.is_occupied(location):
                location = random.sample(range(self.world.size), 2)
            organism.move(location)
            
    def selection(self):
        self.prev_n_dead = self.selector.select(self)
        
    
    def reproduce(self):
        #TODO: make this more extensible
        target_n = self.starting_n
        n_current = len(self.population)
        # n_needed = starting_n - n_current
        i = 0
        while len(self.population) != target_n:
            new_genome = create_genome(
                self.population[i].genome
            )
            #TODO: birth location should be near parent
            location = random.sample(range(self.world.size), 2)
            while self.world.is_occupied(location):
                location = random.sample(range(self.world.size), 2)
                
            self.population.append(
                Organism(new_genome, location, self.world)
            )
            if i == n_current:
                i = 0
            else:
                i += 1
        
    def step(self, world: World):
        for organism in self.population:
            organism.act(world)
        
        if self.step_count == GENERATION_LENGTH:
            self.selection()
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
            'prev_n_died': self.prev_n_dead
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