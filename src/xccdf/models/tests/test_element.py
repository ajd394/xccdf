# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io
import sys

# lxml
from lxml import etree

# XCCDF
from xccdf.models.element import Element


class ElementTestCase(unittest.TestCase):

    """
    Test cases for Element class
    """

    def load_example_element(self):
        """
        Helper method to load an XML element
        """

        xml_path = os.path.abspath(os.path.dirname(__file__))
        xml_file = io.open(os.path.join(
            xml_path,
            'examples',
            'example_xccdf.xml'))

        xml_string = xml_file.read()
        xml_file.close()

        element_tree = etree.fromstring(xml_string.encode('utf-8'))

        for element in element_tree:
            uri, tag = Element.get_namespace_and_tag(element.tag)

            if tag == 'Group':
                return element

    def test_init_all_ok_with_element(self):
        """
        Tests the class constructor with an xml_element
        """
        xml_element = self.load_example_element()

        xccdf_element = Element(xml_element)

        uri, tag = Element.get_namespace_and_tag(xml_element.tag)

        self.assertEqual(xccdf_element.namespace, uri,
                         'Namespace does not match')
        self.assertEqual(xccdf_element.name, tag,
                         'Tag name does not match')

        # Attributes asserting
        for attr, value in iter(xml_element.attrib.items()):
            self.assertEqual(getattr(xccdf_element, attr), value,
                             '{attr} attribute value does not match'.format(
                                 attr=attr))

    def test_init_all_ok_with_tag_name(self):
        """
        Tests the class constructor with a tag_name
        """

        tag_name = 'element'

        xccdf_element = Element(tag_name=tag_name)

        self.assertEqual(xccdf_element.name, tag_name,
                         'Tag name does not match')

    def test_init_empty(self):
        """
        Tests the class constructor passing a different element
        rather than a XML element
        """

        xml_element = None
        tag_name = None

        error_msg = 'either xml_element or tag_name are required'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(ValueError,
                                        error_msg):
                Element(xml_element, tag_name)
        else:
            with self.assertRaisesRegexp(ValueError,
                                         error_msg):
                Element(xml_element, tag_name)

    def test_print_object(self):
        """
        Tests the string representation of an Element object
        """

        xml_element = self.load_example_element()

        xccdf_element = Element(xml_element)

        uri, tag = Element.get_namespace_and_tag(xml_element.tag)

        string_element = '<{namespace}>{tag}'.format(namespace=uri, tag=tag)

        self.assertEqual(str(xccdf_element), string_element,
                         'String representation does not match')

    def test_print_object_only_tag(self):
        """
        Tests the string representation of an Element object
        """

        tag_name = 'element'
        xccdf_element = Element(tag_name=tag_name)

        string_element = '{tag}'.format(tag=tag_name)

        self.assertEqual(str(xccdf_element), string_element,
                         'String representation does not match')

    def test_method_as_dict(self):
        """
        Tests the as_dict method
        """

        xml_element = self.load_example_element()

        xccdf_element = Element(xml_element)

        attr_list = xccdf_element.attrs

        element_dict = xccdf_element.as_dict()

        self.assertEqual(element_dict['namespace'],
                         xccdf_element.namespace,
                         'Namespace does not match')

        self.assertEqual(element_dict['name'],
                         xccdf_element.name,
                         'Tag name does not match')

        self.assertEqual(element_dict['text'],
                         xccdf_element.text,
                         'Text content does not match')

        attr_dict = element_dict['attrs']

        for attr in attr_list:
            self.assertIsNotNone(
                attr_dict.get(attr, None),
                '{attr} attr no in dictionary'.format(attr=attr))
            self.assertEqual(
                getattr(xccdf_element, attr),
                attr_dict.get(attr),
                '{attr} value does not match'.format(attr=attr))

        for attr, value in iter(attr_dict.items()):
            self.assertIn(attr, attr_list, 'Unexpected attr in dictionary')

    def test_method_as_dict_no_attrs(self):
        """
        Tests the as_dict method without attrs
        """

        xml_element = self.load_example_element()

        xccdf_element = Element(xml_element)

        xccdf_element.attrs = []

        attr_dict = xccdf_element.as_dict()['attrs']

        self.assertEqual(attr_dict, dict(), 'as_dict dictionary is not empty')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(ElementTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
