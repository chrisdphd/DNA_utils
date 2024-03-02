#!/usr/local/bin/python3

""" description
.. module:: count_occurrencces_YYYYMMDD.py
    :members:
    :platform: linux, Unix, OS X
    :synopsis: Count occcurences (i.e frequency count) of values in a field, and output only those (key-vals) above a certain value
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
import sys
from collections import defaultdict


def workflow(verbose, fh, field_num, num_filter):
    """description of workflow
    
    :param <parameter name>: <parameter description>
    :type <parameter name>: <parameter type>
    :returns: <what function returns>
    """
    if verbose:
        print ("verbose, eh")

    occurrence_dict = defaultdict(int)

    for line in fh:
        line = line.strip('\n')
        l0 = line.split('\t')
        field_val = l0[field_num]
        #print (field_val)
        occurrence_dict[field_val] += 1

    print('item\tcount')
    for item in sorted(occurrence_dict):
        ct = occurrence_dict[item]
        if ct >= num_filter:
            print(item + '\t' + str(ct))


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
    argparser.add_argument('-f', '--file', help='file to analyse. For this skeleton, a list of ints (odd and even), one per line', type=str, required=False)
    argparser.add_argument('-c', '--stdin', help='(Flag) info on STDIN to analyse', action="store_true", required=False)
    argparser.add_argument('-t', '--field', help='field/column (0-based) to analyse', type=int, required=True)
    argparser.add_argument('-n', '--num_filter', help='frequency/ occurrence count below which to filter out', type=int, default=False, required=False)
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

    field_num = args.field
    num_filter = args.num_filter

    if args.verbose:
        verbose = True
        print ("input FILE?:", args.file)
        print ("input STDIN?", args.stdin)
        print ("input:", fh)
    else:
        verbose = False

    workflow(verbose, fh, field_num, num_filter)

if __name__ == "__main__":
    main(argv)
