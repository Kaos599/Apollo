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
        self.app_instance.generate_data()  # Call generate_data here
        self.destroy()

class SurveyGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Survey Data Generator")

        self.fake = Faker()
        self.options = []
        self.checkboxes = []

        self.create_entry_button = tk.Button(root, text="Create Entry", command=self.create_option_window)
        self.create_entry_button.grid(row=0, column=0, padx=10, pady=5)

        self.delete_entry_button = tk.Button(root, text="Delete Selected", command=self.delete_selected)
        self.delete_entry_button.grid(row=0, column=1, padx=10, pady=5)

        self.num_entries_label = tk.Label(root, text="Number of Entries:")
        self.num_entries_label.grid(row=1, column=0, padx=10, pady=5)

        self.num_entries_var = tk.StringVar()
        self.num_entries_entry = tk.Entry(root, textvariable=self.num_entries_var)
        self.num_entries_entry.grid(row=1, column=1, padx=10, pady=5)

        self.output_file_label = tk.Label(root, text="Output File Path:")
        self.output_file_label.grid(row=2, column=0, padx=10, pady=5)

        self.output_file_path_var = tk.StringVar()
        self.output_file_entry = tk.Entry(root, textvariable=self.output_file_path_var)
        self.output_file_entry.grid(row=2, column=1, padx=10, pady=5)

        self.output_format_label = tk.Label(root, text="Output Format:")
        self.output_format_label.grid(row=3, column=0, padx=10, pady=5)

        self.output_format_var = tk.StringVar()
        self.output_format_dropdown = ttk.Combobox(root, textvariable=self.output_format_var, state="readonly")
        self.output_format_dropdown['values'] = ["CSV", "Text"]
        self.output_format_dropdown.grid(row=3, column=1, padx=10, pady=5)

        self.generate_button = tk.Button(root, text="Generate Data", command=self.generate_data)
        self.generate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def create_option_window(self):
        OptionWindow(self.root, self)

    def add_option(self, option_type):
        row = len(self.options) + 5
        option_label = tk.Label(self.root, text=option_type)
        option_label.grid(row=row, column=0, padx=10, pady=5)

        name_entry = tk.Entry(self.root)
        name_entry.grid(row=row, column=1, padx=10, pady=5)

        probability_entry = tk.Entry(self.root)
        probability_entry.grid(row=row, column=2, padx=10, pady=5)

        self.options.append((option_type, option_label, name_entry, probability_entry))

    def add_weighted_choice_option(self):
        row = len(self.options) + 5
        option_label = tk.Label(self.root, text="Generate Weighted Choice")
        option_label.grid(row=row, column=0, padx=10, pady=5)

        name_entry = tk.Entry(self.root)
        name_entry.grid(row=row, column=1, padx=10, pady=5)

        self.options.append(("Generate Weighted Choice", option_label, name_entry))

    def get_weighted_choices(self):
        weighted_values = simpledialog.askstring("Input", "Enter weighted values (e.g., 'hi:0.1,hello:0.9'):")
        if not weighted_values:
            messagebox.showerror("Error", "Please enter weighted values.")
            return None
        try:
            choices = [item.split(":") for item in weighted_values.split(",")]
            return [(choice[0], float(choice[1])) for choice in choices]
        except Exception as e:
            messagebox.showerror("Error", "Invalid format for weighted values. Please use 'value:weight' format.")
            return None

    def generate_response(self, probability_yes):
        return 'Yes' if random.random() < probability_yes else 'No'

    def generate_weighted_choice(self, weighted_choices):
        total = sum(weight for choice, weight in weighted_choices)
        rand = random.uniform(0, total)
        upto = 0
        for choice, weight in weighted_choices:
            if upto + weight >= rand:
                return choice
            upto += weight
        assert False, "Shouldn't get here"

    def delete_selected(self):
        selected_indices = [i for i, var in enumerate(self.checkboxes) if var.get()]
        for index in sorted(selected_indices, reverse=True):
            for widget in self.options[index][1:]:
                widget.grid_forget()
            del self.options[index]
            del self.checkboxes[index]

    def generate_data(self):
        try:
            num_entries = int(self.num_entries_var.get())
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
            entry_data = {'Entry Name': '', 'Response': ''}
            for option_type, _, *entries in self.options:
                if option_type == "Generate Response":
                    name_entry, probability_entry = entries
                    entry_name = name_entry.get()
                    try:
                        probability_yes = float(probability_entry.get())
                    except ValueError:
                        messagebox.showerror("Error", "Please enter a valid probability for response generation.")
                        return
                    entry_data['Entry Name'] = entry_name
                    entry_data['Response'] = self.generate_response(probability_yes)
                elif option_type == "Generate Weighted Choice":
                    entry_name = entries[0].get()
                    weighted_choices = self.get_weighted_choices()
                    if weighted_choices is None:
                        return
                    entry_data['Entry Name'] = entry_name
                    entry_data['Response'] = self.generate_weighted_choice(weighted_choices)

            survey_data.append(entry_data)

        survey_df = pd.DataFrame(survey_data)
        print("Generated Survey Data:")
        print(survey_df)  # Print generated data for debugging

        if output_format == 'CSV':
            survey_df.to_csv(output_path, index=False)
        elif output_format == 'Text':
            survey_df.to_csv(output_path, index=False, sep='\t')

        messagebox.showinfo("Success", "Data generation completed.")

def main():
    root = tk.Tk()
    app = SurveyGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
