
from config import COLOR_DICT, AVAILABLE_ACTORS, AVAILABLE_RECEPTORS, NEURON_COLORS
from world import World
from math import tanh
from gene import Gene



class Neuron:
    def __init__(self, organism):
        self.name = 'Base Neuron'
        self.organism = organism
        self.activation_value = 0
    
    def __repr__(self) -> str:
        return self.name
    
class Receptor(Neuron):
    def __init__(self, gene: Gene, organism):
        if gene is None:
            self.sink_type = None
            self.sink_index = None
            self.weight = None
        else:
            self.sink_type = gene.sink_type
            self.sink_index = gene.sink_index
            self.weight = gene.weight
            
        self.gene = gene
        super().__init__(organism)
        self.name = 'Receptor'
    
    def connect(self):
        if self.sink_type == 'internal':
            self.sink = self.organism.brain.internals[self.sink_index]
        elif self.sink_type == 'action':
            self.sink = self.organism.brain.actors[self.sink_index]
        elif self.sink_type is None:
            self.sink = None
        else:
            raise NotImplementedError()

    def activate(self):
        if self.sink is not None:
            output = self.weight * tanh(self.activation_value)
            try:
                self.sink.input(output)
            except AttributeError as e:
                print(self)
                print(self.sink)
                print(self.sink_type)
                print(self.sink_index)
                raise e
                
            self.activation_value = 0
    
    def __repr__(self) -> str:
        out = f"""
        {self.name}:
            sink_type: {self.sink_type}
            sink_index: {self.sink_index}
            weight: {self.weight}
        """
        return out
        
class Actor(Neuron):
    def __init__(self, organism):
        super().__init__(organism)
        self.name = 'Actor'
    #TODO: activate method (make an act method)
    def __repr__(self) -> str:
        return self.name
    
    def input(self, value):
        self.activation_value += value
        
class LatitudeReceptor(Receptor):
    def __init__(self, gene: Gene, organism):
        super().__init__(gene, organism)
        self.name = 'latitude'
        self.color = COLOR_DICT[self.name]
        
    def sense(self, world: World):
        y_location = self.organism.loc[0]
        self.activation_value += y_location / world.n_rows
    
class LongitudeReceptor(Receptor):
    def __init__(self, gene: Gene, organism):
        super().__init__(gene, organism)
        self.name = 'longitude'
        self.color = COLOR_DICT[self.name]
        
    def sense(self, world: World):
        x_location = self.organism.loc[1]
        self.activation_value += x_location / len(world.grid[0])
        
class SouthBlockedReceptor(Receptor):
    def __init__(self, gene: Gene, organism, distance = 1):
        super().__init__(gene, organism)
        self.name = 'south_blocked'
        self.color = COLOR_DICT[self.name]
        self.distance = distance
        self.max_distance = sum([1/(d+1) for d in range(distance)])
        
    def sense(self, world: World):
        blocks = [0] * self.distance
        for distance in range(self.distance):
            loc = (self.organism.loc[0] + 1 + distance, self.organism.loc[1])
            if world.is_in_bounds(loc):
                blocks[distance] = 1/(distance + 1)
            elif world.is_occupied(loc):
                blocks[distance] = 1/(distance+1)
        self.activation_value += sum(blocks) / self.max_distance

class NorthBlockedReceptor(Receptor):
    def __init__(self, gene: Gene, organism, distance = 1):
        super().__init__(gene, organism)
        self.name = 'north_blocked'
        self.color = COLOR_DICT[self.name]
        self.distance = distance
        self.max_distance = sum([1/(d+1) for d in range(distance)])
        
    def sense(self, world: World):
        blocks = [0] * self.distance
        for distance in range(1, self.distance):
            loc = (self.organism.loc[0] - 1 - distance, self.organism.loc[1])
            if world.is_in_bounds(loc):
                blocks[distance] = 1/(distance + 1)
            elif world.is_occupied(loc):
                blocks[distance] = 1/(distance+1)
        self.activation_value += sum(blocks) / self.max_distance
        
class WestBlockedReceptor(Receptor):
    def __init__(self, gene: Gene, organism, distance = 1):
        super().__init__(gene, organism)
        self.name = 'east_blocked'
        self.color = COLOR_DICT[self.name]
        self.distance = distance
        self.max_distance = sum([1/(d+1) for d in range(distance)])
        
    def sense(self, world: World):
        blocks = [0] * self.distance
        for distance in range(1, self.distance):
            loc = (self.organism.loc[0], self.organism.loc[1] - 1 - distance)
            if world.is_in_bounds(loc):
                blocks[distance] = 1/(distance + 1)
            elif world.is_occupied(loc):
                blocks[distance] = 1/(distance+1)
        self.activation_value += sum(blocks) / self.max_distance
        
