from world import World
from population import Population, load_population
from selection import BoxSelector
import game
from config import *
import pygame
import numpy as np
import copy
import argparse

def sim(world: World, population: Population):
    #TODO: make this a class with .step and then you can use it in game and ensure it's the exact same?
    i = 0
    prev_gen = 0
    while True:
        i += 1
        population.step(world)
        if (i % (GENERATION_LENGTH * 10)) == 0:
            # prev_gen = population.generation_count
            print('Generation:', population.generation_count)
            population.save()
            population.save_generation_data()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the simulation.")
    parser.add_argument("-g", "--game-mode", action = 'store_true', help = 'Run in game mode')
    args = parser.parse_args()
    
    the_world = World(128)
    the_population = Population(
        world = the_world, 
        n_organisms=POPULATION_SIZE, 
        selector = BoxSelector(.4, 0.0, .6, 1.0, the_world)
    )
    # the_population = load_population(DATA_DIR+'/population.pkl')
    # the_world = the_population.world
    
    if args.game_mode:
        print('playing the game')
        pygame.init()
        screen = pygame.display.set_mode((game.WIDTH + game.SIDEBAR_WIDTH, game.HEIGHT))
        pygame.display.set_caption("Game of Life") 
        game.gameplay(screen, the_world, the_population)
    else:
        print('running the sim')
        sim(the_world, the_population)