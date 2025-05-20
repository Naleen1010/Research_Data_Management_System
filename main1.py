import os 
from datetime import datetime

# Custom function to calculate the mean (average)
def calculate_mean(data_points):
    return sum(data_points) / len(data_points)

# Custom function to calculate the median
def calculate_median(data_points):
    sorted_data = sorted(data_points)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2.0
    else:
        return sorted_data[mid]

# Custom function to calculate the standard deviation
def calculate_stdev(data_points):
    if len(data_points) < 2:
        return 0.0  # Standard deviation requires at least 2 data points
    mean = calculate_mean(data_points)
    variance = sum((x - mean) ** 2 for x in data_points) / (len(data_points) - 1)
    return variance ** 0.5

# Function to add a research data entry 
def add_entry(entries):
    while True:
        experiment_name = input("Enter the experiment name: ").strip()
        if not experiment_name:
            print("Experiment name cannot be empty. Please enter a valid name.")
        else:
            break

    while True:
        date_str = input("Enter the date (YYYY-MM-DD): ").strip()
        try:
            # Try to parse the date
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

    # Creating the new entry as a dictionary
    new_entry = {
        'experiment_name': experiment_name,
        'date': date,
        'researcher': researcher,
        'data_points': data_points
    }
    
    # Adding the new entry to the entries list
    entries.append(new_entry)
    print(f"Entry for experiment '{experiment_name}' added successfully!")

# Function to view all research data entries
def view_entries(entries):
    if not entries:
        print("No entries available.")
    else:
        for i, entry in enumerate(entries, 1):
            print(f"\nEntry {i}:")
            print(f"Experiment Name: {entry['experiment_name']}")
            print(f"Date: {entry['date']}")
            print(f"Researcher: {entry['researcher']}")
            print(f"Data Points: {', '.join(map(str, entry['data_points']))}")


# Function to save entries to a text file
def save_entries_to_file(entries, filename):
    with open(filename, "w") as f:
        for entry in entries:
            # Format the data as a comma-separated string
            line = f"{entry['experiment_name']},{entry['date']},{entry['researcher']},{', '.join(map(str, entry['data_points']))}\n"
            f.write(line)
    print(f"Entries saved to {filename}")


# Function to load entries from a text file
def load_entries_from_file(filename):
    entries = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if line:  # Check if line is not empty
                    parts = line.split(",")
                    experiment_name = parts[0]
                    date = parts[1]
                    researcher = parts[2]
                    data_points = list(map(float, parts[3:]))  # Convert data points to float
                    entry = {
                        'experiment_name': experiment_name,
                        'date': date,
                        'researcher': researcher,
                        'data_points': data_points
                    }
                    entries.append(entry)
    else:
        print(f"{filename} does not exist. Starting with an empty list.")
    return entries


# Function to perform data analysis
def analyze_data(entries):
    if not entries:
        print("No entries available to analyze.")
        return
    
    # Prompt the user to select an entry number
    while True:
        try:
            entry_number = int(input("Enter the entry number to analyze: ").strip())
            if 1 <= entry_number <= len(entries):
                break
            else:
                print(f"Invalid entry number. Please enter a number between 1 and {len(entries)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    # Get the selected entry
    entry = entries[entry_number - 1]
    data_points = entry['data_points']
    
    # Perform calculations using custom functions
    average = calculate_mean(data_points)
    median = calculate_median(data_points)
    stdev = calculate_stdev(data_points)

    # Print results
    print(f"\nAnalysis for Entry {entry_number}:")
    print(f"Average: {average:.2f}")
    print(f"Median: {median:.2f}")
    print(f"Standard Deviation: {stdev:.2f}")

# Function to delete a research data entry
def delete_entry(entries, filename):
    if not entries:
        print("No entries available to delete.")
        return
    
    # Prompt the user to select an entry number
    while True:
        try:
            entry_number = int(input("Enter the entry number to delete: ").strip())
            if 1 <= entry_number <= len(entries):
                break
            else:
                print(f"Invalid entry number. Please enter a number between 1 and {len(entries)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    # Display the selected entry details
    entry = entries[entry_number - 1]
    print(f"\nEntry to be deleted:")
    print(f"Experiment Name: {entry['experiment_name']}")
    print(f"Date: {entry['date']}")
    print(f"Researcher: {entry['researcher']}")
    print(f"Data Points: {', '.join(map(str, entry['data_points']))}")

    # Confirm deletion
    confirm = input("Are you sure you want to delete this entry? (yes/no): ").strip().lower()
    if confirm == 'yes':
        entries.pop(entry_number - 1)  # Remove the entry from the list
        print("Entry deleted successfully.")
        # Save updated entries to file
        save_entries_to_file(entries, filename)
    else:
        print("Entry deletion cancelled.")


def update_entry(entries, filename):
    if not entries:
        print("No entries available to update.")
        return
    
    # Prompt the user to select an entry number
    while True:
        try:
            entry_number = int(input("Enter the entry number to update: ").strip())
            if 1 <= entry_number <= len(entries):
                break
            else:
                print(f"Invalid entry number. Please enter a number between 1 and {len(entries)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    # Display the current details of the selected entry
    entry = entries[entry_number - 1]
    print(f"\nCurrent details of the entry:")
    print(f"Experiment Name: {entry['experiment_name']}")
    print(f"Date: {entry['date']}")
    print(f"Researcher: {entry['researcher']}")
    print(f"Data Points: {', '.join(map(str, entry['data_points']))}")

    # Update the entry details
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
    
    # Display the updated details
    print(f"\nUpdated details of the entry:")
    print(f"Experiment Name: {entry['experiment_name']}")
    print(f"Date: {entry['date']}")
    print(f"Researcher: {entry['researcher']}")
    print(f"Data Points: {', '.join(map(str, entry['data_points']))}")
    
    # Save updated entries to file
    save_entries_to_file(entries, filename)
    print("Entry updated successfully.")


# Main function to run the program
def main():
    filename = "research_data.txt"
    entries = load_entries_from_file(filename)
    
    while True:
        print("\nResearch Data Management System")
        print("1. Add a new entry")
        print("2. View all entries")
        print("3. Analyze data")
        print("4. Delete an entry")
        print("5. Update an entry")
        print("6. Save entries to file")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            add_entry(entries)
        elif choice == '2':
            view_entries(entries)
        elif choice == '3':
            analyze_data(entries)
        elif choice == '4':
            delete_entry(entries, filename)
        elif choice == '5':
            update_entry(entries, filename)
        elif choice == '6':
            save_entries_to_file(entries, filename)
        elif choice == '7':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
