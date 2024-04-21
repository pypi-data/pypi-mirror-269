"""
Some miscellaneous functions
"""

import logging
import os
import pathlib
import re
import subprocess
import sys
import time

import dateutil.parser as dparser
import numpy as np
import pandas as pd
import yaml
from numpy.testing import assert_equal

from pymarine.utils import Q_

logger = logging.getLogger(__name__)


class Chdir:
    """Class to move to a directory, do something, and move back when done

    Parameters
    ----------
    new_path: str
        Location where you want to do something

    Notes
    -----
    Used on the Gompute cluster in the batch processing script to submit a job inside a
    directory and then move back to the higher directory to move to the next case

    Examples
    --------

    Go to a known directory (C:/)

    >>> os.chdir("C:/")
    >>> os.getcwd()
    'C:\\\\'

    With the Chdir command we move to the C:/Temp directory where we can do something.

    >>> with Chdir("C:/Temp") as d:
    ...    # in this block we can do something in the directory Temp.
    ...    os.getcwd()
    'C:\\\\Temp'

    We have left the block under Chdir, so we are back at the directory where we started

    >>> os.getcwd()
    'C:\\\\'

    """

    def __init__(self, new_path):
        self.newPath = new_path

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)
        return self

    def __exit__(self, *args):
        os.chdir(self.savedPath)


class Timer:
    """Class to measure the time it takes execute a section of code

    Parameters
    ----------
    message : str
        a string to use to the output line
    name : str, optional
        The name of the routine timed.
    verbose : bool, optional
        if True, produce output
    units : str, optional
        time units to use. Default  'ms'
    n_digits : int, optional
        number of decimals to add to the timer units

    Example
    -------

    Use a `with` / `as` construction to enclose the section of code which need to be
    timed

    >>> from numpy import allclose
    >>> number_of_seconds = 1.0
    >>> with Timer(units="s", n_digits=0) as timer:
    ...    time.sleep(number_of_seconds)
    Elapsed time         routine              :          1 s
    >>> allclose(number_of_seconds, timer.secs, rtol=0.1)
    True
    """

    def __init__(
        self,
        message="Elapsed time",
        name="routine",
        verbose=True,
        units="ms",
        n_digits=0,
        field_width=20,
    ):
        self.verbose = verbose
        self.message = message
        self.name = name
        self.units = units
        self.secs = None

        # Build the format string. E.g. for field_with=20 and n_digits=1 and units=ms,
        # this produces the following
        # "{:<20s} : {:<20s} {:>10.1f} ms"
        self.format_string = (
            "{:<"
            + f"{field_width}"
            + "s}"
            + " {:<"
            + f"{field_width}"
            + "s} : {:>"
            + f"{10}.{n_digits}"
            + "f}"
            + f" {self.units}"
        )

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()

        # start and end are in seconds. Convert time delta to nano seconds
        self.delta_time = np.timedelta64(int(1e9 * (self.end - self.start)), "ns")

        self.secs = float(self.delta_time / np.timedelta64(1, "s"))

        # debug output
        logger.debug(f"Found delta time in ns: {self.delta_time}")

        if self.verbose:
            # convert the delta time to the desired units
            duration = self.delta_time / np.timedelta64(1, self.units)

            # produce output
            logger.info(
                self.format_string.format(self.message, self.name, duration, self.units)
            )


