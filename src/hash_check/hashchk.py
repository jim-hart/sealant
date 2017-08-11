# ----------------------------Compatibility Imports----------------------------
from __future__ import print_function
from six.moves import range
# -----------------------------------------------------------------------------

import hashlib
import os
import sys
import hmac  # Python 2.7 and 3.3+

# from hashchk_parser.py
from hashchk_parser import (HashChkParser, Output)


# TODO: Implement hash method choices
# TODO: Repent for not adding doc-strings, then add the doc-strings

class HashCheck(object):
    """Class for comparing, processing, and generating hash digests"""

    @staticmethod
    def process_digest(digest):
        """Either returns digest read from file, or returns digest with
        leading/trailing whitespace stripped.  Process action based on digest
        source."""

        if os.path.isfile(digest):
            with open(digest, 'r') as f:
                return f.read().split(' ')[0]
        else:
            return digest.strip()

    @staticmethod
    def generate_digest(filename):
        """Returns hexadecimal digest generated from filename"""

        buffer_size = 65536 # Buffer used to cut down on memory for large files.
        blocks = (os.path.getsize(filename) // buffer_size) + 1

        hash_digest = hashlib.sha256()

        with open(filename, 'rb') as f:
            #generator expression used for reading file in chunks
            generator = (f.read(buffer_size) for _ in range(blocks))
            for data in generator:
                hash_digest.update(data)

        return hash_digest.hexdigest()

    @staticmethod
    def compare_digests(digest_1, digest_2):
        """Returns True if digest_1 == digest_2"""

        return hmac.compare_digest(digest_1, digest_2)


def _compare_verify_digests(verify_args):
    """Takes in parsed arguments from HashChkParserverify subparser and prints
    out comparison results."""

    Output.print_comparison_startup()

    # provided printout
    provided_digest = HashCheck.process_digest(verify_args.digest)
    print(" Provided :{}".format(provided_digest))

    # stdout used to provide status message while digest is being generated
    sys.stdout.write(' Generated: {}'.format('Calculating'.center(60)))
    generated_digest = HashCheck.generate_digest(args.binary)
    sys.stdout.write("\r Generated:{}\n".format(generated_digest))

    # Compare and printout results
    result = HashCheck.compare_digests(provided_digest, generated_digest)
    Output.print_comparison_results(result)


if __name__ == '__main__':
    os.system('cls')
    args = HashChkParser().get_parser_args()
    compare_verify_digests(args)
