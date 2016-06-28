import csv
from DictUtils.misc import NameUtils
from . import grabber
from multiprocessing.dummy import Pool as ThreadPool
import os
from time import sleep

class csvEntry:
    __entries = list()
    __auto_sha1 = False
    __url_prefix = ''
    __file_prefix = ''
    __file_ext = ''
    def __init__(self, f, *, url_prefix = '', file_prefix='', file_ext = '', sha1 = False):
        self.__auto_sha1 = sha1
        self.__url_prefix = url_prefix
        self.__file_prefix = file_prefix
        self.__file_ext = file_ext

        print( 'Reading list...' )
        f.readline()
        f_csv = csv.reader(f)
        for row in f_csv:
            entry = {
                'hw':   row[0],
                'id':   row[1],
                'url':  row[2]
            }
            self.__entries.append( entry )

    def __download_list(self, entry_list = None, strip_filename = False):
        if entry_list == None:
            entry_list = self.__entries
        for entry in entry_list:
            e_dl = grabber.EntryDictDownloader(entry,
                                       url_prefix=self.__url_prefix,
                                       file_ext=self.__file_ext,)
            e_dl.download(prefix=self.__file_prefix, gen_sha1=self.__auto_sha1, strip_filename=strip_filename)

    def download_all(self, *, resume = True, thread = 1, strip_filename = False):
        # self.__entries = sorted( self.__entries, itemgetter('id') )
        print( 'Soring list...' )
        self.__entries.sort(key=lambda entry: entry['id'].lower())

        # resume from break point
        if resume:
            skip_count = 0
            queued = list()
            for entry in self.__entries:
                if strip_filename:
                    fn = self.__file_prefix + NameUtils.strip_filename( entry['id'] ) + self.__file_ext
                else:
                    fn = self.__file_prefix + entry['id'] + self.__file_ext
                if os.path.exists( fn ):
                    # print( 'Skipping ' + entry['id'] + ' (' + fn + ') ...' )
                    skip_count += 1
                else:
                    queued.append( entry )
            print( 'Determining files to download...' )
            print( 'Skipped ' + str(skip_count) + ', ', end='' )
            self.__entries = queued

        if len(self.__entries) <= 0:
            print('Nothing to download.')
        else:
            print( str(len(self.__entries)) + ' to be downloaded...' )
            if thread > len(self.__entries):
                thread = len(self.__entries)
            if thread == 1:
                self.__download_list()
            else:
                # split the list
                entries_list = list()
                width = int(len(self.__entries) / thread)
                i = 0
                while i + width < len( self.__entries ):
                    entries_list.append(self.__entries[i: i + width])
                    i += width
                if i < len( self.__entries ):
                    entries_list.append(self.__entries[i: len( self.__entries ) - 1])

                # Let's go multi-thread!
                pool = ThreadPool( thread )
                pool.map(self.__download_list, entries_list)

            for entry in self.__entries:
                unfinished = list()
                if strip_filename:
                    fn = self.__file_prefix + NameUtils.strip_filename( entry['id'] ) + self.__file_ext
                else:
                    fn = self.__file_prefix + entry['id'] + self.__file_ext
                if not os.path.exists( fn ):
                    unfinished.append( entry )

                if len(unfinished) > 0:
                    # exit(1)
                    self.__entries = unfinished
                    sleep( 20 )
                    self.download_all(resume=True, thread=thread, strip_filename=strip_filename)