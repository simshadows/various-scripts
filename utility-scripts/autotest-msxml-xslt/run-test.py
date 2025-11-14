#!/usr/bin/env python3

"""
Filename: run-test.py
Author:   simshadows <contact@simshadows.com>

This is a template script you can use as a base for automated MSXML XSLT testing on Windows.
This script isn't designed to work on Linux/MacOS.
"""

import win32com.client

MSXML_PROGID = "Msxml2.DOMDocument.6.0"

XSLT_PATH = "./sample_transform.xslt"
DATA_PATH = "./sample_data.xml"

def load_xml(com, filepath):
    success = com.load(filepath)
    if not success:
        error = com.parseError
        raise ValueError(f"XML parsing error at line {error.line}: {error.reason}")

def run():
    com_msxml_xslt = win32com.client.Dispatch(MSXML_PROGID)
    com_msxml_data = win32com.client.Dispatch(MSXML_PROGID)

    load_xml(com_msxml_xslt, XSLT_PATH)
    load_xml(com_msxml_data, DATA_PATH)

    result = com_msxml_data.transformNode(com_msxml_xslt)
    print(result)

run()
