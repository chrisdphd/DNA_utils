#!/usr/local/bin/python3

""" description
.. module:: count_kmers_YYYYMMDD.py
    :members:
    :platform: linux, Unix, OS X
    :synopsis: Make a kmer frequency table for a piece of DNA (e.g a chromosome or a prokaryotic genome)
.. moduleauthor:: Author Name <chrisdphd@gmail.com>
"""

__author__ = "Christopher Davies"
__copyright__ = "Copyright 2020, ChrisD"
__credits__ = ["FirstName LastName"]
__license__ = "Copyright"
__version__ = "0.1"
__maintainer__ = "Christopher Davies"
__email__ = "chrisdphd@gmail.com"
__status__ = "Development"

from sys import argv
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from os.path import exists, isfile
from collections import defaultdict
import sys

def workflow(verbose, fh, kmersize, report):
    """description of workflow
    
    :param <parameter name>: <parameter description>
    :type <parameter name>: <parameter type>
    :returns: <what function returns>
    """
    if verbose:
        print ("verbose, eh")

    kmerdict = defaultdict(int)
    all_bases = True
    uc_bases = False   ### only use uppercase kmers (heterochromatin)
    lc_bases = False   ### only use lowercase kmersw (euchromatin/repeatmasked)
    output_uppercase = True

    for line in fh:
        line = line.strip('\n')
        linelen = len(line)
        for i in range(0, (linelen - kmersize), 1):
            kmer = line[i:(i+kmersize)]
            if 'N' in kmer:
                continue
            if all_bases:
                kmer = kmer.upper()
            elif lc_bases:
                if ('A' in kmer) or ('C' in kmer) or ('G' in kmer) or ('T' in kmer):
                    continue
            elif uc_bases:
                if ('a' in kmer) or ('c' in kmer) or ('g' in kmer) or ('t' in kmer):
                    continue
            else:
                pass

            if verbose:
                print(kmer)
            kmerdict[kmer] += 1

    #print (kmerdict)
    for kmer in kmerdict:
        ct = kmerdict[kmer]
        if ct >= report:
            if output_uppercase:
                print(kmer.upper() + '\t' + str(ct))
            else:
                print (kmer + '\t' + str(ct))  ### native case


def parseCmdlineParams(arg_list=argv):
    """Parses commandline arguments.
    
    :param arg_list: Arguments to parse. Default is argv when called from the
    command-line.
    :type arg_list: list.
    """
    #Create instance of ArgumentParser
    argparser = ArgumentParser(formatter_class=\
        ArgumentDefaultsHelpFormatter, description='Makes/enumerates/generates oligos suitable for SNAIL application')
    #argparser = ArgumentParser(description='Makes/enumerates/generates oligos suitable for PCR application')
    # the arguments:
    #Script arguments.  Use:
    # argparser.add_argument('--argument',help='help string')
    argparser.add_argument('-f', '--file', help='file to analyse, one seq per line', type=str, required=False)
    argparser.add_argument('-c', '--stdin', help='(Flag) seq on STDIN to analyse', action="store_true", required=False)
    argparser.add_argument('-k', '--kmer_size', help='kmer size to find', required=False, type=int, default=14)
    argparser.add_argument('-r', '--report', help='Only report counts gt/eq this freQuency ', required=False, type=int, default=1)
    argparser.add_argument('-v', '--verbose', help='(Flag) verbose output for errror checking', action="store_true", required=False)


    return argparser.parse_args()

def main(args,args_parsed=None):
    
    #If parsed arguments is passed in, do not parse command-line arguments
    if args_parsed is not None:
        args = args_parsed
    #Else, parse arguments from command-line
    else:
        args = parseCmdlineParams(args)

    if args.stdin:
        fh = sys.stdin
    elif args.file:   ### the input file
        filename = args.file
        if not exists(filename):
            sys.stderr.write('ERROR: file {} does not exist'.format(filename))
            exit(1)
        if not isfile(filename):
            sys.stderr.write('ERROR: file {} is not a file'.format(filename))
            exit(1)
        fh = open(filename, 'r')
    else:
        raise Exception("INPUT source not specified as -c or -f")

    kmersize = args.kmer_size
    report = args.report  ## (to filter out low counts)

    if args.verbose:
        verbose = True
        print ("input FILE?:", args.file)
        print ("input STDIN?", args.stdin)
        print ("input:", fh)
    else:
        verbose = False

    workflow(verbose, fh, kmersize, report)

if __name__ == "__main__":
    main(argv)
