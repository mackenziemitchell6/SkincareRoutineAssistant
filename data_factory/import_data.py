import os
import pandas as pd
import sqlite3


def import_csv_to_sqlite(db_name, csv_folder):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Iterate over all CSV files in the folder
    for csv_file in os.listdir(csv_folder):
        if csv_file.endswith(".csv"):
            csv_path = os.path.join(csv_folder, csv_file)

            # Load the CSV file into a pandas DataFrame
            df = pd.read_csv(csv_path)

            # Use the filename as the table name
            table_name = os.path.splitext(csv_file)[0]

            # Insert the DataFrame into the SQLite database
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"Imported {csv_file} into table {table_name}")

    conn.commit()
    conn.close()


def display_table_data(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Execute a query to retrieve all data from the specified table
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)

    # Fetch all rows from the query result
    rows = cursor.fetchall()

    # Print the column names
    column_names = [description[0] for description in cursor.description]
    print(column_names)

    # Print each row of data
    for row in rows:
        print(row)

    # Close the connection
    conn.close()


# Specify the database name and the folder containing CSV files
db_name = 'skincare.db'
csv_folder = 'raw_data'

# Run the import function
import_csv_to_sqlite(db_name, csv_folder)

# Call the function to display the data
display_table_data(db_name, 'product_info')