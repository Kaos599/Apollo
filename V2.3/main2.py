import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from faker import Faker
import random
import pandas as pd

class OptionWindow(tk.Toplevel):
    def __init__(self, parent, app_instance):
        super().__init__(parent)
        self.title("Create Option")

        self.parent = parent
        self.app_instance = app_instance
        self.option_type_var = tk.StringVar()
        self.option_type_var.set("Generate Response")

        self.option_type_label = tk.Label(self, text="Select Option Type:")
        self.option_type_label.grid(row=0, column=0, padx=10, pady=5)

        self.option_type_dropdown = ttk.Combobox(self, textvariable=self.option_type_var, state="readonly")
        self.option_type_dropdown['values'] = ["Generate Response", "Generate Weighted Choice"]
        self.option_type_dropdown.grid(row=0, column=1, padx=10, pady=5)

        self.create_button = tk.Button(self, text="Create", command=self.create_option)
        self.create_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    def create_option(self):
        option_type = self.option_type_var.get()
        if option_type == "Generate Response":
            self.app_instance.add_option(option_type)
        elif option_type == "Generate Weighted Choice":
            self.app_instance.add_weighted_choice_option()

        self.destroy()

class DefineChoicesWindow(tk.Toplevel):
    def __init__(self, parent, name_entry):
        super().__init__(parent)
        self.title("Define Choices")
        self.parent = parent
        self.name_entry = name_entry
        self.generator = WeightedChoiceGenerator()

        self.choice_label = tk.Label(self, text="Choice:")
        self.choice_label.grid(row=0, column=0, padx=10, pady=5)

        self.choice_entry = tk.Entry(self)
        self.choice_entry.grid(row=0, column=1, padx=10, pady=5)

        self.probability_label = tk.Label(self, text="Probability (0-1):")
        self.probability_label.grid(row=1, column=0, padx=10, pady=5)

        self.probability_entry = tk.Entry(self)
        self.probability_entry.grid(row=1, column=1, padx=10, pady=5)

        self.add_button = tk.Button(self, text="Add", command=self.add_choice)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        self.show_choices_button = tk.Button(self, text="Show Choices", command=self.show_choices)
        self.show_choices_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.finish_button = tk.Button(self, text="Finish", command=self.finish)
        self.finish_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        self.finish_button.grid_remove()

    def add_choice(self):
        choice = self.choice_entry.get()
        probability = self.probability_entry.get()

        try:
            probability = float(probability)
            if not 0 <= probability <= 1:
                messagebox.showerror("Error", "Probability must be between 0 and 1")
                return

            self.generator.add_choice_entry(choice, probability)
            self.choice_entry.delete(0, tk.END)
            self.probability_entry.delete(0, tk.END)

            total_prob = sum(self.generator.choices.values())
            if total_prob >= 1.0:
                self.finish_button.grid()
        except ValueError:
            messagebox.showerror("Error", "Invalid probability value")

    def show_choices(self):
        choices_str = "\n".join([f"{choice}: {probability}" for choice, probability in self.generator.choices.items()])
        messagebox.showinfo("Weighted Choices", choices_str)

    def finish(self):
        self.name_entry.weighted_choices = self.generator
        self.destroy()

class SyntheticDataGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Apollo - Synthetic Data Generator")

        self.fake = Faker()
        self.options = []
        self.checkboxes = []

        self.create_entry_button = tk.Button(root, text="Create Entry", command=self.create_option_window)
        self.create_entry_button.grid(row=0, column=0, padx=10, pady=5)

        self.delete_entry_button = tk.Button(root, text="Delete Selected", command=self.delete_selected)
        self.delete_entry_button.grid(row=0, column=1, padx=10, pady=5)

        self.entry_frame = tk.Frame(root)
        self.entry_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.output_file_path_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
        self.output_file_path_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.output_file_path_label = tk.Label(self.output_file_path_frame, text="Output File Path:")
        self.output_file_path_label.grid(row=0, column=0, padx=5, pady=5)
        self.output_file_path_var = tk.StringVar()
        self.output_file_path_entry = tk.Entry(self.output_file_path_frame, textvariable=self.output_file_path_var)
        self.output_file_path_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_button = tk.Button(self.output_file_path_frame, text="Browse", command=self.browse_output_path)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        self.output_format_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
        self.output_format_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.output_format_label = tk.Label(self.output_format_frame, text="Output Format:")
        self.output_format_label.grid(row=0, column=0, padx=5, pady=5)
        self.output_format_var = tk.StringVar()
        self.output_format_dropdown = ttk.Combobox(self.output_format_frame, textvariable=self.output_format_var, state="readonly")
        self.output_format_dropdown['values'] = ['CSV', 'Text']
        self.output_format_dropdown.current(0)
        self.output_format_dropdown.grid(row=0, column=1, padx=5, pady=5)

        self.num_entries_label = tk.Label(root, text="Number of Entries:")
        self.num_entries_label.grid(row=4, column=0, padx=10, pady=5)

        self.num_entries_var = tk.StringVar()
        self.num_entries_entry = tk.Entry(root, textvariable=self.num_entries_var)
        self.num_entries_entry.grid(row=4, column=1, padx=10, pady=5)

        self.generate_button = tk.Button(root, text="Generate", command=self.generate_data)
        self.generate_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def create_option_window(self):
        option_window = OptionWindow(self.root, self)

    def add_option(self, option_type):
        var = tk.StringVar(value="0")
        checkbox = tk.Checkbutton(self.entry_frame, variable=var)
        checkbox.grid(row=len(self.options), column=0, padx=5, pady=5)
        self.checkboxes.append(checkbox)

        label = tk.Label(self.entry_frame, text=option_type)
        label.grid(row=len(self.options), column=1, padx=5, pady=5)

        if option_type == "Generate Response":
            name_label = tk.Label(self.entry_frame, text="Name:")
            name_label.grid(row=len(self.options), column=2, padx=5, pady=5)

            name_entry = tk.Entry(self.entry_frame)
            name_entry.grid(row=len(self.options), column=3, padx=5, pady=5)

            probability_label = tk.Label(self.entry_frame, text="Probability (0-1):")
            probability_label.grid(row=len(self.options), column=4, padx=5, pady=5)

            probability_entry = tk.Entry(self.entry_frame)
            probability_entry.grid(row=len(self.options), column=5, padx=5, pady=5)

            self.options.append((option_type, var, name_entry, probability_entry))
        else:
            self.options.append((option_type, var))

    def add_weighted_choice_option(self):
        var = tk.StringVar(value="0")
        checkbox = tk.Checkbutton(self.entry_frame, variable=var)
        checkbox.grid(row=len(self.options), column=0, padx=5, pady=5)
        self.checkboxes.append(checkbox)

        label = tk.Label(self.entry_frame, text="Generate Weighted Choice")
        label.grid(row=len(self.options), column=1, padx=5, pady=5)

        name_label = tk.Label(self.entry_frame, text="Name:")
        name_label.grid(row=len(self.options), column=2, padx=5, pady=5)

        name_entry = tk.Entry(self.entry_frame)
        name_entry.grid(row=len(self.options), column=3, padx=5, pady=5)

        weighted_choice_button = tk.Button(self.entry_frame, text="Define Choices", command=lambda: self.define_weighted_choices(name_entry))
        weighted_choice_button.grid(row=len(self.options), column=4, padx=5, pady=5)

        self.options.append(("Generate Weighted Choice", var, name_entry))

    def define_weighted_choices(self, name_entry):
        DefineChoicesWindow(self.root, name_entry)

    def delete_selected(self):
        selected_indices = []
        for i, option_tuple in enumerate(self.options):
            if len(option_tuple) > 1:
                _, var, *_ = option_tuple
                if var.get() == '1':
                    selected_indices.append(i)

        for index in reversed(selected_indices):
            self.options.pop(index)
            self.checkboxes[index].destroy()

        self.update_options_display()

    def update_options_display(self):
        for widget in self.entry_frame.winfo_children():
            widget.destroy()

        self.checkboxes = []
        for i, (option, _, *entries) in enumerate(self.options):
            checkbox = tk.Checkbutton(self.entry_frame)
            checkbox.grid(row=i, column=0, padx=5, pady=5)
            self.checkboxes.append(checkbox)

            label = tk.Label(self.entry_frame, text=option)
            label.grid(row=i, column=1, padx=5, pady=5)

            if option == "Generate Response":
                name_entry, probability_entry = entries
                name_entry.grid(row=i, column=2, padx=5, pady=5)
                probability_entry.grid(row=i, column=3, padx=5, pady=5)
            elif option == "Generate Weighted Choice":
                name_entry = entries[0]
                name_entry.grid(row=i, column=2, padx=5, pady=5)
                weighted_choice_button = tk.Button(self.entry_frame, text="Define Choices", command=lambda: self.define_weighted_choices(name_entry))
                weighted_choice_button.grid(row=i, column=4, padx=5, pady=5)

                view_choices_button = tk.Button(self.entry_frame, text="View Choices", command=lambda: self.view_weighted_choices(name_entry))
                view_choices_button.grid(row=i, column=5, padx=5, pady=5)

    def view_weighted_choices(self, name_entry):
        generator = name_entry.weighted_choices
        if generator is None:
            messagebox.showerror("Error", "Weighted choices not defined.")
            return

        choices_str = "\n".join([f"{choice}: {probability}" for choice, probability in generator.choices.items()])
        messagebox.showinfo("Weighted Choices", choices_str)

    def browse_output_path(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt")])
        self.output_file_path_var.set(filename)

    def generate_response(self, probability):
        return 'Yes' if random.random() < probability else 'No'

    def generate_weighted_choice(self, choices):
        population = [val for val, cnt in choices.items() for _ in range(int(cnt * 100))]
        return random.choice(population)

    def generate_data(self):
        num_entries_str = self.num_entries_var.get()
        try:
            num_entries = int(num_entries_str)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of entries.")
            return

        if num_entries <= 0:
            messagebox.showerror("Error", "Number of entries must be greater than zero.")
            return

        output_path = self.output_file_path_var.get()
        output_format = self.output_format_var.get()

        survey_data = []
        for _ in range(num_entries):
            entry_data = {}
            for option_type, _, *entries in self.options:
                if option_type == "Generate Response":
                    name_entry, probability_entry = entries
                    entry_name = name_entry.get()
                    probability_yes = float(probability_entry.get())
                    entry_data[entry_name] = self.generate_response(probability_yes)
                elif option_type == "Generate Weighted Choice":
                    entry_name = entries[0].get()
                    weighted_choices_generator = entries[0].weighted_choices
                    if weighted_choices_generator is None:
                        messagebox.showerror("Error", "Weighted choices not defined.")
                        return
                    entry_data[entry_name] = weighted_choices_generator.generate_weighted_choice()

            survey_data.append(entry_data)

        survey_df = pd.DataFrame(survey_data)

        if output_format == 'CSV':
            survey_df.to_csv(output_path, index=False)
        elif output_format == 'Text':
            survey_df.to_csv(output_path, index=False, sep='\t')

        messagebox.showinfo("Success", "Data generation completed.")

class WeightedChoiceGenerator:
    def __init__(self):
        self.choices = {}

    def add_choice_entry(self, option, probability):
        # Add the option and its probability to the choices dictionary
        self.choices[option] = float(probability)

    def generate_weighted_choice(self):
        population = [val for val, cnt in self.choices.items() for _ in range(int(cnt * 100))]
        return random.choice(population)

def main():
    root = tk.Tk()
    root.iconbitmap('Frame 14.ico')
    app = SyntheticDataGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()


