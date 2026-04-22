import string
import random

def generateCardNumber():
    return int(''.join(random.choices(string.digits, k=16)))