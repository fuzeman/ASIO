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

from asio_windows import WindowsASIO, WindowsInterop

NULL = 0

if __name__ == '__main__':
    file_path = 'test_tmp/test_windows_interop.dat'

    fp = open(file_path, 'w')
    fp.write(file_path)
    fp.close()

    file_handle = WindowsInterop.create_file(
        file_path,
        WindowsASIO.GenericAccess.READ,
        WindowsASIO.ShareMode.ALL,
        WindowsASIO.CreationDisposition.OPEN_EXISTING,
        NULL
    )
    print "file_handle", file_handle

    map_handle = WindowsInterop.create_file_mapping(file_handle, WindowsASIO.Protection.READONLY)
    print "map_handle", map_handle

    view_handle = WindowsInterop.map_view_of_file(map_handle, WindowsASIO.FileMapAccess.READ, 1)
    print "map_view", view_handle

    file_name = WindowsInterop.get_mapped_file_name(view_handle)
    print file_name

    # Close
    WindowsInterop.unmap_view_of_file(view_handle)
    WindowsInterop.close_handle(map_handle)
    WindowsInterop.close_handle(file_handle)
