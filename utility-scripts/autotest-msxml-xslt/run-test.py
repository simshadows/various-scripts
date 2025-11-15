#!/usr/bin/env python3

"""
Filename: run-test.py
Author:   simshadows <contact@simshadows.com>

This is a template script you can use as a base for automated MSXML XSLT testing on Windows.
This script isn't designed to work on Linux/MacOS.

We use MSXML exclusively to carry out the transformation, then we use lxml to check the result.
This allows the code to be easier to port if you need to autotest with a different XML engine.
I would've liked to use the built-in xml module, but its XPath implementation is too limited.
"""

import win32com.client
from lxml import etree
#import xml.etree.ElementTree as etree

MSXML_PROGID = "Msxml2.DOMDocument.6.0"

def msxml_load(filepath):
    com = win32com.client.Dispatch(MSXML_PROGID)
    success = com.load(filepath)
    if not success:
        error = com.parseError
        raise ValueError(f"XML parsing error at line {error.line}: {error.reason}")
    return com

def msxml_transform(com_xslt, com_data):
    result = com_data.transformNode(com_xslt)
    return etree.fromstring(result)

def xml_to_string(node):
    return etree.tostring(node, encoding="unicode")

################################################################################
# TESTS ########################################################################
################################################################################

XSLT_PATH = "./sample_transform.xslt"
DATA_PATH = "./sample_data.xml"

def run():
    com_xslt = msxml_load(XSLT_PATH)
    com_data = msxml_load(DATA_PATH)

    root = msxml_transform(com_xslt, com_data)
    print(root)
    print(xml_to_string(root))
    print()

    result = root.findall("./MonkaS")
    print(result)
    print()

    result = root.findall("./MonkaSs")
    print(result)
    print()

    #result = root.findall("not(./MonkaSs)")
    #print(result)
    #print()

    #result = root.findall("./Barbaz[@lmao='ayy']")
    #print(result)
    #print()

    result = root.xpath("./Barbaz[not(@lmao='ayyx')]")
    print(result)
    print()

    result = root.xpath("./Barbaz and ./MonkaS")
    print(result)
    print()

run()
