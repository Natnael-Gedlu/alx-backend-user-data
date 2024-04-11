#!/usr/bin/env python3
"""
This script deals with logging and redaction of sensitive user data.
"""

import re
from typing import List

# Regular expression patterns for extracting and
# replacing sensitive information
patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}

# Sensitive fields that need to be redacted
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Filter sensitive data in a message.

    Args:
        fields (List[str]): List of sensitive fields to filter.
        redaction (str): Redaction string.
        message (str): Message containing sensitive data.
        separator (str): Separator between fields in the message.

    Returns:
        str: Message with sensitive data filtered.
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)