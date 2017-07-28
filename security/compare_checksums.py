import hashlib
import sys
import os

#terminal colors
import colorama
from colorama import (Fore, Style)
colorama.init(convert=True)

class Files:
    """Mixin class for file handling"""

    def __init__(self):
        pass

    @staticmethod
    def read_file(filename, mode='r'):

        filename = os.path.abspath(filename)
        with open(filename, mode) as f:
            return f.read()

class HashCheck(Files):
    """Class for comparing a provided checksum file against the locally
    generated checksum of that file"""

    def __init__(self, target_file=None, checksum_file=None):
        self.target_file = target_file
        self.checksum_file = checksum_file

    def generate_checksums(self):
        """Returns tuple containing the generated SHA256 checksum for
        self.target_file, and the SHA256 checksum provided with the
        target_file"""

        provided_checksum = self.read_file(self.checksum_file)[0:64]
        generated_checksum = hashlib.sha256(self.read_file(self.target_file, 'rb')).hexdigest()

        return (provided_checksum, generated_checksum)

    def compare_checksums(self):
        """Compares and prints out results of generated and provided checksums"""

        print("\n --------------------------------Comparing Now--------------------------------\n")

        checksums = self.generate_checksums()
        print(" Provided  : ", checksums[0])
        print(" Generated : ", checksums[1])

        if checksums[0] == checksums[1]:
            print("\n --------------------------{}SUCCESS: Checksums Match{}---------------------------\n".format(Fore.CYAN, Style.RESET_ALL))
        else:
            print("\n ************************{}FAIL: Checksums DO NOT Match{}*************************\n".format(Fore.RED, Style.RESET_ALL))

def _main(target, checksum):
    """Prints out comparison of two checksums: one generated from a file, and
    one provided with the file to be checked.  File names are provided via
    command line."""

    my_hash = HashCheck(target_file=target, checksum_file=checksum)
    my_hash.compare_checksums()

if __name__ == '__main__':
    os.system('cls')
    _main(sys.argv[1], sys.argv[2])

