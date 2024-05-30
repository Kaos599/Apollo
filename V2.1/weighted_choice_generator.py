import random

class WeightedChoiceGenerator:
    def __init__(self):
        self.choices = {}

    def add_choice_entry(self, option, probability):
        # Add the option and its probability to the choices dictionary
        self.choices[option] = float(probability)

    def generate_weighted_choice(self):
        population = [val for val, cnt in self.choices.items() for _ in range(int(cnt * 100))]
        return random.choice(population)
