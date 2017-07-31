# ----------------------------Compatibility Imports----------------------------
from __future__ import print_function
from builtins import dict
from six.moves import range
# -----------------------------------------------------------------------------

import hashlib
import argparse
import colorama
import sys
import os
import hmac  # Python 2.7 and 3.3+


# TODO: Implement argparse
# TODO: Implement hash method choices


class HashCheck(object):
    """Class for comparing a provided checksum file against the locally
    generated checksum of that file"""

    def __init__(self, digest_sources):
        self.digest_sources = digest_sources
        self.digests = self.process_digest_sources()


    def process_digest_sources(self):
        """Returns list of tuples containing hash digests from
        self.digest_sources.  If digest is either generated from, or provided
        through a file filename, source is sent to approriate file handling
        method first."""

        digests = []
        file_sources = {'txt': self.read_digest_file, 
                        'bin': self.generate_digest}

        for attr, values in self.digest_sources.items():
            while values:
                value = values.pop(0)
                if attr in file_sources.keys():
                    digests.append((attr, file_sources[attr](value)))                
                else:
                    digests.append((attr, value))

        return digests

    @staticmethod
    def read_digest_file(filename):
        """Returns contents of provided checksum file (if one is provided)"""

        with open(filename, 'r') as f:
            return f.read().split(' ')[0]

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
        

    def compare_digests(self):
        """Compares and prints out results of generated and provided hash digest"""

        print("\n --------------------------------Comparing Now--------------------------------\n")

        digest_1, digest_2 = self.digests[0][1], self.digests[1][1]

        for digest in self.digests:
            print(" {}:{}".format(digest[0].upper(), digest[1]))

        if hmac.compare_digest(digest_1, digest_2):
            print("\n ---------------------------{}SUCCESS: Digests Match{}----------------------------\n".format(
                colorama.Fore.CYAN, colorama.Style.RESET_ALL))
        else:
            print("\n ************************{}FAIL: Digests DO NOT Match{}*************************\n".format(
                colorama.Fore.RED, colorama.Style.RESET_ALL))


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
        non-emtpy arguments retrieved through parser are returned as a dictionary"""

        self.add_arguments()
        parsed_args = vars(self.parser.parse_args())        
        
        # Check that only 2 digest sources provided
        if sum(len(values) for values in parsed_args.values() if values) != 2:
            print("ERROR: hashchk uses 2 and ONLY 2 digest sources")
            sys.exit("""Check that digest sources meet this requirement.""")
        else:
            return parsed_args


    def add_arguments(self):
        """Organizational method for holding arguments added to self.parser
        object."""

        self.parser.add_argument(
            '-bin', '--binary-file', action="append", metavar='FILENAME', dest='bin',
            help="Generate a hash digest of the following file")

        self.parser.add_argument(
            '-txt', '--text-file', action="append", metavar='FILENAME', dest='txt', 
            help="Read the digest stored in the following .txt file")

        self.parser.add_argument(
            '-stdin', '--standard-input', action="append", metavar='STRING', dest='stdin', 
            help="Take the following string as a hash digest")


def main():
    """Prints out comparison of two hash digests: one generated from a file, and
    one provided with the file to be checked.  File names are provided via
    command line."""

    os.system('cls')
    colorama.init(convert=True)

    parsed_args = HashChkParser().args
    HashCheck(parsed_args).compare_digests()

    
if __name__ == '__main__':
    main()
