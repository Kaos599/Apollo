
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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
        self.app_instance.add_option(option_type)
        self.destroy()


class SurveyGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Survey Data Generator")

        self.fake = Faker()
        self.options = []

        # Create Entry Button
        self.create_entry_button = tk.Button(root, text="Create Entry", command=self.create_option_window)
        self.create_entry_button.grid(row=0, column=0, padx=10, pady=5)

        # Delete Entry Button
        self.delete_entry_button = tk.Button(root, text="Delete Selected", command=self.delete_selected)
        self.delete_entry_button.grid(row=0, column=1, padx=10, pady=5)

        # Entry Frame
        self.entry_frame = tk.Frame(root)
        self.entry_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        # Output File Path Frame
        self.output_file_path_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
        self.output_file_path_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.output_file_path_label = tk.Label(self.output_file_path_frame, text="Output File Path:")
        self.output_file_path_label.grid(row=0, column=0, padx=5, pady=5)
        self.output_file_path_var = tk.StringVar()
        self.output_file_path_entry = tk.Entry(self.output_file_path_frame, textvariable=self.output_file_path_var)
        self.output_file_path_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_button = tk.Button(self.output_file_path_frame, text="Browse", command=self.browse_output_path)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Output Format Frame
        self.output_format_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
        self.output_format_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.output_format_label = tk.Label(self.output_format_frame, text="Output Format:")
        self.output_format_label.grid(row=0, column=0, padx=5, pady=5)
        self.output_format_var = tk.StringVar()
        self.output_format_dropdown = ttk.Combobox(self.output_format_frame, textvariable=self.output_format_var, state="readonly")
        self.output_format_dropdown['values'] = ['CSV', 'Text']
        self.output_format_dropdown.current(0)
        self.output_format_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Generate Button
        self.generate_button = tk.Button(root, text="Generate", command=self.generate_data)
        self.generate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def create_option_window(self):
        option_window = OptionWindow(self.root, self)

    def add_option(self, option_type):
        self.options.append(option_type)
        self.update_options_display()

    def update_options_display(self):
        for widget in self.entry_frame.winfo_children():
            widget.destroy()

        for i, option in enumerate(self.options):
            label = tk.Label(self.entry_frame, text=option)
            label.grid(row=i, column=0, padx=5, pady=5)

    def delete_selected(self):
        selected_indices = [i for i, option in enumerate(self.options) if option]
        for index in reversed(selected_indices):
            self.options.pop(index)

        self.update_options_display()

    def browse_output_path(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt")])
        self.output_file_path_var.set(filename)

    def generate_response(self, probability):
        return 'Yes' if random.random() < probability else 'No'

    def generate_weighted_choice(self, choices):
        population = [val for val, cnt in choices.items() for _ in range(int(cnt * 100))]
        return random.choice(population)

    def generate_data(self):
        num_entries = len(self.options)

        if num_entries == 0:
            messagebox.showerror("Error", "Please create at least one entry.")
            return

        probability_yes = 0
        weighted_choice_str = ''
        output_path = self.output_file_path_var.get()
        output_format = self.output_format_var.get()

        survey_data = []
        for _ in range(num_entries):
            if self.options[_] == "Generate Response":
                probability_yes = float(self.probability_entry.get())
                survey_data.append([
                    self.fake.unique.random_int(min=1000, max=9999),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes

)
                ])
            elif self.options[_] == "Generate Weighted Choice":
                weighted_choice_str = self.weighted_choice_var.get()
                weighted_choice_dict = eval(weighted_choice_str)
                survey_data.append([
                    self.fake.unique.random_int(min=1000, max=9999),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_response(probability_yes),
                    self.generate_weighted_choice(weighted_choice_dict)
                ])

        columns = [
            'Student ID',
            'Studying to Full Potential',
            'Able to Focus',
            'Difficulty in Time Management',
            'Single Platform Helpfulness',
            'App Helped in Studying',
            'Used Study Techniques',
            'Familiar Study Techniques',
            'Q1 - Losing Focus',
            'Q2 - Study Planner Satisfaction',
            'Q3 - Interest in Study Platform',
            'Willing to Pay for App',
            'Amount Willing to Pay',
            'Focus Duration'
        ]

        survey_df = pd.DataFrame(survey_data, columns=columns)

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
