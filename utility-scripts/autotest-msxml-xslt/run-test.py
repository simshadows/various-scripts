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

from copy import deepcopy

import win32com.client
from lxml import etree

################################################################################
# BASE UTILITIES ###############################################################
################################################################################

MSXML_PROGID = "Msxml2.DOMDocument.6.0"

def read_file(filepath):
    with open(filepath, "r") as f:
        return etree.parse(f)

def msxml_transform(xslt_filepath, xml_data_etree):
    def get_msxml_com(filepath_or_etree):
        com = win32com.client.Dispatch(MSXML_PROGID)
        if isinstance(filepath_or_etree, etree.ElementTree):
            success = com.loadXML(etree.tostring(filepath_or_etree).decode())
        elif isinstance(filepath_or_etree, str):
            success = com.load(filepath_or_etree)
        else:
            raise RuntimeError(f"Unexpected type {type(filepath_or_etree)}")

        if not success:
            error = com.parseError
            raise TypeError(f"XML parsing error at line {error.line}: {error.reason}")
        
        return com

    com_xslt = get_msxml_com(xslt_filepath)
    com_data = get_msxml_com(xml_data_etree)
    result = com_data.transformNode(com_xslt)
    return etree.fromstring(result)

def prettyprint(node):
    return etree.tostring(node, pretty_print=True).decode()


################################################################################
# HIGHER-LEVEL XPATH-BASED UTILITIES ###########################################
################################################################################

def xpath_replace_values(root, xpath, new_inner, *, num_expected_changes):
    if isinstance(new_inner, int):
        new_inner = str(new_inner)

    nodes = root.xpath(xpath)
    if len(nodes) != num_expected_changes:
        raise ValueError(f"XPath expected {num_expected_changes} nodes. Instead got {len(nodes)}.\n\nXPath: {xpath}")

    for node in nodes:
        if isinstance(node, etree._ElementUnicodeResult):
            if node.is_attribute:
                if f"@{node.attrname}" not in xpath:
                    raise ValueError(f"The attribute name is not directly found in the XPath. Your XPath probably works fine, but it should be simplified.\n\nAttribute found: {node.attrname}\n\nXPath: {xpath}")
                node.getparent().set(node.attrname, new_inner)
            else:
                raise RuntimeError("Unsupported operation.")
        elif isinstance(node, etree.Element):
            node.text = new_inner
            for child in list(node):
                node.remove(child)
        else:
            raise RuntimeError(f"XPath resulted in unexpected type `{type(node)}`.")

def xpath_add_child_element(root, xpath, new_inner, *, num_expected_changes):
    nodes = root.xpath(xpath)
    if len(nodes) != num_expected_changes:
        raise ValueError(f"XPath expected {num_expected_changes} nodes. Instead got {len(nodes)}.\n\nXPath: {xpath}")
    
    for node in nodes:
        node.append(deepcopy(new_inner))

def xpath_add_attribute(root, xpath, key, value, *, num_expected_changes):
    assert isinstance(key, str)
    assert isinstance(value, str)
    nodes = root.xpath(xpath)
    if len(nodes) != num_expected_changes:
        raise ValueError(f"XPath expected {num_expected_changes} nodes. Instead got {len(nodes)}.\n\nXPath: {xpath}")
    
    for node in nodes:
        node.set(key, value)

def xpath_assert_count(root, xpath, num_expected):
    nodes = root.xpath(xpath)
    if len(nodes) != num_expected:
        raise AssertionError(f"Test failed.\n\nXPath expected {num_expected} nodes. Instead got {len(nodes)}.\n\nXPath: {xpath}")


################################################################################
# TESTS ########################################################################
################################################################################

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
