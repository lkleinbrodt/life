

class World:
    def __init__(self, size):
        self.grid = [[None] * size for _ in range(size)]
        self.size = size
        self.n_rows = size
        self.n_columns = size
        
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
        
    

