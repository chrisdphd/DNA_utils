#!/usr/bin/python
# generates [a number] of randomers of [a fixed length] to run thru a filter (GC%, Tm, homopolymer check), and then output the desired number of filter-passing sequences, with properties

import sys
import random
import re
from Bio.SeqUtils import MeltingTemp as melttemp
from argparse import ArgumentParser


def parseArgs():
    argparser = ArgumentParser(description='Creates RANDOMers and does some properties and filtering')
    # the arguments:
    #argparser.add_argument('-f', '--file', help='Seq file to analyse', type=str, required=False)
    #argparser.add_argument('-c', '--stdin', help='(Flag) Seqs on STDIN to analyse', action="store_true", required=False)

    argparser.add_argument('-n', '--number', help='Number of CANDIDATE randomers to create', type=int, required=True)
    argparser.add_argument('-np', '--number_pass', help='(up to) Number of PASSING-FILTERS randomers to create', type=int, required=False)
    argparser.add_argument('-l', '--length', help='Length of randomers to create', type=int, required=True)
    argparser.add_argument('-t', '--trim', help='Num bases to trim from 5 prime end before getting Tm', type=int, required=False)
    argparser.add_argument('-p', '--prefix_tail5', help='Bases to add to 5 prime end of final randomer', type=str, required=False)
    argparser.add_argument('-s', '--suffix_tail3', help='Bases to add to 3 prime end of final randomer', type=str, required=False)

    return argparser.parse_args()


def generate_randomer(N, alphabet='ACGT'):
    return ''.join([random.choice(alphabet) for i in xrange(N)])

def dna_regex(dna):
    regexp = re.compile(r'AAAA|TTTT|CCCC|GGGG')
    if regexp.search(dna):
      return 'matched'

def get_base_frequencies(dna):
    return {base: dna.count(base) / float(len(dna))
            for base in 'ATGC'}

def format_frequencies(frequencies):
    return ', '.join(['%s: %.3f' % (base, frequencies[base]) for base in frequencies])

def get_gcfreq(dna):
    return {base: dna.count(base) / float(len(dna))
            for base in 'GC'}

def format_gcpct(gc_freqs):
    cum = (sum([gc_freqs[base] for base in gc_freqs]))
    return '%.1f' % (cum * 100)

def calcTm(dnaSeq):
    tm = melttemp.Tm_NN(dnaSeq, Na = 50, Mg = 0.0, dNTPs = 0.0, saltcorr=5, dnac1=250, dnac2=0) ### for client 20180129
    return  '%.1f' % (tm)


def main():
    args = parseArgs()

    oligo_len = args.length
    num_candidates = args.number
    if args.number_pass:
        num_passed = args.number_pass
    else:
        num_passed = args.number
    passed = 0
    
    if args.trim:
        trim_5 = args.trim
    else:
        trim_5 = 0 ### i.e. just Tm the complete randomer, else, ignore 5' overhang e.g. because of client requirement

    #if args.self:
    #    self_dimer = "true"

    for i in range(0, num_candidates, 1):
        if passed < num_passed:
            dna = generate_randomer(oligo_len)
            subdna = dna[trim_5:999] ### removes bases 0,1,2 or more from start (left side, or 5 prime end). End at 999 = i.e. effectively infinite, for this purpose

            homopol = dna_regex(dna)
            gc_freqs = get_gcfreq(dna)
            gc_pct = float(format_gcpct(gc_freqs))
            tm = float(calcTm(subdna))

            print "Candidate:",dna
            ### applying tests to the randomer:
            #if (36 <= gc_pct <= 55) and (42 <= tm <= 48) and homopol is not "matched": ### client barcodes?
            if (36 <= gc_pct <= 55) and (66 <= tm <= 72) and homopol is not "matched": ### client backbones

                #frequencies = get_base_frequencies(dna)
                #base_freqs = format_frequencies(frequencies)
                randomer_length = len(dna)

                if args.prefix_tail5:
                    tail5 = args.prefix_tail5
                    dna = (tail5 + dna)
                if args.suffix_tail3:
                    tail3 = args.suffix_tail3
                    dna = (dna + tail3)
                final_length = len(dna)

                print "Pass:",i, dna, final_length, gc_pct, tm
                passed += 1



if __name__ == "__main__":
    main()
