#!/Users/cdavie/miniconda3/bin/python3
# /usr/bin/python
#/usr/env/bin python
# file **filename**.py
#from __future__ import division

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


def workflow(verbose, fh, out1, out2):
    """description of workflow
    
    :param <parameter name>: <parameter description>
    :type <parameter name>: <parameter type>
    :returns: <what function returns>
    """
    if verbose:
        print ("verbose, eh")

    for line in fh:
        line = line.strip('\n')
        l0 = line.split('\t')
        id = l0[0]
        print (id)
        #print (tmp.isnumeric())
        if id.isnumeric():
            id = int(id)
            print ("we got a number!\n")
            if (id % 2) == 0:  ### looking for remainder
                print(id,"....even\n")
                #print("{0} is Even".format(id))
                out1.write(line+"\n")
            else:
                #print("{0} is Odd".format(id))
                print(id, "....odd\n")
                out2.write(line+"\n")
        else:
            print ("Line not a numerical ID", line)


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
    argparser.add_argument('-f', '--file', help='file to analyse. Format ID<tab>ACTGTGCATGC...etc, on 1 line.', type=str, required=False)
    argparser.add_argument('-c', '--stdin', help='(Flag) info on STDIN to analyse', action="store_true", required=False)

    argparser.add_argument('-1', '--output1', help='1st output file', type=str, required=True)
    argparser.add_argument('-2', '--output2', help='2nd output file', type=str, required=True)
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
        print ("input FILE?:", args.file)
        print ("input STDIN?", args.stdin)
        print ("input:", fh)
    else:
        verbose = False

    if args.output1:
        out1 = open(args.output1, 'w+')
    if args.output2:
        out2 = open(args.output2, 'w+')


    #Call workflow for script after parsing command line parameters.
    workflow(verbose, fh, out1, out2)

if __name__ == "__main__":
    main(argv)
