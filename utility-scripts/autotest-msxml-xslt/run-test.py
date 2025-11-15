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
#import xml.etree.ElementTree as etree

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

def clear_inner(node):
    assert isinstance(node, etree.Element)
    node.text = None
    for child in list(node):
        node.remove(child)


################################################################################
# HIGHER-LEVEL XPATH-BASED UTILITIES ###########################################
################################################################################

def xpath_replace_children_of(root, xpath, new_inner, *, num_expected_changes):
    assert isinstance(root, etree.ElementTree)
    assert isinstance(xpath, str) and xpath
    # new_inner currently only supports text
    assert (new_inner is None) or (isinstance(new_inner, str) and new_inner)
    assert isinstance(num_expected_changes, int)

    nodes = root.xpath(xpath)
    if len(nodes) != num_expected_changes:
        raise ValueError(f"XPath expected {num_expected_changes} nodes. Instead got {len(nodes)}.\n\nXPath: {xpath}")

    for node in nodes:
        node.text = new_inner
        for child in list(node):
            node.remove(child)


################################################################################
# TESTS ########################################################################
################################################################################

XSLT_PATH = "./sample_transform.xslt"
DATA_PATH = "./sample_data.xml"

def run():
    root_original = read_file(DATA_PATH)
    print("Original data:")
    print("===")
    print(prettyprint(root_original))
    print()

    root_result = msxml_transform(XSLT_PATH, root_original)
    print("After running transform:")
    print("===")
    print(prettyprint(root_result))
    print()

    
    print("Modifying a deep copy:")
    print("===")
    root = deepcopy(root_original)
    print(prettyprint(root))

    print("===")
    xpath_replace_children_of(root, "/Foobar/Omegalul", "42069", num_expected_changes=3)
    print(prettyprint(root))
    
    print("===")
    root_result = msxml_transform(XSLT_PATH, root)
    print(prettyprint(root_result))

run()
