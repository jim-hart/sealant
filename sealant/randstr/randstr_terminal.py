"""Classes and functions that provide terminal integration for RandomString
methods.

Todo:
    * Look into adding switch that allows character set to be built from ASCII
      attributes found in string module.  This would allow user to quickly
      override default character set with basic sub-sets like 'only lowercase
      letters', or 'all lower-case, upper-case, and digits'.
"""

import os
import sys
import argparse
import pyperclip

from randstr import RandomString


class RandstrParser(object):
    """Class for managing argparse objects and arguments

    Attributes:
        parser (:obj:`ArgumentParser`): Parent argparse object used by all
            parser arguments.
    """

    def __init__(self):
        self.parser = self.create_parser()

        self.add_parser_arguments()

    @staticmethod
    def create_parser():
        """
        Returns:
            :obj:`ArgumentParser`: Parent argparse object used by all parser
                arguments.
        """
        return argparse.ArgumentParser(
            description="Generate a cryptographically secure randomized string.",
            epilog="""\tDefault character set includes all ASCII upper and \
                   lower case letters, digits, punctuation, and a character \
                   space.""")

    def add_parser_arguments(self):
        """Adds parser arguments that define characteristics of the randomly
        generated string, and how that string should be output."""

        self.parser.add_argument(
            'len', type=int, metavar='LENGTH',
            help="""Length of the randomized string.  By default, length is \
            limited by default to 1000 characters unless the --remove-limit \
            is switch provided. Values exceeding the default limit will be \
            reduced to 1000 if the --remove-limit switch is not included.""")

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

        randomization_options.add_argument(
            '-rl', '--remove-limit', action='store_true', dest='remove_limit',
            help="""Removes the default 1000 character length limit imposed on \
            string generation.  Please note strings in excess of ten-thousand \
            (10K) characters may cause unintended or undesirable \
            side-effects.""")

    @property
    def args(self):
        """:obj:`NameSpace`: User arguments parsed by argparse parser object"""
        return self.parser.parse_args()


class RandstrOutput(object):
    """Class for controlling how the randomly generated string is output

    Attributes:
        args (obj:`NameSpace`): Arguments parsed by RandstrParser; used as
            control switches for different output options.
        generated_string (str): Randomly generated string retrieved through
            _generated_string property.
    """

    def __init__(self, parsed_args):
        self.args = parsed_args
        self.generated_string = self._generated_string

    @property
    def _generated_string(self):
        """str: randomly generated string via RandomString() class."""

        if self.args.remove_limit:
            str_length = self.args.len
        else:
            str_length = self.args.len if self.args.len <= 1000 else 1000

        string_generator = RandomString(
            length=str_length, shuffle=self.args.shuffle,
            user_char_set=self.args.characters)

        return string_generator()

    def process_parsed_args(self):
        """Dispatches output control based on whether or not the --raw-output
        switch was provided to the argparser."""

        if self.args.raw_output:
            self.print_raw_output()
        else:
            self.print_formatted_output()

    def print_raw_output(self):
        """Suppresses any kind of output formatting and/or verbose output so
        only randomly generated string is printed to terminal."""

        sys.stdout.write(self.generated_string)

        if self.args.file:
            _write_file(self.generated_string, self.args.file)

        if self.args.copy:
            pyperclip.copy(self.generated_string)

    def print_formatted_output(self):
        """Displays randomly generated string with additional information like
        visual delimiters and status messages."""

        print("\n{}Length: {}{}".format(
            '---------------------------------', len(self.generated_string),
            '---------------------------------'))

        if self.args.print:
            print()
            print(self.generated_string)

        if self.args.file:
            _write_file(self.generated_string, self.args.file)
            print("\nOutput written to: {}".format(
                os.path.abspath(self.args.file)))

        if self.args.copy:
            pyperclip.copy(self.generated_string)
            print("\nOutput String copied to clipboard")

        print("\n{}{}".format(
            '---------------------------------------',
            '--------------------------------------'))


def _write_file(random_string, filename):
    """Utility function for writing randomly generated strings to a file.

    Args:
        random_string (str)
        filename (str)
    """

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


if __name__ == '__main__':
    terminal_output = RandstrOutput(RandstrParser().args)
    terminal_output.process_parsed_args()
