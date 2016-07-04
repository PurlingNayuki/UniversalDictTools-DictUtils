import hashlib
import os
from urllib.request import urlopen
import urllib.error
from DictUtils.misc import NameUtils, ColoredDisplay

class EntryDictDownloader:
    __entry = {}
    __fn = None
    __url_prefix = ''
    __file_ext = ''

    def __init__(self, entry, *, url_prefix = '', file_ext = ''):
        self.__entry = entry
        self.__url_prefix = url_prefix
        self.__file_ext = file_ext

    def download(self, *, prefix = '', gen_sha1 = False, strip_filename = False):
        print( ColoredDisplay.blue('[i] ') + 'Downloading \"' + self.__entry['hw'] + '\" (' + self.__entry['id'] + ')...')
        if strip_filename:
            self.__fn = NameUtils.strip_filename( self.__entry['id'] )
        else:
            self.__fn = self.__entry['id']
        self.__fn = prefix + self.__fn

        # Create non-existing directory
        dir_name = os.path.dirname( self.__fn )
        if not os.path.exists( dir_name ):
            print( 'Created directory \"' + dir_name + '\"' )
            os.makedirs(dir_name, exist_ok=True)

        # Judge files that have the same name and auto-rename them
        if os.path.exists( self.__fn + self.__file_ext ):
            i = 1
            while os.path.exists( self.__fn + '-' + str( i ) + self.__file_ext ):
                i += 1
            self.__fn = self.__fn + '-' + str( i )

        try:
            with open(self.__fn + '.downloading', 'wb') as f:
                f.write( urlopen(self.__url_prefix + self.__entry['url']).read() )

            # After finished downloading, mark them as downloaded
            os.rename(self.__fn + '.downloading', self.__fn + self.__file_ext)
            print( ColoredDisplay.green('[i] ') + 'Finished \"' + self.__entry['id'] + '\" => ' + self.__fn + self.__file_ext)

            # Auto generate checksum
            if gen_sha1:
                sha1 = self.get_hash()
                if not sha1 == None:
                    with open(self.__fn + self.__file_ext + '.sha1.checksum', 'w') as f_chksum:
                        f_chksum.write( sha1 )
        except urllib.error.URLError as err:
            print( ColoredDisplay.red('[w] ') + 'Failed downloading \"' + self.__entry['hw'] + '\" (' + self.__entry['id'] + '): ', end='')
            print( err.reason )
        except urllib.error.HTTPError as err:
            print( ColoredDisplay.red('[w] ') + 'Failed downloading \"' + self.__entry['hw'] + '\" (' + self.__entry['id'] + '): ', end='')
            print( err.reason )

    def get_hash(self):
        print( 'Generating SHA-1 hashcode for ' + self.__fn + self.__file_ext + ' ...')
        if not self.__fn == None:
            with open(self.__fn + self.__file_ext, 'rb') as f:
                byte = f.read()
                return hashlib.sha1(byte).hexdigest()
        else:
            return None
