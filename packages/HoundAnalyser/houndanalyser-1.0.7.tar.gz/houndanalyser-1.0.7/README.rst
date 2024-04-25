HOUND
=====

Scaleable pipeline for the assembly *de novo* and analysis of bacterial
genomes. Users must provide the sequence(s) in FASTA format (for
monitoring presence of certain genes, amino acid sequence is advised),
and Hound will return mutations in the coding sequence (nucleotide),
mutations in the promoter sequence, and relative copy number. In a nice
spreadsheet.

Hound does not rely on specific databases, but it can be used with them
depending on data availability to screen through the assemblies
(i.e. ResFinder database can be used after translating the database into
amino acid sequences). Because of this wide scope, Hound does not come
with databases bundled.

The number of isolates that Hound can handle will depend on your
infrastructure, given that it does not rely on web servers. While an
off-the-shelf multi-core computer with at least 16GB can operate Hound,
disk space might be an issue depending on your use-case.

Why default to protein sequences?
---------------------------------

Hound is designed to monitor genetic changes that are associated to a
given phenotype—whether related to resistance, virulence, or ability to
metabolise soil pollutants. Synonymous mutations do not help this, so
instead Hound operates internally using amino acid sequences and only
mutations that result in a change of amino acid is reported. The
analysis of promoter regions is the only exception to this.

What do I need?
---------------

0. A computer running GNU/Linux or macOS. Windows is not currently
   supported.
1. Data. Hound currently supports short-read illumina data in FASTQ[.gz]
   format. We aim to support long-read nanopore sequence data in future
   releases.
2. The assembler `SPAdes <https://cab.spbu.ru/software/spades/>`__. Note
   that, if you use GNU/Linux, it may be already available through your
   distribution’s package manager
   (i.e. `AUR <https://aur.archlinux.org/packages/spades>`__ in Arch or
   `apt <https://packages.debian.org/search?searchon=sourcenames&keywords=spades>`__
   in Debian).
3. `SAMtools <http://www.htslib.org/>`__. Again, if you use GNU/Linux,
   it may be already available through your distribution’s package
   manager.
4. `BWA <https://bio-bwa.sourceforge.net/>`__. If you use GNU/Linux, it
   may be already available through your distribution’s package manager.
5. `Muscle v3.8 <https://drive5.com/muscle/downloads_v3.htm>`__. Newer
   versions of this software remove the ability to introduce penalties
   for gap introduction and extension. If you use GNU/Linux, it may be
   already available through your distribution’s package manager.
6. The latest
   `BLAST+ <https://blast.ncbi.nlm.nih.gov/doc/blast-help/downloadblastdata.html#blast-executables>`__
   executables. Again, If you use GNU/Linux they may already be
   available through your distribution’s package manager.
7. `Python 3.9+ <https://www.python.org/downloads/>`__. Note macOS ships
   with Python 3.8 through the XCode Command Line Tools. Hound **is NOT
   compatible** with this version since I use a new syntax introduced in
   v3.9 in a few places. Since the support for Python 3.8 ends in 2024,
   I have decided not to introduce compatibility with v3.8 (might change
   in the future).
8. Python libraries ``matplotlib``, ``ete3``, ``numpy``, ``pyqt5``, etc.
   These will be automatically installed by pip and conda.

Installation
------------

pip
~~~

::

   pip install HoundAnalyser-XXX-py3-none-any.whl 

where XXX is the version of the wheel file. Note that if you use Arch
Linux, you may need to add ``--break-system-packages``.

conda
~~~~~

::

   todo

Build wheel from source
~~~~~~~~~~~~~~~~~~~~~~~

To build Hound from scratch, first you must clone this repository with
``git clone https://gitlab.com/rc-reding/software.git``. Following this,
type ``cd software/Hound`` and then ``python -m build --wheel``. Lots of
text will be shown with progress and steps.

Once finished, install with
``pip install dist/HoundAnalyser-X.Y.Z-py3-none-any.whl`` where
``X.Y.Z`` is the version of the package (i.e. 1.0.4)

Quick Start
-----------

Help
~~~~

