#!/usr/bin/python
from __future__ import division

from string import maketrans
from Bio.Seq import Seq

""" description
.. module:: revcomp_utils_YYYYMMDD.py
    :members:
    :platform: Unix, OS X
    :synopsis: **synopsis here**
.. moduleauthor:: Author Name <chrisdphd@gmail.com>
"""

__author__ = "Christopher Davies"
__copyright__ = "Copyright 2020, chrisD"
__credits__ = ["FirstName LastName"]
__license__ = "Copyright"
__version__ = "0.1"
__maintainer__ = "FirstName LastName"
__email__ = "chrisdphd@gmail.com"
__status__ = "Development"


def revcomp1(dnaseq):
    dnaseq = list(dnaseq)
    nuc_count = len(dnaseq)
    for index in xrange(nuc_count):
        if dnaseq[index] == 'a':
            dnaseq[index] = 't'
        elif dnaseq[index] == 'A':
            dnaseq[index] = 'T'
        elif dnaseq[index] == 'c':
            dnaseq[index] = 'g'
        elif dnaseq[index] == 'C':
            dnaseq[index] = 'G'
        elif dnaseq[index] == 'g':
            dnaseq[index] = 'c'
        elif dnaseq[index] == 'G':
            dnaseq[index] = 'C'
        elif dnaseq[index] == 't':
            dnaseq[index] = 'a'
        elif dnaseq[index] == 'T':
            dnaseq[index] = 'A'
        # Ns passed thru unchanged
    return ''.join(reversed(dnaseq))


def revcomp2_iterable(iterable):
    for line in iterable:
        line = line.strip('\n')
        l0 = line.split('\t')
        # print "the input, from iterable:", l0  # debug
        sequence = list(l0[0])
        nucleotide_count = len(sequence)
        for index in xrange(nucleotide_count):
            if sequence[index] == 'a':
                sequence[index] = 't'
            elif sequence[index] == 'A':
                sequence[index] = 'T'
            elif sequence[index] == 't':
                sequence[index] = 'a'
            elif sequence[index] == 'T':
                sequence[index] = 'A'
            elif sequence[index] == 'C':
                sequence[index] = 'G'
            elif sequence[index] == 'c':
                sequence[index] = 'g'
            elif sequence[index] == 'G':
                sequence[index] = 'C'
            elif sequence[index] == 'g':
                sequence[index] = 'c'
            # N,.,-,spaces passed thru unchanged
        yield l0[0], ''.join(reversed(sequence))   # so, actually a generator?


def revcomp2_iterable2(iterable):
    for x in iterable:
        x = x.strip('\n')
        y = x.translate(maketrans('ACGTacgtRYMKrymkVBHDvbhd', 'TGCAtgcaYRKMyrkmBVDHbvdh'))[::-1]
        yield(x, y)


def complement(s):
    basecomplement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'a': 't', 'c': 'g', 'g': 'c', 't': 'a', 'N': 'N', 'n': 'n'}
    letters = list(s)
    letters = [basecomplement[base] for base in letters]
    return ''.join(letters)


def revcomp3(s):
    return complement(s[::-1])


def revcomp4(s):
    return ''.join([{'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'a': 't', 'c': 'g', 'g': 'c', 't': 'a', 'N': 'N', 'n': 'n'}[B] for B in s][::-1])


def revcomp5(seq):  # full IUPAC
    return seq.translate(maketrans('ACGTacgtRYMKrymkVBHDvbhd', 'TGCAtgcaYRKMyrkmBVDHbvdh'))[::-1]


def revcomp6(seq):
    dna_seqclassinstance = Seq(seq)
    rc_seq = dna_seqclassinstance.reverse_complement()
    return rc_seq
