from DictUtils.datatype import Entry, Dictionary
import logging

class MDictProvider (Dictionary):
    def __init__(self, f, echo = False):
        super().__init__(f.name)
        for line in f:
            hw = line.replace('\n', '')
            # fill contents
            line = f.readline()
            content = ''
            while not line.startswith('</>'):
                content += line
                line = f.readline()
            self.append(Entry(hw, content = content))

        if echo:
            logging.info( 'Read ' + str(len(self)) + ' entries')
