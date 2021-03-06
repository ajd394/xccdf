# -*- coding: utf-8 -*-

"""
xccdf.models.html_element includes the class HTMLElement,
the base for every element with a HTML enabled text.

This module is part of the xccdf library.

Author: Rodrigo Núñez <rnunezmujica@icloud.com>
"""

# Python stdlib
from xml.etree import ElementTree
import re

# lxml
from lxml import etree
from lxml.etree import _Comment

# XCCDF
from xccdf.models.element import Element
from xccdf.constants import NSMAP


class HTMLElement(Element):

    """
    Generic class to implement a XCCDF element with HTML enabled text.
    """

    def __init__(self, xml_element=None, tag_name=None):
        """
        Initializes the attrs attribute to serialize the attributes.

        :param lxml.etree._Element xml_element: XML element to load.
        :param str tag_name: Tag name of the element.
        """

        super(HTMLElement, self).__init__(xml_element, tag_name)

        if xml_element is not None:
            self.import_element(xml_element)

    def import_element(self, xml_element):
        """
        Imports the element from an lxml element and loads its content.
        """

        super(HTMLElement, self).import_element(xml_element)

        self.content = self.get_html_content()

    def as_dict(self):
        """
        Serializes the object necessary data in a dictionary.

        :returns: Serialized data in a dictionary.
        :rtype: dict
        """

        element_dict = super(HTMLElement, self).as_dict()

        if hasattr(self, 'content'):
            element_dict['content'] = self.content

        return element_dict

    def get_html_content(self):
        """
        Parses the element and subelements and parses any HTML enabled text to
        its original HTML form for rendering.

        :returns: Parsed HTML enabled text content.
        :rtype: str
        """

        # Extract full element node content (including subelements)
        html_content = ''
        if hasattr(self, 'xml_element'):
            xml = self.xml_element
            content_list = ["" if xml.text is None else xml.text]

            def to_string(xml):
                if isinstance(xml, _Comment):
                    return str(xml)
                else:
                    return ElementTree.tostring(xml).decode('utf-8')

            content_list += [to_string(e) for e in xml.getchildren()]

            full_xml_content = "".join(content_list)

            # Parse tags to generate HTML valid content
            first_regex = r'html:'
            second_regex = r' xmlns:html=(["\'])(?:(?=(\\?))\2.)*?\1'
            html_content = re.sub(first_regex, '',
                                  re.sub(second_regex, '', full_xml_content))

        return html_content

    def convert_html_to_xml(self):
        """
        Parses the HTML parsed texts and converts its tags to XML valid tags.

        :returns: HTML enabled text in a XML valid format.
        :rtype: str
        """

        if hasattr(self, 'content') and self.content != '':
            regex = r'<(?!/)(?!!)'
            xml_content = re.sub(regex, '<xhtml:', self.content)
            return xml_content
        else:
            return ''

    def update_xml_element(self):
        """
        Updates the xml element contents to matches the instance contents.

        :returns: Updated XML element.
        :rtype: lxml.etree._Element
        """

        if not hasattr(self, 'xml_element'):
            self.xml_element = etree.Element(self.name, nsmap=NSMAP)

        for element in self.xml_element:
            self.xml_element.remove(element)

        self.xml_element.tail = ''
        self.xml_element.text = self.convert_html_to_xml()

        return self.xml_element
