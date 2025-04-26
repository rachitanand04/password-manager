import random
import string

def generate_password():
    length = int(input("Enter length: "))
    if length < 4:
        raise ValueError("Password length must be at least 4 characters")
    
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    print(password)
