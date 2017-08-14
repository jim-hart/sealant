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

"""Classes and functions for creating and comparing hash digests

Todo:
    * Implement SHAKE and BLAKE
    * Resist urge to call it "SHAKE'N BLAKE"
    * Allow user to pass get_hash_method string of hashlib hexdigest call
"""


class Digest(object):
    """Class for comparing, processing, and generating hash digests.

    Attributes:
        hash_family (str): Designates which hash family/version will be used to
            generate a digest from a binary.
        reference_digest (str, optional):  Digest used to deduce SHA2/SHA3 bit
            length-e.g., SHA224 vs SHA226. This is primarily used for comparing a
            master digest of a binary against a local copy.
    """

    def __init__(self, hash_family, reference_digest=None):
        self.hash_family = hash_family
        if reference_digest:
            self.reference_digest = self.process_digest(reference_digest)

    @staticmethod
    def process_digest(source):
        """Determines if source of digest is stored in a text file, or if it's a
        string provided by user.

        Args:
            source (str): Filename or string containing source to be processed.

        Returns:
            str: Hash source digest stripped of leading and trailing whitespace.
        """

        if os.path.isfile(source):
            with open(source, 'r') as f:
                return f.read().split(' ')[0]
        else:
            return source.strip()

    def generate_digest(self, filename):
        """Returns hexadecimal digest generated from filename

        Args:
            filename (str): Filename of binary file.

        Returns:
            str: Hash digest generated from binary file.
        """

        buffer_size = 65536  # Buffer used to cut down on memory for large files.
        blocks = (os.path.getsize(filename) // buffer_size) + 1

        hash_digest = getattr(hashlib, self.get_hash_method())()

        with open(filename, 'rb') as f:
            # generator expression used for reading file in chunks
            generator = (f.read(buffer_size) for _ in range(blocks))
            for data in generator:
                hash_digest.update(data)

        return hash_digest.hexdigest()

    def get_hash_method(self):
        """Returns method to be used for digest comparison

        Args:
            sha_digest (str, optional): SHA2/SHA3 digest to be dispatched
                against sha_methods dictionary.

        Returns:
            str: Exact name of built-in hashlib method as a string.
        """

        # Method can be deduced by digest length if SHA2/SHA3 digest provided
        sha_methods = {
            'sha2': {56: 'sha224', 64: 'sha256', 96: 'sha384', 128: 'sha512'},
            'sha3': {56: 'sha3_224', 64: 'sha3_256', 96: 'sha3_384', 128: 'sha3_512'}
        }

        if self.reference_digest and (self.hash_family in sha_methods):
            family = sha_methods[self.hash_family]
            reference_length = len(self.reference_digest)
            try:
                return family[reference_length]
            except KeyError:
                """If the reference digest length doesn't match any standard SHA
                digest output length, the 'closest' value is returned.  This
                will result in a comparison fail, but output formatting will
                show the length difference"""

                deviations = [(abs(x-reference_length), x) for x in family.keys()]
                return family[min(deviations)[1]]

        elif self.hash_family in ['md5', 'sha1']:
            return self.hash_family

def compare_digests(digest_1, digest_2):
    """Returns result of equality comparison between digest_1 and digest_2.

    Args:
        digest_1 (str): Digest to be compared against digest_2.
        digest_2 (str): Digest to be compared against digest_1.

    Returns:
        bool: Result of comparison of digest_1 and digest_2.
    """

    return hmac.compare_digest(digest_1, digest_2)


if __name__ == '__main__':
    pass
