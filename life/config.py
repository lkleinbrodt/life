import colorsys
import numpy as np
import os

CONNECTION_MAGNITUDE = 4.0
GENOME_SIZE = 8
N_INTERNAL_NEURONS = 3
MUTATION_RATE = .001
MUTATION_MAGNITUDE = .5
GENERATION_LENGTH = 50
POPULATION_SIZE = 500

AVAILABLE_RECEPTORS = [
    'latitude',
    'longitude',
]

AVAILABLE_ACTORS = [
    'move_north',
    'move_south',
    'move_east',
    'move_west',
]

AVAILABLE_INTERNALS = [f'internal_{i}' for i in range(N_INTERNAL_NEURONS)]

def generate_uniform_colors(n):
    colors = []
    for i in range(n):
        hue = i / n  # Uniformly spaced hue values
        rgb_color = colorsys.hsv_to_rgb(hue, 1.0, 1.0)  # Convert HSV to RGB
        int_color = tuple(float(val * 255) for val in rgb_color)  # Convert to integer values (0-255)
        colors.append(np.array(int_color))
    return colors

NEURON_COLORS = generate_uniform_colors(len(AVAILABLE_RECEPTORS) + len(AVAILABLE_ACTORS) + 1)


script_dir = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(script_dir)
# Get the parent directory of the script's directory
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')