#!/usr/local/bin/python3


""" description
.. module:: find_field_headers_YYYYMMDD.py
    :members:
    :platform: Unix, OS X
    :synopsis: searches for header column names (-n), in an input datafile (-f or -c), and prints them out in the order in -n,
    example:  cat ~/resource/keep_me_here.tmp1.tab | ./find_field_headers_20210506.py -c -n seq,id,tm_p3,tm_diff | less
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


def workflow(verbose, fh, cols):
    """description of workflow
    
    :param <parameter name>: <parameter description>
    :type <parameter name>: <parameter type>
    :returns: <what function returns>
    """

    listcount = -1
    for col in cols.split(','):
        listcount += 1
        str(listcount)
        if verbose:
            print("from list", col, listcount)

    col_dict = {}

    linecount=-1
    for line in fh:
        linecount += 1
        line = line.strip('\n')
        l0 = line.split('\t')

        if linecount == 0:
            for col in cols.split(','):  # the input list that we are looking for
                fieldcount = -1
                if verbose:
                    print("looking for:", str(col))
                found = False
                for field in l0:
                    field = field.strip('\n')
                    fieldcount += 1
                    if col == field:
                        found = True
                        if verbose:
                            print("found", col, "at", fieldcount)
                        col_dict[col] = fieldcount
                if found == False:
                    sys.stderr.write('ERROR: field name not found in file...')
                    print("THIS ONE: ", col, "ERROR'd OUT!")
                    exit(1)
            if verbose:
                print(col_dict)

        else:
            printlist = []
            for col in cols.split(','):
                printlist.append(l0[col_dict.get(col)])
            print('\t'.join(printlist))


def parseCmdlineParams(arg_list=argv):
    """Parses commandline arguments.
    
    :param arg_list: Arguments to parse. Default is argv when called from the
    command-line.
    :type arg_list: list.
    """
    #Create instance of ArgumentParser
    argparser = ArgumentParser(formatter_class=\
        ArgumentDefaultsHelpFormatter, description='cat ~/resource/keep_me_here.tmp1.tab | ~/bin/templates.dir/find_field_headers.py -c -v | less')
    # Script arguments.  Use:
    # argparser.add_argument('--argument',help='help string')
    argparser.add_argument('-f', '--file', help='file to analyse. Format ID<tab>ACTGTGCATGC...etc, on 1 line.', type=str, required=False)
    argparser.add_argument('-c', '--stdin', help='(Flag) info on STDIN to analyse', action="store_true", required=False)
    argparser.add_argument('-n', '--colnames', help='a csv string (on the command line) of the column header NAMES to find, in the order desired for printout', type=str, required=True)

    argparser.add_argument('-1', '--int1', help='Integer 1 in math function', default=3, type=int, required=False)
    argparser.add_argument('-2', '--int2', help='Integer 2 in math function', default=4, type=int, required=False)
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
    elif args.file:   ### the mRNA file
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

    if args.verbose:
        verbose = True
        print("input FILE?:", args.file)
        print("input STDIN?", args.stdin)
        print("actual input:", fh)
    else:
        verbose = False


    cols = (args.colnames)
    if verbose:
        print(cols)

    #Call workflow for script after parsing command line parameters.
    workflow(verbose, fh, cols)


if __name__ == "__main__":
    main(argv)
