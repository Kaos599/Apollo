import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from faker import Faker
import random
import pandas as pd


class SurveyGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Survey Data Generator")

        self.fake = Faker()

        # Number of Entries Input
        self.num_entries_label = tk.Label(root, text="Number of Entries:")
        self.num_entries_label.grid(row=0, column=0, padx=10, pady=5)
        self.num_entries_entry = tk.Entry(root)
        self.num_entries_entry.grid(row=0, column=1, padx=10, pady=5)

        # Generate Response Frame
        self.generate_response_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
        self.generate_response_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.generate_response_label = tk.Label(self.generate_response_frame, text="Generate Response:")
        self.generate_response_label.grid(row=0, column=0, padx=5, pady=5)
        self.probability_entry = tk.Entry(self.generate_response_frame)
        self.probability_entry.grid(row=0, column=1, padx=5, pady=5)

        # Generate Weighted Choice Frame
        self.generate_weighted_choice_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
        self.generate_weighted_choice_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.generate_weighted_choice_label = tk.Label(self.generate_weighted_choice_frame, text="Generate Weighted Choice:")
        self.generate_weighted_choice_label.grid(row=0, column=0, padx=5, pady=5)
        self.weighted_choice_var = tk.StringVar()
        self.weighted_choice_dropdown = ttk.Combobox(self.generate_weighted_choice_frame, textvariable=self.weighted_choice_var, state="readonly")
        self.weighted_choice_dropdown['values'] = ['1: 2.6, 2: 4.3, 3: 7.1, 4: 9.7, 5: 11, 6: 7.2, 7: 7.8, 8: 20.1, 9: 12.8, 10: 17.4']
        self.weighted_choice_dropdown.current(0)
        self.weighted_choice_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Output File Path Frame
        self.output_file_path_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
        self.output_file_path_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.output_file_path_label = tk.Label(self.output_file_path_frame, text="Output File Path:")
        self.output_file_path_label.grid(row=0, column=0, padx=5, pady=5)
        self.output_file_path_var = tk.StringVar()
        self.output_file_path_entry = tk.Entry(self.output_file_path_frame, textvariable=self.output_file_path_var)
        self.output_file_path_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_button = tk.Button(self.output_file_path_frame, text="Browse", command=self.browse_output_path)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Output Format Frame
        self.output_format_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
        self.output_format_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.output_format_label = tk.Label(self.output_format_frame, text="Output Format:")
        self.output_format_label.grid(row=0, column=0, padx=5, pady=5)
        self.output_format_var = tk.StringVar()
        self.output_format_dropdown = ttk.Combobox(self.output_format_frame, textvariable=self.output_format_var, state="readonly")
        self.output_format_dropdown['values'] = ['CSV', 'Text']
        self.output_format_dropdown.current(0)
        self.output_format_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Generate Button
        self.generate_button = tk.Button(root, text="Generate", command=self.generate_data)
        self.generate_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def browse_output_path(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt")])
        self.output_file_path_var.set(filename)

    def generate_response(self, probability):
        return 'Yes' if random.random() < probability else 'No'

    def generate_weighted_choice(self, choices):
        population = [val for val, cnt in choices.items() for _ in range(int(cnt * 100))]
        return random.choice(population)

    def generate_data(self):
        num_entries = int(self.num_entries_entry.get())

        probability_yes = float(self.probability_entry.get())
        weighted_choice_str = self.weighted_choice_var.get()
        output_path = self.output_file_path_var.get()
        output_format = self.output_format_var.get()

        weighted_choice_dict = eval(weighted_choice_str)

        survey_data = []
        for _ in range(num_entries):
            survey_data.append([
                self.fake.unique.random_int(min=1000, max=9999),
                self.generate_response(probability_yes),
                self.generate_response(probability_yes),
                self.generate_response(probability_yes),
                self.generate_response(probability_yes),
                self.generate_response(probability_yes),
                self.generate_response(probability_yes),
                self.generate_response(probability_yes),
                self.generate_weighted_choice(weighted_choice_dict),
                self.generate_weighted_choice(weighted_choice_dict),
                self.generate_weighted_choice(weighted_choice_dict),
                self.generate_response(probability_yes),
                self.generate_weighted_choice(weighted_choice_dict),
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
