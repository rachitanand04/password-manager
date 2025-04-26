from userSession import logIn
from accountCreation import addUser, deleteUser
from gen import generate_password

import mysql.connector
import os


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Racram_123",
    database = "password_manager"
    )

cursor = db.cursor()
os.system('clear')

while(True):
    print(f"Choose an option: \n 1. Log in\n 2. Create User\n 3. Delete User\n 4. Generate password\n 5. Exit")
    choice = int(input("Enter choice: "))
    

    if(choice == 1):
        logIn(cursor,db)
    elif(choice == 2):
        addUser(cursor)   
    elif(choice == 3):
        deleteUser(cursor)
    elif(choice == 4):
        generate_password()
    elif(choice == 5):
        cursor.close()
        break
    db.commit()
    print()
    