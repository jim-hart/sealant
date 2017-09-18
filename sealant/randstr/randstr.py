"""Methods for generating cryptographically secure random strings.

Todo:
    * Track last generated string?

"""

from __future__ import print_function
from six.moves import range

import importlib
import string
import random

""""Cryptographically secure random numbers are generated using SystemRandom
class.  The secrets module has a secrets.SystemRandom class, but this is just an
alias for random.SystemRandom. It's inclusion is to to favor newer Python
modules if available."""
try:
    RAND_METHOD = importlib.import_module('secrets')
except ImportError:
    RAND_METHOD = random.SystemRandom()


class RandomString(object):
    """Class for generating random strings based on default, or user-defined
    parameters

    Args:
        length (int): Desired length of randomized string.
        shuffle (bool, optional): If True, self.char_set will be shuffled prior
            to string generation.
        user_char_set (str, optional): Character set that will replace character
            set provided by self.default_char_set property.

    Attributes:
        length (int): Length of the randomly generated string.
        shuffle (bool): If True, self.char_set will be shuffled prior to string
            generation.
        char_set (str): character set to be used as population sample for
            randomization process.
    """

    def __init__(self, length=None, shuffle=False, user_char_set=None):
        self.length = length
        self.shuffle = shuffle
        self.char_set = user_char_set or self.default_char_set

    def __call__(self):
        """Allows calling RandomString() like a function for continual random
        string generation"""

        if self.length:
            return str(self.generate_random_string())

    def generate_random_string(self):
        """Returns randomized string generated using instance attributes as
        generation parameters"""

        if self.shuffle:
            self.shuffle_characters()

        return "".join(
            [RAND_METHOD.choice(self.char_set) for _ in range(0, self.length)])

    def shuffle_characters(self):
        """Implementation of Python's random.shuffle(), except random numbers
        generated for shuffle process use SystemRandom() instead.

        Although this implementation matches random.shuffle(), pseudo-RNGs
        produce values faster than cryptographically-secure-RNGs, making this
        implementation 3X slower."""

        char_list = list(self.char_set)
        for i in range(len(char_list) - 1, 1, -1):
            j = RAND_METHOD.randbelow(i + 1)
            char_list[i], char_list[j] = char_list[j], char_list[i]

        self.char_set = ''.join(char_list)

    @property
    def default_char_set(self):
        """Returns string containing ASCII lower case, upper case, and
        punctuation characters, and a single character space."""

        # Note character space at the end
        return '{s.ascii_letters}{s.digits}{s.punctuation} '.format(s=string)


if __name__ == '__main__':
    pass
