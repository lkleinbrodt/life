import pygame
import copy
import sys
from simulation import Simulation
from config import *
from selection import ShapeSelector

WIDTH, HEIGHT = 800, 800
SIDEBAR_WIDTH = 200  # Width of the sidebar

black = (0, 0, 0)
white = (255, 255, 255)
update_button_color = (0, 255, 0)

### A function for pygame that renders text and wraps it to fit within a rectangle


    
    
    


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
        
def shape_screen(screen, cell_size):
    font = pygame.font.Font(None, 36)
    selected_points = []
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
            
                row = event.pos[1] // cell_size
                col = event.pos[0] // cell_size
                print((row, col))
                selected_points.append((row, col))
                    
                if len(selected_points) == 4:
                    # simulation.world.add_wall(x1, y1, x2, y2) #not adding walls here, put elsewhere!
                    return selected_points
        
        screen.fill((0, 0, 0))
        
        render_wrapped_text(screen, 'Click 4 points to mark the boundaries of the zone', font, white, 0, 0, 200)


def draw_polygon_alpha(surface, color, points, cell_size = 1):
    ly, lx = zip(*points)
    min_x, min_y, max_x, max_y = min(lx)*cell_size, min(ly)*cell_size, max(lx)*cell_size, max(ly)*cell_size
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x*cell_size - min_x, y*cell_size - min_y) for y,x in points])
    surface.blit(shape_surf, target_rect)
    
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
                    selected_points = []
                    if drawing:
                        paused = True
                    else:
                        paused = False
            
            

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

                
                # if isinstance(simulation.selector, ShapeSelector):
                #     if simulation.selector.contains((j, i)):
                #         print('inside')
                #         pygame.draw.rect(screen, white, (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                #     else:
                #         pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                # else:
                pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(screen, (50, 50, 50), (WIDTH, 0, SIDEBAR_WIDTH, HEIGHT))
        
        draw_polygon_alpha(screen, (255, 255, 255, 100), simulation.selector.points, CELL_SIZE)
        
        # n_organisms = len(population.population)
        
        # Draw the sidebar
        side_bar_texts = [
            "Press 'f' to speed up the clock",
            "Press 's' to slow down the clock",
            "Press 'p' to pause/unpause",
            '',
            f"Generation: {simulation.population.generation_count}",
            f"Information: \n{simulation.population.generation_data.get(str(simulation.population.generation_count))}"
        ]
        
        y_offset = 0
        for text in side_bar_texts:
            render_wrapped_text(screen, text, font, white, WIDTH+100, y_offset, 200)
            y_offset += 100
        
        pygame.display.flip()
        clock.tick(clock_speed)  # Limit the frame rate

    pygame.quit()

def render_wrapped_text(screen, text, font, color, x, y, allowed_width):
    # first, split the text into words
    words = text.split()

    # now, construct lines out of these words
    lines = []
    while len(words) > 0:
        # get as many words as will fit within allowed_width
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        # add a line consisting of those words
        line = ' '.join(line_words)
        lines.append(line)

    # now we've split our text into lines that fit into the width, actually
    # render them

    # we'll render each line below the last, so we need to keep track of
    # the culmative height of the lines we've rendered so far
    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)

        # (tx, ty) is the top-left of the font surface
        tx = x - fw / 2
        ty = y + y_offset

        font_surface = font.render(line, True, color)
        screen.blit(font_surface, (tx, ty))

        y_offset += fh