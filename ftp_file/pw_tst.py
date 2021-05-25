import random
import string

i = 1
while i <= 42:
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 4))
    print(salt.lower())
    i += 1
