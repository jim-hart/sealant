# Overview
Sealant offers simple utilities and testing tools based around modules like `secrets`, `hashlib`, `hmac`, and [cryptography](https://cryptography.io/en/latest/).  All files can be run via a CLI or, relevant classes can be imported into your python project.

Because this project is in alpha, this README is subject to change frequently. For now, the content below only reflects information related to the available modules.

## Compatibility

The standalone executables have no dependencies beyond an OS-level source of random number generation.  This is usually provided by default and shouldn't require any action on your end.

If you want to run the .py file directly, or import the relevant class into your own project, Python 2.7 and 3.3+ are supported.

### General Use

The tools themselves operate like most other CLI programs:  `-h`/`--help` is available for all commands, and all switch options are fully detailed.  Because these tools were built to provide some type of cryptographically secure function, extended documentation is provided for each respective tool.

This documentation should provide enough insight to determine whether or not each utilities specific purpose is secure enough for personal use.  The source code itself is heavily commented as well if you want code specific documentation.

If you want to jump right in though, built in help messages provide all the information needed to use each respective tool.

## randstr - Secure Random String Generation

randstr uses Python's `random.SystemRandom` to access OS-level randomization sources in order to provide cryptographically secure random number generation functionality.  Unlike standard pseudo random number generators, cryptographically secure RNG's are suitable for tasks like password generation or account authentication procedures. The documentation for Python's [secrets module](https://docs.python.org/3/library/secrets.html), which relies on `SystemRandom` for its random number generation, provides a more detailed explanation of the benefits.

`SystemRandom` provides this access to OS-level RNG sources by calling on either `CryptGenRandom()` if using Windows, and `/dev/urandom` if using *nix.  While these sources should be available on most systems, a `NotImplemented` error will be raised if they are missing.  randstr only works if one of these systems is present.

While randstr ultimately uses `SystemRandom`, the route it takes to get there is dependent on the Python interpreter version running the actual program files.  Python 3.6+ will make use of the secrets module while Python 2.7 and Python 3.2+ use `random.SystemRandom`.  This difference is arbitrary; although the steps to get there may differ, eventually `SystemRandom`is called for actual random number generation.

### Features

randstr provides an interface for generating random data in the form of strings by pulling randomly generated numbers through `SystemRandom`.  The length of the string is defined by the user; the only limiting factor is performance considerations for extremely large (10,000+ character) strings.  The default character set used for string generations is made up of the following:

  1. ASCII uppercase
  2. ASCII lowercase
  3. ASCII punctuation
  4. Single whitespace character

The default character set can be replaced by the user if desired.  String output is available through any combination of the following:

  1. Auto-copy to clipboard
  2. Terminal printout
  3. `.txt` file


## hashchk - Cryptographic Hash Digest Generation and Comparison

hashchk acts as a CLI of sorts for access for various methods found in the `hashlib` and `hmac` libraries.  At it's core, hashchk primarily provides methods for comparing and generating hash digests.  Although these two actions define hashchk as a whole, optional switches extend this functionality in various ways.


#### Supported Hash Functions
hashchk supports the following bit lengths for **both** SHA-2 and SHA-3:

  * 224
  * 256
  * 384
  * 512

MD5 is provided out of convenience as it's still widely used, and more often than not, it's the only hash method provided for file integrity validation.  It suffers from numerous vulnerabilities however, and it's best avoided if given other options.  Although SHA1 is significantly more secure, recent collision attacks make it worth an asterisk. hashchk still provides MD5 and SHA1 access; this section serves as a disclaimer and not a notice of limitation.

Although only Python 3.6+ supports SHA-3 natively, the [pysha3](https://github.com/tiran/pysha3) provides a patch for full SHA-3 support in Python 2.7-3.5.  Because `pyinstaller` only supports Python 3.5+, it uses `pysha3` for SHA-3; if you run the `.py` version of hashchk, however, `hashlib` will be used to invoke SHA-3 methods instead.  The wonderful team behind `pyinstaller` is working on Python 3.6 support now; when available, the executables will be updated to use `hashlib` exclusively.


#### Ease of Use
hashchk, at its core, provides a simple way to compare and generate cryptographic hash function digests. Used without any optional switches, hashchk only needs a reference digest (either in a `.txt` file or copied directly into the terminal) and a binary file to compare the the reference digest  against.  Comparison of hash digests defaults to SHA-2, although a `-sha3` switch can be supplied as an override.  hashchk was designed to provide a way of validating file integrity with as little input as possible; it does this by automatically determining if the source digest is provided via a string or a text file, and by inferring the SHA bit-length (e.g. SHA-244 vs SHA-256).

Although *explicit is better than implicit*, SHA digests are fixed length and are provided in standard formats; sources of error are limited to incorrect input of the reference digest.  Errors of this nature lead only to digest comparison failures; the error source itself can easily be traced as hashchk provides a printout of the reference digest and the generated digest it used during the comparison process.

A measure of control has been provided however; the reference digest must be distinguished from the file that needs to be validated.  This distinction prevents any false positives from erroneous input, i.e., the reference digest being compared against itself.  At worst, incorrect input will lead to a crash, so you can sleep easy knowing that hashchk will die in a blaze of traceback glory before providing an inaccurate integrity check!


#### Big Files, Low Memory
hashchk generates hash digests by reading files in small 64MB sequential blocks via generator expressions.  While smaller files don't gain much benefit, this method prevents larger files from being read into memory all at once, and it improves overall digest generation time.


## Additional Contributers

**P. Robertson** - User experience consolation