class EastBlockedReceptor(Receptor):
    def __init__(self, gene: Gene, organism, distance = 1):
        super().__init__(gene, organism)
        self.name = 'south_blocked'
        self.color = COLOR_DICT[self.name]
        self.distance = distance
        self.max_distance = sum([1/(d+1) for d in range(distance)])
        
    def sense(self, world: World):
        blocks = [0] * self.distance
        for distance in range(1, self.distance):
            loc = (self.organism.loc[0], self.organism.loc[1] + 1 + distance)
            if world.is_in_bounds(loc):
                blocks[distance] = 1/(distance + 1)
            elif world.is_occupied(loc):
                blocks[distance] = 1/(distance+1)
        self.activation_value += sum(blocks) / self.max_distance
    
class Internal(Receptor):
    def __init__(self, gene: Gene, organism):
        super().__init__(gene, organism)
        self.color = NEURON_COLORS[2]
    
    def input(self, value):
        self.activation_value += value
    
receptor_dict = {
    'latitude': LatitudeReceptor,
    'longitude': LongitudeReceptor,
    'north_blocked': NorthBlockedReceptor,
    'south_blocked': SouthBlockedReceptor,
    'east_blocked': EastBlockedReceptor,
    'west_blocked': WestBlockedReceptor,
    'internal': Internal
}

assert all([x in receptor_dict.keys() for x in AVAILABLE_RECEPTORS])
# for i in range(N_INTERNAL_NEURONS): #TODO: better way
#     AVAILABLE_RECEPTORS[i] = Internal


    
class MoveEast(Actor):
    def __init__(self, organism):
        super().__init__(organism)
        self.color = NEURON_COLORS[3]
        self.name = 'MoveEast'
    
    def activate(self, world: World):
        self.activation_value = 0 #TODO: even if this fails?
        x_position = self.organism.loc[1]
        at_last_column = (x_position == world.n_columns - 1)
        
        
        if (not at_last_column):
            new_loc = (self.organism.loc[0], self.organism.loc[1] + 1)
            spot_is_occupied = world.is_occupied(new_loc)
            if (not spot_is_occupied):
                return self.organism.move(new_loc)
            
        return False
            
class MoveWest(Actor):
    def __init__(self, organism):
        super().__init__(organism)
        self.color = NEURON_COLORS[4]
        self.name = 'MoveWest'
    
    def activate(self, world: World):
        self.activation_value = 0 #TODO: even if this fails?
        x_position = self.organism.loc[1]
        at_first_column = (x_position == 0)
        
        if (not at_first_column):
            new_loc = (self.organism.loc[0], self.organism.loc[1] - 1)
            spot_is_occupied = world.is_occupied(new_loc)
            if (not spot_is_occupied):
                return self.organism.move(new_loc)
        return False

class MoveNorth(Actor):
    def __init__(self, organism):
        super().__init__(organism)
        self.color = NEURON_COLORS[5]
        self.name = 'MoveNorth'
    
    def activate(self, world: World):
        self.activation_value = 0 #TODO: even if this fails?
        y_position = self.organism.loc[0]
        at_first_row = (y_position == 0)
        if not at_first_row:
            new_loc = (self.organism.loc[0] - 1, self.organism.loc[1])
            spot_is_occupied = world.is_occupied(new_loc)
            if not spot_is_occupied:
                return self.organism.move(new_loc)
        return False
                
class MoveSouth(Actor):
    def __init__(self, organism):
        super().__init__(organism)
        self.color = NEURON_COLORS[6]
        self.name = 'MoveSouth'
    
    def activate(self, world: World):
        self.activation_value = 0 #TODO: even if this fails?
        y_position = self.organism.loc[0]
        at_last_row = (y_position == world.n_rows-1)
        if not at_last_row:
            new_loc = (self.organism.loc[0] + 1, self.organism.loc[1])
            spot_is_occupied = world.is_occupied(new_loc)
            if not spot_is_occupied:
                return self.organism.move(new_loc)
        return False
    
actor_dict = {
    'move_north': MoveNorth,
    'move_south': MoveSouth,
    'move_east': MoveEast,
    'move_west': MoveWest
}

assert all([x in actor_dict.keys() for x in AVAILABLE_ACTORS])

# AVAILABLE_NEURONS = {**AVAILABLE_RECEPTORS, **AVAILABLE_ACTORS}