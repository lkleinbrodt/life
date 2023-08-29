from config import *

class Parameters:
    #TODO: make this cooler and better lol
    def __init__(
        self, 
        selector: str,
        world_size = WORLD_SIZE,
        genome_size = GENOME_SIZE,
        n_internal_neurons = N_INTERNAL_NEURONS,
        mutation_rate = MUTATION_RATE,
        mutation_magnitude = MUTATION_MAGNITUDE,
        generation_length = GENERATION_LENGTH,
        population_size = POPULATION_SIZE,
        connection_magnitude = CONNECTION_MAGNITUDE,
        infection_step = INFECTION_STEP,
        mortality_rate = MORTALITY_RATE,
        infection_rate = INFECTION_RATE
        
    ):
        self.selector = selector 
        self.selector_params = []
        self.world_size = world_size
        self.genome_size = genome_size
        self.n_internal_neurons = n_internal_neurons
        self.mutation_rate = mutation_rate 
        self.mutation_magnitude = mutation_magnitude
        self.generation_length = generation_length
        self.population_size = population_size
        self.connection_magnitude = connection_magnitude
        self.infection_step = infection_step #TODO: things like this should go into selector params
        self.mortality_rate = mortality_rate
        self.infection_rate = infection_rate
        
        