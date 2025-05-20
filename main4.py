import os
import avro.schema
import avro.io
import io
from datetime import datetime
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import base64

class ResearchDataManager:
    def __init__(self):
        self.__entries = []
        self.__filename = "research_data.avro"
        self.__schema = avro.schema.Parse(open("research_data_schema.avsc", "r").read())

    def add_entry(self, experiment_name, date, researcher, data_points):
        # If data_points is a string, split it into a list of strings, otherwise keep it as is
        if isinstance(data_points, str):
            data_points_list = [float(dp) for dp in data_points.split()]
        else:
            data_points_list = [float(dp) for dp in data_points]  # Assuming data_points is a list of strings or floats
        
        new_entry = {
            'experiment_name': experiment_name,
            'date': date,  # Convert date to string
            'researcher': researcher,
            'data_points': data_points_list
        }

        self.__entries.append(new_entry)
        print(f"Entry for experiment '{experiment_name}' added successfully!")
        self.save_entries_to_file()

    def __encode_base64(self, data):
        return base64.urlsafe_b64encode(data).decode('utf-8')

    def __decode_base64(self, data):
        return base64.urlsafe_b64decode(data.encode('utf-8'))

    def save_entries_to_file(self):
        try:
            with open(self.__filename, "w") as f:
                writer = avro.io.DatumWriter(self.__schema)
                for entry in self.__entries:
                    buffer = io.BytesIO()
                    encoder = avro.io.BinaryEncoder(buffer)
                    writer.write(entry, encoder)
                    data = buffer.getvalue()
                    encoded_data = self.__encode_base64(data)
                    f.write(encoded_data + '\n')  # Append newline for separation
        except Exception as e:
            print(f"An error occurred while saving entries: {e}")
        else:
            print(f"Entries saved to {self.__filename}")

    def get_entries(self):
        self.__entries = []  # Clear current entries
        self.load_entries_from_file()
        return self.__entries 

    def load_entries_from_file(self):
        if os.path.exists(self.__filename):
            try:
                with open(self.__filename, "r") as f:
                    reader = avro.io.DatumReader(self.__schema)
                    for encoded_data in f:
                        decoded_data = self.__decode_base64(encoded_data.strip())  # Remove trailing newline
                        buffer = io.BytesIO(decoded_data)
                        decoder = avro.io.BinaryDecoder(buffer)
                        entry = reader.read(decoder)
                        self.__entries.append(entry)
            except Exception as e:
                print(f"An error occurred while loading entries: {e}")
            else:
                print(f"Entries loaded from {self.__filename}")
        else:
            print(f"{self.__filename} does not exist. Starting with an empty list.")

    def delete_entry_by_line(self, line_number):
        if line_number < 1 or line_number > len(self.__entries):
            print("Error: Line number out of range.")
            return

        # Delete the entry from the list
        self.__entries.pop(line_number - 1)
        print(f"Entry at line {line_number} deleted successfully!")
        self.save_entries_to_file()

    def update_entry(self, line_number, experiment_name=None, date=None, researcher=None, data_points=None):
        if line_number < 1 or line_number > len(self.__entries):
            print("Error: Line number out of range.")
            return

        # Retrieve the existing entry
        entry = self.__entries[line_number - 1]

        # Update the fields with new values if provided
        if experiment_name is not None:
            entry['experiment_name'] = experiment_name
        if date is not None:
            entry['date'] = date
        if researcher is not None:
            entry['researcher'] = researcher
        if data_points is not None:
            if isinstance(data_points, str):
                entry['data_points'] = [float(dp) for dp in data_points.split()]
            else:
                entry['data_points'] = [float(dp) for dp in data_points]

        # Save the updated entries back to the file
        self.save_entries_to_file()
        print(f"Entry at line {line_number} updated successfully!")

    def get_records(self):
        return self.__entries

selected_row_no = None

def add_entry(manager, tree):
    for item in tree.get_children():
        tree.delete(item)

    for i, entry in enumerate(manager.get_entries(), start=1):
        tree.insert("", "end", values=(i, entry['experiment_name'], entry['date'], entry['researcher'], entry['data_points'])) 

def refresh_table(manager, tree): 
    pass 

