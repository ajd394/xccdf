# -*- coding: utf-8 -*-

"""
xccdf.models.profile includes the class RearMatter
to create or import a <xccdf:rear-matter> element.

This module is part of the xccdf library.

Author: Rodrigo Núñez <rnunezmujica@icloud.com>
"""

# XCCDF
from xccdf.models.html_element import HTMLElement


class RearMatter(HTMLElement):

    """
    Class to implement <xccdf:rear-matter> element.
    """

    def __init__(self, xml_element=None):
        """
        Initializes the attrs attribute to serialize the attributes.

        :param lxml.etree._Element xml_element: XML element to load_xml_attrs.
        """

        tag_name = 'rear-matter' if xml_element is None else None

        super(RearMatter, self).__init__(xml_element, tag_name)

    def __str__(self):
        """
        String representation of RearMatter object.

        :returns: RearMatter object as a string.
        :rtype: str
        """

        string_value = 'rear-matter'
        if hasattr(self, 'content'):
            string_value += ' {rrmatter}'.format(rrmatter=self.content)
        if hasattr(self, 'lang'):
            string_value += ' ({lang})'.format(lang=self.lang)
        return string_value
