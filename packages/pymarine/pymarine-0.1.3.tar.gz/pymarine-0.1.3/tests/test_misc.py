#!/usr/bin/env python

import os
import re
import sys
import time

from numpy import array
from numpy.testing import (
    assert_almost_equal,
    assert_equal,
    assert_raises,
    assert_string_equal,
)

try:
    from pymarine.utils import Q_
except ImportError:
    Q_ = None
from pymarine.utils.misc import (
    Chdir,
    Timer,
    clear_argument_list,
    clear_path,
    get_clean_version,
    get_python_version_number,
    get_regex_pattern,
    get_value_magnitude,
    is_exe,
    set_default_dimension,
)


def test_timer():
    number_of_seconds = 1.0
    with Timer() as timer:
        time.sleep(number_of_seconds)
    assert_almost_equal([timer.secs], [number_of_seconds], decimal=0)


def test_chdir():
    python_dir = os.path.dirname(sys.prefix)
    with Chdir(new_path=python_dir):
        current_dir = os.getcwd()

    assert_string_equal(python_dir, current_dir)


def test_is_exe():
    # works only on linux
    test_file = "ls"
    this_is_an_executable = is_exe(test_file)
    if os.name != "nt":
        # this test can only succeed on linux
        assert_equal(this_is_an_executable, True)


def test_clean_path():
    python_dir = os.path.dirname(sys.prefix)
    new_path = clear_path(python_dir)
    assert_string_equal(python_dir, new_path)


def test_get_clean_version():
    version_number = "1.1"
    test_version_clean = "test_clean_version-" + version_number
    test_version_string = test_version_clean + "+jkjfds"
    clean_version = get_clean_version(test_version_string)
    assert_string_equal(version_number, clean_version)


def test_get_python_version_number():
    get_python_version_number(sys.version_info)


def test_get_regex_pattern():
    regular_expression = r"\s\d+\w"
    result_1 = get_regex_pattern(regular_expression)
    result_2 = re.compile(f"{regular_expression}")
    assert_equal(result_1, result_2)


def test_clear_argument_list():
    arg_old = ["blabla\r", "fdsafds", "blablabla\r", "blabla\n"]
    arg_new = clear_argument_list(arg_old)
    arg_new_expected = ["blabla", "fdsafds", "blablabla", "blabla\n"]
    assert_equal(arg_new, arg_new_expected)


def test_set_default_dimensions():
    # in case no dimension is given, we add the default dimension
    val_in = "1.0"
    val_out = set_default_dimension(val_in, "meter")
    assert_equal(val_out, Q_(val_in, "meter"))

    # in case x dimension is given, we do not the default dimension
    val_in = Q_(2.0, "meter")
    val_out = set_default_dimension(val_in, "meter")
    assert_equal(val_out, Q_(val_in, "meter"))

    # in case we pass a value with a different dimensionality as the default dimension,
    # raise an AssertionError
    val_in = Q_(3.0, "second")
    assert_raises(AssertionError, set_default_dimension, val_in, "meter")

    val_in = [0, 1, 2]
    val_out = set_default_dimension(val_in, "meter")
    for i, x in enumerate(val_out):
        assert_equal(x, Q_(val_in[i], "meter"))

    val_in = ["0", "1", "2"]
    val_out = set_default_dimension(val_in, "meter")
    for i, x in enumerate(val_out):
        assert_equal(x, Q_(val_in[i], "meter"))

    val_in = array([0, 1, 2])
    val_out = set_default_dimension(val_in, "meter")
    for i, x in enumerate(val_out):
        assert_equal(x, Q_(val_in[i], "meter"))
    assert_equal(val_out.all(), Q_(val_in, "meter").all())

    val_in = Q_(array([0, 1, 2]), "meter")
    val_out = set_default_dimension(val_in, "meter")
    for i, x in enumerate(val_out):
        assert_equal(x, Q_(val_in[i], "meter"))
    assert_equal(val_out.all(), Q_(val_in, "meter").all())

    # We pass an array with dimension second while we request a default dimension of
    # meter. This should raise an error
    val_in = Q_(array([0, 1, 2]), "second")
    assert_raises(AssertionError, set_default_dimension, val_in, "meter")

    val_in = "1.0 meter"
    val_out = set_default_dimension(val_in, "meter")
    assert_equal(val_out, Q_("1 meter"))


def test_value_magnitude():
    frequency_bare = 1.0
    frequency_unit = Q_(frequency_bare, "Hz")

    frequency_bare_2 = get_value_magnitude(frequency_unit)

    assert_equal([frequency_bare], [frequency_bare_2])

    frequency_bare_2 = get_value_magnitude(frequency_bare)
    assert_equal([frequency_bare], [frequency_bare_2])

    frequency_none = get_value_magnitude(None)
    assert_equal([frequency_none], [None])

    velocity_knots_mag = get_value_magnitude(Q_("1.0 knots"))
    assert_almost_equal([velocity_knots_mag], [0.514444444])

    velocity_knots_mag = get_value_magnitude(
        Q_("1.0 knots"), convert_to_base_units=False
    )
    assert_almost_equal([velocity_knots_mag], [1.0])
