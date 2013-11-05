from asio_base import BaseASIO, DEFAULT_BUFFER_SIZE, BaseFile
import os


class PosixASIO(BaseASIO):
    @classmethod
    def open(cls, file_path, parameters=None):
        """
        :type file_path: str
        :rtype: PosixFile
        """
        if not parameters:
            parameters = {}

        if not parameters.get('mode'):
            parameters.pop('mode')

        if not parameters.get('buffering'):
            parameters.pop('buffering')

        print parameters

        return PosixFile(open(file_path, *parameters))

    @classmethod
    def get_size(cls, fp):
        """
        :type fp: PosixFile
        :rtype: int
        """
        return os.path.getsize(cls.get_path(fp))

    @classmethod
    def get_path(cls, fp):
        """
        :type fp: PosixFile
        :rtype: int
        """
        return fp.file.name

    @classmethod
    def seek(cls, fp, offset, origin):
        """
        :type fp: PosixFile
        :type offset: int
        :type origin: int
        """
        fp.file.seek(offset, origin)

    @classmethod
    def read(cls, fp, buf_size=DEFAULT_BUFFER_SIZE):
        """
        :type fp: PosixFile
        :type buf_size: int
        :rtype: str
        """
        return fp.file.read(buf_size)

    @classmethod
    def close(cls, fp):
        """
        :type fp: PosixFile
        """
        fp.file.close()


class PosixFile(BaseFile):
    platform_handler = PosixASIO

    def __init__(self, file_object):
        """
        :type file_object: FileIO
        """
        self.file = file_object

    def __str__(self):
        return "<asio_posix.PosixFile file: %s>" % self.file
