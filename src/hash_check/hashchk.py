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

class Digest(object):
    """Class for comparing, processing, and generating hash digests."""

    def determine_sha_method(digest, family):
        """Returns SHA method to be used for digest comparison

        Args:
            digest (str): user provided hexdigest used to determine sha method
            family (str, optional): determines sha2 vs sha3 usage

        Returns:
            object: built in hashlib method built from sha_variants dictionary
        """

        sha_versions = {
            'sha2': {56: 'sha224', 64: 'sha256', 96: 'sha384', 128: 'sha512'},
            'sha3': {56: 'sha3_224', 64: 'sha3_256', 96: 'sha3_384', 128: 'sha3_512'}
        }

        variant = sha_versions[family][len(digest)]

        return getattr(hashlib, variant)


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

    @staticmethod
    def generate_digest(filename):
        """Returns hexadecimal digest generated from filename

        Args:
            filename (str): filename of binary file

        Returns:
            str: hash digest generated from binary file
        """

        buffer_size = 65536  # Buffer used to cut down on memory for large files.
        blocks = (os.path.getsize(filename) // buffer_size) + 1

        hash_digest = hashlib.sha256()

        with open(filename, 'rb') as f:
            # generator expression used for reading file in chunks
            generator = (f.read(buffer_size) for _ in range(blocks))
            for data in generator:
                hash_digest.update(data)

        return hash_digest.hexdigest()


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
