#!/usr/bin/python
#/usr/env/bin python
# file **filename**.py
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

from sys import argv
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from os.path import exists, isfile
import sys

def add(x, y):
    """Add Function"""
    return x + y


def workflow(verbose, fh):
    """description of workflow
    
    :param <parameter name>: <parameter description>
    :type <parameter name>: <parameter type>
    :returns: <what function returns>
    """
    if verbose:
        print "The addition function: ",(add(2,2))

    linecount=-1
    for line in fh:
        linecount += 1
        line = line.strip('\n')
        l0 = line.split('\t')

        #seqfield = 0
        if linecount == 0:
            fieldcount = -1
            for field in l0:
                fieldcount+= 1
                if "id" in field:
                    idfield = fieldcount
                if "seq" in field:
                    seqfield = fieldcount
                if "tm_p3" in field:
                    tmp3field = fieldcount
                if "kolmogorov" in field:
                    kolfield = fieldcount

            if verbose:
                print "found id in field:", idfield
                print "found seq in field:", seqfield
                print "found tm_p3 in field:", tmp3field
                print "found kolmogorov in field:", kolfield
            print "id","seq","tm_p3","kolmogorov"

        else:

            #id = l0[0]
            print l0[idfield], l0[seqfield],l0[tmp3field], l0[kolfield]



    #raise NotImplementedError


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

    fh = None
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
        print "input FILE?:", args.file
        print "input STDIN?", args.stdin
        print "input:", fh
    else:
        verbose = False



    #Call workflow for script after parsing command line parameters.
    workflow(verbose, fh)

if __name__ == "__main__":
    main(argv)
