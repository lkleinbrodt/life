from world import World
from population import Population
from selection import BoxSelector
from config import *
import pygame
import numpy as np
import copy
import argparse

def sim(world: World, population: Population):
    #TODO: make this a class with .step and then you can use it in game and ensure it's the exact same?
    i = 0
    while True:
        i += 1
        population.step(world)
        if i % 100 == 0:
            population.save()



    
def game(world: World, population: Population):
    # Initialize Pygame
    pygame.init()

    # Constants
    # CELL_SIZE = 10
    # WIDTH, HEIGHT = world.n_rows * CELL_SIZE, world.n_columns * CELL_SIZE
    WIDTH, HEIGHT = 800, 800
    ARRAY_SIZE = world.size
    CELL_SIZE = WIDTH // ARRAY_SIZE
    SIDEBAR_WIDTH = 200  # Width of the sidebar
    
    # Create the screen

    screen = pygame.display.set_mode((WIDTH + SIDEBAR_WIDTH, HEIGHT))
    pygame.display.set_caption("Game of Life")
    
    
    def render_wrapped_text(text, font, color, rect, max_lines=None):
        lines = text.split('\n')
        rendered_lines = []

        for line in lines:
            if max_lines is None or len(rendered_lines) < max_lines:
                rendered_text = font.render(line, True, color)
                rendered_lines.append(rendered_text)

        total_height = sum(text.get_height() for text in rendered_lines)
        y_offset = rect.centery - total_height // 2

        for rendered_text in rendered_lines:
            text_rect = rendered_text.get_rect(centerx=rect.centerx, top=y_offset)
            screen.blit(rendered_text, text_rect)
            y_offset += text_rect.height
        
    ###    
    
    black = (0, 0, 0)
    white = (255, 255, 255)
    font = pygame.font.Font(None, 36)
    def render_text(text, x, y):
        text_surface = font.render(text, True, white)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        screen.blit(text_surface, text_rect)

    running = True
    clock_speed = 10
    paused = False
    drawing = False
    clock = pygame.time.Clock()
    iterations = 0
    while running:
        iterations += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    clock_speed += 10  # Slow down the clock
                    print('Clock Speed: ', clock_speed)
                elif event.key == pygame.K_s:
                    if clock_speed >= 10:
                        clock_speed -= 10  # Speed up the clock
                    print('Clock Speed: ', clock_speed)
                elif event.key == pygame.K_p:  # Pause/unpause the simulation
                    paused = not paused
                    print('Paused:', paused)
                elif event.key == pygame.K_d:  # Enter drawing mode
                    drawing = True
                    paused = True
                    current_shape = []
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if drawing:
                    row = event.pos[1] // CELL_SIZE
                    col = event.pos[0] // CELL_SIZE
                    current_shape.append((row, col))

            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    drawing = False
                    captured_shape = copy.deepcopy(current_shape)
                    current_shape = []
                    print('Captured Shape:', captured_shape)

        if not paused:
            population.step(world)
        # print(f'Step {iterations}')
        # print(population.get_organism(5))

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the array
        for i in range(world.n_rows):
            for j in range(world.n_columns):
                grid_item = world.grid[i][j]
                if grid_item is None:
                    color = (0, 0, 0)
                else:
                    color = grid_item.color

                pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(screen, (50, 50, 50), (WIDTH, 0, SIDEBAR_WIDTH, HEIGHT))
        
        # n_organisms = len(population.population)
        render_text("Press 'p' to pause/unpause", WIDTH, HEIGHT - 100)
        render_text(f"Generation: {population.generation_count}", WIDTH, 20)
        render_wrapped_text(f"Information: \n{population.generation_data.get('selection_data', '')}", font, white, pygame.Rect(WIDTH, 100, 20, HEIGHT), max_lines=5)
        
        pygame.display.flip()
        clock.tick(clock_speed)  # Limit the frame rate

    pygame.quit()

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the simulation.")
    parser.add_argument("-g", "--game-mode", choices=['game', "simulation"], default="simulation", help="Choose the run mode.")
    args = parser.parse_args()
    
    the_world = World(128)
    the_population = Population(
        world = the_world, 
        n_organisms=POPULATION_SIZE, 
        selector = BoxSelector(.4, .4, .6, .6, the_world)
    )
    
    if args.game_mode == "game":
        print('playing the game')
        game(the_world, the_population)
    elif args.game_mode == "simulation":
        print('running the sim')
        sim(the_world, the_population)