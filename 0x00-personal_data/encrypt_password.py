#!/usr/bin/env python3
"""
This script provides functions for hashing passwords and validating them.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.
    Args:
        password (str): The password to hash.
    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate a password against its hashed version.
    Args:
        hashed_password (bytes): The hashed password to compare against.
        password (str): The password to validate.
    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
