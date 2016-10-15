from DictUtils.datatype import Dictionary
import logging

class MDictGenerator:
    __source = None
    __css_fn = None
    def __init__(self, provider: Dictionary, css = None, echo = True):
        self.__source = provider
        self.__css_fn = css

    def __str__(self):
        result = ''
        dictionary = self.__source.to_dict_name()
        for hw in dictionary.keys():
            logging.info('[i] Converting ' + hw)
            result += hw + '\n'
            if self.__css_fn != None:
                if not isinstance(self.__css_fn, str):
                    logging.warning('Parameter \"css\" should be a str object')
                result += '<link rel=\"stylesheet\" type=\"text/css\" href=\"' + str(self.__css_fn) + '\">\n'
            for entry in dictionary[hw]:
                result += entry.content + '\n'
            result += '</>\n'

        return result

    def __getitem__(self, item: str):
        result = ''
        if self.__source.has(item):
            result += item + '\n'
            result += self.__source[item].content + '\n'
            result += '</>\n'

        return result