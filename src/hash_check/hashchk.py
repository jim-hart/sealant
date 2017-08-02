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

# TODO: Implement hash method choices
# TODO: Repent for not adding docstrings, then add the docstinrgs.  

class HashCheck(object):
    """Class for comparing a provided checksum file against the locally
    generated checksum of that file"""

    def __init__(self, digest_sources):
        pass

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

        pass

        # print("\n --------------------------------Comparing Now--------------------------------\n")

        # if hmac.compare_digest(digest_1, digest_2):
        #     print("\n ---------------------------{}SUCCESS: Digests Match{}----------------------------\n".format(
        #         colorama.Fore.CYAN, colorama.Style.RESET_ALL))
        # else:
        #     print("\n ************************{}FAIL: Digests DO NOT Match{}*************************\n".format(
        #         colorama.Fore.RED, colorama.Style.RESET_ALL))


class HashChkParser(object):
    def __init__(self):
        self.parser = self.create_parser()
        self.subparser = self.create_subparser()
        self.args = self.get_parser_args()

    @staticmethod
    def create_parser():
        """Returns parser object used for all argparse arguments"""

        return argparse.ArgumentParser(
            description="Generate and compare hash digests")

    def create_subparser(self):
        """Creates and returns subparser object derived from self.parser"""
        
        return self.parser.add_subparsers(title="Subcommands",
            description="Avaiable Actions")
            

    def get_subparser_args(self):
        """Calls method responsible for adding subparser arguments, after which,
        non-emtpy arguments retrieved through parser are returned as a dictionary"""

        self.add_arguments()
    
        
    def add_arguments(self):
        """Organizational method for holding arguments added to self.parser
        object."""

        pass


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
