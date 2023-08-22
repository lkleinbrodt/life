from world import World
from population import Population, load_population
from selection import BoxSelector, DiseaseSelector
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
        
        sim = simulation.Simulation(params)
        app.parameters
        
        print(sim.population.directory)
        pygame.init()
        screen = pygame.display.set_mode((game.WIDTH + game.SIDEBAR_WIDTH, game.HEIGHT))
        pygame.display.set_caption("Game of Life") 
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