def is_exe(fpath):
    """Test if a file is an executable

    Parameters
    ----------
    fpath : str
        return true or false:

    Returns
    -------
    bool
        In case `fpath` is a file that can be executed return True, else False

    Notes
    -----
    This function can only be used on Linux file systems as the `which` command is used
    to identity the location of the program.
    """
    # use system command 'which' to locate the full location of the file
    p = subprocess.Popen(
        f"which {fpath}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    p_list = p.stdout.read().splitlines()
    if p_list:
        # which return a path so copy it to fpath
        fpath = p_list[0]
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def clear_path(path_name):
    """routine to clear spurious dots and slashes from a path name
     example bla/././oke becomes bla/oke

    Parameters
    ----------
    path_name :
        return: clear_path as a string

    Returns
    -------
    type
        clear_path as a string

    Examples
    --------

    >>> long_path = os.path.join(".", "..", "ok", "yoo", ".", ".", "") + "/"
    >>> print(long_path)
    .\\..\\ok\\yoo\\.\\.\\/
    >>> print(clear_path(long_path))
    ..\\ok\\yoo

    """
    return str(pathlib.PurePath(path_name))


def delete_module(modname, paranoid=None):
    """Delete a module from memory which loaded before

    Parameters
    ----------
    modname : str
        The name of the module to remove

    paranoid : list or None
         (Default value = None)
    """
    from sys import modules

    try:
        thismod = modules[modname]
    except KeyError:
        raise ValueError(modname)
    these_symbols = dir(thismod)
    if paranoid:
        try:
            paranoid[:]  # sequence support
        except IndexError:
            raise ValueError("must supply a finite list for paranoid")
        else:
            these_symbols = paranoid[:]
    del modules[modname]
    for mod in list(modules.values()):
        try:
            delattr(mod, modname)
        except AttributeError:
            pass
        if paranoid:
            for symbol in these_symbols:
                if symbol[:2] == "__":  # ignore special symbols
                    continue
                try:
                    delattr(mod, symbol)
                except AttributeError:
                    pass


def get_clean_version(version):
    r"""turns the full version string into a clean one without the build

    Parameters
    ----------
    version : str
        The version string as return from versioneer.

    Returns
    -------
    str
        The clean version string

    Notes
    -----
    The version string matches the following regular expression

        "([.|\d]+)([+]*)(.*)"

    This function return the clean version string given by the part "([.|\d]+)"

    Examples
    --------

    >>> get_clean_version("1.3")
    '1.3'
    >>> get_clean_version("2.5+dev.g43429")
    '2.5'
    >>> get_clean_version("4.3.1+dev.g43429-dirty")
    '4.3.1'

    """
    match = re.search(r"([.|\d]+)([+]*)(.*)", version)
    if bool(match):
        version = match.group(1)
    else:
        version = version
    return version


def read_settings_file(file_name):
    """Read the yaml file to get the setup information.

    Parameters
    ----------
    file_name : str
        Name of the configuration file. Can be a full path name as well

    Returns
    -------
    dict
        All the settings as obtained from the yaml configuration file

    Notes
    -----
    The file name of the yaml file is searched for in the following order

    1. The current directory where the script is executed. If a full path is given,
       this will be accepted too.
    2. The directory where the original script is located.

    In this way, a default settings file can be put in the script directory and the user
    does not need to copy it except a setting values needs to be changed

    Raises
    ------
    AssertionError:
        In case the file cannot be found
    """

    if os.path.exists(file_name):
        logger.info(f"Loading configuration file {file_name}")
        configuration_file = file_name
    else:
        logger.info(f"Loading configuration file from script dir {__name__}")
        configuration_file = os.path.join(
            os.path.split(__file__)[0], os.path.split(file_name)[1]
        )
    try:
        logger.debug(f"Trying to read configuration file {configuration_file}")
        with open(configuration_file) as stream:
            settings = yaml.load(stream=stream)
    except OSError as err:
        raise AssertionError(
            "Configuration file can not be found in either current directory of "
            "script directory. Goodbye. {}".format(err)
        )

    return settings


def get_python_version_number(version_info):
    """Script to turn the version info as obtained with sys.version_info into a digit
    number

    Parameters
    ----------
    version_info :
        return: a string with the current python version as a clear digit, i.e., 3.5.3

    Returns
    -------
    type
        a string with the current python version as a clear digit, i.e. 3.5.3

    Examples
    --------
    >>> version_string = get_python_version_number(sys.version_info)

    """

    python_version = f"{version_info.major:d}"
    if version_info.minor != "":
        python_version += f".{version_info.minor:d}"
    if version_info.micro != "":
        python_version += f".{version_info.micro:d}"

    return python_version


def get_regex_pattern(search_pattern):
    """Routine to turn a string into a regular expression which can be used to match a
    string

    Parameters
    ----------
    search_pattern : str
        A regular expression in the form of a string

    Returns
    -------
    None or compiled regular expression
        A regular expression as return by the re.compile function or None in case a
        invalid regular expression was given

    Notes
    -----
    An empty string or an invalid search_pattern will yield a None return

    """
    regular_expression = None
    if search_pattern != "":
        try:
            regular_expression = re.compile(f"{search_pattern}")
        except re.error:
            regular_expression = None
    return regular_expression


def clear_argument_list(argv):
    """
    Small utility to remove the \'\\\\r\' character from the last argument of the argv
    list appearing in cygwin

    Parameters
    ----------
    argv : list
        The argument list stored in `sys.argv`

    Returns
    -------
    list
        Cleared argument list

    """
    new_argv = list()
    for arg in argv:
        # replace the '\r' character with a empty space
        arg = re.sub("\r", "", arg)
        if arg != "":
            # only add the argument if it is not empty
            new_argv.append(arg)
    return new_argv


def query_yes_no(question, default_answer="no"):
    """Ask a yes/no question via raw_input() and return their answer.

    Parameters
    ----------
    question : str
        A question to ask the user
    default_answer : str, optional
        A default answer that is given when only return is hit. Default to 'no'

    Returns
    -------
    str:
        "yes" or "no", depending on the input of the user
    """
    valid = {"yes": "yes", "y": "yes", "ye": "yes", "no": "no", "n": "no"}
    if not default_answer:
        prompt = " [y/n] "
    elif default_answer == "yes":
        prompt = " [Y/n] "
    elif default_answer == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default_answer)

    while 1:
        # sys.stdout.write(question + prompt)
        logger.warning(question + prompt)
        choice = input().lower()
        if default_answer is not None and choice == "":
            return default_answer
        elif choice in list(valid.keys()):
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def print_banner(
    title,
    top_symbol="-",
    bottom_symbol=None,
    side_symbol=None,
    width=80,
    to_stdout=False,
    no_top_and_bottom=False,
):
    """Create a banner for plotting a bigger title above each section in the log output

    Parameters
    ----------
    title :
        The title to plot
    top_symbol : str
        the symbol used for the top line. Default value = "-"
    bottom_symbol : str
        the symbol used for the bottom line. Assume same as top if None is given
        (Default value = None)
    side_symbol : str
        The side symbol. Assume same as top if None is given, except if top is -, then
        take | (Default value = None)
    width : int
        the width of the banner (Default value = 80)
    no_top_and_bottom : bool
        make a simple print without the top and bottom line (Default value = False)
    to_stdout : bool, optional
        Print the banner to the standard output of the console instead of the logging
        system. Defaults to False

    Examples
    --------

    >>> print_banner("This is the start of a section")
    <BLANKLINE>
    --------------------------------------------------------------------------------
    | This is the start of a section                                               |
    --------------------------------------------------------------------------------

    Notes
    -----

    Unless the option 'to_stdout' is set to True, the banner is printed via the logging
    system. Therefore, a logger needs to be created first
    """

    logger.debug("message debug in print_banner")

    if bottom_symbol is None:
        bottom_symbol = top_symbol

    if side_symbol is None:
        if bool(re.match("-", top_symbol)):
            side_symbol = "|"
        else:
            side_symbol = top_symbol

    if not no_top_and_bottom:
        message_string = (
            "{}\n"
            + f"{side_symbol} "
            + "{:"
            + f"{width - 4:d}"
            + "}"
            + f" {side_symbol}"
            + "\n{}"
        )
        message = message_string.format(
            top_symbol * width, title, bottom_symbol * width
        )
    else:
        message_string = f"{side_symbol} " + "{:" + f"{width - 4:d}" + "}"
        message = message_string.format(title)
    if to_stdout:
        print(f"\n{message}")
        sys.stdout.flush()
    else:
        logger.info(f"\n{message}")


