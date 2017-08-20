import os
import sys
import argparse
import datetime
import string

import pyperclip
from randstr import RandomString


class RandstrParser(object):
    """Class for managing argparse object and arguments"""

    def __init__(self):
        self.parser = self.create_parser()
        self.args = self.get_parser_args()

    @staticmethod
    def create_parser():
        """Returns parser object used for all argparse arguments"""

        return argparse.ArgumentParser(
            description="Generate a cryptographically secure randomized string.",
            epilog="""\tDefault character set includes all ASCII upper and lower \
                   case letters, digits, punctuation, and a character space.""")

    def get_parser_args(self):
        """Calls methods that add arguments to parser objects, after which, it
        returns arguments parsed from user input."""

        self.add_input_parameters()
        self.add_output_parameters()

        return self.parser.parse_args()

    def add_input_parameters(self):
        """Adds parser arguments that define characteristics of the randomly
        generated string"""

        # length
        self.parser.add_argument(
            '-l', '--length', type=int, required=True,
            help="Length of the randomized string")

        # character set
        default_charset = "".join(
            [char for char in string.printable if char not in '\t\n\r\f\v'])

        self.parser.add_argument(
            '-cs', '--characters', type=str, default=default_charset,
            help="""Overrides default character set with characters in the \
                 provided string""")

        # shuffle
        self.parser.add_argument(
            '-s', '--shuffle', action='store_true',
            help="""Pre-shuffle character positions in set 3-5 times \
                 (randomly chosen)""")

    def add_output_parameters(self):
        """Adds parser arguments that define how the randomly generated
        string should be output"""

        # terminal output
        self.parser.add_argument(
            '-p', '--print', action='store_true',
            help="Print output string to terminal")

        # copy output
        self.parser.add_argument(
            '-cp', '--copy', action='store_true',
            help="Copy output string to clipboard")

        # file output
        filename = "output_str_{}.txt".format(
            datetime.datetime.now().strftime('%a%d-%H%M%S'))

        self.parser.add_argument(
            '-f', '--file', nargs='?', const=filename,
            help="""Write output string to .txt file in cwd; if no filename is \
                   provided, name will default to current date and time""")


def _write_file(file_data, filename):
    """Writes file_data to filename in programs working directory"""

    with open(filename, 'w') as f:
        f.write(file_data)

    print("Output written to: {}\n".format(os.path.abspath(sys.argv[0])))


def main():
    """Main flow control for program"""

    parser_args = RandStrParser().args
    randomized_string = str(
        RandomString(length=parser_args.length, shuffle=parser_args.shuffle,
                     char_set=parser_args.characters))

    # Printout verifies if string is desired length
    print("\n{} len(randomized_string):{} {}".format(
        '-------------------------', len(randomized_string),
        '-------------------------\n'))

    if parser_args.print:
        print("Output:{}\n".format(randomized_string))

    if parser_args.file:
        _write_file(randomized_string, parser_args.file_output)

    if parser_args.copy:
        pyperclip.copy(randomized_string)
        print("Output String copied to clipboard\n")

    #  END ------------------------------------
    print("{} END {}".format(
        '------------------------------------',
        '------------------------------------'))


if __name__ == '__main__':
    main()
