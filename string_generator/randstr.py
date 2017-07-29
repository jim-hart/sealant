from __future__ import print_function
from functools import wraps
from datetime import datetime

import os
import sys
import random
import string
import time
import pyperclip
import argparse  # Not Available for Python 3.0 and 3.1

# ----------------------------Randomization Method-----------------------------
"""This program utilizes SystemRandom, which generates cryptographically random
data from an OS-specific source. Windows uses CryptGenRandom() while *nix should
use /dev/urandom.  If neither is available, the program won't work.

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


def benchmark(func):
    """Decorator for benchmarking string creation time.  Useful for large string
    blocks"""

    @wraps(func)
    def function_wrapper(*args, **kwargs):
        print("Function : {}()".format(func.__name__))
        print("Benchmark: ", end='')
        sys.stdout.flush()

        start = time.time()
        result = func(*args, **kwargs)
        print("{:4.3f}s".format(time.time() - start))

        return result

    return function_wrapper


class RandomString(object):
    """Class for generating random strings based on default, or user-defined
    parameters"""

    def __init__(self, length, shuffle, char_set):
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
        self.char_set = char_set

    def __repr__(self):
        """Returns object instance itself as representation of randomized string"""

        return self.generate_random_string()

    @benchmark
    def generate_random_string(self):
        """Returns a randomized string of either preset, or user-defined length."""

        if self.shuffle:
            self.char_set = self.shuffle_characters(list(self.char_set))

        return "".join([RAND_METHOD.choice(self.char_set) for _ in range(0, self.length)])

    @staticmethod
    def shuffle_characters(char_set):
        """Method for shuffling character set between 3-5 times.  Shuffle count
        is randomly chosen."""

        shuffle_count = RAND_METHOD.choice(list(range(3, 6)))

        for _ in range(0, shuffle_count):
            random.shuffle(char_set)

        return "".join(char_set)


def _write_file(file_data, filename):
    """Writes file_data as filename in programs working directory"""

    with open(filename, 'w') as f:
        f.write(file_data)

    print("\nOutput written to: {}".format(os.path.abspath(sys.argv[0])))


def _get_args():
    """Sets up argparse object and returns all arguments gathered by the parser."""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Generate a cryptographically secure randomized string.",
        epilog="  Default character set includes all printable ASCII characters except:\n"
               "  tab, linefeed, return, formfeed, and vertical tab.")

    # -------------------------------Parameters--------------------------------
    # length
    parser.add_argument('l', 'length', type=int, required=True,
                        help="Length of the randomized string")

    # character set
    default_charset = string.digits + string.ascii_letters + ' ' + string.punctuation
    parser.add_argument('-cs', '--characters', type=str, default=default_charset,
                        help="Overrides default character set with characters in the provided string")

    # shuffle
    parser.add_argument('-s', '--shuffle', action='store_true',
                        help="Pre-shuffle character positions in set 3-5 times (randomly chosen)")

    # ---------------------------------Output----------------------------------
    # terminal output
    parser.add_argument('-po', '--print_output', action='store_true',
                        help='Print randomized string to terminal')

    # copy output
    parser.add_argument('-co', '--copy_output', action='store_true',
                        help='Copy randomized string to clipboard')

    # file output
    filename = "output_{}.txt".format(datetime.now().strftime('%a%d-%H%M%S'))
    parser.add_argument('-fo', '--file_output', nargs='?', const=filename,
                        help='Write randomized string to .txt file in cwd (filename optional)')

    return parser.parse_args()


def main():
    """Main flow control for program"""

    args = _get_args()

    randomized_string = str(
        RandomString(length=args.length, shuffle=args.shuffle, char_set=args.characters))

    if args.print_output:
        print("\nOutput:{}\nLength:{}".format(randomized_string, len(randomized_string)))
    if args.file_output:
        _write_file(randomized_string, args.file_output)
    if args.copy_output:
        pyperclip.copy(randomized_string)
        print("\nOutput String (length: {}) copied to clipboard".format(len(randomized_string)))


if __name__ == '__main__':
    main()
