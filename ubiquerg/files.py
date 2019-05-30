""" Functions facilitating file operations """

def checksum(path, blocksize=int(2e+9)):
    """
    Generates a md5 checksum for the file contents in the provided path

    :param str path: path to the file to generate checksum for
    :param int blocksize: number of bytes to read per iteration, default: 2GB
    :return str: checksum hash
    """
    m = md5()
    with open(path, "rb") as f:
        # gotta split the file into blocks since some of the archives are to big to be read and checksummed
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()