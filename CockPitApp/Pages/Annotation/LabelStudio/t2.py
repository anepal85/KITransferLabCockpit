import sqlite3
import os 


path = 'C:/Users/anjit/AppData/Local/label-studio/label-studio/'
# Open a connection to the database file
conn = sqlite3.connect(os.path.join(path, 'label_studio.sqlite3'))

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# # List all the tables in the database
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# output = cursor.fetchall()


# # Print the table names
# for row in output:
#     print(row)

# List all the tables in the database
cursor.execute("SELECT * FROM auth_permission;")
output = cursor.fetchall()


# Print the table names
for row in output:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
