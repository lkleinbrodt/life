import tkinter as tk
from tkinter import ttk
from config import *

class ParameterEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Parameter Editor")
        
        self.parameters = {
            "genome_size": tk.IntVar(value=GENOME_SIZE),
            "selection_criteria": tk.StringVar(value="Fitness"),
            "n_internal_neurons": tk.IntVar(value=N_INTERNAL_NEURONS),
            "mutation_rate": tk.DoubleVar(value=MUTATION_RATE),
            "mutation_magnitude": tk.DoubleVar(value=MUTATION_MAGNITUDE),
            "generation_length": tk.IntVar(value=GENERATION_LENGTH),
            "population_size": tk.IntVar(value=POPULATION_SIZE),
        }
        
        self.create_widgets()
        
    def create_widgets(self):
        for i, (param, var) in enumerate(self.parameters.items()):
            label = tk.Label(self.root, text=f"{param.capitalize()}:")
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            
            if isinstance(var, tk.StringVar):
                options = ["Hemisphere", "Box"]
                dropdown = ttk.Combobox(self.root, textvariable=var, values=options)
                dropdown.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            else:
                entry = tk.Entry(self.root, textvariable=var)
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")

        save_button = tk.Button(self.root, text="Save Parameters", command=self.save_parameters)
        save_button.grid(row=len(self.parameters), columnspan=2, pady=10)
        
    def save_parameters(self):
        # with open("parameters.txt", "w") as file:
        #     for param, var in self.parameters.items():
        #         value = var.get()
        #         file.write(f"{param}: {value}\n")
        return self.parameters

if __name__ == "__main__":
    root = tk.Tk()
    app = ParameterEditor(root)
    tk.Button(root, text="Quit", command=root.destroy).pack() #button to close the window
    root.mainloop()