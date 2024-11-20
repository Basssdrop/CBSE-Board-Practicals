# 1.
with open('input.txt', 'r') as file:
    for line in file:
        words = line.split()
        print('#'.join(words))

# 2.
vowels = "aeiouAEIOU"
consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"

vowel_count = consonant_count = uppercase_count = lowercase_count = 0

with open('input.txt', 'r') as file:
    for line in file:
        for char in line:
            if char.isupper():
                uppercase_count += 1
            if char.islower():
                lowercase_count += 1
            if char in vowels:
                vowel_count += 1
            elif char in consonants:
                consonant_count += 1

print(f"Vowels: {vowel_count}, Consonants: {consonant_count}, Uppercase: {uppercase_count}, Lowercase: {lowercase_count}")

# 3.
with open('input.txt', 'r') as infile, open('output.txt', 'w') as outfile:
    for line in infile:
        if 'a' not in line and 'A' not in line:
            outfile.write(line)

# 4.
import pickle

data = [{'roll_no': 1, 'name': 'Alice'}, {'roll_no': 2, 'name': 'Bob'}]

with open('students.dat', 'wb') as file:
    pickle.dump(data, file)

roll_no_to_search = int(input("Enter roll number to search: "))

with open('students.dat', 'rb') as file:
    students = pickle.load(file)
    for student in students:
        if student['roll_no'] == roll_no_to_search:
            print(f"Name: {student['name']}")
            break
    else:
        print("Roll number not found.")

# 5.
import pickle

data = [{'roll_no': 1, 'name': 'Alice', 'marks': 85}, {'roll_no': 2, 'name': 'Bob', 'marks': 90}]

with open('students.dat', 'wb') as file:
    pickle.dump(data, file)

roll_no_to_update = int(input("Enter roll number to update marks: "))
new_marks = int(input("Enter new marks: "))

with open('students.dat', 'rb') as file:
    students = pickle.load(file)

for student in students:
    if student['roll_no'] == roll_no_to_update:
        student['marks'] = new_marks
        print("Marks updated.")
        break
else:
    print("Roll number not found.")

with open('students.dat', 'wb') as file:
    pickle.dump(students, file)

# 6.
import random

dice_roll = random.randint(1, 6)
print(f"Dice rolled: {dice_roll}")

# 7.
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            print("Stack is empty.")

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            print("Stack is empty.")

    def is_empty(self):
        return len(self.stack) == 0

# 8.
import csv

with open('users.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['user_id', 'password'])
    writer.writerow(['user1', 'pass123'])
    writer.writerow(['user2', 'secure456'])

user_id_to_search = input("Enter user ID to search: ")

with open('users.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['user_id'] == user_id_to_search:
            print(f"Password: {row['password']}")
            break
    else:
        print("User ID not found.")
        
# 9. SQL
import sqlite3

# Connect to SQLite (or create a database file)
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Create the student table
cursor.execute("""
CREATE TABLE IF NOT EXISTS student (
    roll_no INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    marks INTEGER
)
""")

# Insert sample data
cursor.executemany("""
INSERT INTO student (roll_no, name, age, marks)
VALUES (?, ?, ?, ?)
""", [
    (1, 'User1', 20, 85),
    (2, 'User2', 21, 90),
    (3, 'User3', 20, 75),
    (4, 'User4', 22, 88),
    (5, 'User5', 20, 92)
])
conn.commit()

# --------- SQL Operations ---------

# ALTER TABLE: Add new attribute
try:
    cursor.execute("ALTER TABLE student ADD COLUMN email TEXT")
except sqlite3.OperationalError:
    print("Column 'email' already exists.")

# UPDATE: Modify data
cursor.execute("UPDATE student SET marks = 95 WHERE roll_no = 3")
conn.commit()

# ORDER BY: Display data in ascending and descending order
print("Ascending Order by Marks:")
for row in cursor.execute("SELECT * FROM student ORDER BY marks ASC"):
    print(row)

print("\nDescending Order by Marks:")
for row in cursor.execute("SELECT * FROM student ORDER BY marks DESC"):
    print(row)

# DELETE: Remove tuple(s)
cursor.execute("DELETE FROM student WHERE age > 21")
conn.commit()
print("\nAfter Deletion:")
for row in cursor.execute("SELECT * FROM student"):
    print(row)

# GROUP BY: Find min, max, sum, count, and average of marks grouped by age
print("\nGROUP BY Age with Aggregates:")
cursor.execute("""
SELECT age, MIN(marks), MAX(marks), SUM(marks), COUNT(*), AVG(marks)
FROM student
GROUP BY age
""")
for row in cursor.fetchall():
    print(f"Age: {row[0]}, Min: {row[1]}, Max: {row[2]}, Sum: {row[3]}, Count: {row[4]}, Avg: {row[5]}")

# Close connection
conn.close()
