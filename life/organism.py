
from world import World
import random
from gene import create_genome
from brain import Brain
from parameters import Parameters

class Organism:
    def __init__(self, genome, starting_loc, world: World, params: Parameters):
        self.genome = genome
        self.loc = starting_loc
        world.set_loc(starting_loc, self)
        self.world = world
        self.params = params
        
        self.is_diseased = False
        self.infection_step = params.infection_step
        self.infection_timer = params.infection_step
        
        self.brain = Brain(genome = genome, organism = self)
        self.brain.connect()
        
        # import numpy as np
        # self.color = np.array([1, 1, 1], dtype=float)
        # for neuron in self.brain.receptors + list(self.brain.internals.values()):
        #     if neuron.weight is not None:
        #         self.color += (neuron.color * neuron.weight)
        
        # self.color += abs(self.color.min())
        # self.color /= self.color.sum()
        # self.color *= 255
        self.color = (0, 150, 255)
        
        
    
    def move(self, new_location):
        if self.world.is_occupied(new_location):
            #TODO: return false or raise error?
            return False
        else:
            self.world.clear_loc(self.loc)
            self.loc = new_location
            self.world.set_loc(new_location, self)
            
            return True
        
    def contract(self):
        if self.is_diseased:
            pass
        else:
            self.is_diseased = True
            self.infection_timer = self.infection_step
            # self.disease_timer = self.mortality_step
            self.color = (238, 75, 43)
    
    def infect(self, world: World):
        self.infection_timer -= 1
        if self.infection_timer == 0:
            self.infection_timer = self.infection_step
            for loc in [
                (self.loc[0] - 1, self.loc[1]),
                (self.loc[0] + 1, self.loc[1]),
                (self.loc[0], self.loc[1] - 1),
                (self.loc[0], self.loc[1] + 1),
            ]:
                org = world.get_loc(loc)
                if isinstance(org, Organism):
                    if random.random() <= self.params.infection_rate:
                        org.contract()
        
    def act(self, world: World):
        if self.is_diseased:
            self.infect(world)
            # self.disease_timer -= 1
        self.brain.sense(world)
        self.brain.take_actions(world)
        
        
        
    
    def __repr__(self) -> str:
        brain = "Brain:\n" + str(self.brain)
        location = "Location: " + str(self.loc) + '\n'
        return "Organism" + location + brain