import os
from datetime import datetime
import numpy as np

# Custom function to calculate the mean (average)
def calculate_mean(data_points):
    return np.mean(data_points)

# Custom function to calculate the median
def calculate_median(data_points):
    return np.median(data_points)

# Custom function to calculate the standard deviation
def calculate_stdev(data_points):
    return np.std(data_points, ddof=1)  # ddof=1 for sample standard deviation

# Custom function to calculate correlation coefficient
def calculate_correlation(x, y):
    return np.corrcoef(x, y)[0, 1]

# Custom function to perform linear regression
def perform_regression(x, y):
    x = np.array(x)
    y = np.array(y)
    A = np.vstack([x, np.ones(len(x))]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    y_pred = slope * x + intercept
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    ss_res = np.sum((y - y_pred) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    return slope, intercept, r_squared

class ResearchDataManager:
    def __init__(self):
        self.entries = []
        self.filename = "research_data.txt"
        self.load_entries_from_file()

    def add_entry(self):
        while True:
            experiment_name = input("Enter the experiment name: ").strip()
            if not experiment_name:
                print("Experiment name cannot be empty. Please enter a valid name.")
            else:
                break

        while True:
            date_str = input("Enter the date (YYYY-MM-DD): ").strip()
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

        while True:
            researcher = input("Enter the researcher name: ").strip()
            if not researcher:
                print("Researcher name cannot be empty. Please enter a valid name.")
            else:
                break

        while True:
            data_points_str = input("Enter space-separated data points: ").strip()
            if not data_points_str:
                print("Data points cannot be empty. Please enter valid data points.")
            else:
                try:
                    data_points = list(map(float, data_points_str.split()))
                    break
                except ValueError:
                    print("Please enter valid numerical values for data points.")

        new_entry = {
            'experiment_name': experiment_name,
            'date': date,
            'researcher': researcher,
            'data_points': data_points
        }

        self.entries.append(new_entry)
        print(f"Entry for experiment '{experiment_name}' added successfully!")

    def view_entries(self):
        if not self.entries:
            print("No entries available.")
        else:
            for i, entry in enumerate(self.entries, 1):
                print(f"\nEntry {i}:")
                print(f"Experiment Name: {entry['experiment_name']}")
                print(f"Date: {entry['date']}")
                print(f"Researcher: {entry['researcher']}")
                print(f"Data Points: {', '.join(map(str, entry['data_points']))}")

    def save_entries_to_file(self):
        with open(self.filename, "w") as f:
            for entry in self.entries:
                line = f"{entry['experiment_name']},{entry['date']},{entry['researcher']},{', '.join(map(str, entry['data_points']))}\n"
                f.write(line)
        print(f"Entries saved to {self.filename}")

    def load_entries_from_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(",")
                        experiment_name = parts[0]
                        date = parts[1]
                        researcher = parts[2]
                        data_points = list(map(float, parts[3:]))
                        entry = {
                            'experiment_name': experiment_name,
                            'date': date,
                            'researcher': researcher,
                            'data_points': data_points
                        }
                        self.entries.append(entry)
            print(f"Entries loaded from {self.filename}")
        else:
            print(f"{self.filename} does not exist. Starting with an empty list.")

    def analyze_data(self):
        if not self.entries:
            print("No entries available to analyze.")
            return
        
        while True:
            try:
                entry_number = int(input("Enter the entry number to analyze: ").strip())
                if 1 <= entry_number <= len(self.entries):
                    break
                else:
                    print(f"Invalid entry number. Please enter a number between 1 and {len(self.entries)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        
        entry = self.entries[entry_number - 1]
        data_points = entry['data_points']
        
        # Perform calculations
        average = calculate_mean(data_points)
        median = calculate_median(data_points)
        stdev = calculate_stdev(data_points)

        # Display results
        print(f"\nAnalysis for Entry {entry_number}:")
        print(f"Average: {average:.2f}")
        print(f"Median: {median:.2f}")
        print(f"Standard Deviation: {stdev:.2f}")

        # Perform and display correlation and regression analysis if applicable
        if len(data_points) >= 2:
            x = list(range(len(data_points)))  # Use index as x values
            y = data_points
            
            correlation = calculate_correlation(x, y)
            print(f"Correlation coefficient: {correlation:.2f}")

            slope, intercept, r_squared = perform_regression(x, y)
            print(f"Regression line: y = {slope:.2f}x + {intercept:.2f}")
            # Comment out or remove the following line if you don't want to print R-squared
            # print(f"R-squared: {r_squared:.2f}")
        else:
            print("Not enough data points for correlation or regression analysis.")

    def delete_entry(self):
        if not self.entries:
            print("No entries available to delete.")
            return
        
        while True:
            try:
                entry_number = int(input("Enter the entry number to delete: ").strip())
                if 1 <= entry_number <= len(self.entries):
                    break
                else:
                    print(f"Invalid entry number. Please enter a number between 1 and {len(self.entries)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        
        entry = self.entries[entry_number - 1]
        print(f"\nEntry to be deleted:")
        print(f"Experiment Name: {entry['experiment_name']}")
        print(f"Date: {entry['date']}")
        print(f"Researcher: {entry['researcher']}")
        print(f"Data Points: {', '.join(map(str, entry['data_points']))}")

        confirm = input("Are you sure you want to delete this entry? (yes/no): ").strip().lower()
        if confirm == 'yes':
            self.entries.pop(entry_number - 1)
            print("Entry deleted successfully.")
            self.save_entries_to_file()
        else:
            print("Entry deletion cancelled.")

    def update_entry(self):
        if not self.entries:
            print("No entries available to update.")
            return
        
        while True:
            try:
                entry_number = int(input("Enter the entry number to update: ").strip())
                if 1 <= entry_number <= len(self.entries):
                    break
                else:
                    print(f"Invalid entry number. Please enter a number between 1 and {len(self.entries)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        
        entry = self.entries[entry_number - 1]
        print(f"\nCurrent details of the entry:")
        print(f"Experiment Name: {entry['experiment_name']}")
        print(f"Date: {entry['date']}")
        print(f"Researcher: {entry['researcher']}")
        print(f"Data Points: {', '.join(map(str, entry['data_points']))}")

        new_experiment_name = input(f"Enter new experiment name (leave empty to keep '{entry['experiment_name']}'): ").strip()
        if new_experiment_name:
            entry['experiment_name'] = new_experiment_name
        
        new_date = input(f"Enter new date (YYYY-MM-DD) (leave empty to keep '{entry['date']}'): ").strip()
        if new_date:
            entry['date'] = new_date

        new_researcher = input(f"Enter new researcher name (leave empty to keep '{entry['researcher']}'): ").strip()
        if new_researcher:
            entry['researcher'] = new_researcher
        
        data_points_input = input(f"Enter new data points separated by spaces (leave empty to keep '{', '.join(map(str, entry['data_points']))}'): ").strip()
        if data_points_input:
            try:
                entry['data_points'] = list(map(float, data_points_input.split()))
            except ValueError:
                print("Invalid data points. Please enter numeric values separated by spaces.")
        
        print(f"\nUpdated details of the entry:")
        print(f"Experiment Name: {entry['experiment_name']}")
        print(f"Date: {entry['date']}")
        print(f"Researcher: {entry['researcher']}")
        print(f"Data Points: {', '.join(map(str, entry['data_points']))}")

        self.save_entries_to_file()
        print("Entry updated successfully.")

def main():
    manager = ResearchDataManager()
    manager.load_entries_from_file()

    while True:
        print("\nResearch Data Manager")
        print("1. Add new entry")
        print("2. View all entries")
        print("3. Save entries to file")
        print("4. Analyze data")
        print("5. Delete an entry")
        print("6. Update an entry")
        print("7. Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            manager.add_entry()
        elif choice == '2':
            manager.view_entries()
        elif choice == '3':
            manager.save_entries_to_file()
        elif choice == '4':
            manager.analyze_data()
        elif choice == '5':
            manager.delete_entry()
        elif choice == '6':
            manager.update_entry()
        elif choice == '7':
            manager.save_entries_to_file()  # Save before exiting
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
