import os
import sys
import argparse
import datetime

import pyperclip
from randstr import RandomString


class RandstrParser(object):
    """Class for managing argparse object and arguments"""

    def __init__(self):
        self.parser = self.create_parser()

        self.add_parser_arguments()

    @staticmethod
    def create_parser():
        """Returns parser object used for all argparse arguments"""

        return argparse.ArgumentParser(
            description="Generate a cryptographically secure randomized string.",
            epilog="""\tDefault character set includes all ASCII upper and lower \
                   case letters, digits, punctuation, and a character space.""")

    def add_parser_arguments(self):
        """Adds parser arguments that define characteristics of the randomly
        generated string"""

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

        _time = datetime.datetime.now().strftime('%a%d-%H%M%S')
        output_options.add_argument(
            '-f', '--file', default="output_str_{}.txt".format(_time),
            help="""Write output string to .txt file in cwd; if no filename is \
                   provided, name will default to current date and time""")

        # Character set and shuffle options
        random_options = self.parser.add_argument_group('Randomization Options')
        random_options.add_argument(
            '-cs', '--character-set', type=str, default=None,
            help="""Overrides default character set with characters in the \
                 provided string""")

        random_options.parser.add_argument(
            '-s', '--shuffle', action='store_true',
            help="""Pre-shuffle character positions in character set 3-5 times \
                 (randomly chosen)""")

    @property
    def args(self):
        return self.parser.parse_args()


def _write_file(file_data, filename):
    """Writes file_data to filename in programs working directory"""

    with open(filename, 'w') as f:
        f.write(file_data)

    print("Output written to: {}\n".format(os.path.abspath(sys.argv[0])))


def main():
    """Main flow control for program"""

    parser_args = RandstrParser().args
    randomized_string = str(
        RandomString(length=parser_args.length, shuffle=parser_args.shuffle,
                     user_char_set=parser_args.characters))

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

    # END ------------------------------------
    print("{} END {}".format(
        '------------------------------------',
        '------------------------------------'))


if __name__ == '__main__':
    main()
