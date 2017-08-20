from __future__ import print_function
from six.moves import range
import string

# -----------------------------Randomization Method----------------------------
"""SystemRandom access determined by python interpreter version.  Python 3.6+
uses secrets module while all other versions use random.SystemRandom().
Additional details can be found in README."""

import random
try:
    import secrets as RAND_METHOD

    print('\nSystem Python Version >= 3.6 | Using secrets module')
except ImportError:
    RAND_METHOD = random.SystemRandom()
    print('\nSystem Python Version < 3.6 | Using random.SystemRandom')


# -----------------------------------------------------------------------------


class RandomString(object):
    """Class for generating random strings based on default, or user-defined
    parameters"""

    def __init__(self, length, shuffle, user_char_set):
        """
        Args:
            length (int)  -- Defines length of randomized string.
            shuffle (bool)-- If true, char_set is shuffled via
                             self.shuffle_characters() method prior to
                             randomization process.
            char_set (str)-- String of characters to be used as sample
                             population for randomization process.  Defaults to
                             ASCII character space, uppercase, lowercase, and
                             punctuation characters if no argument provided.
        """

        self.length = length
        self.shuffle = shuffle
        self.char_set = user_char_set or self.default_char_set

    def __repr__(self):
        """Returns object instance itself as representation of randomized
        string"""

        return self.generate_random_string()

    def generate_random_string(self):
        """Returns a randomized string of either preset, or user-defined
        length."""



        if self.shuffle:
            self.char_set = self.shuffle_characters(list(self.char_set))

        return "".join(
            [RAND_METHOD.choice(self.char_set) for _ in range(0, self.length)])

    @staticmethod
    def shuffle_characters(char_set):
        """Method for shuffling character set between 3-5 times.  Shuffle count
        is randomly chosen."""

        shuffle_count = RAND_METHOD.choice(list(range(3, 6)))

        for _ in range(0, shuffle_count):
            random.shuffle(char_set)

        return "".join(char_set)

    @property
    def default_char_set(self):
        return ''.join(
            char for char in string.printable if char not in '\t\n\r\f\v')

if __name__ == '__main__':
    pass
