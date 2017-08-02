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
            

    def get_parser_args(self):
        """Calls method responsible for adding subparser arguments, after which,
        non-emtpy arguments retrieved through parser are returned as a dictionary"""
        pass
    
        
    def create_verify_subparser(self):
        """Creates the 'verify' subparser and adds related arguments"""

        verify_parser = self.subparser.add_parser('verify',
            help="Generate a hash digest from a binary and compare it against \
            a provided SHA-digest")

        verify_parser.add_argument('-d', '--digest', 
            required=True, metavar="STRING|FILENAME", 
            help="Either a string or filename containing the SHA-2 hash digest")           

        verify_parser.add_argument('-bin', '--binary-file', dest='binary', 
            required=True, metavar="FILENAME", 
            help="Binary file to compare the provided SHA digest against")

        verify_parser.add_argument('--insecure' 
            metavar='HASH-ALGORITHM', choices=['md5', 'sha1']
            help="WARNING: MD5 and SHA-1 suffer from vulnerabilties (MD5 to a \
            much greater extent)  While SHA-1 is significantly more secure \
            than MD5, recent collision attacks have demonstrated its \
            vulnerabilities as well, albeit at the cost of significant \
            computational resources. This switch must be used with the HA's \
            name if you want to use them for comparing digests.") 


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
