#! /Users/cdavie/miniconda3/bin/python3
### !/user/bin/env python3 -tt

"""
Module documentation.
"""
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


# Imports
import sys
from sys import argv
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from os.path import exists, isfile
import psycopg2
from configparser import ConfigParser
#import config
#import os
import time
from functools import wraps
from memory_profiler import memory_usage

from typing import Iterator, Optional
import io

# Global variables

# Class declarations

# Function declarations




def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

#@profile
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        print('Archive mode:')
        cur.execute('SHOW archive_mode')
        arch = cur.fetchone()
        print(arch)

        print('Table query1:')
        cur.execute('SELECT * FROM test_primers where seq like \'%GG\' LIMIT 5')
        result = cur.fetchall()
        print (result)

        print('Table query2:')
        cur.execute('SELECT * FROM test_primers where seq like \'%G\'')
        result = cur.fetchmany(8)
        result_list = list(result)
        for item in result_list:
            #print(item[0], item[1], item[2])
            print('\t'.join(map(str, item)))

        # close the communication with the PostgreSQL
        #### causes issues in other queries?
        # cur.close()
        # conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    #finally:
    #    if conn is not None:
    #        conn.close()
    #        print('Database connection closed.')


def copy_fromfile(filename):

    params = config()
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    # create a cursor
    cur = conn.cursor()

    ### open the csv file using python standard file I/O
    ### copy file into the table just created
    with open(filename) as f:
        #next(f)  # Skip the header row.
        ### f , <database name>, Comma-Seperated
        print("LOADING")
        cur.copy_from(f, 'test_primers6', sep=',')
        ### COMMIT Changes
        conn.commit()

    # Close connection
    conn.close()
    f.close()


def workflow(filename):

    print('Connecting to the PostgreSQL database...')
    # read connection parameters
    params = config()
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    ### OR:
    #conn = psycopg2.connect("dbname=postgres user=postgres password=TheActualPassword")

    cur = conn.cursor()
    cur.execute('SELECT * FROM test_primers where loc_3p = \'25397982\' limit 20')
    result = cur.fetchall()
    print (result)

    #cur.execute('CREATE TABLE  IF NOT EXISTS test_primers5 (loc VARCHAR(30) PRIMARY KEY, seq VARCHAR(40) NOT NULL, loc_3p VARCHAR(15))')
    cur.execute('CREATE TABLE  IF NOT EXISTS test_primers6 (loc_id VARCHAR(40), \
    sequence VARCHAR(40), n3p_end_1base_p3 VARCHAR(40), len_p3 VARCHAR(40), \
    Ns_p3 VARCHAR(40), GC_pct_p3 VARCHAR(40), Tm_p3 VARCHAR(40), self_any_th VARCHAR(40), \
    self_end_th VARCHAR(40), hairpin VARCHAR(40), quality_p3 VARCHAR(40), \
    length VARCHAR(40), strand VARCHAR(40), tm_diff VARCHAR(40), gc_pct VARCHAR(40), \
    tm VARCHAR(40), homopol_ck VARCHAR(40), dinuc_ck VARCHAR(40), lofreq_score VARCHAR(40), \
    kolmogorov VARCHAR(40), n3pGCwt VARCHAR(40))')
    conn.commit()

    copy_fromfile(filename)

    conn.close()
    print('Database connection closed.')


def parseArgs(arg_list=argv):
    """Parses commandline arguments.

    :param arg_list: Arguments to parse. Default is argv when called from the
    command-line.
    :type arg_list: list.
    """
    #Create instance of ArgumentParser
    argparser = ArgumentParser(formatter_class=\
        ArgumentDefaultsHelpFormatter, description='loads csv file to pg database')

    # the arguments:
    #Script arguments.  Use:
    # argparser.add_argument('--argument',help='help string')
    argparser.add_argument('-f', '--file', help='mRNA Seq file to analyse. Format ID<tab>ACTGTGCATGC...etc, on 1 line. '
                            'Can handle multiple input seqs in file or STDIN, each on its own line', type=str, required=False)
    argparser.add_argument('-c', '--stdin', help='(Flag) Sequences on STDIN to analyse', action="store_true", required=False)

    argparser.add_argument('-v', '--verbose', help='(Flag) verbose output for errror checking', action="store_true", required=False)

    return argparser.parse_args()


# Main body
if __name__ == '__main__':
    args = parseArgs()

    if args.verbose:
        verbose = True
    else:
        verbose = False

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
        #fh = open(filename, 'r')
        #file = filename
    else:
        raise Exception("INPUT source not specified as -c or -f")


    connect()
    workflow(filename)
    
