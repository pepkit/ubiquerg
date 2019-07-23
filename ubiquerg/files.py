""" Functions facilitating file operations """

from hashlib import md5
import os

__all__ = ["checksum", "size"]
FILE_SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']


def checksum(path, blocksize=int(2e+9)):
    """
    Generate a md5 checksum for the file contents in the provided path.

    :param str path: path to file for which to generate checksum
    :param int blocksize: number of bytes to read per iteration, default: 2GB
    :return str: checksum hash
    """
    m = md5()
    with open(path, 'rb') as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def size(path):
    """
    Gets the size of the file or directory in the provided path

    :param str path: path to the file to check size of
    :return int: file size
    """
    def _size_str(size):
        """
        Converts the numeric bytes to the size string

        :param int|float size: file size to convert
        :return str: file size string
        """
        if isinstance(size, (int, float)):
            for unit in FILE_SIZE_UNITS:
                if size < 1024:
                    return "{}{}".format(round(size, 1), unit)
                size /= 1024
        return size

    if os.path.isfile(path):
        s = _size_str(os.path.getsize(path))
    elif os.path.isdir(path):
        s = 0
        symlinks = []
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    s += os.path.getsize(fp)
                else:
                    s += os.lstat(fp).st_size
                    symlinks.append(fp)
        if len(symlinks) > 0:
            print("{} symlinks were found: '{}'".format(len(symlinks), "\n".join(symlinks)))
    else:
        print("size could not be determined for: '{}'".format(path))
        s = None
    return _size_str(s)