def move_script_path_to_back_of_search_path(script_file, append_at_the_end=True):
    """Move the name of a script to the front or the back of the search path

    Parameters
    ----------
    script_file : str
        Name of the script to move

    append_at_the_end: bool, optional, default=True
        Append the name of the script to the end. In case this flag is false, the script
        file is added to the beginning of the path

    Returns
    -------
    list:
        The new system path stored in a list

    Notes
    -----
    This script is sometimes required if the __version string is messing up with
    another __version string

    Examples
    --------

    sys.path = move_script_path_to_back_of_search_path(__file__)
    """
    script_file = os.path.realpath(script_file)
    path_to_script = os.path.split(script_file)[0]
    path_to_script_forward = re.sub("\\\\", "/", path_to_script)
    new_sys_path = list()
    for path in sys.path:
        path_forward = re.sub("\\\\", "/", path)
        if path_forward != path_to_script_forward:
            new_sys_path.append(path)

    if append_at_the_end:
        new_sys_path.append(path_to_script)
    else:
        new_sys_path = [path_to_script] + new_sys_path
    return new_sys_path


def read_value_from_dict_if_valid(dictionary, key, default_value=None):
    """Read a value from a dictionary. If the value is not set, just return the
    default value

    Parameters
    ----------
    dictionary :
        dictionary which is supposed to carry this key field
    key :
        the name of the field to read the value from
    default_value :
        default value in case we fail to read the key field (if it does not exist)

    Returns
    -------
    type
        value of the key field or the default value

    """
    try:
        value = dictionary[key]
    except KeyError:
        value = default_value

    return value


