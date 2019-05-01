""" NGS file utilities """

from collections import defaultdict, namedtuple
import os
import subprocess

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


PeekBamResult = namedtuple("PeekBamResult", ["read_lengths", "paired"])


def count_fail_reads(file_name, paired_end, prog_path):
    """
    Count the number of reads that failed platform/vendor quality checks.

    :param str file_name: name/path to file to examine
    :param paired_end: this parameter is ignored; samtools automatically
        correctly responds depending on the data in the bamfile; we leave the
        option here just for consistency, since all the other counting
        functions require the parameter; this makes it easier to swap counting
        functions during pipeline development.
    :param str prog_path: path to main program/tool to use for the counting
    :return int: count of failed reads
    """
    return int(count_flag_reads(file_name, 512, paired_end, prog_path))


def count_flag_reads(file_name, flag, paired_end, prog_path):
    """
    Counts the number of reads with the specified flag.

    :param str file_name: name/path to file to examine
    :param str int | flag: SAM flag value to be read
    :param paired_end: this parameter is ignored; samtools automatically
        correctly responds depending on the data in the bamfile; we leave the
        option here just for consistency, since all the other counting
        functions require the parameter; this makes it easier to swap counting
        functions during pipeline development.
    :param str prog_path: path to main program/tool to use for the counting
    :return str: terminal-like text output
    """

    param = " -c -f" + str(flag)
    if file_name.endswith("sam"):
        param += " -S"
    return samtools_view(file_name, param=param, prog_path=prog_path)


def count_lines(file_name):
    """
    Uses the command-line utility wc to count the number of lines in a file.

    For MacOS, must strip leading whitespace from wc.

    :param str file_name: name of file whose lines are to be counted
    :return str: terminal-like text output
    """
    cmd = "wc -l " + file_name + " | sed -E 's/^[[:space:]]+//' | cut -f1 -d' '"
    return subprocess.check_output(cmd, shell=True).decode().strip()


def count_lines_zip(file_name):
    """
    Count number of lines in a zipped file.

    This function eses the command-line utility wc to count the number of lines
    in a file. For MacOS, strip leading whitespace from wc.

    :param str file_name: path to file in which to count lines
    :return str: terminal-like text output
    """
    cmd = "gunzip -c " + file_name + " | wc -l | sed -E 's/^[[:space:]]+//' | cut -f1 -d' '"
    return subprocess.check_output(cmd, shell=True).decode().strip()


def count_reads(file_name, paired_end, prog_path):
    """
    Count reads in a file.

    Paired-end reads count as 2 in this function.
    For paired-end reads, this function assumes that the reads are split
    into 2 files, so it divides line count by 2 instead of 4.
    This will thus give an incorrect result if your paired-end fastq files
    are in only a single file (you must divide by 2 again).

    :param str file_name: Name/path of file whose reads are to be counted.
    :param bool paired_end: Whether the file contains paired-end reads.
    :param str prog_path: path to main program/tool to use for the counting
    :return str: terminal-like text output (if input is SAM/BAM), or actual
        count value (if input isn't SAM/BAM)
    """

    _, ext = os.path.splitext(file_name)
    if not (is_sam_or_bam(file_name) or is_fastq(file_name)):
        # TODO: make this an exception and force caller to handle that
        # rather than relying on knowledge of possibility of negative value.
        return -1

    if is_sam_or_bam(file_name):
        param_text = "-c" if ext == ".bam" else "-c -S"
        return samtools_view(file_name, param=param_text, prog_path=prog_path)
    else:
        num_lines = count_lines_zip(file_name) \
                if is_gzipped_fastq(file_name) \
                else count_lines(file_name)
        divisor = 2 if paired_end else 4
        return int(num_lines) / divisor


