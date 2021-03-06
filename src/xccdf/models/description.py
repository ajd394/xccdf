# -*- coding: utf-8 -*-

"""
xccdf.models.description includes the class Description
to create or import a <xccdf:description> element.

This module is part of the xccdf library.

Author: Rodrigo Núñez <rnunezmujica@icloud.com>
"""

# lxml
from lxml import etree

# XCCDF
from xccdf.models.html_element import HTMLElement


class Description(HTMLElement):

    """
    Class to implement <xccdf:description> element.
    """

    def __init__(self, xml_element=None):
        """
        Initializes the attrs attribute to serialize the attributes.

        :param lxml.etree._Element xml_element: XML element to load.
        """

        tag_name = 'description' if xml_element is None else None

        super(Description, self).__init__(xml_element, tag_name)

    def __str__(self):
        """
        String representation of Description object.

        :returns: Description object as a string.
        :rtype: str
        """

        string_value = 'description'
        if hasattr(self, 'content'):
            string_value += ' {desc}'.format(desc=self.content)
        if hasattr(self, 'lang'):
            string_value += ' ({lang})'.format(lang=self.lang)
        return string_value

    def update_xml_element(self):
        """
        Updates the xml element contents to matches the instance contents.

        :returns: Updated XML element.
        :rtype: lxml.etree._Element
        """

        super(Description, self).update_xml_element()

        if hasattr(self, 'lang'):
            self.xml_element.set(
                '{http://www.w3.org/XML/1998/namespace}lang', self.lang)
        if hasattr(self, 'override'):
            self.xml_element.set('override', str(self.override))

        return self.xml_element

    def to_xml_string(self):
        """
        Updates the XML element and returns it as a string.

        :returns: XML block as a string.
        :rtype: str
        """

        self.update_xml_element()
        xml = self.xml_element

        return etree.tostring(xml, pretty_print=True).decode('utf-8')
