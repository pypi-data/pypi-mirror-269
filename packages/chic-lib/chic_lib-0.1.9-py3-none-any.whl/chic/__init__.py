"""
chic: A Python library for coarse-graining hybrid and inorganic frameworks.

This library provides tools for working with complex structures, allowing for
efficient analysis and manipulation of hybrid and inorganic framework materials.

Version modifications:
"23.04.24" "0.1.9", "Added radial cut-off for neighbour searching."
"""


from .structure import Structure
from .net import Net


__version__ = "0.1.9"
__author__ = "Thomas C. Nicholas"
__email__ = "thomas.nicholas@chem.ox.ac.uk"
__url__ = "https://github.com/tcnicholas/chic"


__all__ = ['Structure', 'Net']
