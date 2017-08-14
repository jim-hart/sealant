from __future__ import print_function

import os
import sys
import argparse
import colorama
import hashchk

"""Classes and functions for hashchk terminal use"""


# TODO: Re-implement shake and blake
# TODO: More tests on what arguments common argument groups return


class HashChkParser(object):
    """Class for creating and assembling argparse object used in hashchk.py"""

    def __init__(self):
        self.parser = self.create_parser()
        self.subparser = self.create_subparser()

        self.add_verify_subparser()

    @staticmethod
    def create_parser():
        """Returns main parser object used for all argparse arguments"""

        return argparse.ArgumentParser(
            description="Generate and compare hash digests")

    def create_subparser(self):
        """returns main subparser derived from self.parser"""

        return self.parser.add_subparsers(
            title="Commands", description="Available Actions")

    def add_verify_subparser(self):
        """Creates the 'verify' subparser and adds related arguments"""

        verify_parser = self.subparser.add_parser(
            'verify',
            help="""Generate a hash digest from a binary and compare it against \
            a provided digest using SHA-2 (default) or SHA-3""")

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

        # Algorithm choices
        algorithms_group = verify_parser.add_argument_group('Algorithm Parameters')
        algorithms_group.add_argument(
            '-sha3', dest='hash_family', action='store_const', const='sha3',
            default='sha2',
            help="""Use SHA-3 (fixed length) instead of SHA-2. Regardless of \
            the SHA version used, bit length is determined automatically based \
            on the length of the provided digest.""")

        algorithms_group.add_argument(
            '--insecure', metavar='NAME', dest='hash_family', choices=['md5', 'sha1'],
            help="""WARNING: MD5 and SHA1 are insecure hash algorithms; they \
            should only be used to check for unintentional data corruption. \
            You can force use of one of these two methods by using this switch \
            along with the hash algorithm name.""")

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


def _compare_verify_digests(verify_args):
    """Takes in parsed arguments from HashChkParser verify subparser and prints
    out comparison results."""

    Output.print_comparison_startup()
    digest = hashchk.Digest(hash_family=verify_args.hash_family)

    # provided printout
    provided_digest = digest.process_digest(verify_args.digest)
    print(" Provided :{}".format(provided_digest))

    # stdout used to provide status message while digest is being generated
    sys.stdout.write(' Generated: {}'.format('Calculating'.center(60)))
    generated_digest = digest.generate_digest(verify_args.binary)
    sys.stdout.write("\r Generated:{}\n".format(generated_digest))

    # Compare and printout results
    result = hashchk.compare_digests(provided_digest, generated_digest)
    Output.print_comparison_results(result)


if __name__ == '__main__':
    os.system('cls')
    colorama.init(convert=True)
    args = HashChkParser().get_parser_args()
    _compare_verify_digests(args)
