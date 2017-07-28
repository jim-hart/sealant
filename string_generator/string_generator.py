from __future__ import print_function
from functools import wraps

import os
import sys
import random
import string
import time

# ----------------------------Randomization Method-----------------------------
"""This program utilizes SystemRandom, which generates cryptographically random
data from an OS-specific source. Windows uses CryptGenRandom() while *nix should
use /dev/urandom.  If neither is avaibable, the program won't work.

The module used to invoke SystemRandom depends on the version of Python used to
run this file.  3.6+ will use the secrets module while anything lower uses
random.SystemRandom; in either case, the result is the same: SystemRandom gets
called.

The inclusion of the secrets module was to utilize newer Python modules if
available.  Because secrets is available on only the latest versions of Python,
a backwards compatible method was included as well."""

try:
    import secrets as RAND_METHOD
    print('System Python Version >= 3.6 | Using secrets module\n')
except ImportError:
    RAND_METHOD = random.SystemRandom()
    print('System Python Version < 3.6 | Using random.SystemRandom\n')
# -----------------------------------------------------------------------------


def benchmark(function):
    """Decorator for benchmarking string creation time"""
    @wraps(function)
    def function_wrapper(*args, **kwargs):

        print("Function : {}()".format(function.__name__))
        print("Benchmark: ", end='')
        sys.stdout.flush()

        start = time.time()
        result = function(*args, **kwargs)
        print("{:4.3f}s\n".format(time.time()-start))

        return result
    return function_wrapper


class RandomString(object):
    """Class for generating random strings based on default, or user-defined
    parameters"""

    def __init__(self, char_set=None, length=None, shuffle=False):
        """
        Args:
        length (int) -- defines length of randomized string. If not provided,
                        function will default length to the length of
                        self.char_set
        char_set (list[str]) -- list containing single string elements.  If not
                                provided, ASCII upper, lower, punctuation, and
                                whitespace (single) characters will comprise
                                sample population for the randomization process
        shuffle (bool) -- If true, char_set is shuffled via
                               _shuffle_characters() method prior to
                               randomization process
        """

        self.char_set = char_set or (string.ascii_letters+' '+string.punctuation)
        self.length = length or len(self.char_set)
        self.shuffle = shuffle


    def __repr__(self):
        """Returns object instance itself as representation of randomized string"""

        return self._generate_random_string()

    @benchmark
    def _generate_random_string(self):
        """Returns a randomized string of either pre-set, or user-defined length.

        Args:
            shuffle (bool) -- If True, character list is sent to _shuffle()
            function
        """

        if self.shuffle:
            self.char_set = _shuffle_characters(list(self.char_set))

        return "".join([RAND_METHOD.choice(self.char_set) for _ in range(0, self.length)])


    @benchmark
    def _shuffle_characters(self):
        """Method for shuffling character set between 3-5 times.  Shuffle count
        is randomly chosen."""

        shuffle_count = secrets.choice(range(3, 6))

        for _ in range(0, shuffle_count):
            random.shuffle(self.char_set)

        return "".join(self.char_set)


def main(output_file=False):

    randomized_string = str(RandomString())

    if output_file:
        filename = 'randomized_string.txt'
        with open(filename, 'w') as f:
            f.write(randomized_string)
        print("Output string written to: {}".format(os.path.abspath(sys.argv[0])))

    else:
        print("Output: {}\nLength: {}\n".format(randomized_string, len(randomized_string)))

if __name__ == '__main__':
    main()