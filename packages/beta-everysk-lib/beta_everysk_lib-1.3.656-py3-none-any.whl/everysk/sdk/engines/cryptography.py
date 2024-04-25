###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

###############################################################################
#   Imports
###############################################################################
import string
import secrets
import uuid

from everysk.config import settings

###############################################################################
#   Globals
###############################################################################
ALPHANUMERIC = string.ascii_letters + string.digits
SYMBOL_ID_MAX_LEN = settings.SYMBOL_ID_MAX_LEN

###############################################################################
#   Cryptography Implementation
###############################################################################
def generate_random_id(length: int, characters: str = ALPHANUMERIC) -> str:
    """
    Generate a random ID of the specified length.

    Args:
        length (int): The desired length for the random ID.
        characters (str, optional): The characters to use for generating the ID.
            Default is alphanumeric characters.

    Returns:
        str: The generated random ID consisting of the specified characters.
    """
    return ''.join(secrets.choice(characters) for i in range(length))

def generate_unique_id():
    """
    Generate a unique ID with fixed length (32 characters).

    Returns:
        str: The generated unique ID consisting of hexadecimal characters.
    """
    return uuid.uuid4().hex

def generate_short_random_id() -> str:
    """
    Generate a short random ID with fixed length (8 characters).

    Returns:
        str: The generated unique ID consisting of alphanumeric characters.
    """
    return generate_random_id(length=settings.SIMPLE_UNIQUE_ID_LENGTH)
