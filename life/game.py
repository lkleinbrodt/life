import pygame
import copy
import sys
from simulation import Simulation
from config import *

WIDTH, HEIGHT = 800, 800
SIDEBAR_WIDTH = 200  # Width of the sidebar

black = (0, 0, 0)
white = (255, 255, 255)
update_button_color = (0, 255, 0)

def render_wrapped_text(screen, text, font, color, rect, max_lines=None):
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

GAME_PARAMETERS = {
    "genome_size": 10,
    "selection_criteria": "Fitness",
    "num_neurons": 5,
    "mutation_rate": 0.1,
    "mutation_magnitude": 0.2,
    "generation_length": 100,
    "population_size": 50,
}

def settings_page(screen):
    font = pygame.font.Font(None, 36)
    update_button = pygame.Rect(350, 500, 100, 40)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    input_text = ''
    active_input = None
    inputs = {}
    
    y = 100
    for param, value in GAME_PARAMETERS.items():
        inputs[param] = pygame.Rect(300, y - 20, 100, 30)
        y += 50
    
    def display_parameters():
        for param, value in GAME_PARAMETERS.items():
            text = f"{param}:"
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(topleft=(50, inputs[param].centery - 15))
            screen.blit(text_surface, text_rect)

            pygame.draw.rect(screen, (255, 255, 255), inputs[param], 2)
            input_text = font.render(str(value), True, (255, 255, 255))
            input_rect = input_text.get_rect(midleft=(inputs[param].left + 10, inputs[param].centery))
            screen.blit(input_text, input_rect)
            
    def draw_buttons():
        pygame.draw.rect(screen, update_button_color, update_button)
        update_text = font.render("Update", True, (0, 0, 0))
        update_rect = update_text.get_rect(center=update_button.center)
        screen.blit(update_text, update_rect)
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("click", event.pos)
                active_input = None
                for key, input in inputs.items():
                    if input.collidepoint(event.pos):
                        print('collide', key)
                        active_input = key
                        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
                GAME_PARAMETERS[active_input] = input_text
                print(input_text)
                
                    
        display_parameters()
        # draw_buttons()
        pygame.display.flip()
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH + SIDEBAR_WIDTH, HEIGHT))
    pygame.display.set_caption("Game of Life")
    
    settings_page(screen)
    
    #input screen


def gameplay(screen, simulation: Simulation):
    font = pygame.font.Font(None, 36)
    ARRAY_SIZE = simulation.world.size
    CELL_SIZE = WIDTH // ARRAY_SIZE
    
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
                    drawing = not drawing
                    if drawing:
                        paused = True
                        current_shape = []
                    else:
                        paused = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if drawing:
                    row = event.pos[1] // CELL_SIZE
                    col = event.pos[0] // CELL_SIZE
                    current_shape.append((row, col))

            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    captured_shape = copy.deepcopy(current_shape)
                    current_shape = []
                    print('Captured Shape:', captured_shape)

        if not paused:
            simulation.step()
        # print(f'Step {iterations}')
        # print(population.get_organism(5))

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the array
        for i in range(simulation.world.n_rows):
            for j in range(simulation.world.n_columns):
                grid_item = simulation.world.grid[i][j]
                if grid_item is None:
                    color = (0, 0, 0)
                else:
                    color = grid_item.color

                pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(screen, (50, 50, 50), (WIDTH, 0, SIDEBAR_WIDTH, HEIGHT))
        
        # n_organisms = len(population.population)
        render_wrapped_text(screen, "Press 'p' to pause/unpause", font, white, pygame.Rect(WIDTH, 100, 20, HEIGHT - 100))
        render_wrapped_text(screen, f"Generation: {simulation.population.generation_count}", font, white, pygame.Rect(WIDTH, 100, 20, 20))
        render_wrapped_text(screen, f"Information: \n{simulation.population.generation_data.get('selection_data', '')}", font, white, pygame.Rect(WIDTH, 100, 20, HEIGHT), max_lines=5)
        
        pygame.display.flip()
        clock.tick(clock_speed)  # Limit the frame rate

    pygame.quit()
    
    
if __name__ == '__main__':
    main()