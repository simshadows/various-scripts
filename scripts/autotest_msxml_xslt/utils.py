#!/usr/bin/env python3

"""
Filename: utils.py
Author:   simshadows <contact@simshadows.com>
"""

from copy import deepcopy

import win32com.client
from lxml import etree

__MSXML_PROGID = "Msxml2.DOMDocument.6.0"

def read_file(filepath):
    with open(filepath, "r") as f:
        return etree.parse(f)

def msxml_transform(xslt_filepath, xml_data_etree):
    def get_msxml_com(filepath_or_etree):
        com = win32com.client.Dispatch(__MSXML_PROGID)
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
