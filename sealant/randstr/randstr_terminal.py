"""Classes and functions that provide terminal integration for RandomString
methods.

Todo:
    * Add some kind of safety check to ensure OS brick-leveling strings aren't
      created because of typo in length argument
    * Look into adding switch that allows character set to be built from ASCII
      attributes found in string module.  This would allow user to quickly
      override default character set with basic sub-sets like 'only lowercase
      letters', or 'all lower-case, upper-case, and digits'.
    * Rewrite randstr_output as class to imrpove flow-control

"""

import os
import sys
import argparse

import pyperclip
from randstr import RandomString


class RandstrParser(object):
    """Class for managing argparse objects and arguments

    Attributes:
        parser (obj): main argparse object
    """

    def __init__(self):
        self.parser = self.create_parser()

        self.add_parser_arguments()

    @staticmethod
    def create_parser():
        """Returns parser object used for all argparse arguments"""

        return argparse.ArgumentParser(
            description="Generate a cryptographically secure randomized string.",
            epilog="""\tDefault character set includes all ASCII upper and \
                   lower case letters, digits, punctuation, and a character \
                   space.""")

    def add_parser_arguments(self):
        """Adds parser arguments that define characteristics of the randomly
        generated string."""

        self.parser.add_argument(
            'len', type=int, metavar='LENGTH',
            help="Length of the randomized string")

        # Terminal, clipboard, and file output options
        output_options = self.parser.add_argument_group('Output Options')
        output_options.add_argument(
            '-p', '--print', action='store_true',
            help="Print output string to terminal")

        output_options.add_argument(
            '-cp', '--copy', action='store_true',
            help="Copy output string to clipboard")

        output_options.add_argument(
            '-f', '--file', nargs='?', const=_generate_filename(),
            help="""Write output string to .txt file in cwd; if no filename is \
                   provided with this switch, a default name will be \
                   assigned.""")

        output_options.add_argument(
            '-ro', '--raw-output', action='store_true', dest='raw_output',
            help="""Limits output to only randomized string.  Use this option \
            if you want to pipe output elsewhere, or if you don't want \
            additional details included in the printout.  This option \
            replaces --print if used.""")

        # Character set and shuffle options
        randomization_options = self.parser.add_argument_group(
            'Randomization Options')
        randomization_options.add_argument(
            '-cs', '--character-set',
            type=str, default=None, dest='characters', metavar='STRING',
            help="""Overrides default character set with characters in the \
                 provided string""")

        randomization_options.add_argument(
            '-s', '--shuffle', action='store_true',
            help="""Randomly shuffle character positions in character set prior
            to string generation.""")

    @property
    def args(self):
        """Returns arguments parsed from terminal"""

        return self.parser.parse_args()


def _write_file(random_string, filename):
    """Utility function for writing randomly generated strings to a file."""

    with open(filename, 'w') as f:
        f.write(random_string)


def _generate_filename():
    """Generates handle used by the .txt file that will hold randomly generated
    string.

    Returns:
        str: Unique filename in respect to current working directory
    """

    count = 1
    while os.path.exists("randstr_{}.txt".format(count)):
        count += 1

    return "randstr_{}.txt".format(count)


class RandstrOutput(object):
    def __init__(self, parsed_args):
        self.args = parsed_args

    def process_parsed_args(self):

        string_generator = RandomString(length=self.args.len,
                                        shuffle=self.args.shuffle, user_char_set=self.args.characters)

        randomized_string = string_generator()

        if self.args.raw_output:
            self.print_raw_output(randomized_string)
        else:
            self.print_formatted_output(randomized_string)

    def print_raw_output(self, randomized_string):

        sys.stdout.write(randomized_string)

        if self.args.file:
            _write_file(randomized_string, self.args.file)

        if self.args.copy:
            pyperclip.copy(randomized_string)

    def print_formatted_output(self, randomized_string):

        print("\n{}Length: {}{}".format(
            '---------------------------------', len(randomized_string),
            '---------------------------------'))

        if self.args.print:
            print()
            print(randomized_string)

        if self.args.file:
            _write_file(randomized_string, self.args.file)
            print("\nOutput written to: {}".format(
                os.path.abspath(self.args.file)))

        if self.args.copy:
            pyperclip.copy(randomized_string)
            print("\nOutput String copied to clipboard")

        print("\n{}{}".format(
            '---------------------------------------',
            '--------------------------------------'))


if __name__ == '__main__':
    terminal_output = RandstrOutput(RandstrParser().args)
    terminal_output.process_parsed_args()