def set_value_if_valid(value, new_value):
    """small routine to set a value on if it is not none.
    Otherwise, the original value is taken

    Parameters
    ----------
    value :
        the original value which you can pre-define with a default value
    new_value :
        the new value. Only set this if it is not none

    Returns
    -------
    type
        net value or the original if new_value was None

    """

    if new_value is not None:
        value = new_value

    return value


def compare_objects(obj1, obj2, counter=0, max_recursion_depth=4):
    """
    Compare if two object are equal

    Parameters
    ----------
    obj1: class
        first object
    obj2: class
        second object
    counter: int
        Current recursion depth. Keeps track of how many time we have recursively called
        this function
    max_recursion_depth: int
        Maximum depth to which we are comparing the objects.


    Notes
    -----
    * This function compares all the attributes of two objects to see if their values
      are the same
    * An attribute field may be another object which we also want to compare with the
      same attribute of the other object. This is done by recursively calling this
      function again.
    * Due to the recursive call mechanism we may end up in a infinite loop. To prevent
      this, a maximum recursion depth can be given.
    * The test function *test_sequence_tool* of the *sequence_tool_utils* module uses
      this function to compare to *SequenceToolSummary* objects

    Raises
    ------
    AssertionError:
        In case on of the object fields is not equal

    """
    for att in dir(obj1):
        if att.startswith("_"):
            continue
        val1 = getattr(obj1, att)
        val2 = getattr(obj2, att)
        try:
            assert_equal(val1, val2)
        except AssertionError:
            if type(val1) is str or type(val1) is list:
                raise
            counter += 1
            if counter < max_recursion_depth:
                compare_objects(val1, val2)
            else:
                continue


