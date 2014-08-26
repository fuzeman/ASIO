# Copyright 2013 Dean Gardiner <gardiner91@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import yappi

from asio import ASIO

from random import randint
from threading import Thread
import logging
import os
import time


class TestApplication(object):
    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.base_path = os.path.join(self.base_path, 'test_tmp')

        self.writing = False

        print 'Base Path: "%s"' % self.base_path

    def random_write(self, path, prefix, seconds, count=250):
        start_time = time.time()
        fp = open(path, 'a+')

        num = 1
        while time.time() - start_time < seconds and num <= count:
            line = '%s:%s\n' % (prefix, randint(10000, 99999))
            print 'write %r' % line.strip()

            fp.write(line)
            fp.flush()

            time.sleep(0.1)
            num += 1

        remaining_sleep = seconds - (time.time() - start_time)
        if remaining_sleep > 0:
            time.sleep(remaining_sleep)

        fp.close()

    def read(self, file_path):
        while not self.writing:
            time.sleep(1)

        print "Read starting..."

        f = ASIO.open(file_path, opener=False)
        orig_path = f.get_path()

        while True:
            if f is None:
                print 'Opening file...'
                f = ASIO.open(file_path, opener=False)

            # Try read line
            line = f.read_line(timeout=1, timeout_type='return')

            if not line:
                if f.get_path() != orig_path:
                    f.close()
                    f = None
                elif not self.writing:
                    return

            print 'read %r' % (line,)

        f.close()

    def run(self):
        # Ensure directory exists
        if not os.path.exists(self.base_path):
            os.mkdir(self.base_path)

        if os.path.exists(os.path.join(self.base_path, 'test.log.1')):
            os.remove(os.path.join(self.base_path, 'test.log.1'))

        # Start reading
        read_thread = Thread(target=self.read, args=(os.path.join(self.base_path, 'test.log'),))
        read_thread.start()

        self.run_write()

    def run_write(self):
        self.writing = True

        # Start writing
        self.random_write(os.path.join(self.base_path, 'test.log'), 'one', 10)

        # "rotate" file
        os.rename(os.path.join(self.base_path, 'test.log'), os.path.join(self.base_path, 'test.log.1'))

        # Continue writing..
        self.random_write(os.path.join(self.base_path, 'test.log'), 'two', 10)

        # Finished.
        self.writing = False


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    yappi.start()

    app = TestApplication()
    app.run()

    yappi.get_func_stats().print_all(columns={
        0: ("name", 140),
        1: ("ncall", 10),
        2: ("tsub", 8),
        3: ("ttot", 8),
        4: ("tavg", 8)
    })

