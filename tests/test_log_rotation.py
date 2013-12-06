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

from random import randint
import time
import os


def random_write(path, prefix, seconds, sleep=100, count=250):
    start_time = time.time()
    fp = open(path, 'a+')

    num = 1
    while time.time() - start_time < seconds and num <= count:
        line = '%s:%s\n' % (prefix, randint(10000, 99999))
        print 'write "%s"' % line.strip()

        fp.write(line)
        fp.flush()

        time.sleep(0.1)
        num += 1

    remaining_sleep = seconds - (time.time() - start_time)
    if remaining_sleep > 0:
        time.sleep(remaining_sleep)

    fp.close()


if __name__ == '__main__':
    base_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(base_path, 'test_tmp')

    # Ensure directory exists
    if not os.path.exists(base_path):
        os.mkdir(base_path)

    if os.path.exists(os.path.join(base_path, 'test.log.1')):
        os.remove(os.path.join(base_path, 'test.log.1'))

    print 'Base Path: "%s"' % base_path

    random_write(os.path.join(base_path, 'test.log'), 'one', 10)

    os.rename(os.path.join(base_path, 'test.log'), os.path.join(base_path, 'test.log.1'))

    random_write(os.path.join(base_path, 'test.log'), 'two', 10)
