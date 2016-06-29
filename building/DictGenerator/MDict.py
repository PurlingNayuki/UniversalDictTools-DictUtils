from DictUtils.Datatype import Dictionary
import sys
import logging

class MDictGenerator:
    __source = None
    def __init__(self, provider: Dictionary, echo = True):
        self.__source = provider

    def __str__(self):
        result = ''
        dictionary = self.__source.to_dict_name()
        for hw in dictionary.keys():
            logging.info('[i] Converting ' + hw)
            result += hw + '\n'
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