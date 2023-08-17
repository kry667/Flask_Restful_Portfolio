import random
import string
import secrets

def password_generator() -> str:
    
    password_list = []

    for _ in range(12):
        password_list.append(secrets.choice(string.ascii_letters))

    for _ in range(2):
        password_list.append(secrets.choice(string.punctuation))

    for _ in range(2):
        password_list.append(secrets.choice(string.digits))

    for index, value in enumerate(password_list):
      if value == "l":
        password_list[index] = "L"
      if value == "O":
        password_list[index] = "o"

    random.shuffle(password_list)
  
    password = ''.join(password_list)
    
    return password

print(password_generator())
