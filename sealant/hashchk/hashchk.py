"""Classes and functions for creating and comparing hash digests

Todo:
    * Implement SHAKE and BLAKE
    * Resist urge to call it "SHAKE'N BLAKE"
    * Allow user to explicitly define hash method
"""

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
import hmac


class Digest(object):
    """Class for determining what hash generation method to use based off a
    provided reference digest.


    Attributes:
        hash_family (str): Name of base hash family name (md5, sha1, sha2, or
            sha3)
        reference_digest (str): Either a filename containing a generated hash
            digest, or the actual hash digest itself

    """

    def __init__(self, hash_family, reference_digest):
        self.hash_family = hash_family
        self.reference_digest = self.process_reference(reference_digest)

    @staticmethod
    def process_reference(source):
        """Determines if source of digest is stored in a text file, or if it's a
        string provided by user.

        Args:
            source (str): Filename or string containing a generated hash digest.

        Returns:
            str: Hash source digest stripped of leading and trailing whitespace.
        """

        if os.path.isfile(source):
            with open(source, 'r') as f:
                return f.read().split(' ')[0]
        else:
            return source.strip()

    @property
    def hash_method(self):
        """str: Exact name of built-in hashlib method as a string."""

        available_hash_methods = {
            'md5': {32, 'md5'},
            'sha1': {40, 'sha1'},
            'sha2': {56: 'sha224', 64: 'sha256', 96: 'sha384', 128: 'sha512'},
            'sha3': {56: 'sha3_224', 64: 'sha3_256', 96: 'sha3_384', 128: 'sha3_512'}
        }

        family = available_hash_methods[self.hash_family]
        digest_length = len(self.reference_digest)

        try:
            return family[digest_length]
        except KeyError:
            deviations = [(abs(x - digest_length), x) for x in family]
            return family[min(deviations)[1]]


def generate_digest(filename, hash_method):
    """
    Args:
        filename (str): Filename of binary file.
        hash_method (str): exact name of hashlib method used for digest
            generation.

    Returns:
        str: Hash digest generated from binary file.
    """

    # Buffer used read file into memory in smaller blocks
    buffer_size = 65536
    blocks = (os.path.getsize(filename) // buffer_size) + 1

    hash_digest = getattr(hashlib, hash_method)()

    with open(filename, 'rb') as f:
        generator = (f.read(buffer_size) for _ in range(blocks))
        for data in generator:
            hash_digest.update(data)

    return hash_digest.hexdigest()


def compare_digests(digest_1, digest_2):
    """
    Args:
        digest_1 (str):
        digest_2 (str):

    Returns:
        bool: Result of comparison between digest_1 and digest_2
    """

    return hmac.compare_digest(digest_1, digest_2)


if __name__ == '__main__':
    pass
