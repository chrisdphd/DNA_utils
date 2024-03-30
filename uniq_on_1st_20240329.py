#! /usr/local/bin/python3
# file uniq_on_1st.py

""" description
.. module:: uniq_on_1st.py
    :members:
    :platform: Unix, OS X
    :synopsis: ** example:   cat ~/resource/keep_me_here.tmp1.tsv | ~/bin/templates.skeletons.dir/uniq_on_1st.py -c -t 3 | sort -k4,4n | less  ### looking at primer length
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


def workflow(verbose, fh, list_of_fields):
    """
    prints lines with FIRST instance of whatever value(s) in the designated field(s); passes over subsequent lines
    :param verbose:
    :param fh: input file
    :param field: the zero-based field to process
    :param out1: output file
    :return: returns output dictionary back to main to send on to either stdout orr file
    NOTE, to use less memory, could just keep a uniq list or set (or val-blank dict), and output the lines on the fly if not in the collection
    """
    if verbose:
        print("verbose...\n")

    line_dict = {}

    for line in fh:
        if line.startswith('id'):
            continue  #(not break or pass)
        else:
            line = line.strip('\n')
            l0 = line.split('\t')
            the_tuple = ()
            for field in list_of_fields:
                the_tuple = the_tuple + (l0[int(field)],)
            if verbose:
                print('the tuple', the_tuple)
            if the_tuple in line_dict:
                continue
            else:
                line_dict[the_tuple] = line   ### as noted above, could simply print full line here to save memory

    return line_dict



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
    #argparser.add_argument('-t', '--field', help='field number to process, 0-based', type=str, required=True) ### deprecated
    argparser.add_argument('-t', '--list_of_fields', nargs='+', help='<Required> the fields to uniq-on-first on. (ZERO-based). Using "t" cos gnu sort does', required=True)
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

    #field = args.field
    list_of_fields = args.list_of_fields

    if args.output1:
        out1 = open(args.output1, 'w+')
    else: out1 = sys.stdout

    if args.verbose:
        verbose = True
        print("input FILE?:", args.file)
        print("input STDIN?", args.stdin)
        print("input:", fh, "\n")
    else:
        verbose = False

    #Call workflow for script after parsing command line parameters.
    line_dict = workflow(verbose, fh, list_of_fields)

    for entry in line_dict:
        out1.write(line_dict[entry] + '\n')


if __name__ == "__main__":
    main(argv)
