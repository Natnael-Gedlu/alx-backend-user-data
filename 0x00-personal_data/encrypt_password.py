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