::

   >HoundAnalyser --help
   usage: HoundAnalyser [-h] [--preprocess FILE DIRNAME] [--project DIR] [--assemble] [--reference FILE] [--de-novo]
                        [--coverage] [--hk-genes FILE] [--genes FILE] [--genes-dir DIR] [--nucl] [--prefix NAME]
                        [--identity NUM NUM] [--promoter] [--cutoff NUM] [--phylo] [--phylo-thres NUM] [--plot FILE]
                        [--roi FILE] [--summary FILE] [--labels FILE] [--force]

   HOUND: species-independent genetic profiling system

   options:
     -h, --help            show this help message and exit
     --preprocess FILE DIRNAME
                           Unzip Illumina reads and create appropriate directory structure. It requires a name to create
                           destination directory. REQUIRED unless --project is given.
     --project DIR         Directory where FASTQ files can be found. It can be a directory of directories if FASTQ files
                           are contained in a 'reads' directory. Maximum directory depth is 2. REQUIRED unless
                           --preprocess is given.
     --assemble            Assemble reads. Requires --project.
     --reference FILE      Reference genome in FASTA format. Requires --assemble.
     --de-novo             Assemble reads de novo. Used to assemble genomes and specify assembly type for data analysis.
                           Requires --assemble.
     --coverage            Compute coverage depth to estimate gene copy number. Can be used to assemble genomes or include
                           coverage depth in the data analysis. Requires --hk-genes.
     --hk-genes FILE       List of Multilocus sequence typing (MLST) genes, or other reference genes, in FASTA format to
                           compute baseline coverage depth. Requires --coverage.
     --genes FILE          List of genes to be found, in FASTA format. Requires --identity and --prefix.
     --genes-dir DIR       Directory containing genes of interest in FASTA format. Requires --summary.
     --nucl                Use nucleotide sequences for the search. Requires --genes.
     --prefix NAME         Label added to all output files. Required to do multiple searches with the same assemblies.
     --identity NUM NUM    Identity threshold required to shortlist sequences found. Two floats (min identity, max
                           identity) between 0 and 1 are required. Requires --genes.
     --promoter            Isolate the promoter region of the target gene(s) sequences found and ignore coding sequences.
                           Requires --cutoff.
     --cutoff NUM          Length of the promoter in nucleotides. Requires --promoter.
     --phylo               Align sequences of promoter/coding sequences found, and generate the corresponding phylogeny.
     --phylo-thres NUM     Remove sequences that are a fraction of the total size of alignment. Used to improve quality
                           alignment. Requires a number between 0 and 1 (defaults to 0.5).
     --plot FILE           Generate plot from the multiple alignment of sequences found, and save as FILE.
     --roi FILE            Sequences of interest to look for in the gene(s) found, in FASTA format. Requires --plot.
     --summary FILE        Save Hound analysis as a spreadsheet. Requires --project.
     --labels FILE         XLS file containing assembly name (col 1), and assembly type (col 6) to label phylogeny leafs
                           (defaults to assembly name). Requires --plot.
     --force               Force re-generation of phylogeny and/or plot even if they already exist.

   Carlos Reding (c) Copyright 2022-2023. Software developed as part of FARM-SAFE (BBSRC grant BB/T004592/1) and Arwain
   DGC at the University of Bristol (United Kingdom).

Assembly
~~~~~~~~

Assemble FASTQ reads *de novo*, and compute genome coverage depth:

::

   HoundAnalyser --project $FOLDER --assemble --de-novo --coverage

Assemble FASTQ reads using a reference:

::

   HoundAnalyser --project $FOLDER --assemble --reference REFERENCE.fa 

Summary
~~~~~~~

To generate an EXCEL spreasheet (.xlsx) containing the results and
metadata:

::

   HoundAnalyser --summary $SPREADSHEET --genes-dir $GENES_DIR

Where ``$GENES_DIR`` is a directory containing the amino acid sequences
of interest in FASTA format (one sequence per file).

Data from `MicrobesNG <https://microbesng.com/>`__ ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Expand ``reads.zip``:

::

   HoundAnalyser --preprocess reads.zip $DIRECTORY

The result will be FASTQ[.gz] files in ``$DIRECTORY/reads`` with paired
reads, and ``$DIRECTORY/reads/unpaired`` with unpaired reads.
``$DIRECTORY`` is ready to use with Hound.
