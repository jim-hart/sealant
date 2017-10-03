"""Classes and functions for hashchk.py terminal use

Todo:
    * Re-implement SHAKE and BLAKE arguments
    * More tests on what arguments common argument groups return
    * Generate command
    * Compare command
"""

# ----------------------------Compatibility Imports----------------------------
from __future__ import print_function
from six.moves import range
# -----------------------------------------------------------------------------

import sys
import argparse
import difflib

import colorama
import hashchk

# ANSI escape sequences provided by colorama
RED, GREEN, CYAN = colorama.Fore.RED, colorama.Fore.GREEN, colorama.Fore.CYAN
BRIGHT, RESET_COLOR = colorama.Style.BRIGHT, colorama.Style.RESET_ALL


class HashchkParser(object):
    """Class for creating and assembling argparse object used in hashchk.py

    Attributes:
        parser (obj): Top-level argparse object
        subparser (obj): Parent subparser object
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Generate and compare hash digests")
        self.subparser = self.parser.add_subparsers(
            title="Commands", description="Available Actions", dest='command')

        self.add_verify_command()

    def add_verify_command(self):
        """Adds verify command and arguments to parent subparser object."""

        verify_parser = self.subparser.add_parser(
            'verify',
            help="""Generate a hash digest from a binary and compare it \
            against a provided digest using SHA-2 (default) or SHA-3""")

        # Required parameters
        req_group = verify_parser.add_argument_group('Required Parameters')
        req_group.add_argument(
            '-digest', metavar="STRING|FILENAME",
            help="""Either a string or filename to a file containing a valid \
            hash digest""")

        req_group.add_argument(
            '-binary', metavar="FILENAME|PATH/FILENAME",
            help="""Generates a hash digest of of the file located at \
            PATH/FILENAME, or just FILENAME if file is located in the CWD.""")

        # Hash method specifications
        algorithms_group = verify_parser.add_argument_group('Hash Methods')
        algorithms_group.add_argument(
            '-sha3', dest='sha3', action="store_true",
            help="""SHA3 will be used for hash digest generation instead of \
            SHA2 (used for automatic hash method detection).""")

        algorithms_group.add_argument(
            '-hf', '--hash-function', dest='hash_function', default=None,
            choices=['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
                     'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512'],
            help="""Override automatic detection of the hash method and \
            explicitly define the hash method used for digest verification.""")

    @property
    def args(self):
        """:obj:`NameSpace`: arguments parsed by main argparse object"""
        return self.parser.parse_args()


class HashchkOutput(object):
    """Class for managing methods related to different subcommands made
        available by HashchkParser.

    Attributes:
        args (obj:`NameSpace`): Subcommand arguments parsed by HashchkParser.
    """

    def __init__(self, parsed_args):
        self.args = parsed_args

    def dispatch_subparser(self):
        """Calls method associated with HashchkParser subcommand by dispatching
        `commands` dictionary"""

        commands = {'verify': self.verify_digests}
        commands[self.args.command]()

    def verify_digests(self):
        """Processes args parsed args by verify sub-command.  Processing results
        in the comparison of a provided hash digest against one generated from a
        binary."""

        digest = hashchk.Digest(
            reference_digest=self.args.digest, sha3=self.args.sha3)

        formatting = OutputFormatting(width=len(digest.reference_digest))
        print("\n{}\n".format(
            formatting.build_line_break(header='Comparing Now')))

        # provided printout
        provided_digest = digest.reference_digest
        print(" Provided :{}".format(provided_digest))

        # stdout used to provide status message while digest is being generated
        sys.stdout.write(' Generated: {}'.format('Calculating'.center(60)))
        generated_digest = hashchk.generate_digest(
            filename=self.args.binary,
            hash_method=self.args.hash_function or digest.hash_method)
        sys.stdout.write("\r Generated:{}\n".format(generated_digest))

        # Compare and printout results
        result = hashchk.compare_digests(provided_digest, generated_digest)
        formatting.print_comparison_results(result)

        if not result:
            formatting.print_diffs(
                provided_digest, generated_digest, ['Provided', 'Generated'])


class OutputFormatting(object):
    """Organizational class for reusable and dynamic output messages

    Attributes:
        width (int, optional): Length of display text plus predefined padding
            length of 7 to best account for different prefixes ('generated' and
            'provided') associated with said display text.
    """

    def __init__(self, width=None):
        self.width = (67 or width) + 7

    def build_line_break(self, header, delimiter='-', color=None):
        """Generates dynamically padded visual line breaks.

        Args:
            header (str): Text to be centered
            delimiter (str, optional): Character used to pad header with
            color (None, optional): color highlighting for header

        Returns:
            str: formatted string padded left/right with a repeating character
        """

        size = self.width - len(header)
        highlight = color if color else ''

        left_line = ''.join(delimiter for _ in range(size // 2))
        right_line = ''.join(delimiter for _ in range(size - (size // 2)))

        tag = "{}{}{}".format(highlight + BRIGHT, header, RESET_COLOR)
        return " {}{}{}".format(left_line, tag, right_line)

    def print_comparison_results(self, comparison_result):
        """Prints out results of comparison between two hash digests

        Args:
            comparison_result (bool): Result of digest comparison
        """

        if comparison_result:
            print("\n{}\n".format(self.build_line_break(
                header='SUCCESS: Digests Match', color=GREEN)))

        else:
            print("\n{}\n".format(self.build_line_break(
                header='FAIL: Digests DO NOT Match', delimiter='*', color=RED)))

    def print_diffs(self, d1, d2, identifiers=None):
        """Prints out `diff` style differences between two strings

        Args:
            d1 (str): digest1 used for diff comparison
            d2 (str): digest2 used for diff comparison
            identifiers (list[str], optional): Prefix titles to distinguish
                digests apart
        """

        diffs = list(difflib.Differ().compare([d1 + '\n'], [d2 + '\n']))
        titles = identifiers or ['Digest1', 'Digest2']

        print("\n{}\n".format(self.build_line_break(header='Diffs')))

        padding = max(len(title) for title in titles)
        for index, line in enumerate(diffs):
            if index in [0, 2]:
                sys.stdout.write(" {:{p}}: {}".format(
                    titles.pop(0), line, p=padding))
            else:
                sys.stdout.write(" {:{p}}  {}".format(" ", line, p=padding))

        print("{}\n".format(self.build_line_break(header='End')))


if __name__ == '__main__':
    colorama.init(convert=True)
    terminal = HashchkOutput(parsed_args=HashchkParser().args)
