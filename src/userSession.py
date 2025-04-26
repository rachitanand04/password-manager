from aes import encrypt,decrypt
from kdf import KDF
from hash import SHA_256

import os

def deleteList(masterPassword,cursor):
    deleteArray = []
    count = 0
    for i in cursor:
        count+=1
        print(count)
        showPassword(masterPassword,i)
        deleteArray.append(i)
    return deleteArray

def checkExistence(masterUserId,userid,service,cursor):
    cursor.execute("SELECT * FROM passwords WHERE(masteruser = %s AND userid = %s AND service = %s)",(masterUserId, userid, service))
    result = cursor.fetchall()
    if(result):
        return True
    return False

def search(masterUserId,masterPassword,cursor):
    os.system('clear')
    print(f"Choose an option: \n 1. Search by username\n 2. Search by service\n 3. Search by both username and service")
    choice = int(input("Enter choice: "))
    if(choice == 1):
        user = input("Enter user id: ")
        cursor.execute("SELECT * FROM passwords WHERE(masteruser = %s AND userid LIKE %s)",(masterUserId, f"%{user}%"))
        result = cursor.fetchall()
        if result:
            for i in result:
                print()
                showPassword(masterPassword,i)
        else:
            print("Query returned no results")
            return

    elif(choice == 2):
        service = input("Enter service name: ")
        cursor.execute("SELECT * FROM passwords WHERE(masteruser = %s AND service LIKE %s)",(masterUserId,f"%{service}%"))
        result = cursor.fetchall()
        if result:
            for i in result:
                print()
                showPassword(masterPassword,i)
        else:
            print("Query returned no results")
            return
            
    elif(choice == 3):
        user = input("Enter user id: ")
        service = input("Enter service name: ")
        cursor.execute("SELECT * FROM passwords WHERE(masteruser = %s AND userid LIKE %s AND service LIKE %s)",(masterUserId, f"%{user}%",f"%{service}%"))
        result = cursor.fetchall()
        if result:
            for i in result:
                print()
                showPassword(masterPassword,i)
        else:
            print("Query returned no results")
            return

def delete(masterUserId,masterPassword,cursor):
    os.system('clear')
    print(f"Choose an option: \n 1. Search by username\n 2. Search by service\n 3. Search by both username and service")
    choice = int(input("Enter choice: "))
    deleteArray = []
    count = 0;
    
    if(choice == 1):
        user = input("Enter user id: ")
        cursor.execute("SELECT * FROM passwords WHERE(masteruser = %s AND userid LIKE %s)",(masterUserId, f"%{user}%"))
        result = cursor.fetchall()
        if result:
            print()
            deleteArray = deleteList(masterPassword,result)
        else:
            print("Query fetched no results")
            return

    elif(choice == 2):
        service = input("Enter service name: ")
        cursor.execute("SELECT * FROM passwords WHERE(masteruser = %s AND service LIKE %s)",(masterUserId,f"%{service}%"))
        result = cursor.fetchall()
        if result:
            print(result)
            deleteArray = deleteList(masterPassword,result)
        else:
            print("Query fetched no results")
            return
            
    elif(choice == 3):
        user = input("Enter user id: ")
        service = input("Enter service name: ")
        cursor.execute("SELECT * FROM passwords WHERE(masteruser = %s AND userid LIKE %s AND service LIKE %s)",(masterUserId, f"%{user}%",f"%{service}%"))
        result = cursor.fetchall()
        if result:
            print()
            deleteArray = deleteList(masterPassword,result)
        else:
            print("Query fetched no results")
            return
    
    deleteIndex = int(input("Enter number of the password to be deleted or 0 to cancel: "))
    deleteIndex -= 1
    if(deleteIndex>len(deleteArray)):
        print("Enter valid index")
        return
    elif(deleteIndex == -1):
        print("Operation cancelled")
        return
    
    cursor.execute("DELETE FROM passwords WHERE(masteruser = %s AND userid = %s AND service = %s)",(deleteArray[deleteIndex][0],deleteArray[deleteIndex][2],deleteArray[deleteIndex][1]))

        
def showPassword(masterPassword,i):
    print(f"Service Name:{i[1]}")
    print(f"User Id:{i[2]}")
    key = KDF(masterPassword,i[3])
    encrypted = i[4]
    plaintext = decrypt(encrypted,key)
    print(f"Password:{plaintext.decode()}")
    print()


def logIn(cursor, db):
    userId = input("Enter user ID: ")
    userId = SHA_256(userId.encode())
    cursor.execute("SELECT * FROM master WHERE userid = %s", (userId,))
    result = cursor.fetchone()
    
    if(result):
        masterPassword = input("Enter master password: ")
        masterPassword = SHA_256(masterPassword.encode(),result[1])
        if(masterPassword == result[2]):
            print("User logged in successfully")
            userSession(userId,masterPassword,cursor, db)
            return
        else:
            print("Incorrect password")
            return  
    else:
        print("Invalid user")
        return
 
   
def userSession(masterUserId,masterPassword,cursor,db):
    os.system('clear')
    while(True):
        print(f"Choose an option: \n 1. Save Password\n 2. View all Passwords\n 3. Search Password\n 4. Delete Password\n 5. Exit")
        choice = int(input("Enter choice: "))
        if(choice == 1):
            service = input("Enter service name: ")
            userid = input("Enter user id: ")
            if checkExistence(masterUserId,userid,service,cursor):
                print("Entry already exists")
                continue
            
            password = input("Enter password: ")
            
            salt = os.urandom(16)
            key = KDF(masterPassword, salt)
            cursor.execute("INSERT INTO passwords VALUES(%s, %s, %s, %s, %s)", (masterUserId, service, userid, salt, encrypt(password.encode(),key)))
            db.commit()
            
        elif(choice == 2):
            cursor.execute("SELECT * FROM passwords WHERE(masteruser = %s)",(masterUserId,))
            print()
            for i in cursor:
                showPassword(masterPassword,i)
        elif(choice == 3):
            search(masterUserId,masterPassword,cursor)
        elif(choice == 4):
            delete(masterUserId,masterPassword,cursor)
            db.commit()
        elif(choice == 5):
            os.system('clear')
            return;