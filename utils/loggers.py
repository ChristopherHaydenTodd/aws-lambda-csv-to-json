#!/usr/bin/env python3
"""
    Purpose:
        Library for getting loggers of specific configurations in Python.
        This will utilize Pythons built-in logging library and will return
        an instance of logging that can be implemented in any code
        taht already implements the logging class.
"""

# Python Library Imports
import inspect
import sys
import logging


###
# Define Loggers
###

def get_stdout_logging(
    log_level=logging.INFO,
    log_msg_fmt='%(asctime)s %(levelname)s %(message)s',
    log_date_fmt='%a, %d %b %Y %H:%M:%S',
    log_prefix=None
):
    """
    Purpose:
        Get Logger to standard out.
    Args:
        log_level (log level from logging): Minimum level for messages to log
        log_msg_fmt (String): Mesage format for all logs with variable
            substitution for known logging options
        log_date_fmt (Stringg): Dateformat to append to message
        log_prefix (String): prefix to append to message
    Return:
        logging (Python logging object): Configured logging object
    Examples:
        >>> logging = get_stdout_logging()
        or
        >>> logging =\
            get_stdout_logging(
                log_level=logging.DEBUG,
                prefix='[test_script]: '',
            )
    """

    if log_prefix:
        log_msg_fmt = f"{log_prefix}{log_msg_fmt}"

    logging.basicConfig(
        stream=sys.stdout,
        level=log_level,
        format=log_msg_fmt,
        datefmt=log_date_fmt
    )

    return logging


def get_file_logger(
    log_file=None,
    log_filemode='a',
    log_level=logging.INFO,
    log_msg_fmt='%(asctime)s %(levelname)s %(message)s',
    log_date_fmt='%a, %d %b %Y %H:%M:%S',
    log_prefix=None
):
    """
    Purpose:
        Get Logger to file
    Args:
        log_level (log level from logging): Minimum level for messages to log
        log_msg_fmt (String): Mesage format for all logs with variable
            substitution for known logging options
        log_date_fmt (Stringg): Dateformat to append to message
        log_prefix (String): prefix to append to message
    Return:
        logging (Python logging object): Configured logging object
    Examples:
        >>> logging = get_file_logger()
        or
        >>> logging =\
            get_file_logger(
                log_level=logging.ERROR,
                prefix='[test_script]: '',
                log_file='./script_im_writing.log'
            )
    """

    # If no log_file is specified, find the calling file and use that name
    if not log_file:
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        log_file = calframe[1].filename.replace('.py', '.log')

    if log_prefix:
        log_msg_fmt = f"{log_prefix}{log_msg_fmt}"

    logging.basicConfig(
        filename=log_file,
        filemode=log_filemode,
        level=log_level,
        format=log_msg_fmt,
        datefmt=log_date_fmt,
    )

    return logging

###
# Log Management
###

def clear_log_handlers():
    """
    Purpose:
        Remove previous log handlers and configurations. This
        will ensure that any new logging that is configured
        will take precedence, as logging is first setting
        is not overwritten.
    Args:
        N/A
    Return:
        N/A
    """

    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)