def sort_by_column(tree, col, descending):
    data = [(tree.set(item, col), item) for item in tree.get_children('')]
    try:
        data.sort(key=lambda t: float(t[0]), reverse=descending)
    except ValueError:
        data.sort(reverse=descending)
    for index, (val, item) in enumerate(data):
        tree.move(item, '', index)
    tree.heading(col, command=lambda: sort_by_column(tree, col, not descending))

def validate_inputs(manager, tree, experiment_name_entry, date_entry, researcher_entry, data_points_entry):
    # Get the values from each input field
    experiment_name = experiment_name_entry.get().strip()
    date = date_entry.get().strip()
    researcher = researcher_entry.get().strip()
    data_points = data_points_entry.get().strip()

    errors = []

    # Validate Experiment Name
    if not experiment_name:
        errors.append("Experiment Name cannot be empty.")

    # Validate Date
    if not date:
        errors.append("Date cannot be empty.")
    else:
        try:
            datetime.strptime(date, "%Y-%m-%d")  # Validate date format
        except ValueError:
            errors.append("Date is not valid. Must be in YYYY-MM-DD format.")

    # Validate Researcher
    if not researcher:
        errors.append("Researcher cannot be empty.")

    # Validate Data Points
    if not data_points:
        errors.append("Data Points cannot be empty.")
    else:
        # Check if all data points are numbers (allow decimal points)
        try:
            data_points_list = [float(dp) for dp in data_points.split()]  # Convert to list of floats
        except ValueError:
            errors.append("Data Points must be space-separated numbers or decimals only.")

    # If there are any errors, show them in a single message box
    if errors:
        messagebox.showerror("Validation Errors", "\n".join(errors))
        return

    # If all validations pass, print the values to the console
    print(f"Experiment Name: {experiment_name}")
    print(f"Date: {date}")
    print(f"Researcher: {researcher}")
    print(f"Data Points: {data_points_list}")
    manager.add_entry(experiment_name, date, researcher, data_points_list)
    add_entry(manager, tree)
    experiment_name_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    researcher_entry.delete(0, tk.END)
    data_points_entry.delete(0, tk.END)

def on_row_select(event, tree, experiment_name_input, date_input, researcher_name_input, data_points_input):
    # Get the selected row(s)
    selected_item = tree.selection()
    if selected_item:
        # Get the item details using item() method
        item_data = tree.item(selected_item[0])
        
        # Extracting the values from the item
        row_data = item_data['values']
        global selected_row_no
        selected_row_no = row_data[0]
        # Print the data to the console (for debugging)
        print(f"Selected Row Data: {row_data}")

        # Fill the input fields with the selected row data
        experiment_name_input.delete(0, tk.END)
        experiment_name_input.insert(0, row_data[1])  # Experiment Name
        
        date_input.delete(0, tk.END)
        date_input.insert(0, row_data[2])  # Date
        
        researcher_name_input.delete(0, tk.END)
        researcher_name_input.insert(0, row_data[3])  # Researcher

        # Assuming row_data[4] is a list or tuple of numbers
        if isinstance(row_data[4], (list, tuple)):
            data_points_formatted = ' '.join(map(str, row_data[4]))
        else:
            # Handle cases where data_points are stored as a string with unwanted characters
            data_points_formatted = row_data[4].replace(',', ' ').strip()
        
        data_points_input.delete(0, tk.END)
        data_points_input.insert(0, data_points_formatted)  # Data Points

def delete_entry_event(manager, tree, experiment_name_input, date_input, researcher_name_input, data_points_input):
    global selected_row_no
    if selected_row_no is not None:
        manager.delete_entry_by_line(selected_row_no)
        add_entry(manager, tree)  # Update the tree view after deletion
        selected_row_no = None
    else:
        messagebox.showwarning("No Selection", "Please select a row to delete.")


    experiment_name_input.delete(0, tk.END)
    date_input.delete(0, tk.END)
    researcher_name_input.delete(0, tk.END)
    data_points_input.delete(0, tk.END)

