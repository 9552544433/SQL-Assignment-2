import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('email_counts.db')
cur = conn.cursor()

# Create the Counts table if it doesn't exist
cur.execute('''
DROP TABLE IF EXISTS Counts''')
cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)
''')

# Prompt for the file name
file_name = input('Enter file name: ')
if len(file_name) < 1:
    file_name = 'mbox.txt'

try:
    # Open the file
    with open(file_name, 'r') as file:
        for line in file:
            # Look for lines that start with 'From '
            if not line.startswith('From '):
                continue
            
            # Extract the email address
            pieces = line.split()
            email = pieces[1]
            
            # Extract the domain name
            domain = email.split('@')[1]
            
            # Insert or update the count for the domain name
            cur.execute('SELECT count FROM Counts WHERE org = ? ', (domain,))
            row = cur.fetchone()
            if row is None:
                cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (domain,))
            else:
                cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (domain,))
        
        # Commit changes to the database
        conn.commit()
        
except FileNotFoundError:
    print(f"Error: File '{file_name}' not found.")
    conn.close()
    exit()

# Print the results
print('Counts:')
cur.execute('SELECT org, count FROM Counts ORDER BY count DESC')

for row in cur.fetchall():
    print(row[0], row[1])

# Close database connection
conn.close()
