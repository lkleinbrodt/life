from world import World
from population import Population, load_population
from selection import ShapeSelector, DiseaseSelector
import game
from config import *
import pygame
import numpy as np
import copy
import argparse
import simulation
import parameters
from settings_gui import ParameterEditor
import tkinter as tk
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the simulation.")
    parser.add_argument("-g", "--game-mode", action = 'store_true', help = 'Run in game mode')
    args = parser.parse_args()
    
    
    
    # the_population = load_population(DATA_DIR+'/population.pkl')
    # the_world = the_population.world
    
    if args.game_mode:
        print('playing the game')
        

        root = tk.Tk()
        app = ParameterEditor(root)
        root.mainloop()
        
        params = parameters.Parameters(
            **app.get_parameters()
        )
        
        pygame.init()
        pygame.display.set_caption("Game of Life") 
        
        
        if params.selector == 'shape':
            screen = pygame.display.set_mode(
                (game.WIDTH, #+ game.SIDEBAR_WIDTH, 
                game.HEIGHT)
            )
            cell_size = game.WIDTH // params.world_size
            params.selector_params = game.shape_screen(screen, cell_size)
        elif params.selector == 'disease':
            pass
            
        sim = simulation.Simulation(params)
        
        print(sim.population.directory)
        
        screen = pygame.display.set_mode(
            (game.WIDTH + game.SIDEBAR_WIDTH, 
            game.HEIGHT)
        )
        
        game.gameplay(screen, sim)
    else:
        
        print('running the sim')
        
        params = parameters.Parameters(
            selector = 'disease'
        ) #TODO: user input
        
        sim = simulation.Simulation(params)
        print(sim.population.directory)
        while True:
            sim.step()