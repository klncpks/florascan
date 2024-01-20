import csv
import json

# Load the JSON data
with open("Enter the path to the .json file in the dataset") as json_file:
    data = json.load(json_file)

# Create a CSV file and write the header
with open('output.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['ID', 'Plant_Name'])

    # Write data to CSV
    for key, value in data.items():
        writer.writerow([key, value])
