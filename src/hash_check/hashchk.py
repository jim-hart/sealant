import hashlib
import sys
import os
import hmac  # Python 2.7 and 3.3+
import argparse

# terminal colors
import colorama
from colorama import (Fore, Style)

colorama.init(convert=True)


# TODO: Implement argparse
# TODO: Implement hash method choices


class HashCheck(object):
    """Class for comparing a provided checksum file against the locally
    generated checksum of that file"""

    def __init__(self, target_file, digest_file=None):
        self.target_file = target_file
        self.digest_file = digest_file

    def read_digest_file(self):
        """Returns contents of provided checksum file (if one is provided)"""

        with open(self.digest_file, 'r') as f:
            return f.read().split(' ')[0]

    def generate_digest(self):
        """Returns hexadecimal digest generated from self.target_file"""

        # File is read in 4096 byte blocks to cut down on memory usage
        blocks = (os.path.getsize(self.target_file) // 4096) + 1
        hash_digest = hashlib.sha256()

        with open(self.target_file, 'rb') as f:
            # Blocks are read via generator expression for improved performance
            generator = (f.read(4096) for _ in range(blocks))
            for data in generator:
                hash_digest.update(data)

        return hash_digest.hexdigest()

    def compare_digests(self):
        """Compares and prints out results of generated and provided hash digest"""

        print("\n --------------------------------Comparing Now--------------------------------\n")

        provided_digest = self.read_digest_file()
        generated_digest = self.generate_digest()
        print(" Provided  : ", provided_digest)
        print(" Generated : ", generated_digest)

        if hmac.compare_digest(provided_digest, generated_digest):
            print("\n ---------------------------{}SUCCESS: Digests Match{}----------------------------\n".format(
                Fore.CYAN, Style.RESET_ALL))
        else:
            print("\n ************************{}FAIL: Digests DO NOT Match{}*************************\n".format(
                Fore.RED, Style.RESET_ALL))


class HashChkParser(object):
    def __init__(self):
        self.parser = self.create_parser()
        self.args = self.get_parser_args()

    @staticmethod
    def create_parser():
        """Returns parser object used for all argparse arguments"""

        return argparse.ArgumentParser(
            description="Generate and compare hash digests", 
            epilog="""Hashchk requires two hash digests from any source.  It \
                   can generate digests from a file, read digests stored in \
                   .txt files, or be provided a digest directly through \
                   standard input.  Any combination of any two inputs (even \
                   the same input type twice) will be accepted.""")

    def get_parser_args(self):
        """Calls method responsible for adding parser arguments, after which,
        arguments retrieved through parser are returned"""

        self.add_arguments()

        return self.parser.parse_args()

    def add_arguments(self):
        """Organizational method for holding arguments added to self.parser
        object."""

        self.parser.add_argument(
            '-bin', '--binary-file', action="append", metavar='binary_files',
            help="Generate a hash digest of the following file")

        self.parser.add_argument(
            '-txt', '--text-file', action="append", metavar='text_files',
            help="Read the digest stored in the following .txt file")

        self.parser.add_argument(
            '-stdin', '--standard-input', action="append", metavar='input_str',
            help="Take the following string as a hash digest")


def main():
    """Prints out comparison of two hash digests: one generated from a file, and
    one provided with the file to be checked.  File names are provided via
    command line."""

    parser_args = HashChkParser().args
    print(parser_args)
    sys.exit()

    # my_hash = HashCheck(target_file=target_file, digest_file=digest_file)
    # my_hash.compare_digests()


if __name__ == '__main__':
    # Test cases
    main()
