import os
import csv

def lookup_properties(name, filename='Enchants.csv'):
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, filename)

        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0].lower() == name.lower():
                    return row[1:5]  # Assuming properties are in columns 2 to 5
        return None  # Name not found in the CSV file
    except FileNotFoundError:
        print(f"Error: The CSV file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_values_for_columns(properties, pips, filename='Reagents.csv'):
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, filename)

        matching_rows = []  # Store matching rows

        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Get the header row

            # Find the indices of the matching columns after stripping whitespaces
            matching_columns = [i for i, col in enumerate(map(str.strip, header)) if col.lower() in map(str.lower, properties)]

            # Iterate over the rows and store matching rows
            for row in reader:
                name_value = row[0].strip()  # Get the value in the "Name" column
                property_values = {}

                for col_index in matching_columns:
                    value = row[col_index].strip()
                    property_values[header[col_index].strip()] = value

                # Check if at least one specified property has a non-empty value
                if any(property_values.get(prop) for prop in properties):
                    # Check if any property value meets or exceeds the user input
                    if any(is_valid_int(value) and int(value) >= pips for value in property_values.values()):
                        matching_rows.append((name_value, property_values))

        # Print "Match Found!"
        print("\nMatch Found!")

        # Print count and matching rows after iterating through the entire CSV file
        count = len(matching_rows)
        if count > 0:
            print(f"Number of matches: {count}")
            for name_value, property_values in matching_rows:
                print(f"\nName: {name_value}")
                print(f"Properties: {property_values}")
        else:
            print("No matching rows found in the other CSV file.")

    except FileNotFoundError:
        print(f"Error: The CSV file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def is_valid_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def main():
    while True:
        user_input = input("Enter a name to look up (or type 'exit' to quit): ")

        if user_input.lower() == 'exit':
            break  # Exit the loop if the user types 'exit'

        properties = lookup_properties(user_input)

        if properties is not None:
            print(f"Properties for {user_input}: {properties}")
            pips = int(input("Enter the number of pips (1-6): "))
            print("Searching for matching rows...\n")

            get_values_for_columns(properties, pips)
        else:
            print(f"Name '{user_input}' not found in the CSV file.")

if __name__ == "__main__":
    main()
