import sqlite3
import numpy as np
import pandas as pd

#creating array with data to be uploaded in db
arr = np.array([["nalini", "bisht",9898], ["rachit","phartiyal",4567],["mrinalini","bisht",6789]])

try:
    #connecting to db employee
    conn=sqlite3.connect('employee.db')
    print("Connection successful!")
except sqlite3.OperationalError as e:
    print(f"OperationalError: {e}")

try:
    #initiate the db as active
    c=conn.cursor()
    #creating table with ID as key for unique value
    c.execute("""CREATE TABLE IF NOT EXISTS employee(
                 first_name text,
                 last_name text,
                 ID integer PRIMARY KEY
              )""")
    print("Table created successfully!")
except sqlite3.IntegrityError as e:
        print(f"IntegrityError: {e}")
length=int(len(arr))

#inserting array data into db table
i=0
for i in range(length):
    c.execute("INSERT INTO employee VALUES (?,?,?)",arr[i])
    i+=1
conn.commit()

#getting data from employee db and converting it into dataframe
query = "SELECT * FROM employee"
data_frame = pd.read_sql(query, conn)
print(data_frame.head())

#creating csv file and exporting dataframe to csv
csv_file_name = 'exported_data.csv'
data_frame.to_csv(csv_file_name, index=False)
print(f"Data exported to '{csv_file_name}' successfully.")
conn.commit()
conn.close()