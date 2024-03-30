#! /usr/local/bin/python3
# file **skeleton**.py

""" description
.. module:: **filename**.py
    :members:
    :platform: Unix, OS X
    :synopsis: ** example:   ~/bin/templates.skeletons.dir/skeleton_full_w_IO_20240328.py -f ~/resource/keep_me_here.tmp1.1.tsv -1 out1 -v | less  #(version with a dup line)
    similar to: cat ~/resource/keep_me_here.tmp1.tsv | tail -n+2 | cut -f20 | perl -lane 'print $F[0],"\t==>\t",(sprintf "%.1f", $F[0]),"\n"' | less
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


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def is_numeric(maybe_a_string):
    try:
        int(maybe_a_string)
        return True
    except ValueError:
        return False


def rounding_function(verbose, number):
    """
    A few examples of rounding a number
    :param verbose: be verbose
    :param number: a string or a float or an int, hopefully
    :return: the input, '==>', and a list of rounded numbers
    """
    if verbose:
        print('verbose again')
    tmp1 = number
    rounded1 = round(tmp1, 1)  # rounds to 1 decimal places
    rounded2 = '%.1f' % tmp1  # ROUNDS to 1 decimal places
    rounded3 = '%.2g' % tmp1  ## 2 SIGNIFICANT figures, will return 1.2e+04
    ### other formats:
    # rounded = '%.2f' % (tmp1)
    # rounded = '%.2f' % (tmp1,)
    # rounded = "{0:.2f}".format(tmp1)
    rounded4 = ("{0:.3g}".format(tmp1)) # 3 sig figures. will return 1.23e+04
    rounded5 = '{:f}'.format(tmp1) # rounds to 6 decimal places
    #rounded4 = f'{tmp1:.20f}'
    #print ("\nROUNDED:", rounded1, rounded2, rounded3, rounded4, rounded5)
    #print("**************************\n")

    return (number, '==>', rounded1, rounded2, rounded3, rounded4, rounded5)


def workflow(verbose, fh, out1):
    """
    the skeleton workflow
    :param verbose:
    :param fh: input file
    :param out1: output file
    :return: sends output to both stdout and file
    """
    if verbose:
        print("verbose, eh?\n")

    for line in fh:
        if line.startswith('id'):
            continue  #(not break or pass)
        else:
            line = line.strip('\n')
            l0 = line.split('\t')
            kolmog = l0[19]
            if is_numeric(float(kolmog)):
                #print("kolmog-score", kolmog)
                result = rounding_function(verbose, float(kolmog))
                printliststrings = [str(num) for num in result]
                print('\t'.join(printliststrings))
                out1.write('\t'.join(printliststrings) + '\n')
            else:
                eprint("WARNING: field is not a digit/numerical ID:", "\t", line)




def parseCmdlineParams(arg_list=argv):
    """Parses command line arguments.
    :param arg_list: Arguments to parse. Default is argv when called from the command line.
    :type arg_list: list.
    """
    #Create instance of ArgumentParser
    argparser = ArgumentParser(formatter_class=\
        ArgumentDefaultsHelpFormatter, description='skeleton for <tab delimited> input, then text process, then output to 2 files and STDOUT')

    argparser.add_argument('-f', '--file', help='file to analyse. If -f or -c unset, uses the default test file', type=str, required=False, default='/Users/cdavie/resource/demo_data.dir/odd-even.ids.txt')
    argparser.add_argument('-c', '--stdin', help='(Flag) info on STDIN to analyse', action="store_true", required=False)
    argparser.add_argument('-1', '--output1', help='1st output file', type=str, required=False)
    argparser.add_argument('-v', '--verbose', help='(Flag) verbose output for errror checking', action="store_true", required=False)

    return argparser.parse_args()



def main(args,args_parsed=None):

    if args_parsed is not None:   #If parsed arguments are passed in, do not parse command line arguments
        args = args_parsed
    else:                         #Else, parse arguments from command line
        args = parseCmdlineParams(args)

    if args.stdin:
        fh = sys.stdin
    elif args.file:   ### the input file
        filename = args.file
        if not exists(filename):
            sys.stderr.write('ERROR: file {} does not exist\n'.format(filename))
            exit(1)
        if not isfile(filename):
            sys.stderr.write('ERROR: file {} is not a file\n'.format(filename))
            exit(1)
        fh = open(filename, 'r')
    else:
        raise Exception("INPUT source not specified as -c or -f\n")

    if args.verbose:
        verbose = True
        print ("input FILE?:", args.file)
        print ("input STDIN?", args.stdin)
        print ("input:", fh, "\n")
    else:
        verbose = False

    if args.output1:
        out1 = open(args.output1, 'w+')
    else: out1 = sys.stdout

    #Call workflow for script after parsing command line parameters.
    workflow(verbose, fh, out1)


if __name__ == "__main__":
    main(argv)
