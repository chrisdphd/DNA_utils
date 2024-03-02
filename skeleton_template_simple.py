#!/usr/local/bin/python3

""" description
.. module:: skeleton_template_simple.py
    :members:
    :platform: Unix, OS X
    :synopsis: A simple script to use as a template to get stated. Addition function. No file I/O
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

def add(x,y):
    """Add Function"""
    return x + y

def workflow(a,b):
    """description of workflow
    
    :param <parameter name>: <parameter description>
    :type <parameter name>: <parameter type>
    :returns: <what function returns>
    """

    print(add(a,b))



def parseCmdlineParams(arg_list=argv):
    """Parses commandline arguments.
    
    :param arg_list: Arguments to parse. Default is argv when called from the
    command-line.
    :type arg_list: list.
    """
    #Create instance of ArgumentParser
    argparser = ArgumentParser(formatter_class=\
        ArgumentDefaultsHelpFormatter, description='Makes/enumerates/generates oligos suitable for SNAIL application')
    # argparser.add_argument('--argument',help='help string')
    argparser.add_argument('-1', '--int1', help='Integer 1 in math function', type=int, required=True)
    argparser.add_argument('-2', '--int2', help='Integer 2 in math function', type=int, required=True)

    return argparser.parse_args()

def main(args,args_parsed=None):
    
    #If parsed arguments is passed in, do not parse command-line arguments
    if args_parsed is not None:
        args = args_parsed
    #Else, parse arguments from command-line
    else:
        args = parseCmdlineParams(args)

    int1=args.int1
    int2=args.int2

    #Call workflow for script after parsing command line parameters.
    workflow(int1,int2)

if __name__ == "__main__":
    main(argv)
