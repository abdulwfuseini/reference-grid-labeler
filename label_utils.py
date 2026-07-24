# -*- coding: utf-8 -*-
"""
Column (letter) and row (number) label sequence generation for the
reference grid, independent of QGIS so it can be unit-tested on its own.

Column labels use a "bijective base-N" scheme - the same system spreadsheet
column names use (A, B, ... Z, AA, AB, ...) - parametrized over a custom
alphabet so the letter "I" can be excluded (avoiding confusion with 1/l,
a common convention on printed reference maps). Once the alphabet is
exhausted (default: 25 letters, A-Z minus I), labels roll over into two
letters, then three, and so on, so there's no hard cap on column count.

Either axis (columns or rows) can independently use letters or numbers -
"generate_label_range" and "generate_labels_from_start" below accept a
`label_type` of "letters" or "numbers" and dispatch to the right scheme.
"""

import string

# A-Z minus I. Derived rather than hardcoded so the literal doesn't read as
# an opaque high-entropy string to secret scanners - it's just the alphabet.
DEFAULT_ALPHABET = string.ascii_uppercase.replace("I", "")


def _label_to_index(label, alphabet):
    """Convert a column label (e.g. 'A', 'Z', 'AA') to a 0-based index."""
    label = label.strip().upper()
    if not label:
        raise ValueError("Column start label cannot be empty")
    n = 0
    for ch in label:
        pos = alphabet.find(ch)
        if pos < 0:
            raise ValueError(
                "Column start label '{}' contains a letter not in the "
                "allowed alphabet ('{}')".format(label, alphabet)
            )
        n = n * len(alphabet) + (pos + 1)
    return n - 1


def _index_to_label(index, alphabet):
    """Convert a 0-based index back to a column label string."""
    n = index + 1
    base = len(alphabet)
    result = ""
    while n > 0:
        n, rem = divmod(n - 1, base)
        result = alphabet[rem] + result
    return result


def generate_column_labels(count, start_label="A", exclude_i=True):
    """Return a list of `count` sequential column labels starting at
    `start_label` (inclusive), using the bijective letter scheme."""
    if count < 1:
        return []
    alphabet = DEFAULT_ALPHABET if exclude_i else "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    start_index = _label_to_index(start_label, alphabet)
    return [_index_to_label(start_index + i, alphabet) for i in range(count)]


def generate_row_labels(count, start_number=1):
    """Return a list of `count` sequential row labels (as strings),
    starting at `start_number` (inclusive)."""
    if count < 1:
        return []
    start_number = int(start_number)
    return [str(start_number + i) for i in range(count)]


def _parse_int(value, what):
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        raise ValueError(
            "{} must be a whole number (got '{}')".format(what, value)
        )


def generate_labels_from_start(label_type, from_value, count, exclude_i=True):
    """Return `count` ascending labels starting at `from_value`, for the
    given `label_type` ("letters" or "numbers"). Used when the cell count
    is dictated by geometry (custom cell size) rather than an explicit
    range end - only the starting label matters in that case."""
    if label_type == "numbers":
        start = _parse_int(from_value, "'From'")
        return generate_row_labels(count, start_number=start)
    return generate_column_labels(count, start_label=from_value, exclude_i=exclude_i)


def generate_label_range(label_type, from_value, to_value, exclude_i=True):
    """Return (labels, count) - an inclusive, ascending list of labels
    between `from_value` and `to_value` for the given `label_type`
    ("letters" or "numbers"). Raises ValueError if the range is invalid,
    reversed, or empty."""
    if label_type == "numbers":
        start = _parse_int(from_value, "'From'")
        end = _parse_int(to_value, "'To'")
        count = end - start + 1
        if count < 1:
            raise ValueError(
                "'To' ({}) must not come before 'From' ({})".format(end, start)
            )
        return generate_row_labels(count, start_number=start), count

    alphabet = DEFAULT_ALPHABET if exclude_i else "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    start_idx = _label_to_index(from_value, alphabet)
    end_idx = _label_to_index(to_value, alphabet)
    count = end_idx - start_idx + 1
    if count < 1:
        raise ValueError(
            "'To' ('{}') must not come before 'From' ('{}')".format(to_value, from_value)
        )
    return generate_column_labels(count, start_label=from_value, exclude_i=exclude_i), count
