""" NGS file utilities """

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"

__all__ = ["check_fastq"]


def check_fastq(self, input_files, output_files, paired_end):
    """
    Returns a follow sanity-check function to be run after a fastq conversion.
    Run following a command that will produce the fastq files.

    This function will make sure any input files have the same number of reads as the
    output files.
    """

    # Define a temporary function which we will return, to be called by the
    # pipeline.
    # Must define default parameters here based on the parameters passed in. This locks
    # these values in place, so that the variables will be defined when this function
    # is called without parameters as a follow function by pm.run.

    # This is AFTER merge, so if there are multiple files it means the
    # files were split into read1/read2; therefore I must divide by number
    # of files for final reads.
    def temp_func(input_files=input_files, output_files=output_files,
                  paired_end=paired_end):

        if not isinstance(input_files, list):
            input_files = [input_files]
        if not isinstance(output_files, list):
            output_files = [output_files]

        print(input_files)
        print(output_files)

        n_input_files = sum(1 if f else 0 for f in input_files)

        total_reads = sum([int(self.count_reads(input_file, paired_end))
                           for input_file in input_files])
        raw_reads = total_reads / n_input_files
        self.pm.report_result("Raw_reads", str(raw_reads))

        total_fastq_reads = sum(
            [int(self.count_reads(output_file, paired_end))
             for output_file in output_files])
        fastq_reads = total_fastq_reads / n_input_files

        self.pm.report_result("Fastq_reads", fastq_reads)
        input_ext = self.get_input_ext(input_files[0])
        # We can only assess pass filter reads in bam files with flags.
        if input_ext == ".bam":
            num_failed_filter = sum(
                [int(self.count_fail_reads(f, paired_end))
                 for f in input_files])
            pf_reads = int(raw_reads) - num_failed_filter
            self.pm.report_result("PF_reads", str(pf_reads))
        if fastq_reads != int(raw_reads):
            raise Exception("Fastq conversion error? Number of reads "
                            "doesn't match unaligned bam")

        return fastq_reads

    return temp_func
