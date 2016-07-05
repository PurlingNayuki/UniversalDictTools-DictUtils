import csv
from DictUtils.misc import NameUtils
from . import grabber
from multiprocessing import Queue
from threading import Thread, Lock
import os
from time import sleep

class by_csv:
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

    def __download_entry(self, queue: Queue, strip_filename = False):
        if not queue.empty():
            entry = queue.get(1)
            e_dl = grabber.EntryDictDownloader(entry,
                                       url_prefix=self.__url_prefix,
                                       file_ext=self.__file_ext,)
            e_dl.download(prefix=self.__file_prefix, gen_sha1=self.__auto_sha1, strip_filename=strip_filename)

    def download_all(self, *, resume = True, thread = 1, strip_filename = False):
        # self.__entries = sorted( self.__entries, itemgetter('id') )
        print( 'Soring list...' )
        self.__entries.sort(key=lambda entry: entry['id'].lower())

        queued = Queue()
        # resume from break point
        if resume:
            skip_count = 0
            for entry in self.__entries:
                if strip_filename:
                    fn = self.__file_prefix + NameUtils.strip_filename( entry['id'] ) + self.__file_ext
                else:
                    fn = self.__file_prefix + entry['id'] + self.__file_ext
                if os.path.exists( fn ):
                    # print( 'Skipping ' + entry['id'] + ' (' + fn + ') ...' )
                    skip_count += 1
                else:
                    queued.put( entry )
            print( 'Determining files to download...' )
            print( 'Skipped ' + str(skip_count) + ', ', end='' )
        else:
            for entry in self.__entries:
                queued.put( entry )

        if queued.empty():
            print( 'Nothing to be downloaded.' )
        else:
            print( str(len(self.__entries)) + ' to be downloaded...' )

        # Let's go multi-thread!
        pool = list()
        args = [queued, strip_filename]
        for i in range(0, thread):
            t = Thread(target=self.__download_entry, args=args)
            pool.append( t )

        # wait the threads
        for t in pool:
            t.join()