def analyse(selected_row_no, average_value_label, std_dev_value_label, median_value_label, correlation_value_label, regression_value_label,manager ):
    if selected_row_no is None:
        messagebox.showwarning("No Selection", "Please select a row to analyze.")
        return

    # Retrieve the selected entry from the manager's entries
    entry = manager.get_entries()[selected_row_no - 1]  # Subtracting 1 because the list is 0-indexed

    data_points = entry['data_points']

    if not data_points:
        messagebox.showwarning("No Data", "The selected entry has no data points to analyze.")
        return

    # Calculate statistics
    average = np.mean(data_points)
    std_dev = np.std(data_points)
    median = np.median(data_points)

    # For correlation and regression, we need at least two data sets. Here we'll just correlate and regress against the indices.
    indices = np.arange(len(data_points))
    correlation = np.corrcoef(indices, data_points)[0, 1]  # Correlation between indices and data_points
    slope, intercept = np.polyfit(indices, data_points, 1)  # Linear regression (1st degree polynomial)
    regression = f"y = {slope:.2f}x + {intercept:.2f}"

    # Display the results in the provided labels
    average_value_label.config(text=f"{average:.2f}")
    std_dev_value_label.config(text=f"{std_dev:.2f}")
    median_value_label.config(text=f"{median:.2f}")
    correlation_value_label.config(text=f"{correlation:.2f}")
    regression_value_label.config(text=f"{regression}")

def update(manager,tree,selected_row_no, experiment_name_input, date_input, researcher_name_input, data_points_input):
    # Ensure a row is selected
    if selected_row_no is None:
        messagebox.showwarning("No Selection", "Please select a row to update.")
        return

    # Get the values from each input field
    experiment_name = experiment_name_input.get().strip()
    date = date_input.get().strip()
    researcher = researcher_name_input.get().strip()
    data_points = data_points_input.get().strip()

    errors = []

    # Validate Experiment Name
    if not experiment_name:
        errors.append("Experiment Name cannot be empty.")

    # Validate Date
    if not date:
        errors.append("Date cannot be empty.")
    else:
        try:
            datetime.strptime(date, "%Y-%m-%d")  # Validate date format
        except ValueError:
            errors.append("Date is not valid. Must be in YYYY-MM-DD format.")

    # Validate Researcher
    if not researcher:
        errors.append("Researcher cannot be empty.")

    # Validate Data Points
    if not data_points:
        errors.append("Data Points cannot be empty.")
    else:
        # Check if all data points are numbers (allow decimal points)
        try:
            data_points_list = [float(dp) for dp in data_points.split()]  # Convert to list of floats
        except ValueError:
            errors.append("Data Points must be space-separated numbers or decimals only.")

    # If there are any errors, show them in a single message box
    if errors:
        messagebox.showerror("Validation Errors", "\n".join(errors))
        return

    # If all validations pass, proceed to update the entry
    print(f"Updating Entry - Experiment Name: {experiment_name}")
    print(f"Date: {date}")
    print(f"Researcher: {researcher}")
    print(f"Data Points: {data_points_list}")

    # Call the update_entry method of ResearchDataManager to update the selected row
    manager.update_entry(selected_row_no, experiment_name, date, researcher, data_points_list)

    # Optionally, clear the input fields after the update
    experiment_name_input.delete(0, tk.END)
    date_input.delete(0, tk.END)
    researcher_name_input.delete(0, tk.END)
    data_points_input.delete(0, tk.END)
    add_entry(manager,tree)
    messagebox.showinfo("Update Successful", "The entry has been updated successfully!")

def on_search(manager, tree, experiment_name_search, date_search, researcher_search, data_points_search):
    
    # Get the current values from the search entries
    experiment_name = experiment_name_search.get().strip()
    date_search_str = date_search.get().strip()  # Retrieve the date input as a search string
    researcher = researcher_search.get().strip()
    data_points = data_points_search.get().strip()

    # Debugging output
    print(f"Entered date search: '{date_search_str}'")

    # Clear the tree view before adding new search results
    for item in tree.get_children():
        tree.delete(item)

    # Load all entries
    entries = manager.get_entries()

    # Filter entries based on search criteria
    for i, entry in enumerate(entries, start=1):
        match = True

        # Debugging output
        print(f"Checking entry {i}:")
        print(f"  Stored date: '{entry['date']}'")
        print(f"  Search date: '{date_search_str}'")

        # Match experiment name
        if experiment_name and experiment_name.lower() not in entry['experiment_name'].lower():
            match = False

        # Match date using partial match
        if date_search_str:
            # Check if the search string is a substring of the stored date string
            entry_date_str = entry['date']  # This should be in "YYYY-MM-DD" format
            if date_search_str not in entry_date_str:
                match = False

        # Match researcher name
        if researcher and researcher.lower() not in entry['researcher'].lower():
            match = False

        # Match data points (if provided, check if the search input is in the data points list)
        if data_points:
            try:
                search_data_points = [float(dp) for dp in data_points.split()]
                if not all(dp in entry['data_points'] for dp in search_data_points):
                    match = False
            except ValueError:
                match = False

        # If all conditions match, insert the entry into the tree view
        if match:
            print(f"  Match found: {entry}")  # Debugging output
            tree.insert("", "end", values=(i, entry['experiment_name'], entry['date'], entry['researcher'], entry['data_points']))

    print("Search complete.")  # Debugging output

