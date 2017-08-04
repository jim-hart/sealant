# ----------------------------Compatibility Imports----------------------------
from __future__ import print_function
from six.moves import range
# -----------------------------------------------------------------------------

import hashlib
import argparse
import colorama
import os
import sys
import hmac  # Python 2.7 and 3.3+


# TODO: Implement hash method choices
# TODO: Repent for not adding doc-strings, then add the doc-strings
class HashCheck(object):
    """Class for comparing, processing, and generating hash digests"""

    @staticmethod
    def process_digest(digest):
        """Either returns digest read from file, or returns digest with
        leading/trailing whitespace stripped.  Process action based on digest
        source."""

        if os.path.isfile(digest):
            with open(digest, 'r') as f:
                return f.read().split(' ')[0]
        else:
            return digest.strip()

    @staticmethod
    def generate_digest(filename):
        """Returns hexadecimal digest generated from filename"""

        # File is read in 4096 byte blocks to cut down on memory usage
        blocks = (os.path.getsize(filename) // 4096) + 1
        hash_digest = hashlib.sha256()

        with open(filename, 'rb') as f:
            # Blocks are read via generator expression for improved performance
            generator = (f.read(4096) for _ in range(blocks))
            for data in generator:
                hash_digest.update(data)

        return hash_digest.hexdigest()

    @staticmethod
    def compare_digests(digest_1, digest_2):
        """Returns True if digest_1 == digest_2"""

        return hmac.compare_digest(digest_1, digest_2)


class HashChkParser(object):
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
                "---------------------------", colorama.Fore.CYAN,
                colorama.Style.RESET_ALL, "----------------------------"))
        else:
            print("\n {}{}FAIL: Digests DO NOT Match{}{}\n".format(
                "************************", colorama.Fore.RED,
                colorama.Style.RESET_ALL, "*************************"))


def compare_verify_digests(verify_args):
    """Takes in parsed arguments from verify subparser and prints out comparison
    results"""

    Output.print_comparison_startup()

    # provided printout
    provided_digest = HashCheck.process_digest(verify_args.digest)
    print(" Provided :{}".format(provided_digest))

    # stdout used to provide status message while digest is being generated
    sys.stdout.write(' Generated: {}'.format('Calculating'.center(60)))
    generated_digest = HashCheck.generate_digest(args.binary)
    sys.stdout.write("\r Generated:{}\n".format(generated_digest))

    # Compare and printout results
    result = HashCheck.compare_digests(provided_digest, generated_digest)
    Output.print_comparison_results(result)


if __name__ == '__main__':
    os.system('cls')
    colorama.init(convert=True)

    args = HashChkParser().get_parser_args()
    compare_verify_digests(args)
