import hashlib
import sys
import os

# terminal colors
import colorama
from colorama import (Fore, Style)

colorama.init(convert=True)


# TODO: Implement argparse
# TODO: Implement hash method choices

class Files:
    """Mixin class for file handling"""
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

    def read_checksum(self):
        """Reads the provided checksum file"""
        return self.read_file(self.checksum_file)[0:64]

    def generate_checksum(self):
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

    def compare_checksums(self):
        """Compares and prints out results of generated and provided checksums"""

        print("\n --------------------------------Comparing Now--------------------------------\n")

        provided_checksum = self.read_checksum()
        generated_checksum = self.generate_checksum()
        print(" Provided  : ", provided_checksum)
        print(" Generated : ", generated_checksum)

        if provided_checksum == generated_checksum:
            print("\n --------------------------{}SUCCESS: Checksums Match{}---------------------------\n".format(
                Fore.CYAN, Style.RESET_ALL))
        else:
            print("\n ************************{}FAIL: Checksums DO NOT Match{}*************************\n".format(
                Fore.RED, Style.RESET_ALL))


def main(target, checksum):
    """Prints out comparison of two checksums: one generated from a file, and
    one provided with the file to be checked.  File names are provided via
    command line."""

    my_hash = HashCheck(target_file=target, checksum_file=checksum)
    my_hash.compare_checksums()


if __name__ == '__main__':
    # Test cases
    os.system('cls')
    main(sys.argv[1], sys.argv[2])
