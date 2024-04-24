""" Helper methods for Earth Engine

License:
    BSD, see LICENSE.md
"""


import ee
import re
from pprint import pprint
import requests


#
# UTILS
#
def safe_init(quiet=True):
    """ Safely initialize earth-engine

    Warns, but does not throw an exception on connection-error.
    This is useful for modules that in part use gee, but you want
    to be able to load/run offline

    Returns:
        True if initialized otherwised False
    """
    try:
        ee.Initialize()
        return True
    except requests.exceptions.ConnectionError as e:
        if not quiet:
            print('Failed to Initialize Earth Engine:', e)
        return False


def get_info(*args, **kwargs):
    """ Convinece method for getting python values of ee.Objects

    Works with a single call of `.getInfo()` instead of a call
    per key/value-pair.

    Usage:

    ```python
    data = get_info(
        crs=crs,
        tile=tile,
        bands=s2_median.bandNames(),
        nb_s2_images=S2.size())
     ```

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        a dictionary or list of python objects
    """
    if kwargs:
        if args:
            kwargs['__ARGS__'] = args
        return ee.Dictionary(kwargs).getInfo()
    else:
        if (len(args) == 1) and isinstance(args, tuple):
            args = args[0]
            if re.search(r'ee\.', str(type(args))):
                return args.getInfo()
            else:
                print('[utils.ee] WARNING: get_info called on non-ee object')
                return args
        return ee.List(args).getInfo()


def print_info(*args, **kwargs):
    """ Convinece method for printing python values of ee.Objects

    Works with a single call of `.getInfo()` instead of a call
    per key/value-pair.

    Usage:

    ```python
    print_info(
        crs=crs,
        tile=tile,
        bands=s2_median.bandNames(),
        nb_s2_images=S2.size())
    ```

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """
    pprint(get_info(*args, **kwargs))
