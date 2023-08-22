
from world import World
from math import tanh
from typing import Any, List
from gene import Gene
import neuron

class Brain:
    def __init__(self, genome: List[Gene], organism):
        self.genome = genome
        self.receptors = []
        self.internals = {
            f'internal_{i}': neuron.Internal(None, organism) 
            for i in range(organism.params.n_internal_neurons)
        }
        self.actors = {
            name: actor(organism) for 
            name, actor in neuron.actor_dict.items()
        }
        self.organism = organism
        
        for gene in genome:
            #currently, receptors can only be connected to 1 other neuron
            #so it's possible to have 2 receptors of the same type
            
            
            if gene.source_type == 'internal':
                self.internals[gene.source_class] = neuron.Internal(gene, self.organism)
            else:
                self.receptors.append(neuron.receptor_dict[gene.source_class](gene, self.organism))

        #TODO: currently we must connect the brain after creation, in the org class
    
    def connect(self):
        for receptor in self.receptors:
            receptor.connect()
        for i, internal in enumerate(self.internals.values()):
            internal.connect()
            if internal.sink is None:
                pass #TODO: delete
                
            
    def sense(self, world: World):
        for receptor in self.receptors:
            receptor.sense(world)
            receptor.activate()
        for internal in self.internals.values():
            internal.activate()
    
    def take_actions(self, world: World):
        import random
        
        n_actions = 0
        for actor in self.actors.values():
            if (1-2*random.random()) <= tanh(actor.activation_value):
                actor.activate(world)
                n_actions += 1
    
    def __repr__(self) -> str:
        out = "Receptors\n"
        for neuron in self.receptors + self.internals + list(self.actors.values()):
            out += str(neuron)
            out += "\n"
        return out