def set_default_dimension(
    parse_value, default_dimension=None, force_default_units=False
):
    """
    Add a *pint* dimension to a value


    Parameters
    ----------
    parse_value: ndarray or str or float
        Value with optional a dimension written in the form of a str. Can be an array or
        list of strings as well
    default_dimension: str
        Required default dimension
    force_default_units: bool
        If true the only allowed dimension is the default dimension. Raise an error in
        case this is not the case. Default = False

    Returns
    -------

    :obj:`Quantity`
        Value with the quantity as give by the default

    Raises
    ------
    AssertionError
        In case the dimension of the *parse_value* argument is not not but:

        1. Its dimensionality is not the same as the dimensionality of the
           *default_dimension*
        2. Its units is not the same as the unit of the *default_dimension* and the
           *force_default_units* flag is set to *True*

    Notes
    -----
    * This function is a add-on to the *pint* module, a package to define, operate and
      manipulate physical quantities: https://pypi.python.org/pypi/Pint.
    * This function is used to add a dimension to a value which is parsed from a text
      file.
    * It is checked if the value given in the text file has dimension already, for
      example that it was given as "1.0 m/s".
    * If a dimension was given already: check if the dimensionality (in this case:
      Length/Time)
      is the same as the dimensionality of the *default_dimension* input argument.
    * In case the input value does not have an explicit dimension, the dimension given
      by *default_dimension* is added to the value.
    * This function works on both scalar and list values

    Examples
    --------

    Assume we want to read input values from a text file as plain numbers and we want
    to add a default dimension of *meter* to it in case the value do not have an
    explicit dimension yet. Just do:

    >>> value_without_dimension = 1.0  # value as we read from the text file
    >>> value_with_dimension = set_default_dimension(value_without_dimension, "meter")
    >>> print(value_with_dimension)
    1.0 meter

    The variable *value_with_dimension* is now a pint quantity which carries the
    dimension meter.

    In case the input variable already has a dimension, we should also be able to use
    this *function*. The only requirement is that the dimensionality is the same.
    So this should work:

    >>> value_with_dimension = set_default_dimension("2.5 meter", "meter")
    >>> print(value_with_dimension)
    2.5 meter

    This should work as well

    >>> value_with_dimension = set_default_dimension("5.0 mm", "meter")
    >>> print(value_with_dimension)
    5.0 millimeter

    But this fails as the dimensionality of the input argument is not corresponding with
    the dimensionality of the default dimension

    >>> try:
    ...    value_with_dimension = set_default_dimension("5.0 mm", "second")
    ... except AssertionError:
    ...    print("This fails because the dimensionality is not the same")
    This fails because the dimensionality is not the same

    This function should also work for arrays and list

    >>> values_without_dimension = np.linspace(0, 1, num=5)
    >>> values_with_dimension = set_default_dimension(values_without_dimension,
    ...                                               "meter/second^2")
    >>> print(values_with_dimension)
    [ 0.    0.25  0.5   0.75  1.  ] meter / second ** 2

    Notes
    -----
    * Hz are not converted to rad/s as expected. Therefore, do not try to use this to
      convert Hz -> rad/s
    * If the input argument *parse_val* is None, a None is returned as output as well

    """
    if default_dimension is not None:
        def_unit_val = Q_(1, default_dimension)
    else:
        def_unit_val = None
    dimensionless_unit_val = Q_("1")
    dimensionless = dimensionless_unit_val.dimensionality

    if parse_value is not None:
        # in case no dimensions are given with the parse_value argument, impose them

        if isinstance(parse_value, (list, tuple, np.ndarray)):
            # To properly deal with arrays and lists, first check if we have one
            v = Q_(parse_value[0])
            # If this is allowed, we have and array. Check the value and dimension of
            # the first element
            if (
                v.dimensionality == dimensionless
                and v.units == dimensionless_unit_val.units
            ):
                if not isinstance(parse_value[0], type(dimensionless_unit_val)):
                    # There are no dimensions. Convert the array, add the dimensions
                    # later
                    ret_val = Q_(parse_value)
                else:
                    # We have added the quantity to the parse_value already. Copy it
                    ret_val = parse_value
            else:
                # The elements have a dimension, so convert the array in a bare array
                # without dimensions and copy the dimension type to the default.
                # Then we can just do the conversion below
                parse_value = np.array([Q_(x).magnitude for x in parse_value])
                ret_val = Q_(parse_value)
                if (
                    def_unit_val is not None
                    and v.dimensionality != def_unit_val.dimensionality
                ):
                    raise AssertionError(
                        "The first value of the array given has a dimension with a "
                        "different dimensionality as the default dimension. "
                        "Found {}. Expected {}"
                        "".format(v.dimensionality, def_unit_val.dimensionality)
                    )

                def_unit_val = v.units
        elif not isinstance(parse_value, type(dimensionless_unit_val)):
            # the parse_value is not yet a quantity objects
            ret_val = Q_(parse_value)
        else:
            # The parser value is a quantity already. Copy it
            ret_val = parse_value

        if (
            ret_val.dimensionality == dimensionless
            and ret_val.units == dimensionless_unit_val.units
        ):
            # if no dimension is given, add the default dimension
            ret_val = Q_(np.asarray(parse_value), default_dimension)
            if ret_val.dimensionality != dimensionless:
                logger.debug(
                    "A dimensionless value was and a default dimension was imposed "
                    "{} -> {}.".format(parse_value, ret_val)
                )
        elif def_unit_val is not None:
            # check if the dimensionality is the same as the def_units
            if ret_val.dimensionality != def_unit_val.dimensionality:
                raise AssertionError(
                    "Value given has a dimension with a different dimensionality as "
                    "the default dimension\nFound {}. Expected {}".format(
                        ret_val.dimensionality, def_unit_val.dimensionality
                    )
                )

        # we want to force the units. Check it
        if force_default_units:
            if ret_val.units != def_unit_val.units:
                raise AssertionError(
                    "The dimensions given to the value do not match the default "
                    "units. \n"
                    "Found {}. Expected {}\nPlease fix or set "
                    "*only_default_units_allowed* to False".format(
                        ret_val.units, def_unit_val.units
                    )
                )
    else:
        # in case a none value is given as input just return none as output
        ret_val = None

    return ret_val


