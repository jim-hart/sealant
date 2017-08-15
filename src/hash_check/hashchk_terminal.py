"""Classes and functions for hashchk.py terminal use

Todo:
    * Finish adding doc strings
    * Re-implement SHAKE and BLAKE arguments
    * More tests on what arguments common argument groups return

"""
from __future__ import print_function
import os
import sys
import argparse
import difflib

from colorama import (Fore, Style, init)
import hashchk


class HashChkParser(object):
    """Class for creating and assembling argparse object used in hashchk.py

    Attributes:
        parser (obj): Top-level argparse object
        subparser (obj): Parent subparser object
    """

    def __init__(self):
        """Summary
        """
        self.parser = self.create_parser()
        self.subparser = self.create_subparser()

        self.add_verify_subparser()

    @staticmethod
    def create_parser():
        """Creates and returns main parser object used for all argparse
        arguments."""

        return argparse.ArgumentParser(
            description="Generate and compare hash digests")

    def create_subparser(self):
        """Creates and returns main subparser derived from self.parser."""

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

    def get_parser_args(self):
        """Returns arguments parsed by main argparse object

        Returns:
            obj: Namespace containing all arguments parsed through terminal

        """

        return self.parser.parse_args()


class Output(object):
    """Organizational class for reusable printout messages."""

    GREEN, RED, CYAN = Fore.GREEN, Fore.RED, Fore.CYAN
    BRIGHT, RESET = Style.BRIGHT, Style.RESET_ALL

    @staticmethod
    def print_comparison_startup():
        """Prints out startup message for comparison process
        """

        print("\n {}Comparing Now{}\n".format(
            "--------------------------------",
            "--------------------------------"))

    @classmethod
    def print_comparison_results(cls, comparison_result):
        """Prints out results of comparison between two hash digests

        Args:
            comparison_result (bool): Result of digest comparison
        """

        if comparison_result:
            print("\n {}{}{}SUCCESS: Digests Match{}{}\n".format(
                "---------------------------", cls.BRIGHT, cls.GREEN,
                cls.RESET, "----------------------------"))
        else:
            print("\n {}{}{}FAIL: Digests DO NOT Match{}{}\n".format(
                "************************", cls.BRIGHT, cls.RED,
                cls.RESET, "*************************"))

    @staticmethod
    def print_diffs(digest_1, digest_2, identifiers=None):
        """Summary

        Args:
            digest_1 (str): 1 of 2 digests used for diff comparison
            digest_2 (str): 2 of 2 digests used for diff comparison
            identifiers (list[str], optional): Prefix titles to distinguish
                digests apart
        """

        diffs = list(difflib.Differ().compare([digest_1+'\n'], [digest_2+'\n']))
        titles = identifiers or ['Digest1', 'Digest2']

        print("\n{}Diffs{}\n".format(
            "------------------------------------",
            "------------------------------------"))

        padding = max(len(title) for title in titles)
        for index, line in enumerate(diffs):
            if index in [0, 2]:
                sys.stdout.write("{:{p}}: {}".format(
                    titles.pop(0), line, p=padding))
            else:
                sys.stdout.write("{:{p}}  {}".format(" ", line, p=padding))

        print("{}End{}\n".format(
            "-------------------------------------",
            "-------------------------------------"))


def _compare_verify_digests(verify_args):
    """Takes in parsed arguments from HashChkParser verify subparser and prints
    out comparison results.

    Args:
        verify_args (:obo:`Namespace`): All arguments parsed from HashChkParser
    """

    Output.print_comparison_startup()
    digest = hashchk.Digest(
        hash_family=verify_args.hash_family, reference_digest=verify_args.digest)

    # provided printout
    provided_digest = digest.reference_digest
    print(" Provided :{}".format(provided_digest))

    # stdout used to provide status message while digest is being generated
    sys.stdout.write(' Generated: {}'.format('Calculating'.center(60)))
    generated_digest = digest.generate_digest(verify_args.binary)
    sys.stdout.write("\r Generated:{}\n".format(generated_digest))

    # Compare and printout results
    result = hashchk.compare_digests(provided_digest, generated_digest)
    Output.print_comparison_results(result)

    if verify_args.diff:
        Output.print_diffs(
            provided_digest, generated_digest, ['Provided', 'Generated'])


if __name__ == '__main__':
    os.system('cls')
    init(convert=True)  # colorama module

    args = HashChkParser().get_parser_args()
    _compare_verify_digests(args)
