import sqlite3
from tabulate import tabulate

# connect to the database or create if it doesn't exist
conn = sqlite3.connect('petstore.db')

# db instance
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Pets(
               id INTEGER PRIMARY KEY,
               name TEXT NOT NULL,
               species TEXT NOT NULL,
               age INTEGER NOT NULL
               )
''')

# flush all changes into database
conn.commit()
print("statement executed")

cursor.executemany('''
INSERT INTO pets (name, species, age) VALUES (?, ?, ?)
''', [
    ('Buddy', 'Dog', 3),
    ('Mittens', 'Cat', 2),
    ('Charlie', 'Bird', 4),
    ('Oscar', 'Fish', 1)
])
conn.commit()


# insert a new pet
def create_pet(name, species, age):
    cursor.execute(
        '''INSERT INTO Pets (name, species, age) VALUES (?, ?, ?)''',
        (name, species, age)
        )
    conn.commit()


# retrieve from database
def read_pets():
    cursor.execute('SELECT * FROM Pets')
    rows = cursor.fetchall()    # fetches all data from db

    table2 = tabulate(rows, headers=['Id', 'Name', 'Species', 'Age'], tablefmt='grid')
    print(table2)             


# updating values
def update_pet(pet_id, new_name, new_age):
    cursor.execute('''
    UPDATE Pets SET name = ?, age = ? WHERE id = ?
    ''', (new_name, new_age, pet_id)
    )
    conn.commit()


# delete a pet
def delete_pet(pet_id):
    cursor.execute(
        '''DELETE FROM Pets WHERE id = ?''',
        (pet_id,)
        )
        
    conn.commit()


def menu():
    while True:
        print("""
            \nPet Store Management
              1. Add a new pet
              2. View all pets
              3. Update a pet
              4. Delete a pet
              5. Exit
        """)

        user_choice = input("Enter your choice (1-5): ")

        if user_choice == "1":
            name = input("Enter pet name: ")
            species = input("Enter pet species: ")
            age = int(input("Enter pet age: "))

            create_pet(name, species, age)
            print("Pet added to system")

        elif user_choice == "2":
            print("List of Pets: ")
            read_pets()
        elif user_choice == "3":
            pet_id = int(input("Enter pet ID to update: "))
            new_name = input("Entere new pet name: ")
            new_age = int(input("Enter new pet age: "))

            update_pet(pet_id, new_name, new_age, )
            print("Pet details updated successfuly!")
        elif user_choice == "4":
            pet_id = int(input("Enter pet ID to delete: "))
            delete_pet(pet_id)
            print("PEt has been deleted from system.")
        elif user_choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice entered. Try again. ")


# run the menu
menu()

# close the connection
conn.close()