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
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the simulation.")
    parser.add_argument("-g", "--game-mode", action = 'store_true', help = 'Run in game mode')
    args = parser.parse_args()
    
    params = parameters.Parameters(
        selector = 'disease'
    ) #TODO: user input
    
    sim = simulation.Simulation(params)
    
    # the_population = load_population(DATA_DIR+'/population.pkl')
    # the_world = the_population.world
    
    if args.game_mode:
        print('playing the game')
        pygame.init()
        screen = pygame.display.set_mode((game.WIDTH + game.SIDEBAR_WIDTH, game.HEIGHT))
        pygame.display.set_caption("Game of Life") 
        game.gameplay(screen, sim)
    else:
        print('running the sim')
        print(sim.population.directory)
        while True:
            sim.step()