""" Functions facilitating file operations """

from hashlib import md5
import os
from warnings import warn
from tarfile import open as topen

__all__ = ["checksum", "size", "filesize_to_str", "untar"]
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


def size(path, size_str=True):
    """
    Gets the size of the file or directory in the provided path

    :param str path: path to the file to check size of
    :param bool size_str: whether the size should be converted to a human-readable string, e.g. convert B to MB
    :return int|str: file size or file size string
    """
    if os.path.isfile(path):
        s = os.path.getsize(path)
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
    return filesize_to_str(s) if size_str else s


def filesize_to_str(size):
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
    warn("size argument was neither an int nor a float, returning the original object")
    return size


def untar(src, dst):
    """
    Unpack a path to a target folder. All the required directories will be created

    :param str src: path to unpack
    :param str dst: path to output folder
    """
    with topen(src) as tf:
        tf.extractall(path=dst)
