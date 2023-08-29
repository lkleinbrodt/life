#TODO: parent class
from config import MORTALITY_RATE #TODO: use in params
import random

class ShapeSelector:
    def __init__(self, *points: list):
                 
        # assert all([x >= 0 for x in [x1, x2, y1, y2]])
              
        # #TODO: support percent inputs
        # if all([x <= 1.0 for x in [x1, x2, y1, y2]]):
        #     assert (n_columns is not None) & (n_rows is not None)
            
        #     x1 = int(x1*n_columns)
        #     x2 = int(x2*n_columns)
        #     y1 =  int(y1*n_rows)
        #     y2 = int(y2*n_rows)
        
        self.points = points
    
    from population import Population
    
    
    def _inside_edge(self, loc, x1,y1, x2, y2):
        yp, xp = loc
        D = (x2 - x1) * (yp - y1) - (xp - x1) * (y2 - y1)
        if D > 0:
            return True
        else:
            return False
        
    def _contains(self, loc, points):
        
        p1 = points[0]
        for i in range(0, len(points)):
            if i == len(points)-1:
                p2 = points[0]
            else:
                p2 = points[i+1]
            if not self._inside_edge(loc, *p1, *p2):
                return False
            p1 = p2
        return True

    def contains(self, loc):
        return self._contains(loc, self.points) | self._contains(loc, list(reversed(self.points))) #TODO: IMPROVE
            
        
        

    def select(self, population: Population):
        n_dead = 0
                
        for i, organism in enumerate(population.population):
            # in_x = (self.x1 <= organism.loc[0] <= self.x2) | (self.x2 <= organism.loc[0] <= self.x1)
            # in_y = (self.y1 <= organism.loc[0] <= self.y2) | (self.y2 <= organism.loc[0] <= self.y1)
            # if in_x and in_y:
            if self.contains(organism.loc):
                population.world.clear_loc(organism.loc)
                del population.population[i]
                n_dead += 1
        out = {
            '# Died': n_dead
        }
        return out
    
class DiseaseSelector:
    def __init__(self):
        #TODO: control infection rate ehre
        pass
    
    from population import Population
    def select(self, population: Population):
        n_dead = 0
        n_infected = 0
                
        for i, organism in enumerate(population.population):
            if organism.is_diseased:
                n_infected += 1
                if random.random() <= MORTALITY_RATE:
                    population.world.clear_loc(organism.loc)
                    del population.population[i]
                    n_dead += 1

                
        out = {
            '# Died': n_dead,
            '# Diseased': n_infected
        }
        return out

SELECTOR_MAP = {
    'shape': ShapeSelector,
    'disease': DiseaseSelector
}