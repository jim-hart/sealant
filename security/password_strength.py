import re
import sys
import string
import secrets
import argparse

#TODO: implement argparse

class RegexParameters(object):
    """Class for assembling custom regex search that defines password requirements"""

    def __init__(self, *args, password_length=8):
       self._check_keys(*args)
       self.password_length = password_length
       self.search_parameters = self._build_search(*args)
       self.character_set = self._get_character_set(*args)


    def _check_keys(self, *args):
        """Exits program if invalid regex search parameter provided. Error
        checking method used over try-except blocks to keep code in other areas
        more concise"""

        valid_keys = ('digit', 'upper', 'lower', 'special')
        invalid_keys = [key for key in args if key not in valid_keys]

        if invalid_keys:
            print("INVALID ARGUMENT(S) '{}' -- Only the following arguments are accepted:".format(invalid_keys))
            for valid_key in valid_keys:
                print("\t- {}".format(valid_key))
            sys.exit()


    def _build_search(self, *args):
        """Returns string containing regex search which is built from arguments
        contained in self.search_parameters, which are used as keys in
        regex_parameters"""

        regex_parameters = {
                            'digit': '(?=.*\d)',
                            'upper':'(?=.*[A-Z])',
                            'lower': '(?=.*[a-z])',
                            'special': '(?=.*[{} ])'.format(string.punctuation)
                           }

        regex_search = ''
        for parameter in args:
            regex_search += regex_parameters[parameter]

        return re.compile(r'(^(' + regex_search + '){'+ re.escape(str(self.password_length)) + ',}$)')


    def _get_character_set(self, *args):
        """Returns string which represents character set to be used when
        checking password strengths.  Set is based off arguments passed for
        regex setup"""

        character_groupings = {
                                'digit': string.digits,
                                'upper': string.ascii_lowercase,
                                'lower': string.ascii_uppercase,
                                'special': string.punctuation + ' '
                              }

        character_set = ''
        for parameter in character_groupings:
            character_set += character_groupings[parameter]

        return character_set


def _iteratative_strength_check(iterations=1000):
    """Acts as an analysis tool that highlights correlation between password
    strength, character set variety, and password length.

    The function will randomly generate a passwords of any length from a
    character set (either preset or user defined), and it will test those
    passwords against a regex search.

    Each password is generated using the secrets module, which builds a password
    character by character from the character_set parameter.  This function aims
    to show how likely a non-pseudo randomized strength of a certain length is
    likely to meet a set of password requirements."""

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


def check_password_strength():



def main():
    """Main flow control for password_strength.py"""
    pass

if __name__ == '__main__':
    # Test cases
    my_regex = RegexParameters('digit', 'upper', 'lower')
    print(my_regex.search_parameters)