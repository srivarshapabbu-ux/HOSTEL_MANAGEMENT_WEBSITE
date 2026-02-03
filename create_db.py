import sqlite3

conn = sqlite3.connect('sru_hostel.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS users")

c.execute("""
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    name TEXT,
    phone TEXT
)
""")

users = [
    ("2303A51295", "2303a51295@sru.edu.in", "student123", "student", "Alice", "9999999999"),
    ("2303A51060", "", "student125", "warden", "Bob", "8999999999"),
    ("2303A51337", "", "student126", "parent", "Charlie", "7999999999"),
]

c.executemany("""
INSERT INTO users (id, email, password, role, name, phone)
VALUES (?, ?, ?, ?, ?, ?)
""", users)

conn.commit()
conn.close()

print("Database created: sru_hostel.db")
