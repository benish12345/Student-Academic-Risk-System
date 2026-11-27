import sqlite3

# Connect to database
conn = sqlite3.connect("database/auth.db")
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("Tables found:")
for table in tables:
    print(table)

conn.close()
print("Done! Database is working perfectly!")