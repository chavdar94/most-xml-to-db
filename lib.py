import re
import unicodedata
from xml.etree import ElementTree as ET
import json


def slugify(value):
    """
    Convert a string to a slug.
    """
    value = str(value)
    # Normalize the string to remove accents and special characters
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    # Convert to lowercase
    value = value.lower()
    # Replace spaces with hyphens
    value = re.sub(r'\s+', '-', value)
    # Remove any character that is not alphanumeric, a hyphen, or an underscore
    value = re.sub(r'[^\w\-]+', '', value)
    # Replace multiple hyphens with a single hyphen
    value = re.sub(r'-+', '-', value)
    # Trim hyphens from the start and end of the string
    value = value.strip('-')
    return value


def parse_xml_children(parent_elem, child_tag):
    if parent_elem is None:
        return None

    values = []
    for child in parent_elem.findall(child_tag):
        if len(child):  # child has nested elements
            values.append({
                subchild.tag: (subchild.text.strip() if subchild.text else None)
                for subchild in child
            })
        else:
            text = child.text.strip() if child.text else None
            if text:
                values.append(text)

    return values or None