def get_value_magnitude(value, convert_to_base_units=True):
    """
    Get the magnitude of value with *Pint* dimension in terms of its base units or
    return a float if *value* does not have a dimension

    Parameters
    ----------
    value: Quantity or float or None
        A value with a Pint dimension or a normal float. In both cases, the value
        without dimension is returned
    convert_to_base_units: bool, optional
        Before turning the value into a magnitude first turn the quantity into its SI
        base units. Default = True

    Returns
    -------
    float or None
        Magnitude of the value in case a Pint Quantity was added to the input or just
        the value itself.
        If *convert_to_base_units* was set to True the value is first converted to its
        SI base units

    Examples
    --------
    Assume we have a value with a pint dimension

    >>> velocity = Q_("2.5 m/s")
    >>> print("Current velocity with dimension is: {}".format(velocity))
    Current velocity with dimension is: 2.5 meter / second

    We can now get the magnitude of *velocity* using this function as

    >>> velocity_mag = get_value_magnitude(velocity)
    >>> print("Velocity without dimension is: {}".format(velocity_mag))
    Velocity without dimension is: 2.5

    In case the input argument of the *get_value_magnitude* is a float and does not
    have a dimension, the value itself is returned

    >>> velocity_mag2 = get_value_magnitude(velocity_mag)
    >>> print("Velocity without dimension is: {}".format(velocity_mag2))
    Velocity without dimension is: 2.5

    In case we have a dimension in none SI units, the value  is by default first
    converted to its SI base units.

    >>> velocity_knots = Q_("1 knot")
    >>> velocity_mag = get_value_magnitude(velocity_knots)
    >>> print("Velocity {} is converted to its magnitude in m/s: {:.2f}"
    ...       "".format(velocity_knots, velocity_mag))
    Velocity 1 knot is converted to its magnitude in m/s: 0.51

    In case that the *convert_to_base_units* flag is False we just get the magnitude in
    the same units as the input argument

    >>> velocity_knots = Q_("2.5 knot")
    >>> velocity_mag = get_value_magnitude(velocity_knots, convert_to_base_units=False)
    >>> print("Velocity {} is converted to its magnitude in knots: {:.2f}"
    ... "".format(velocity_knots, velocity_mag))
    Velocity 2.5 knot is converted to its magnitude in knots: 2.50

    Notes
    -----
    * This function is used inside other functions in which it is not know before hand
      if an input argument is passed with or without a Pint dimension and we only are
      interested in the magnitude of the value. Use this function to get the magnitude
    """

    try:
        if convert_to_base_units:
            value = value.to_base_units()
        value_mag = value.magnitude
    except AttributeError:
        value_mag = value

    return value_mag


