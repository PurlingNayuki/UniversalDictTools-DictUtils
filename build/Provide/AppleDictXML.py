from DictUtils.datatype import Entry, Dictionary
import xml.etree.ElementTree as ElementTree
import logging

class AppleDictXMLProvider (Dictionary):
    def __init__(self, f, echo = True, handler = None):
        super().__init__(f.name)
        if echo:
            logging.basicConfig(level=logging.INFO)
        self._dict = Dictionary(f.name)

        namespaces = {'d': '{http://www.apple.com/DTDs/DictionaryService-1.0.rng}'} # namespace for Apple Dictionaries

        for line in f:
            if line.startswith('<d:entry'):
                tree = ElementTree.fromstring(line)

                logging.info('Processing ' + tree.get(namespaces['d'] + 'title'))
                if handler == None:
                    content = line[0:-1]
                else:
                    content = handler(line[0:-1])

                entry = Entry(tree.get(namespaces['d'] + 'title'),
                                    content=content,
                                    hwid=tree.get('id'),
                                    title=tree.get(namespaces['d'] + 'title'))
                self._dict.append(entry)

        if echo:
            print('Providing ' + str(len(self)) + ' entries')