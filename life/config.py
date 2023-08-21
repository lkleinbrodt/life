import colorsys
import numpy as np
import os

GENOME_SIZE = 24
N_INTERNAL_NEURONS = 6
MUTATION_RATE = .01
MUTATION_MAGNITUDE = .5
GENERATION_LENGTH = 50
POPULATION_SIZE = 750
CONNECTION_MAGNITUDE = 4.0

def get_configs():
    out = {
        'CONNECTION_MAGNITUDE': CONNECTION_MAGNITUDE,
        'GENOME_SIZE': GENOME_SIZE,
        'N_INTERNAL_NEURONS': N_INTERNAL_NEURONS,
        'MUTATION_RATE': MUTATION_RATE,
        'MUTATION_MAGNITUDE': MUTATION_MAGNITUDE,
        'GENERATION_LENGTH': GENERATION_LENGTH,
        'POPULATION_SIZE': POPULATION_SIZE,
    }
    return out

AVAILABLE_RECEPTORS = [
    'latitude',
    'longitude',
    'north_blocked',
    'south_blocked',
    'east_blocked',
    'west_blocked',
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

COLOR_DICT = {
    neuron: NEURON_COLORS[i]
    for i, neuron in enumerate(AVAILABLE_ACTORS + AVAILABLE_RECEPTORS + ['internal'])
}


script_dir = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(script_dir)
# Get the parent directory of the script's directory
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')