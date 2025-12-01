import csv
import sqlite3
import os

def initialize_database():
    """Initialize the database with required tables and sample data"""
    conn = sqlite3.connect('velora.db')
    cursor = conn.cursor()

    # Create sys_command table for system applications
    query = "CREATE TABLE IF NOT EXISTS sys_command (id INTEGER PRIMARY KEY, name VARCHAR(100), path VARCHAR(1000))"
    cursor.execute(query)

    # Create web_command table for web applications
    query = "CREATE TABLE IF NOT EXISTS web_command(id INTEGER PRIMARY KEY, name VARCHAR(100), url VARCHAR(1000))"
    cursor.execute(query)

    # Create contacts table
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255))''')

    # Insert some default system commands
    default_sys_commands = [
        ('notepad', 'notepad.exe'),
        ('calculator', 'calc.exe'),
        ('paint', 'mspaint.exe'),
        ('chrome', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'),
        ('firefox', 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'),
    ]

    for name, path in default_sys_commands:
        cursor.execute("INSERT OR IGNORE INTO sys_command (name, path) VALUES (?, ?)", (name, path))

    # Insert some default web commands
    default_web_commands = [
        ('youtube', 'https://www.youtube.com/'),
        ('google', 'https://www.google.com/'),
        ('github', 'https://www.github.com/'),
        ('stackoverflow', 'https://stackoverflow.com/'),
        ('gmail', 'https://mail.google.com/'),
    ]

    for name, url in default_web_commands:
        cursor.execute("INSERT OR IGNORE INTO web_command (name, url) VALUES (?, ?)", (name, url))

    # Import contacts from CSV if it exists
    if os.path.exists('contacts.csv'):
        try:
            with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)  # Skip header if exists
                for row in csvreader:
                    if len(row) >= 2:  # Ensure we have at least name and mobile
                        name = row[0].strip()
                        mobile = row[1].strip() if len(row) > 1 else ''
                        email = row[2].strip() if len(row) > 2 else ''
                        if name and mobile:
                            cursor.execute("INSERT OR IGNORE INTO contacts (name, mobile_no, email) VALUES (?, ?, ?)", 
                                         (name, mobile, email))
        except Exception as e:
            print(f"Error importing contacts: {e}")

    # Add some sample contacts if none exist
    cursor.execute("SELECT COUNT(*) FROM contacts")
    if cursor.fetchone()[0] == 0:
        sample_contacts = [
            ('John Doe', '1234567890', 'john@example.com'),
            ('Jane Smith', '9876543210', 'jane@example.com'),
        ]
        for name, mobile, email in sample_contacts:
            cursor.execute("INSERT INTO contacts (name, mobile_no, email) VALUES (?, ?, ?)", (name, mobile, email))

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()