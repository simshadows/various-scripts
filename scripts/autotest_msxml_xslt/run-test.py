#!/usr/bin/env python3

"""
Filename: run-test.py
Author:   simshadows <contact@simshadows.com>

This is a template script you can use as a base for automated MSXML XSLT testing on Windows.
This script isn't designed to work on Linux/MacOS. The point of this script is for

We use MSXML exclusively to carry out the transformation, then we use lxml to check the result.
This allows the code to be easier to port if you need to autotest with a different XML engine.
I would've liked to use the built-in xml module, but its XPath implementation is too limited.
"""

from lxml import etree

from utils import (
    read_file,
    msxml_transform,
    prettyprint,
    xpath_replace_values,
    xpath_add_child_element,
    xpath_add_attribute,
    xpath_assert_count,
)

XSLT_PATH = "./sample_transform.xslt"
DATA_PATH = "./sample_data.xml"

def get_input_xml(*, aaa="e", number=42069, has_poggers=False, has_rofl=False):
    root = read_file(DATA_PATH)
    xpath_replace_values(root, "/Foobar/Omegalul[@aaa='b']/@aaa", aaa, num_expected_changes=1)
    xpath_replace_values(root, "/Foobar/Omegalul[@aaa='a' or @aaa='c']", number, num_expected_changes=2)
    if has_poggers:
        xpath_add_child_element(root, "/Foobar/Kekw", etree.Element("POGGERS"), num_expected_changes=2)
    if has_rofl:
        xpath_add_attribute(root, "/Foobar/Kekw[not(@xd='lmao')]", "rofl", "Yes", num_expected_changes=1)
    return root

def do_transform(n, input_xml):
    print(f"Test {n}:")
    print("===")
    root_result = msxml_transform(XSLT_PATH, input_xml)
    print(prettyprint(root_result))
    print()
    return root_result

def run_tests():
    root_result = do_transform(1, get_input_xml(has_poggers=True))

    xpath_assert_count(root_result, "/Foobar/MonkaS[@bbb='x']", 0)
    
    root_result = do_transform(2, get_input_xml(aaa="x", number=654, has_rofl=True))

    xpath_assert_count(root_result, "/Foobar/MonkaS[@bbb='x']", 1)

run_tests()
