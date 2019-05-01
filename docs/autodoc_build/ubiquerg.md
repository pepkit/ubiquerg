# Package ubiquerg Documentation

## Class PeekBamResult
PeekBamResult(read_lengths, paired)


### paired
Alias for field number 1
```python
def paired(self)
```




### read\_lengths
Alias for field number 0
```python
def read_lengths(self)
```




## Class UnsupportedFiletypeException
Restrict domain of file types.


## Class defaultdict
defaultdict(default_factory[, ...]) --> dict with default factory

The default factory is called without arguments to produce
a new value when a key is not present, in __getitem__ only.
A defaultdict compares equal to a dict with the same items.
All remaining arguments are treated the same as if they were
passed to the dict constructor, including keyword arguments.


### count\_fail\_reads
Count the number of reads that failed platform/vendor quality checks.
```python
def count_fail_reads(file_name, paired_end, prog_path)
```

**Parameters:**

- `file_name` -- `str`:  name/path to file to examine
- `paired_end` -- ``:  this parameter is ignored; samtools automaticallycorrectly responds depending on the data in the bamfile; we leave the option here just for consistency, since all the other counting functions require the parameter; this makes it easier to swap counting functions during pipeline development.
- `prog_path` -- `str`:  path to main program/tool to use for the counting


**Returns:**

`int`:  count of failed reads




### count\_flag\_reads
Counts the number of reads with the specified flag.
```python
def count_flag_reads(file_name, flag, paired_end, prog_path)
```

**Parameters:**

- `file_name` -- `str`:  name/path to file to examine
- `flag` -- `str int |`:  SAM flag value to be read
- `paired_end` -- ``:  this parameter is ignored; samtools automaticallycorrectly responds depending on the data in the bamfile; we leave the option here just for consistency, since all the other counting functions require the parameter; this makes it easier to swap counting functions during pipeline development.
- `prog_path` -- `str`:  path to main program/tool to use for the counting


**Returns:**

`str`:  terminal-like text output




### count\_lines
Uses the command-line utility wc to count the number of lines in a file.

For MacOS, must strip leading whitespace from wc.
```python
def count_lines(file_name)
```

**Parameters:**

- `file_name` -- `str`:  name of file whose lines are to be counted


**Returns:**

`str`:  terminal-like text output




### count\_lines\_zip
Count number of lines in a zipped file.

This function eses the command-line utility wc to count the number of lines
in a file. For MacOS, strip leading whitespace from wc.
```python
def count_lines_zip(file_name)
```

**Parameters:**

- `file_name` -- `str`:  path to file in which to count lines


**Returns:**

`str`:  terminal-like text output




### count\_reads
Count reads in a file.

Paired-end reads count as 2 in this function.
For paired-end reads, this function assumes that the reads are split
into 2 files, so it divides line count by 2 instead of 4.
This will thus give an incorrect result if your paired-end fastq files
are in only a single file (you must divide by 2 again).
```python
def count_reads(file_name, paired_end, prog_path)
```

**Parameters:**

- `file_name` -- `str`:  Name/path of file whose reads are to be counted.
- `paired_end` -- `bool`:  Whether the file contains paired-end reads.
- `prog_path` -- `str`:  path to main program/tool to use for the counting


**Returns:**

`str`:  terminal-like text output (if input is SAM/BAM), or actualcount value (if input isn't SAM/BAM)




### get\_input\_ext
Get the extension of the input_file.

This function assumes you're using .bam, .fastq/.fq, or .fastq.gz/.fq.gz.
```python
def get_input_ext(input_file)
```

**Parameters:**

- `input_file` -- `str`:  name/path of file for which to get extension


**Returns:**

`str`:  standardized extension


**Raises:**

- `ubiquerg.ngs.UnsupportedFiletypeException`:  if the given file nameor path has an extension that's not supported




### is\_collection\_like
Determine whether an object is collection-like.
```python
def is_collection_like(c)
```

**Parameters:**

- `c` -- `object`:  Object to test as collection


**Returns:**

`bool`:  Whether the argument is a (non-string) collection




### is\_fastq
Determine whether indicated file appears to be in FASTQ format.
```python
def is_fastq(file_name)
```

**Parameters:**

- `file_name` -- `str`:  Name/path of file to check as FASTQ.


**Returns:**

`bool`:  Whether indicated file appears to be in FASTQ format, zippedor unzipped.




### is\_gzipped\_fastq
Determine whether indicated file appears to be a gzipped FASTQ.
```python
def is_gzipped_fastq(file_name)
```

**Parameters:**

- `file_name` -- `str`:  Name/path of file to check as gzipped FASTQ.


**Returns:**

`bool`:  Whether indicated file appears to be in gzipped FASTQ format.




### is\_sam\_or\_bam
Determine whether a file appears to be in a SAM format.
```python
def is_sam_or_bam(file_name)
```

**Parameters:**

- `file_name` -- `str`:  Name/path of file to check as SAM-formatted.


**Returns:**

`bool`:  Whether file appears to be SAM-formatted




### is\_unzipped\_fastq
Determine whether indicated file appears to be an unzipped FASTQ.
```python
def is_unzipped_fastq(file_name)
```

**Parameters:**

- `file_name` -- `str`:  Name/path of file to check as unzipped FASTQ.


**Returns:**

`bool`:  Whether indicated file appears to be in unzipped FASTQ format.




### namedtuple
Returns a new subclass of tuple with named fields.

>>> Point = namedtuple('Point', ['x', 'y'])
>>> Point.__doc__                   # docstring for the new class
'Point(x, y)'
>>> p = Point(11, y=22)             # instantiate with positional args or keywords
>>> p[0] + p[1]                     # indexable like a plain tuple
33
>>> x, y = p                        # unpack like a regular tuple
>>> x, y
(11, 22)
>>> p.x + p.y                       # fields also accessible by name
33
>>> d = p._asdict()                 # convert to a dictionary
>>> d['x']
11
>>> Point(**d)                      # convert from a dictionary
Point(x=11, y=22)
>>> p._replace(x=100)               # _replace() is like str.replace() but targets named fields
Point(x=100, y=22)
```python
def namedtuple(typename, field_names, *, verbose=False, rename=False, module=None)
```




### peek\_read\_lengths\_and\_paired\_counts\_from\_bam
Counting read lengths and paired reads in a sample from a BAM.
```python
def peek_read_lengths_and_paired_counts_from_bam(bam, sample_size)
```

**Parameters:**

- `bam` -- `str`:  path to BAM file to examine
- `sample_size` -- `int`:  number of reads to look at for estimation


**Returns:**

`defaultdict[int, int], int`:  read length observation counts, andnumber of paired reads observed


**Raises:**

- `OSError`: 




### samtools\_view
Run samtools view, with flexible parameters and post-processing.

This is used to implement the various read counting functions.
```python
def samtools_view(file_name, param, prog_path, postpend='')
```

**Parameters:**

- `file_name` -- `str`:  name/path of reads tile to use
- `param` -- `str`:  String of parameters to pass to samtools view
- `prog_path` -- `str`:  path to the samtools program
- `postpend` -- `str`:  String to append to the samtools command;useful to add cut, sort, wc operations to the samtools view output.


**Returns:**

`str`:  terminal-like text output



