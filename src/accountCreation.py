from hash import SHA_256
import os

def addUser(cursor):
    os.system('clear')
    userId = input("Enter user ID: ")
    userId = SHA_256(userId.encode())
    cursor.execute("SELECT userid FROM master WHERE userid = %s", (userId,))
    result = cursor.fetchone()
    
    if(result):
        print("User exists")
        return
    else:
        password = input("Enter password: ")
        salt = os.urandom(16)
        password = SHA_256(password.encode(),salt)
        cursor.execute("INSERT INTO master VALUES(%s, %s, %s)",(userId,salt,password))
    
    print("New user created successfully")
    
def deleteUser(cursor):
    os.system('clear')
    userId = input("Enter user ID: ")
    userId = SHA_256(userId.encode())
    cursor.execute("SELECT * FROM master WHERE userid = %s", (userId,))
    result = cursor.fetchone()
    
    if(result):
        masterPassword = input("Enter master password to confirm: ")
        masterPassword = SHA_256(masterPassword.encode(),result[1])
        if(masterPassword == result[2]):
            cursor.execute("DELETE FROM master WHERE (userid = %s);", (userId,))
            cursor.execute("DELETE FROM passwords WHERE (masteruser = %s);", (userId,))
            print("User deleted successfully")
        else:
            return
    else:
        print("User doesn't exist")
    