import argparse
import datetime
import os


def decomment(file):
    """Generator that, for a given iterable, filters out blank lines and anything after a hash character."""
    for row in file:
        raw = row.split('#')[0].strip()
        if raw:
            yield raw


def valid_date_type(arg):
    """Custom argparse *date* type"""
    try:
        return datetime.datetime.strptime(arg, "%Y-%m-%d")
    except ValueError:
        msg = "Given Date ({0}) not valid! Expected format, YYYY-MM-DD!".format(arg)
        raise argparse.ArgumentTypeError(msg)


def valid_existing_file_path(arg):
    """Custom argparse *existing readable file path* type"""
    if not os.path.isfile(arg):
        raise argparse.ArgumentTypeError("The file '{0}' does not exist or is not a readable file.".format(arg))

    if os.access(arg, os.R_OK):
        return arg
    else:
        raise argparse.ArgumentTypeError("The path '{0}' is not writable.".format(arg))


def valid_writable_file_path(arg):
    """Custom argparse *writable file path* type"""
    try:
        dirname = os.path.dirname(arg) or os.getcwd()
    except Exception as e:
        raise argparse.ArgumentTypeError("The path '{0}' seems to be invalid: {1}".format(arg, e))

    if os.access(dirname, os.W_OK):
        return arg
    else:
        raise argparse.ArgumentTypeError("The path '{0}' is not writable.".format(arg))
