"""Classes and functions for hashchk.py terminal use

Todo:
    * Re-implement SHAKE and BLAKE arguments
    * More tests on what arguments common argument groups return
    * Add property decorators
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
        self.parser = self.create_parser()
        self.subparser = self.create_subparser()

        self.add_verify_subparser()

    @staticmethod
    def create_parser():
        """Returns main parser object used for all argparse
        arguments."""

        return argparse.ArgumentParser(
            description="Generate and compare hash digests")

    def create_subparser(self):
        """Returns main subparser derived from self.parser."""

        return self.parser.add_subparsers(
            title="Commands", description="Available Actions")

    def add_verify_subparser(self):
        """Creates the 'verify' subparser and adds related arguments."""

        verify_parser = self.subparser.add_parser(
            'verify',
            help="""Generate a hash digest from a binary and compare it \
            against a provided digest using SHA-2 (default) or SHA-3""")

        # Required parameters group
        req_group = verify_parser.add_argument_group('Required Parameters')
        req_group.add_argument(
            '-d', '--digest', required=True, metavar="STRING|FILENAME",
            help="""Either a string or filename to a file containing a valid \
            hash digest""")

        req_group.add_argument(
            '-bin', '--binary', dest='binary', required=True,
            metavar="FILENAME|PATH/FILENAME",
            help="""Generates a hash digest of of the file located at \
            PATH/FILENAME, or just FILENAME if file is located in the cwd.""")

        # Algorithm choices group
        algorithms_group = verify_parser.add_argument_group('Algorithm Parameters')
        algorithms_group.add_argument(
            '-sha3', dest='hash_family', action='store_const', const='sha3',
            default='sha2',
            help="""Use SHA-3 (fixed length) instead of SHA-2. Regardless of \
            the SHA version used, bit length is determined automatically based \
            on the length of the provided digest.""")

        algorithms_group.add_argument(
            '--insecure',
            metavar='md5|sha1', dest='hash_family', choices=['md5', 'sha1'],
            help="""WARNING: MD5 and SHA1 are insecure hash algorithms; they \
            should only be used to check for unintentional data corruption. \
            You can force use of one of these two methods by using this switch \
            along with the hash algorithm name.""")

        # Output choices group
        output_group = verify_parser.add_argument_group('Output Options')
        output_group.add_argument(
            '-diff', dest='diff', action='store_true',
            help="Print differences (if any) between digests")

    @property
    def args(self):
        """Returns Namespace object containing arguments parsed by main argparse
        object"""

        return self.parser.parse_args()


class Terminal(object):
    """Class for reusable and dynamic output messages

    Attributes:
        width (int, optional): Length of digest plus predefined padding length
            of 7 to account for digest source prefix (i.e. provided vs
            generated).
    """

    def __init__(self, digest_length=None):
        self.width = (67 or digest_length) + 7

    def build_line_break(self, header, line_char='-', color=None):
        """Dynamically generates visual line breaks by padding a centered header
        with some type of punctuation('-' by default).  Left/right padding
        length is determined by self.width attribute.

        Args:
            header (str): Text to be centered
            line_char (str, optional): Character used to pad header with
            color (None, optional): color highlighting for header

        Returns:
            str: formatted string padded left/right with a repeating character
        """

        size = self.width - len(header)
        highlight = color if color else ''

        left_line = ''.join(line_char for _ in range(size // 2))
        right_line = ''.join(line_char for _ in range(size - (size // 2)))

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
                header='FAIL: Digests DO NOT Match', line_char='*', color=RED)))

    def print_diffs(self, d1, d2, identifiers=None):
        """Prints out `diff` style differences between two strings

        Args:
            d1 (str): 1 of 2 digests used for diff comparison
            d2 (str): 2 of 2 digests used for diff comparison
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

        print("{}\n".format(self.build_line_break('End')))


def _compare_verify_digests(verify_args):
    """Takes in parsed arguments from HashChkParser verify subparser and prints
    out comparison results.

    Args:
        verify_args (:obj:`Namespace`): All arguments parsed from HashChkParser
    """

    digest = hashchk.Digest(
        hash_family=verify_args.hash_family, reference_digest=verify_args.digest)

    output = Terminal(digest_length=len(digest.reference_digest))
    print("\n{}\n".format(output.build_line_break('Comparing Now')))

    # provided printout
    provided_digest = digest.reference_digest
    print(" Provided :{}".format(provided_digest))

    # stdout used to provide status message while digest is being generated
    sys.stdout.write(' Generated: {}'.format('Calculating'.center(60)))
    generated_digest = digest.generate_digest(verify_args.binary)
    sys.stdout.write("\r Generated:{}\n".format(generated_digest))

    # Compare and printout results
    result = hashchk.compare_digests(provided_digest, generated_digest)
    output.print_comparison_results(result)

    if verify_args.diff and not result:
        output.print_diffs(
            provided_digest, generated_digest, ['Provided', 'Generated'])


if __name__ == '__main__':
    os.system('cls')
    colorama.init(convert=True)

    _compare_verify_digests(HashChkParser().args)
