import random

class World:
    def __init__(self, size):
        self.grid = [[None] * size for _ in range(size)]
        self.size = size
        self.n_rows = size
        self.n_columns = size
        self.wall = []
        
    def is_in_bounds(self, loc):
        valid_y = (loc[0] <= (self.n_rows-1)) & (loc[0] >= 0)
        valid_x = (loc[1] <= (self.n_columns-1)) & (loc[0] >= 0)
        
        return valid_y & valid_x
        
    def get_loc(self, loc):
        if self.is_in_bounds(loc):
            try:
                return self.grid[loc[0]][loc[1]]
            except IndexError:
                print((loc[0], loc[1]))
                raise IndexError()
        else:
            return None
    
    def is_occupied(self, loc):
        return self.get_loc(loc) is not None

    def set_loc(self, loc, object):
        if self.is_occupied(loc):
            raise ValueError("space is occupied!")
        else:
            self.grid[loc[0]][loc[1]] = object
    
    def clear_loc(self, loc):
        #TODO: should we just enable overwrite in set_loc?
        self.grid[loc[0]][loc[1]] = None
        
    def add_wall(self, x1, y1, x2, y2):
        assert all([x >= 0 for x in [x1, x2, y1, y2]])
        
        for i in range(x1, x2+1):
            for j in range(y1, y2+1):
                Block(i, j, self) #TODO: should we track these somewhere?
    
    #TODO: following are duplicated from shapeselector
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

    def contains(self, loc, points):
        return self._contains(loc, points) | self._contains(loc, list(reversed(points))) #TODO: IMPROVE
    
    def add_shape(self, points):
        for i in range(self.n_rows):
            for j in range(self.n_columns):
                if self.contains((i,j), points):
                    inhabitant = self.get_loc((i,j))
                    can_move = getattr(inhabitant, "move", None) is not None
                    if can_move:
                        location = random.sample(range(self.size), 2)
                        while self.is_occupied(location):
                            location = random.sample(range(self.size), 2)
                        inhabitant.move(location)
                    else:
                        self.clear_loc((i,j)) 
                    Block((i,j), self)
                
        
    

class Block:
    def __init__(self,loc, world: World):
        self.y = loc[0]
        self.x = loc[1]
        self.loc = loc
        world.set_loc(self.loc, self)
        
        self.color = (169, 169, 169)
        