def get_time_stamp_from_string(
    string_with_date_time, yearfirst=True, dayfirst=False, timezone=None
):
    """
    Try to get a date/time stamp from a string

    Parameters
    ----------
    string_with_date_time: str
        The string to analyses
    yearfirst: bool, optional
        if true put the year first. See *dateutils.parser*. Default = True
    dayfirst: bool, optional
        if true put the day first. See *dateutils.parser*. Default = False
    timezone: str or None, optional
        if given try to add this time zone:w

    Returns
    -------
    :obj:`DateTime`
        Pandas data time string

    Examples
    --------

    The date time in the file 'AMSBALDER_160929T000000' is  29 sep 2016 and does not
    have a time zone specification. The returned time stamp does also not have a time
    zone

    >>> file_name="AMSBALDER_160929T000000"
    >>> time_stamp =get_time_stamp_from_string(string_with_date_time=file_name)
    >>> print("File name {} has time stamp {}".format(file_name, time_stamp))
    File name AMSBALDER_160929T000000 has time stamp 2016-09-29 00:00:00

    We can also force to add a time zone. The Etc/GMT-2 time zone is UTC + 2 time zone
    which is the central europe summer time (CEST) or the Europe/Amsterdam Summer time.

    >>> time_stamp =get_time_stamp_from_string(string_with_date_time=file_name,
    ...                                        timezone="Etc/GMT-2")
    >>> print("File name {} has time stamp {}".format(file_name, time_stamp))
    File name AMSBALDER_160929T000000 has time stamp 2016-09-29 00:00:00+02:00

    This time we assume the file name already contains a time zone, 2 hours + UTC.
    Since we already have a time zone, the *timezone* option can only convert the date
    time to the specified time zone.

    >>> file_name="AMSBALDER_160929T000000+02"
    >>> time_stamp =get_time_stamp_from_string(string_with_date_time=file_name,
    ...                                        timezone="Etc/GMT-2")
    >>> print("File name {} has time stamp {}".format(file_name, time_stamp))
    File name AMSBALDER_160929T000000+02 has time stamp 2016-09-29 00:00:00+02:00

    In case the time zone given by the *timezone* options differs with the time zone in
    the file name, the time zone is converted

    >>> file_name="AMSBALDER_160929T000000+00"
    >>> time_stamp =get_time_stamp_from_string(string_with_date_time=file_name,
    ...                                        timezone="Etc/GMT-2")
    >>> print("File name {} has time stamp {}".format(file_name, time_stamp))
    File name AMSBALDER_160929T000000+00 has time stamp 2016-09-29 02:00:00+02:00

    """
    try:
        file_time_stamp = dparser.parse(
            string_with_date_time, fuzzy=True, yearfirst=yearfirst, dayfirst=dayfirst
        )
        file_time_stamp = pd.Timestamp(file_time_stamp)
    except ValueError:
        file_time_stamp = None
    else:
        # we have found a time stamp. See if we have to add a time zone
        if timezone is not None:
            try:
                file_time_stamp = file_time_stamp.tz_localize(timezone)
            except TypeError:
                # a time zone was present already. Then try to convert it
                file_time_stamp = file_time_stamp.tz_convert(timezone)

    return file_time_stamp


class PackageInfo:
    """
    A class to analyse the version properties of this package

    Parameters
    ----------
    module_object: :obj:`Module`
        reference to the module for which want to to store the properties

    """

    def __init__(self, module_object):
        self.module_object = module_object

        self.package_version = None
        self.git_sha = None
        self.python_version = None
        self.build_date = None
        self.bundle_dir = None

        if getattr(sys, "frozen", False):
            # we are running in a bundle
            self.get_bundle_version()
        else:
            self.get_source_version()

    def get_bundle_version(self):
        """
        Get the version of the current package from the _version_frozen module which was
        written by the build_executable script.
        """
        try:
            import _version_frozen
        except ImportError:
            print("Could not load _version_frozen. All stay None")
        else:
            print(f"here with bundle {_version_frozen}")
            self.bundle_dir = sys._MEIPASS
            self.package_version = _version_frozen.VERSIONTAG
            self.git_sha = _version_frozen.GIT_SHA
            self.python_version = _version_frozen.PYTHON_VERSION
            self.build_date = _version_frozen.BUILD_DATE

    def get_source_version(self):
        """
        Get the version of the current package via the versioneer approach

        """
        # we are running in a normal Python environment
        self.bundle_dir = os.path.dirname(os.path.abspath(self.module_object.__file__))
        self.package_version = self.module_object.__version__
        self.git_sha = self.module_object.__git_sha_key__
        self.python_version = get_python_version_number(sys.version_info)
        self.build_date = pd.to_datetime("now").strftime("%Y%m%d")


class ConditionalDecorator:
    """
    Add a decorator to a function only if the condition is True

    Parameters
    ----------
    dec: decorator
        The decorator which you want to add when condition is true
    condition: bool
        Only add the decorator if this condition is True
    """

    def __init__(self, dec, condition):
        self.decorator = dec
        self.condition = condition

    def __call__(self, func):
        if not self.condition:
            # Return the function unchanged, not decorated.
            return func
        return self.decorator(func)
