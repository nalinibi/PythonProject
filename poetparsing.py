import json
import csv
from dataclasses import field

import pandas as pd
from collections import Counter

# Load the JSON file


with open('Poet_Data.json', "r", encoding="utf-8") as json_file:
    poet_data = json.load(json_file)

# Define the CSV header
csv_headers = ["name", "language", "id", "bio", "version"]


# Write data to CSV file
with open('Raw_Poet_Data.csv', "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader()
    writer.writerows(poet_data)

#changing column name to Poet name
df=pd.DataFrame(poet_data)
df=df.rename(columns={'name':'Poet name'})
df.to_csv("Raw_Poet_Data.csv",index=False)


poet_names = [poet["name"] for poet in poet_data]
poet_counts = Counter(poet_names)

# Write occurrences to a new CSV file
with open('Poet_Occurrence.csv', "w", newline="", encoding="utf-8") as csv_file1:
    writer1 = csv.writer(csv_file1)
    writer1.writerow(["Poet", "Poet Occurrence"])  # Column headers
    for poet, count in poet_counts.items():
        writer1.writerow([poet, count])

# changing column name to first name and last name
poet_df=pd.read_csv("Poet_Occurrence.csv")
new = poet_df['Poet'].str.split(' ', expand=True)
poet_df['First Name'] = new[0]
poet_df['Last Name'] = new[1]


poet_df['Last Name']=poet_df['Last Name'].replace(['Solangi'],'Nolangi')
poet_df.to_csv("Poet_Occurrence.csv")

language_counts = Counter(poet["language"] for poet in poet_data)
with open('Language_Occurrence.csv', "w", newline="", encoding="utf-8") as csv_file2:
    lang_writer = csv.writer(csv_file2)
    lang_writer.writerow(["Language", "Language Occurrence"])

    for language, count in language_counts.items():
        lang_writer.writerow([language, count])


unique_poets = {}
for poet in poet_data:
    name = poet["name"]
    if name not in unique_poets:
        name_parts = name.split(maxsplit=1)  # Split into first and last name
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""  # Handle cases with no last name
        unique_poets[name] = {
            "Poet Name": name,
            "Poet First Name": first_name,
            "Poet Last Name": last_name,
            "bio": poet["bio"],
            "id": poet["id"],
            "language": poet["language"],
            "Language Occurrence": language_counts[poet["language"]],  # Add language occurrence
            "version": poet["version"],
        }

# Write unique poets data to a new CSV file
with open("Unique_Poet_Data.csv", "w", newline="", encoding="utf-8") as csv_file4:
    writer4 = csv.writer(csv_file4)
    writer4.writerow(["Poet Name", "Poet First Name", "Poet Last Name", "bio", "id", "language", "Language Occurrence", "version"])  # Column headers

    for poet in unique_poets.values():
        writer4.writerow([poet["Poet Name"], poet["Poet First Name"], poet["Poet Last Name"], poet["bio"],
                         poet["id"], poet["language"], poet["Language Occurrence"], poet["version"]])

print(f"CSV file has been saved as: {'Raw_Poet_Data.csv'}")
print(f"CSV file has been saved as: {'Poet_Occurrence.csv'}")
print(f"CSV file has been saved as: {'Language_Occurrence.csv'}")