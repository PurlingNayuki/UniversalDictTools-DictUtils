from bs4 import BeautifulSoup, element
import json

from DictUtils.datatype import Entry, Dictionary

class JsonProvider(Dictionary):
    def __init__(self, name, echo = False):
        self.name = name

    @classmethod
    def json_to_html(cls, bsObj: element, json_obj, name=None):
        div = bsObj.new_tag('div')
        if not name == None:
            div.attrs['class'] = name
        else:
            div.attrs['class'] = 'json_list'

        if isinstance(json_obj, dict):
            for child_name in json_obj.keys():
                div.append(cls.json_to_html(bsObj, json_obj[child_name], child_name))
        elif isinstance(json_obj, list):
            for child in json_obj:
                div.append(cls.json_to_html(bsObj, child))
        elif isinstance(json_obj, str):
            div.name = 'span'
            div.attrs['class'] = name if name != None else 'str'
            div.append(cls._handle_str(json_obj))
        return div

    @staticmethod
    def _handle_str(markup):
        """
        Originally from BeautifulSoup 4
        Check if markup looks like it's actually a url and raise a warning
        if so. Markup can be unicode or str (py2) / bytes (py3).
        """
        if isinstance(markup, bytes):
            space = b' '
            cant_start_with = (b"http:", b"https:")
        elif isinstance(markup, str):
            space = ' '
            cant_start_with = ("http:", "https:")
        else:
            return

        if any(markup.startswith(prefix) for prefix in cant_start_with) \
            and not space in markup:
                    decoded_markup = markup
        else:
                    decoded_markup = BeautifulSoup(markup, 'html.parser')

        return decoded_markup