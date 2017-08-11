from __future__ import print_function

import argparse
import colorama

colorama.init(convert=True)

"""Argparse and terminal output classes"""


class HashChkParser(object):
    """Class for creating and assembling argparse object used in hashchk.py"""

    def __init__(self):
        self.parser = self.create_parser()
        self.subparser = self.create_subparser()

        self.add_subparser_parsers()

    @staticmethod
    def create_parser():
        """Returns main parser object used for all argparse arguments"""

        return argparse.ArgumentParser(
            description="Generate and compare hash digests")

    def create_subparser(self):
        """returns main subparser derived from self.parser"""

        return self.parser.add_subparsers(title="Commands",
                                          description="Available Actions")

    def add_subparser_parsers(self):
        """Calls methods responsible for adding parsers to main subparser"""

        self.add_verify_subparser()

    def add_verify_subparser(self):
        """Creates the 'verify' subparser and adds related arguments"""

        verify_parser = self.subparser.add_parser(
            'verify', action='store_true',
            help="Generate a hash digest from a binary and compare it against \
            a provided SHA-digest")

        verify_parser.add_argument(
            '-d', '--digest', required=True, metavar="STRING|FILENAME",
            help="Either a string or filename containing the SHA-2 hash digest")

        verify_parser.add_argument(
            '-bin', '--binary-file', dest='binary', required=True,
            metavar="FILENAME",
            help="Binary file to compare the provided SHA digest against")

        verify_parser.add_argument(
            '--insecure', metavar='HASH-ALGORITHM', choices=['MD5', 'SHA1'],
            help="""WARNING: MD5 and SHA1 are insecure hash algorithms; they \
            should only be used to check for unintentional data corruption. If \
            your options are limited to MD5 and/or SHA1, you can force \
            comparison using this switch followed by the HA name.""")

    def get_parser_args(self):
        """Returns arguments parsed by main argparse object"""

        return self.parser.parse_args()


class Output(object):
    """Organizational class for reusable printout messages"""

    @staticmethod
    def print_comparison_startup():
        """Prints out startup message for comparison process"""

        print("\n {}Comparing Now{}\n".format(
            "--------------------------------",
            "--------------------------------"))

    @staticmethod
    def print_comparison_results(comparison_result):
        """Prints out results of comparison between two hash digests"""

        if comparison_result:
            print("\n {}{}SUCCESS: Digests Match{}{}\n".format(
                "---------------------------", colorama.Fore.GREEN,
                colorama.Style.RESET_ALL, "----------------------------"))
        else:
            print("\n {}{}FAIL: Digests DO NOT Match{}{}\n".format(
                "************************", colorama.Fore.RED,
                colorama.Style.RESET_ALL, "*************************"))
