from asio import ASIO, SEEK_ORIGIN_CURRENT

import sys
import os


def read(path):
    f = ASIO.open(path, opener=False)
    orig_path = f.get_path()

    size = f.get_size()
    print "Seeking to end, %s" % size
    print f.seek(size, SEEK_ORIGIN_CURRENT)

    while True:
        line = f.read_line(timeout=1, timeout_type='return')
        if not line and f.get_path() != orig_path:
            f.close()
            return

        print line

    f.close()



if __name__ == '__main__':
    log_path_components = ['Plex Media Server', 'Logs', 'Plex Media Server.log']

    path = None

    if len(sys.argv) >= 2:
        path = sys.argv[1]
    else:
        base_path = None

        if os.name == 'nt':
            base_path = os.environ.get('LOCALAPPDATA')
        elif os.name == 'posix':
            base_path = '/var/lib/plexmediaserver/Library/Application Support'

        path = os.path.join(base_path, *log_path_components)

    print 'Path: "%s"' % path

    if not os.path.exists(path):
        print 'File at "%s" not found' % path
        path = None

    if not path:
        print 'Unknown path for "%s"' % os.name
        exit()

    while True:
        read(path)
        print 'file timeout, re-opening'
