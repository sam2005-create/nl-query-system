from db import init_db

# wipes the table and puts the sample students back
init_db(reset=True)
print("Database reset with sample data.")
