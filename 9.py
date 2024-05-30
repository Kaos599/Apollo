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

        self.options.append(("Generate Weighted Choice", var, name_entry))

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

    def browse_output_path(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt")])
        self.output_file_path_var.set(filename)

    def generate_response(self, probability):
        return 'Yes' if random.random() < probability else 'No'

    def generate_weighted_choice(self, choices):
        population = [val for val, cnt in choices.items() for _ in range(int(cnt * 100))]
        return random.choice(population)

    def get_weighted_choices(self):
        weighted_choices_str = simpledialog.askstring("Weighted Choices", "Enter weighted choices one by one (press cancel when done):")
        if weighted_choices_str is None:
            return None

        weighted_choices = {}
        total_probability = 0

        while weighted_choices_str:
            choice_prob_pair = weighted_choices_str.split(':')
            if len(choice_prob_pair) != 2:
                messagebox.showerror("Error", "Invalid input format. Please enter choices in the format 'Option:Probability'.")
                return None

            choice, prob = map(str.strip, choice_prob_pair)
            choice = choice.strip("'\"")
            prob = prob.strip("'\"")

            try:
                probability = float(prob)
                if probability < 0 or probability > 1:
                    raise ValueError("Probability must be between 0 and 1")
                weighted_choices[choice] = probability
                total_probability += probability
            except ValueError:
                messagebox.showerror("Error", f"Invalid probability value: {prob}")
                return None

            weighted_choices_str = simpledialog.askstring("Weighted Choices", "Enter next weighted choice (press cancel when done):")

        if not (0.99 <= total_probability <= 1.01):  # Allow for floating-point tolerance
            messagebox.showerror("Error", "Total probability must equal 1")
            return None

        return weighted_choices


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
                    weighted_choices = self.get_weighted_choices()
                    if weighted_choices is None:
                        return
                    entry_data[entry_name] = self.generate_weighted_choice(weighted_choices)

            survey_data.append(entry_data)

        survey_df = pd.DataFrame(survey_data)

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

"""in this code i am trying to use the faker library to create fake data using a GUI. 
there are two options of doing so either u can have generate response option or a generate weighted response. the weighted response option isn't working as planned. whenever i click create entry and then select any of the two options which are generate response or generate weighted response it shows an error "Please enter a valid number of entries"

secondly whenever i enter create entries while weighted response is elected and then i fill the values in enter weighted values prompt like "'hi:0.1', 'hello:0.9' it just prints the values instead of making a file and re-prompts me again with "enter weighted values"""