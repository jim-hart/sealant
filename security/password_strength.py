import re
import sys
import string
import secrets
import random

#TODO: implement argparse

class RegexParameters(object):
    """Class for assembling custom regex search that defines password requirements"""

    def __init__(self, *args):
       self._check_keys(*args)
       self.search_parameters = self._build_search(*args)
       self.character_set = self._get_character_set(*args)


    def _check_keys(self, *args):
        """Exits program if invalid regex search parameter provided. Error
        checking method used over try|except blocks to keep code in other areas
        more concise"""

        valid_keys = ('digit', 'upper', 'lower', 'punctuation')
        invalid_keys = (key for key in args if key not in valid_keys)

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
                            'punctuation': '(?=.*[{} ])'.format(string.punctuation)
                           }

        regex_search = ''
        for parameter in args:
            regex_search += regex_parameters[parameter]

        return '({}).'.format(regex_search)


    def _get_character_set(self, *args):
        """Returns string which represents character set to be used when
        checking password strengths.  Set is based off arguments passed for
        regex setup"""

        character_groupings = {
                                'digit': string.digits,
                                'upper': string.ascii_lowercase,
                                'lower': string.ascii_uppercase,
                                'punctuation': '(?=.*[{} ])'.format(string.punctuation)
                              }

        character_set = ''
        for parameter in character_groupings:
            character_set += character_groupings[parameter]

        return character_set


def _regex_setup(*args, password_length=8):
    """Function for calling methods in RegexParameters, which builds regex search used to test password stength"""

    #default regex_parameters return: ((?=.*\d)(?=.*[A-Z])(?=.*[a-z])) - 1 digit, 1 uppercase, 1 lower case, variable length
    if not args:
        regex = RegexParameters('digit', 'upper', 'lower')
    else:
        regex = RegexParameters(args)

    regex_parameters  = regex_setup.search_parameters
    regex_charset = regex_setup.character_set
    regex = re.compile(r'(^' + regex_parameters + '{'+ re.escape(str(password_length)) + ',}$)')


def _check_password_strength(characters, iterations=1000):

    characters = list(string.ascii_letters+string.digits)

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


def main():
    """Main flow control for password_strength.py"""
    pass

if __name__ == '__main__':
    main()
