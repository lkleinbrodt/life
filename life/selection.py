class BoxSelector:
    def __init__(self, x1, y1, x2, y2, world = None):
                 
        assert all([x > 0 for x in [x1, x2, y1, y2]])
              
        #TODO: support percent inputs
        if all([x <= 1.0 for x in [x1, x2, y1, y2]]):
            
            x1 = int(x1*world.n_columns)
            x2 = int(x2*world.n_columns)
            y1 =  int(y1*world.n_rows)
            y2 = int(y2*world.n_rows)
        
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
    
    from population import Population
    def select(self, population: Population):
        n_dead = 0
                
        for i, organism in enumerate(population.population):
            in_x = (self.x1 <= organism.loc[0] <= self.x2) | (self.x2 <= organism.loc[0] <= self.x1)
            in_y = (self.y1 <= organism.loc[0] <= self.y2) | (self.y2 <= organism.loc[0] <= self.y1)
            if in_x and in_y:
                population.world.clear_loc(organism.loc)
                del population.population[i]
                n_dead += 1
        out = {
            '# Died': n_dead
        }
        return n_dead