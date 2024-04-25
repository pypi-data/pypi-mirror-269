from setuptools import setup, find_packages
import pathlib
import codecs
import os.path


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


PATH = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
readme = (PATH / "README.rst").read_text(encoding="utf-8")

setup(
    name="HoundAnalyser",
    version=get_version('HoundAnalyser/__version__.py'),
    author="Carlos Reding",
    author_email="carlos.reding@bristol.ac.uk",
    description=readme,

    # keywords=[ "raspberrypi", "camera" ],

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Programming Language :: Python :: 3",
        "Topic :: Adaptive Technologies",
    ],

    python_requires=">=3.9",
    install_requires=[
        "PyQt5",
        "matplotlib",
        "ete3 < 4",
        "pyopengl",
        "tk-tools",
        "numpy",
        "biopython",
        "openpyxl",
        "pycairo",
        "psutil"
    ],

    entry_points={
            "console_scripts": [
               "HoundAnalyser=HoundAnalyser.__main__:main",
                ],
    },

    project_urls={
        "Source": "https://gitlab.com/rc-reding/software/-/tree/main/Hound?ref_type=heads",
        "Homepage": "https://gitlab.com/rc-reding/software/-/tree/main/Hound?ref_type=heads",
        # documentation=""
        # changelog=""
    },
)
