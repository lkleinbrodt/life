
from config import *
from world import World
import random
from gene import create_genome
from brain import Brain

class Organism:
    def __init__(self, genome, starting_loc, world: World):
        self.genome = genome
        self.loc = starting_loc
        world.set_loc(starting_loc, self)
        self.world = world
        
        self.brain = Brain(genome = genome, organism = self)
        self.brain.connect()
        
        import numpy as np
        self.color = np.array([1, 1, 1], dtype=float)
        for neuron in self.brain.receptors + list(self.brain.internals.values()):
            if neuron.weight is not None:
                self.color += (neuron.color * neuron.weight)
        
        self.color += abs(self.color.min())
        self.color /= self.color.sum()
        self.color *= 255
        
        
    
    def move(self, new_location):
        if self.world.is_occupied(new_location):
            #TODO: return false or raise error?
            return False
        else:
            self.world.clear_loc(self.loc)
            self.loc = new_location
            self.world.set_loc(new_location, self)
            
            return True
        
    def act(self, world: World):
        self.brain.sense(world)
        self.brain.take_actions(world)
        
    
    def __repr__(self) -> str:
        brain = "Brain:\n" + str(self.brain)
        location = "Location: " + str(self.loc) + '\n'
        return "Organism" + location + brain