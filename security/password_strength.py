import re
import string
import secrets
import random

def check_password_strength(password_length=8, iterations=1000, randomized_sequence=False):
    #1 digit, 1 uppercase, 1 lower case, variable length
    regex = re.compile(r'(^((?=.*\d)(?=.*[A-Z])(?=.*[a-z])).{'+ re.escape(str(password_length)) + ',}$)')

    #Optional randomization of initial set
    characters = list(string.ascii_letters+string.digits)
    if randomized_sequence:
        random.shuffle(characters)
    characters = "".join(characters)

    passed, failed = 0, 0
    for _ in range(iterations):
        password = "".join([secrets.choice(characters) for x in range(password_length)])
        if regex.findall("".join(password)):
            passed += 1
        else:
            failed += 1
            print('Failed: {}'.format(password))

    print()
    print('Pass: {}'.format(passed))
    print('Fail: {}'.format(failed))

check_password_strength(password_length=50, iterations=10000)

