from __future__ import print_function

import os
import sys
import argparse
import colorama
import hashchk

"""Classes and functions for hashchk terminal use"""


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
            help="Either a string or filename to a file containing the SHA hash \
            digest")

        verify_parser.add_argument(
            '-bin', '--binary-file', dest='binary', required=True,
            metavar="FILENAME",
            help="Binary file to compare the provided SHA digest against")

        verify_parser.add_argument(
            '-hf', '--hash-family', dest='hash_family', required=False,
            metavar="NAME", choices=['sha2, sha3'], default='sha2',
            help="The verify command defaults to SHA2 if the -hf switch isn't \
            provided. You can use this switch along with the hash-family's \
            name to override this default.  Specific hash functions within a \
            family are automatically determined by the length of the digest \
            provided to the -d switch.")

        verify_parser.add_argument(
            '--insecure', metavar='HASH-ALGORITHM', choices=['md5', 'sha1'],
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


def _compare_verify_digests(verify_args):
    """Takes in parsed arguments from HashChkParser verify subparser and prints
    out comparison results."""

    Output.print_comparison_startup()
    digest = hashchk.Digest()

    # provided printout
    provided_digest = digest.process_digest(verify_args.digest)
    print(" Provided :{}".format(provided_digest))

    # stdout used to provide status message while digest is being generated
    sys.stdout.write(' Generated: {}'.format('Calculating'.center(60)))
    generated_digest = digest.generate_digest(args.binary)
    sys.stdout.write("\r Generated:{}\n".format(generated_digest))

    # Compare and printout results
    result = hashchk.compare_digests(provided_digest, generated_digest)
    Output.print_comparison_results(result)


if __name__ == '__main__':
    os.system('cls')
    colorama.init(convert=True)
    args = HashChkParser().get_parser_args()
    _compare_verify_digests(args)