def main():
    manager = ResearchDataManager()
    root = tk.Tk()
    root.title("Scientific Research Data Management System")

    # Create heading label
    heading = tk.Label(root, font=("Helvetica", 20, "bold"), text="Scientific Research Data Management System", pady=10)
    heading.pack()

    # Create a container frame to hold the search entries
    container_frame = tk.Frame(root, pady=10, borderwidth=1, relief=tk.RIDGE)
    container_frame.pack(anchor="center")

    # Create and place the "Search" label in the container frame, centered
    search_label = tk.Label(container_frame, text="Search", font=("Helvetica", 25, "bold"))
    search_label.pack(pady=10)

    # Create a frame for the search entries
    search_frame = tk.Frame(container_frame)
    search_frame.pack(fill="x", expand=True)

    # Create frames to hold label-entry pairs vertically and center them horizontally
    experiment_frame = tk.Frame(search_frame)
    experiment_frame.pack(side="left", padx=10)
    date_frame = tk.Frame(search_frame)
    date_frame.pack(side="left", padx=10)
    researcher_frame = tk.Frame(search_frame)
    researcher_frame.pack(side="left", padx=10)
    data_points_frame = tk.Frame(search_frame)
    data_points_frame.pack(side="left", padx=10)

    # Adding labels and entries vertically within each frame
    experiment_label = tk.Label(experiment_frame, text="Experiment Name:")
    experiment_label.pack(anchor="w")
    experiment_name_search = tk.Entry(experiment_frame)
    experiment_name_search.pack(anchor="w", ipady=5)

    date_label = tk.Label(date_frame, text="Date:")
    date_label.pack(anchor="w")
    date_search = tk.Entry(date_frame)
    date_search.pack(anchor="w", ipady=5)

    researcher_label = tk.Label(researcher_frame, text="Researcher:")
    researcher_label.pack(anchor="w")
    researcher_search = tk.Entry(researcher_frame)
    researcher_search.pack(anchor="w", ipady=5)

    data_points_label = tk.Label(data_points_frame, text="Data Points:")
    data_points_label.pack(anchor="w")
    data_points_search = tk.Entry(data_points_frame)
    data_points_search.pack(anchor="w", ipady=5)

    experiment_name_search.bind("<KeyRelease>", lambda event: on_search(manager, tree, experiment_name_search, date_search, researcher_search, data_points_search))
    date_search.bind("<KeyRelease>", lambda event: on_search(manager, tree, experiment_name_search, date_search, researcher_search, data_points_search))
    researcher_search.bind("<KeyRelease>", lambda event: on_search(manager, tree, experiment_name_search, date_search, researcher_search, data_points_search))
    data_points_search.bind("<KeyRelease>", lambda event: on_search(manager, tree, experiment_name_search, date_search, researcher_search, data_points_search))


    # Create a separate frame for the Treeview
    table_frame = tk.Frame(root, pady=10, padx=10, borderwidth=1, relief=tk.RIDGE)
    table_frame.pack(fill="both", expand=True)

    columns = ("No", "Experiment Name", "Date", "Researcher", "Data Points")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    # Define headings
    for col in columns:
        tree.heading(col, text=col, command=lambda _col=col: sort_by_column(tree, _col, False))
        tree.column(col, width=150)

    add_entry(manager, tree)
    
    # Bind the row selection event to on_row_select function



    tree.pack(fill="both", expand=True)



    # Create a frame for input fields
    input_frame = tk.Frame(root, pady=10, padx=10)
    input_frame.pack(anchor="center")

    # Create frames for input fields
    experiment_input_frame = tk.Frame(input_frame)
    experiment_input_frame.pack(side="left", padx=10)
    date_input_frame = tk.Frame(input_frame)
    date_input_frame.pack(side="left", padx=10)
    researcher_input_frame = tk.Frame(input_frame)
    researcher_input_frame.pack(side="left", padx=10)
    data_points_input_frame = tk.Frame(input_frame)
    data_points_input_frame.pack(side="left", padx=10)

    # Adding labels and entries vertically within each frame
    experiment_input_label = tk.Label(experiment_input_frame, text="Experiment Name:")
    experiment_input_label.pack(anchor="w")
    experiment_name_input = tk.Entry(experiment_input_frame)
    experiment_name_input.pack(anchor="w", ipady=5)

    date_input_label = tk.Label(date_input_frame, text="Date:")
    date_input_label.pack(anchor="w")
    date_input = tk.Entry(date_input_frame)
    date_input.pack(anchor="w", ipady=5)

    researcher_input_label = tk.Label(researcher_input_frame, text="Researcher:")
    researcher_input_label.pack(anchor="w")
    researcher_name_input = tk.Entry(researcher_input_frame)
    researcher_name_input.pack(anchor="w", ipady=5)

    data_points_input_label = tk.Label(data_points_input_frame, text="Data Points:")
    data_points_input_label.pack(anchor="w")
    data_points_input = tk.Entry(data_points_input_frame)
    data_points_input.pack(anchor="w", ipady=5)

    # Create a frame for the buttons
    button_frame = tk.Frame(input_frame, pady=10)
    button_frame.pack(side="left", padx=10)

    add_button = tk.Button(button_frame, text="Add", width=10, command=lambda: validate_inputs(manager,tree,experiment_name_input, date_input, researcher_name_input, data_points_input))
    add_button.pack(side="left", padx=5)
    
    update_button = tk.Button(button_frame, text="Update", width=10,command=lambda: update(manager,tree,selected_row_no,experiment_name_input, date_input, researcher_name_input, data_points_input))
    update_button.pack(side="left", padx=5)

    delete_button = tk.Button(button_frame, text="Delete", width=10, command=lambda: delete_entry_event(manager, tree,experiment_name_input, date_input, researcher_name_input, data_points_input))
    delete_button.pack(side="left", padx=5)

    analyze_button = tk.Button(button_frame, text="Analyze", width=10,command=lambda: analyse(selected_row_no, average_value, std_dev_value ,median_value, correlation_value, regression_value, manager))
    analyze_button.pack(side="left", padx=5)

    # Create a frame for analysis labels and values
    analysis_frame = tk.Frame(root, pady=20)
    analysis_frame.pack(anchor="center")

    # Row 1: Average, Standard Deviation, Median
    row1_frame = tk.Frame(analysis_frame)
    row1_frame.pack()

    average_label = tk.Label(row1_frame, text="Average:", font=("Helvetica", 12, "bold"))
    average_label.pack(side="left", padx=5)
    average_value = tk.Label(row1_frame, text="0.00", font=("Helvetica", 12))
    average_value.pack(side="left", padx=5)

    std_dev_label = tk.Label(row1_frame, text="Standard Deviation:", font=("Helvetica", 12, "bold"))
    std_dev_label.pack(side="left", padx=5)
    std_dev_value = tk.Label(row1_frame, text="0.00", font=("Helvetica", 12))
    std_dev_value.pack(side="left", padx=5)

    median_label = tk.Label(row1_frame, text="Median:", font=("Helvetica", 12, "bold"))
    median_label.pack(side="left", padx=5)
    median_value = tk.Label(row1_frame, text="0.00", font=("Helvetica", 12))
    median_value.pack(side="left", padx=5)

    # Row 2: Correlation, Regression
    row2_frame = tk.Frame(analysis_frame)
    row2_frame.pack()

    correlation_label = tk.Label(row2_frame, text="Correlation:", font=("Helvetica", 12, "bold"))
    correlation_label.pack(side="left", padx=5)
    correlation_value = tk.Label(row2_frame, text="0.00", font=("Helvetica", 12))
    correlation_value.pack(side="left", padx=5)

    regression_label = tk.Label(row2_frame, text="Regression:", font=("Helvetica", 12, "bold"))
    regression_label.pack(side="left", padx=5)
    regression_value = tk.Label(row2_frame, text="0.00", font=("Helvetica", 12))
    regression_value.pack(side="left", padx=5)

    tree.bind("<<TreeviewSelect>>", lambda event: on_row_select(event, tree, experiment_name_input, date_input, researcher_name_input, data_points_input))
    root.mainloop()

if __name__ == "__main__":
    main()