def get_input_ext(input_file):
    """
    Get the extension of the input_file.

    This function assumes you're using .bam, .fastq/.fq, or .fastq.gz/.fq.gz.

    :param str input_file: name/path of file for which to get extension
    :return str: standardized extension
    :raise ubiquerg.ngs.UnsupportedFiletypeException: if the given file name
        or path has an extension that's not supported
    """
    if input_file.endswith(".bam"):
        return ".bam"
    elif input_file.endswith(".fastq.gz") or input_file.endswith(".fq.gz"):
        return ".fastq.gz"
    elif input_file.endswith(".fastq") or input_file.endswith(".fq"):
        return ".fastq"
    errmsg = "'{}'; this pipeline can only deal with .bam, .fastq, " \
             "or .fastq.gz files".format(input_file)
    raise UnsupportedFiletypeException(errmsg)


def is_fastq(file_name):
    """
    Determine whether indicated file appears to be in FASTQ format.

    :param str file_name: Name/path of file to check as FASTQ.
    :return bool: Whether indicated file appears to be in FASTQ format, zipped
        or unzipped.
    """
    return is_unzipped_fastq(file_name) or is_gzipped_fastq(file_name)


def is_gzipped_fastq(file_name):
    """
    Determine whether indicated file appears to be a gzipped FASTQ.

    :param str file_name: Name/path of file to check as gzipped FASTQ.
    :return bool: Whether indicated file appears to be in gzipped FASTQ format.
    """
    _, ext = os.path.splitext(file_name)
    return file_name.endswith(".fastq.gz") or file_name.endswith(".fq.gz")


def is_sam_or_bam(file_name):
    """
    Determine whether a file appears to be in a SAM format.

    :param str file_name: Name/path of file to check as SAM-formatted.
    :return bool: Whether file appears to be SAM-formatted
    """
    _, ext = os.path.splitext(file_name)
    return ext in [".bam", ".sam"]


def is_unzipped_fastq(file_name):
    """
    Determine whether indicated file appears to be an unzipped FASTQ.

    :param str file_name: Name/path of file to check as unzipped FASTQ.
    :return bool: Whether indicated file appears to be in unzipped FASTQ format.
    """
    _, ext = os.path.splitext(file_name)
    return ext in [".fastq", ".fq"]


def peek_read_lengths_and_paired_counts_from_bam(bam, sample_size):
    """
    Counting read lengths and paired reads in a sample from a BAM.

    :param str bam: path to BAM file to examine
    :param int sample_size: number of reads to look at for estimation
    :return defaultdict[int, int], int: read length observation counts, and
        number of paired reads observed
    :raise OSError:
    """
    try:
        p = subprocess.Popen(['samtools', 'view', bam], stdout=subprocess.PIPE)
        # Count paired alignments
        paired = 0
        read_lengths = defaultdict(int)
        for _ in range(sample_size):
            line = p.stdout.readline().decode().split("\t")
            flag = int(line[1])
            read_lengths[len(line[9])] += 1
            if 1 & flag:  # check decimal flag contains 1 (paired)
                paired += 1
        p.kill()
    except OSError:
        reason = "Note (samtools not in path): For NGS inputs, " \
                 "pep needs samtools to auto-populate " \
                 "'read_length' and 'read_type' attributes; " \
                 "these attributes were not populated."
        raise OSError(reason)

    return PeekBamResult(read_lengths, paired)


def samtools_view(file_name, param, prog_path, postpend=""):
    """
    Run samtools view, with flexible parameters and post-processing.

    This is used to implement the various read counting functions.

    :param str file_name: name/path of reads tile to use
    :param str param: String of parameters to pass to samtools view
    :param str prog_path: path to the samtools program
    :param str postpend: String to append to the samtools command;
        useful to add cut, sort, wc operations to the samtools view output.
    :return str: terminal-like text output
    """
    cmd = "{prog} view {opts} {f} {extra}".format(
            prog=prog_path, opts=param, f=file_name, extra=postpend)
    # in python 3, check_output returns a byte string which causes issues.
    # with python 3.6 we could use argument: "encoding='UTF-8'""
    return subprocess.check_output(cmd, shell=True).decode().strip()


class UnsupportedFiletypeException(Exception):
    """ Restrict domain of file types. """
    # Use superclass ctor to allow file name/path or extension to pass
    # through as the message for why this error is occurring.
    pass
