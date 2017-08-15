# ----------------------------Compatibility Imports----------------------------
from __future__ import print_function
from six.moves import range

import sys
import hashlib

if sys.version_info < (3, 6):
    # noinspection PyUnresolvedReferences
    import sha3
# -----------------------------------------------------------------------------

import os
import hmac  # Python 2.7 and 3.3+


# TODO: Implement SHAKE and BLAKE
# TODO: Resist urge to call it "SHAKE'N BLAKE"
# TODO: Allow user to pass get_hash_method string of hashlib hexdigest call

class Digest(object):
    """Class for comparing, processing, and generating hash digests."""

    def __init__(self, hash_family):
        self.hash_family = hash_family

    def get_hash_method(self, sha_digest=None):
        """Returns SHA method to be used for digest comparison

        Args:
            sha_digest (str): user provided hex-digest used to determine SHA method

        Returns:
            str: exact name of built in hashlib method as a string
        """

        hash_methods = {
            'sha2': {56: 'sha224', 64: 'sha256', 96: 'sha384', 128: 'sha512'},
            'sha3': {56: 'sha3_224', 64: 'sha3_256', 96: 'sha3_384', 128: 'sha3_512'}
        }

        insecure_methods = ['md5', 'sha1']

        if self.hash_family not in insecure_methods:
            return hash_methods[self.hash_family][len(sha_digest)]
        else:
            return self.hash_family

    @staticmethod
    def process_digest(digest):
        """Determines if source of digest is stored in a text file, or if it's a
        string provided by user.

        Args:
            digest (str): filename or string containing digest to be processed

        Returns:
            str: hash digest stripped of leading and trailing whitespace
        """

        if os.path.isfile(digest):
            with open(digest, 'r') as f:
                return f.read().split(' ')[0]
        else:
            return digest.strip()

    def generate_digest(self, filename):
        """Returns hexadecimal digest generated from filename

        Args:
            filename (str): filename of binary file

        Returns:
            str: hash digest generated from binary file
        """

        buffer_size = 65536  # Buffer used to cut down on memory for large files.
        blocks = (os.path.getsize(filename) // buffer_size) + 1

        hash_object = getattr(hashlib, self.get_hash_method())()

        with open(filename, 'rb') as f:
            # generator expression used for reading file in chunks
            generator = (f.read(buffer_size) for _ in range(blocks))
            for data in generator:
                hash_object.update(data)

        return hash_object.hexdigest()


def compare_digests(digest_1, digest_2):
    """Returns result of equality comparison between digest_1 and digest_2.  Included

    Args:
        digest_1 (str): digest to be compared against digest_2
        digest_2 (str): digest to be compared against digest_1

    Returns:
        bool: result of comparison of digest_1 and digest_2
    """

    return hmac.compare_digest(digest_1, digest_2)


if __name__ == '__main__':
    pass
