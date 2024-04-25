import csv
import json

# Prompt user for input file name
input_file = input("Enter the input CSV file name: ")

# Check if input file name ends with ".csv"
if not input_file.endswith(".csv"):
    print("Error: Input file name must end with '.csv'")
    exit(1)

# Prompt user for output file name
output_file = input("Enter the output JSON file name: ")

# Check if output file name ends with ".json"
if not output_file.endswith(".json"):
    print("Error: Output file name must end with '.json'")
    exit(1)

with open(input_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    data = list(reader)

with open(output_file, 'w') as jsonfile:
    json.dump(data, jsonfile)

print(f"Conversion successful! The new JSON file is {output_file}")
