#!/usr/bin/python
from __future__ import division

""" description
.. module:: **filename**.py
    :members:
    :platform: Unix, OS X
    :synopsis: **synopsis here**
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

from argparse import ArgumentParser
from os.path import exists, isfile
import sys
import revcomp_utils_20210404
 
def parseArgs():
    """Parses commandline arguments.

    :param arg_list: Arguments to parse.
    :type arg_list: list.
    """
    argparser = ArgumentParser(description='demo command line tool to reverse complement DNA sequences, a few of ways. ')
    # the arguments:
    argparser.add_argument('-f', '--file', help='Sequences file to reverse complement', type=str, required=False)
    argparser.add_argument('-c', '--stdin', help='(Flag) Sequences on STDIN to reverse complement (not compatible with '
                                                 'iterator function)', action="store_true", required=False)
    argparser.add_argument('-c2', '--stdin2', help='(Flag) Sequences on STDIN to reverse complement (USES '
                                                 'iterator function)', action="store_true", required=False)
    argparser.add_argument('-p', '--pseq', dest='pseq', type=str,
                                help="The actual oligo sequence (pseq) to analyse, inline.", required=False)
    argparser.add_argument('-i', '--iterable', action="store_true", help='(Flag) -f FILE/STDIN input as iterable object',
                           required=False)
    argparser.add_argument('-i2', '--iterable2', action="store_true",
                           help='(Flag) -f FILE/STDIN input as iterable object', required=False)
    argparser.add_argument('-v', '--verbose', help='(Flag) some more example output, if using -p', action="store_true",
                           required=False)

    if len(sys.argv) == 1:
        argparser.print_help(sys.stderr)
        sys.exit(1)

    return argparser.parse_args()

def revcomp4(s):
    """description of revcomp4

    :param <parameter name>: <parameter description>
    :type <parameter name>: <parameter type>
    :returns:  returns reverse complemented DNA sequence, where input is strictly A,C,G,T
    """
    return ''.join([{'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}[B] for B in s][::-1])


def workflow(subseq):
    """workflow only activated in args.verbose mode. Uses a few utils in revcomp_utils, plus one local fuction and a lambda function.

     :param <parameter name>: <parameter description>
     :type <parameter name>: <parameter type>
     :returns: <returns some hardwired revcomps as text output>
     """
    print ""
    print "a few other ways, for the inline oligo:"
    print subseq
    print "Its complement: ", (revcomp_utils_20210404.complement(subseq))
    print "Its complement, reversed: ", (revcomp_utils_20210404.complement(subseq[::-1]))

    print ""
    print "revcomp3 of", subseq
    print(revcomp_utils_20210404.revcomp3(subseq))

    print ""
    print "local lambda, 1-liner"
    reversecomplement = lambda i: ''.join([{'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}[B] for B in i][::-1])
    print "input:", subseq, "    revcomp:", reversecomplement(subseq)

    print ""
    print "lambda-derived function: (revcomp method 4, local)" # using local function, see above
    print "input:", subseq, "    revcomp:", revcomp4(subseq)

    print ""
    print "hardwired:"
    print ""
    print "revcomp5 of acgtCGGGGY (using maketrans)"
    print (revcomp_utils_20210404.revcomp5("acgtCGGGGY"))

    print ""
    print "revcomp6 of ACTGAAAAAAA (using SEQ class)"
    print revcomp_utils_20210404.revcomp6("ACTGAAAAAAA")


if __name__ == '__main__':
    args = parseArgs()

    inline = args.pseq
    if inline:
        print '=== Hello, a sequence is inline on the command line, using option -p', inline
        print "revcomp:", (revcomp_utils_20210404.revcomp1(inline))   ### a single inline oligo, so no need for loop funct
        print ""

    if args.stdin:
        if args.iterable:
            print '=== Hello, a sequence is from STDIN  (...using iterable object). Key: <input_seq></t><revcomp>'
            for line in revcomp_utils_20210404.revcomp2_iterable(sys.stdin):  ### sending object, looping thru output to print
                print ("\t".join(line))
                print ""
        else:
            print '=== Hello, a sequence is on STDIN (...using non-iterable function)'
            for line in sys.stdin:   ### sending 1 line at a time to funct, so no need for an iterator/loop funct
                line = line.strip('\n')
                print "STDIN", line
                print "revcomp.......", (revcomp_utils_20210404.revcomp1(line))
                print ""

    if args.file:
        filename = args.file
        if not exists(filename):
            print('ERROR: file {} does not exist'.format(filename))
            exit(1)
        if not isfile(filename):
            print('ERROR: file {} is not a file'.format(filename))
            exit(1)
        if args.iterable:
            try:
                file_handle = open(filename, 'r')
                print '=== Hello, a sequence is from file  (...using iterable object). Key: <input_seq></t><revcomp>'
                for line in revcomp_utils_20210404.revcomp2_iterable(file_handle):  ### sending object, looping thru output to print
                    print ("\t".join(line))
                print ""
            except Exception as e:
                print('Exception occurred trying to reverse complement iterable file {}. Exception: {}'
                      .format(filename, e.message or e))
        elif args.iterable2:
            try:
                file_handle = open(filename, 'r')
                print '=== Whoa, a sequence is from FILE  (...and using iterable2 object). Key: <input_seq></t><revcomp>'
                for line in revcomp_utils_20210404.revcomp2_iterable2(file_handle):  ### sending object, looping thru output to print
                    print ("\t".join(line))
                print ""
            except Exception as e:
                print('Exception occurred trying to reverse complement iterable file {}. Exception: {}'
                      .format(filename, e.message or e))
        else:
            try:
                with open(filename, 'rb') as file_handle:
                    print '=== Hello, a sequence is from file (...using non-iterable function)'
                    for line in file_handle:   ### sending 1 line at a time to funct, so no need for an iterator/loop funct
                        line = line.strip('\n')
                        print "input", line, "revcomp non-iterable:  ", (revcomp_utils_20210404.revcomp1(line))
                    print ""
            except Exception as e:
                print('Exception occurred trying to loop thru file {}. Exception: {}'
                      .format(filename, e.message or e))

    if args.verbose and args.pseq:
        workflow(inline)