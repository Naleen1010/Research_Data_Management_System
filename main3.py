import os
import avro.schema
import avro.io
import io
from datetime import datetime
import numpy as np
import base64

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
        self.__entries = []
        self.__filename = "research_data.avro"
        self.__schema = avro.schema.parse(open("research_data_schema.avsc", "r").read())

    def __encode_base64(self, data):
        return base64.urlsafe_b64encode(data).decode('utf-8')

    def __decode_base64(self, data):
        return base64.urlsafe_b64decode(data.encode('utf-8'))
    
    # Getter for entries
    def get_entries(self):
        return self.__entries

    # Setter for entries
    def set_entries(self, entries):
        if isinstance(entries, list):
            self.__entries = entries
        else:
            raise ValueError("Entries must be a list.")

    # Getter for filename
    def get_filename(self):
        return self.__filename

    # Setter for filename
    def set_filename(self, filename):
        self.__filename = filename

    # Getter for schema
    def get_schema(self):
        return self.__schema

    # Setter for schema
    def set_schema(self, schema):
        self.__schema = schema
    
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
            'date': date.isoformat(),  # Convert date to string
            'researcher': researcher,
            'data_points': data_points
        }

        self.__entries.append(new_entry)
        print(f"Entry for experiment '{experiment_name}' added successfully!")

    def view_entries(self):
        if not self.__entries:
            print("No entries available.")
        else:
            for i, entry in enumerate(self.__entries, 1):
                print(f"\nEntry {i}:")
                print(f"Experiment Name: {entry['experiment_name']}")
                print(f"Date: {entry['date']}")
                print(f"Researcher: {entry['researcher']}")
                print(f"Data Points: {', '.join(map(str, entry['data_points']))}")

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

    def analyze_data(self):
        if not self.__entries:
            print("No entries available to analyze.")
            return
        
        while True:
            try:
                entry_number = int(input("Enter the entry number to analyze: ").strip())
                if 1 <= entry_number <= len(self.__entries):
                    break
                else:
                    print(f"Invalid entry number. Please enter a number between 1 and {len(self.__entries)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        
        entry = self.__entries[entry_number - 1]
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
            print(f"R-squared: {r_squared:.2f}")
        else:
            print("Not enough data points for correlation or regression analysis.")

    def delete_entry(self):
        if not self.__entries:
            print("No entries available to delete.")
            return
        
        while True:
            try:
                entry_number = int(input("Enter the entry number to delete: ").strip())
                if 1 <= entry_number <= len(self.__entries):
                    break
                else:
                    print(f"Invalid entry number. Please enter a number between 1 and {len(self.__entries)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        
        entry = self.__entries[entry_number - 1]
        print(f"\nEntry to be deleted:")
        print(f"Experiment Name: {entry['experiment_name']}")
        print(f"Date: {entry['date']}")
        print(f"Researcher: {entry['researcher']}")
        print(f"Data Points: {', '.join(map(str, entry['data_points']))}")

        confirm = input("Are you sure you want to delete this entry? (yes/no): ").strip().lower()
        if confirm == 'yes':
            self.__entries.pop(entry_number - 1)
            print("Entry deleted successfully.")
            self.save_entries_to_file()
        else:
            print("Entry deletion cancelled.")

    def update_entry(self):
        if not self.__entries:
            print("No entries available to update.")
            return
        
        while True:
            try:
                entry_number = int(input("Enter the entry number to update: ").strip())
                if 1 <= entry_number <= len(self.__entries):
                    break
                else:
                    print(f"Invalid entry number. Please enter a number between 1 and {len(self.__entries)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        
        entry = self.__entries[entry_number - 1]
        print(f"\nCurrent details of the entry:")
        print(f"Experiment Name: {entry['experiment_name']}")
        print(f"Date: {entry['date']}")
        print(f"Researcher: {entry['researcher']}")
        print(f"Data Points: {', '.join(map(str, entry['data_points']))}")

        new_experiment_name = input(f"Enter new experiment name (leave empty to keep '{entry['experiment_name']}'): ").strip()
        if new_experiment_name:
            entry['experiment_name'] = new_experiment_name

        new_date_str = input(f"Enter new date (leave empty to keep '{entry['date']}'): ").strip()
        if new_date_str:
            try:
                new_date = datetime.strptime(new_date_str, "%Y-%m-%d").date()
                entry['date'] = new_date.isoformat()
            except ValueError:
                print("Invalid date format. Date not updated.")

        new_researcher = input(f"Enter new researcher name (leave empty to keep '{entry['researcher']}'): ").strip()
        if new_researcher:
            entry['researcher'] = new_researcher

        new_data_points_str = input(f"Enter new space-separated data points (leave empty to keep current data points): ").strip()
        if new_data_points_str:
            try:
                entry['data_points'] = list(map(float, new_data_points_str.split()))
            except ValueError:
                print("Invalid data points. Data points not updated.")

        print("Entry updated successfully.")
        self.save_entries_to_file()

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
