import random
from config import *



class Gene:
    def __init__(self, parent, n_internal):
        if parent is not None:
            #TODO: currently only asexual
            
            if random.random() <= MUTATION_RATE:
                self.source_type = random.sample(['receptor', 'internal'], 1)[0]
                if self.source_type == 'receptor':
                    self.source_class = random.sample(AVAILABLE_RECEPTORS, 1)[0]
                elif self.source_type == 'internal':
                    # self.source_index = random.sample(range(n_internal), 1)[0]
                    self.source_class = f'internal'
            else:
                self.source_type = parent.source_type
                self.source_class = parent.source_class
            
            if random.random() <= MUTATION_RATE:
                self.sink_type = random.sample(['action', 'internal'], 1)[0]
                if self.sink_type == 'action':
                    self.sink_index = random.sample(AVAILABLE_ACTORS, 1)[0]
                elif self.sink_type == 'internal':
                    self.sink_index = f'internal_{random.sample(range(n_internal), 1)[0]}'
                else:
                    raise ValueError(self.sink_type)
            else:
                self.sink_type = parent.sink_type
                self.sink_index = parent.sink_index
            
            if random.random() <= MUTATION_RATE:
                change = random.uniform(-1, 1) * MUTATION_MAGNITUDE
                self.weight = parent.weight + change
                self.weight = max([self.weight, CONNECTION_MAGNITUDE])
                self.weight = min([self.weight, -CONNECTION_MAGNITUDE])
            else:
                self.weight = parent.weight
            
            
        else:
            self.source_type = random.sample(['receptor', 'internal'], 1)[0]
            if self.source_type == 'receptor':
                self.source_class = random.sample(AVAILABLE_RECEPTORS, 1)[0]
            elif self.source_type == 'internal':
                self.source_class = 'internal'#random.sample(range(n_internal), 1)[0]
            else:
                raise ValueError('Source must be receptor or internal')
            
            self.sink_type = random.sample(['action', 'internal'], 1)[0]
            if self.sink_type == 'action':
                self.sink_index = random.sample(AVAILABLE_ACTORS, 1)[0]
            elif self.sink_type == 'internal':
                self.sink_index = f'internal_{random.sample(range(n_internal), 1)[0]}'
            else:
                raise ValueError('Sink must be action or internal')

            self.weight = random.uniform(-CONNECTION_MAGNITUDE, CONNECTION_MAGNITUDE)
        
        
 
def create_genome(parent = None): #TODO: class?
    if parent is None:
        return [
            Gene(parent = None, n_internal=N_INTERNAL_NEURONS)
            for _ in range(GENOME_SIZE)
        ]
    else:
        return [
            Gene(parent = gene, n_internal=N_INTERNAL_NEURONS)
            for gene in parent
        ]