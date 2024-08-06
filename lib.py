import re
import unicodedata


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
