

class World:
    def __init__(self, size):
        self.grid = [[None] * size for _ in range(size)]
        self.size = size
        self.n_rows = size
        self.n_columns = size
        
    def is_occupied(self, loc):
        y = loc[0]
        x = loc[1]
        try:
            return self.grid[y][x] is not None
        except IndexError as e:
            print(x, y)
            print(len(self.grid))
            print(len(self.grid[0]))
            raise e

    def set_loc(self, loc, object):
        if self.is_occupied(loc):
            raise ValueError("space is occupied!")
        else:
            self.grid[loc[0]][loc[1]] = object
    
    def clear_loc(self, loc):
        #TODO: should we just enable overwrite in set_loc?
        self.grid[loc[0]][loc[1]] = None
        
    

