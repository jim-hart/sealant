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

import os
import sys
import argparse
import difflib

import colorama
import hashchk

# ANSI escape sequences provided by colorama
RED, GREEN, CYAN = colorama.Fore.RED, colorama.Fore.GREEN, colorama.Fore.CYAN
BRIGHT, RESET_COLOR = colorama.Style.BRIGHT, colorama.Style.RESET_ALL


class HashChkParser(object):
    """Class for creating and assembling argparse object used in hashchk.py

    Attributes:
        parser (obj): Top-level argparse object
        subparser (obj): Parent subparser object
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Generate and compare hash digests")
        self.subparser = self.parser.add_subparsers(
            title="Commands", description="Available Actions")

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
            'digest', metavar="STRING|FILENAME",
            help="""Either a string or filename to a file containing a valid \
            hash digest""")

        req_group.add_argument(
            'binary', metavar="FILENAME|PATH/FILENAME",
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


class Terminal(object):
    """Class for reusable and dynamic output messages

    Attributes:
        width (int, optional): Length of digest plus predefined padding length
            of 7 to account for digest source prefix (i.e. provided vs
            generated).
    """

    def __init__(self, reference_length=None):
        self.width = (67 or reference_length) + 7

    def build_line_break(self, header, delimiter='-', color=None):
        """Dynamically generates visual line breaks by padding a centered header
        with some type of punctuation('-' by default).  Left/right padding
        length is determined by self.width attribute.

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


def _compare_verify_digests(args):
    """Takes in parsed arguments from HashChkParser verify subparser and prints
    out comparison results.

    Args:
        args (:obj:`Namespace`): Arguments parsed from verify subparser
    """

    digest = hashchk.Digest(reference_digest=args.digest, sha3=args.sha3)

    output = Terminal(reference_length=len(digest.reference_digest))
    print("\n{}\n".format(output.build_line_break(header='Comparing Now')))

    # provided printout
    provided_digest = digest.reference_digest
    print(" Provided :{}".format(provided_digest))

    # stdout used to provide status message while digest is being generated
    sys.stdout.write(' Generated: {}'.format('Calculating'.center(60)))
    generated_digest = hashchk.generate_digest(
        filename=args.binary,
        hash_method=args.hash_function or digest.hash_method)
    sys.stdout.write("\r Generated:{}\n".format(generated_digest))

    # Compare and printout results
    result = hashchk.compare_digests(provided_digest, generated_digest)
    output.print_comparison_results(result)

    if not result:
        output.print_diffs(
            provided_digest, generated_digest, ['Provided', 'Generated'])


if __name__ == '__main__':
    os.system('cls')
    colorama.init(convert=True)

    _compare_verify_digests(HashChkParser().args)
