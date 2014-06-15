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

from asio.file import SEEK_ORIGIN_CURRENT
from asio.interfaces.posix import PosixASIO
from asio.interfaces.windows import WindowsASIO

import os


class ASIO(object):
    platform_handler = None

    @classmethod
    def get_handler(cls):
        if cls.platform_handler:
            return cls.platform_handler

        if os.name == 'nt':
            cls.platform_handler = WindowsASIO
        elif os.name == 'posix':
            cls.platform_handler = PosixASIO
        else:
            raise NotImplementedError()

        return cls.platform_handler

    @classmethod
    def open(cls, file_path, opener=True, parameters=None):
        """Open file

        :type file_path: str

        :param opener: Use FileOpener, for use with the 'with' statement
        :type opener: bool

        :rtype: BaseFile
        """
        if not parameters:
            parameters = OpenParameters()

        if opener:
            return FileOpener(file_path, parameters)

        return ASIO.get_handler().open(
            file_path,
            parameters=parameters.handlers.get(ASIO.get_handler())
        )


class OpenParameters(object):
    def __init__(self):
        self.handlers = {}

        # Update handler_parameters with defaults
        self.posix()
        self.windows()

    def posix(self, mode=None, buffering=None):
        """
        :type mode: str
        :type buffering: int
        """
        self.handlers.update({PosixASIO: {
            'mode': mode,
            'buffering': buffering
        }})

    def windows(self,
                desired_access=WindowsASIO.GenericAccess.READ,
                share_mode=WindowsASIO.ShareMode.ALL,
                creation_disposition=WindowsASIO.CreationDisposition.OPEN_EXISTING,
                flags_and_attributes=0):

        """
        :param desired_access: WindowsASIO.DesiredAccess
        :type desired_access: int

        :param share_mode: WindowsASIO.ShareMode
        :type share_mode: int

        :param creation_disposition: WindowsASIO.CreationDisposition
        :type creation_disposition: int

        :param flags_and_attributes: WindowsASIO.Attribute, WindowsASIO.Flag
        :type flags_and_attributes: int
        """

        self.handlers.update({WindowsASIO: {
            'desired_access': desired_access,
            'share_mode': share_mode,
            'creation_disposition': creation_disposition,
            'flags_and_attributes': flags_and_attributes
        }})


class FileOpener(object):
    def __init__(self, file_path, parameters=None):
        self.file_path = file_path
        self.parameters = parameters

        self.file = None

    def __enter__(self):
        self.file = ASIO.get_handler().open(
            self.file_path,
            self.parameters.handlers.get(ASIO.get_handler())
        )

        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.file:
            return

        self.file.close()
        self.file = None
