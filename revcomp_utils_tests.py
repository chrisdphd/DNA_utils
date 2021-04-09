#!/usr/bin/python
# /usr/env/bin python
# file revcomp_utils_tests.py
from __future__ import division

""" description
.. module:: revcomp_utils_tests.py
    :members:  revcomp_utils
    :platform: Unix, OS X
    :synopsis: /usr/bin/python -m unittest revcomp_utils_tests | less
.. moduleauthor:: Author Name <chrisdphd@gmail.com>s
"""

__author__ = "FirstName LastName"
__copyright__ = "Copyright 2020, chrisD"
__credits__ = ["FirstName LastName"]
__license__ = "Copyright"
__version__ = "0.1"
__maintainer__ = "Christopher Davies"
__email__ = "chrisdphd@gmail.com"
__status__ = "Development"

from sys import argv
from argparse import ArgumentParser
from unittest import TestCase, main
import revcomp_utils_20210404


class TestRevcomp(TestCase):

    def test_revcomp1(self):
        self.assertEqual(revcomp_utils_20210404.revcomp1('X. atcgNnATCG'), 'CGATnNcgat .X')

    def test_revcomp2_iterable(self):
        self.assertEqual(tuple(revcomp_utils_20210404.revcomp2_iterable('XatcgNnATCGGG')),
                         (('X', 'X'), ('a', 't'), ('t', 'a'), ('c', 'g'), ('g', 'c'), ('N', 'N'), ('n', 'n'), ('A', 'T'),
                          ('T', 'A'), ('C', 'G'), ('G', 'C'), ('G', 'C'), ('G', 'C')))
        # code would retutn the revcomp: 'CCCGATnNcgatX'

    def test_revcomp2_iterable_b(self):  # just a different test for the above functon, dereferencing the input
        a_string = 'XatcgNnATCGGG'
        self.assertEqual(tuple(revcomp_utils_20210404.revcomp2_iterable(a_string)),
                         (('X', 'X'), ('a', 't'), ('t', 'a'), ('c', 'g'), ('g', 'c'), ('N', 'N'), ('n', 'n'), ('A', 'T'),
                          ('T', 'A'), ('C', 'G'), ('G', 'C'), ('G', 'C'), ('G', 'C')))

    def test_revcomp2_iterable2(self):
        self.assertEqual(tuple(revcomp_utils_20210404.revcomp2_iterable2('ACGTacgtRYMKrymkVBHDvbhd')),
                         (('A', 'T'), ('C', 'G'), ('G', 'C'), ('T', 'A'), ('a', 't'), ('c', 'g'), ('g', 'c'),
                          ('t', 'a'), ('R', 'Y'), ('Y', 'R'), ('M', 'K'), ('K', 'M'), ('r', 'y'), ('y', 'r'),
                          ('m', 'k'), ('k', 'm'), ('V', 'B'), ('B', 'V'), ('H', 'D'), ('D', 'H'), ('v', 'b'),
                          ('b', 'v'), ('h', 'd'), ('d', 'h')))
        # code would retutn the revcomp: 'hdvbHDVBmkryMKRYacgtACGT'

    def complement(self):
        self.assertEqual(revcomp_utils_20210404.complement('atcgATCGnN'), 'tagcTAGCnN')

    def test_revcomp3(self):
        self.assertEqual(revcomp_utils_20210404.revcomp3('atcgNnATCG'), 'CGATnNcgat')

    def test_revcomp4(self):
        self.assertEqual(revcomp_utils_20210404.revcomp4('atcgNnATCG'), 'CGATnNcgat')

    def test_revcomp5(self):
        self.assertEqual(revcomp_utils_20210404.revcomp5('ACGTacgtRYMKrymkVBHDvbhd'), 'hdvbHDVBmkryMKRYacgtACGT')

    def test_revcomp6(self):
        self.assertEqual(revcomp_utils_20210404.revcomp6('X. atcgNnATCG'), 'CGATnNcgat .X')


# run if called from command-line:       usr/bin/python -m unittest revcomp_utils_tests
if __name__ == "__main__":
    main(argv)
