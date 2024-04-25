from .__version__ import __version__
from .helper_func.sundry import _find_tool

# Detect SPAdes
try:
    tool = _find_tool('spades.py')
except ValueError:
    print("You need to install SPAdes genome assembler.")

# Detect BWA
try:
    tool = _find_tool('bwa')
except ValueError:
    print("You need to install Burrows-Wheeler Aligner.")

# Detect SAMtools
try:
    tool = _find_tool('samtools')
except ValueError:
    print("You need to install SAMtools.")

# Detect BLAST+ suite
try:
    tool = _find_tool('makeblastdb')
except ValueError:
    print("You need to install BLAST+ command line applications.")

# Detect MUSCLE
try:
    tool = _find_tool('muscle')
except ValueError:
    print("You need to install MUSCLE v3.8 for multiple sequence alignment.")

