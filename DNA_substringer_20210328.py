#!/usr/local/bin/python3

""" description
.. module:: DNA_substringer_YYYYMMDD.py
    :members:
    :platform: Linux, Unix, OS X
    :synopsis: Enumerates a set of primers (oligonucleotide substrings of a DNA sequence).....(demo version)
    (many per 3' end, so arguably not very useful, but OK as a demo)
    and filtered for percent GC, Tm and some homopolymers. DNA is input in format ID<tab>ACTGTGCATGC...etc, on 1 line.
    MUST specify --file OR --stdin for the target sequence, which is in the format: ID<tab>sequence (all on one line)
    Output to STDOUT, tab delimited, HEADER:   ID seq_length oligo oligo_length oligo_start(zero-based half open) oligo_stop percent GC Tm Tm_diff_from_optimal.
.. moduleauthor:: Author Name <chrisdphd@gmail.com>
"""

__author__ = "chris davies"
__copyright__ = "Copyright Christopher Davies, 2020"
__credits__ = ["FirstName LastName"]
__license__ = "Copyright"
__version__ = "0.1"
__maintainer__ = "chris davies"
__email__ = "chrisdphd@.gmail.com"
__status__ = "Development"

from argparse import ArgumentParser
from os.path import exists, isfile
import sys
import re
from Bio.SeqUtils import MeltingTemp as melttemp
from Bio.Seq import Seq

def dna_regex(dna):
    regexp = re.compile(r'AAAAA|TTTTT|CCCCC|GGGG|N')
    if regexp.search(dna):
      return 'matched'

def get_gcfreq(dna):
    return {base: dna.count(base) / float(len(dna))
            for base in 'gGcC'}

def format_gcpct(gc_freqs):
    cumulative = (sum([gc_freqs[base] for base in gc_freqs]))
    return '%.1f' % (cumulative * 100)


def calcTm(dnaSeq, Na, Mg, dNTPs, saltcorr, dnac1, dnac2):
    tm = melttemp.Tm_NN(dnaSeq, Na=Na, Mg=Mg, dNTPs=dNTPs, saltcorr=saltcorr, dnac1=dnac1, dnac2=dnac2)
    return  '%.1f' % (tm)


def workflow():

    # header for output:
    print('\t'.join(['ID', 'orientation', 'length', 'oligo_sequence..........', 'oligo_length', 'start', 'stop', 'GC%', 'Tm']))

    for line in fh:
        line = line.strip('\n')
        l0 = line.split('\t')
        id = l0[0]
        dnaseq = l0[1]

        if args.revcomp:
            dna_seqclassinstance = Seq(dnaseq)
            rc_dna = dna_seqclassinstance.reverse_complement()
            dnaseq = rc_dna

        dnalen = len(dnaseq)

        for stop in range(oligolenmin, dnalen+1): ### stop = the 3' end of the oligo or "stop" pos
            if args.verbose:
                print("")
                print("==== next 3p end ====")
            for length in range(oligolenmin, (oligolenmax+1)):
                start = (stop-length)
                oligo = dnaseq[start:stop]
                homopol = dna_regex(oligo)

                if args.verbose:
                    print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
                    print(stop, length, start, oligo, "homopolymer:", homopol)
                    if homopol == "matched":
                        print("Homopolymer matched; ---------- failed!")
                    if (start <0 ):
                        print("start is negative; 5' end of oligo is outside target seq!! ----- failed!")
                    end_pos = (int(dnalen) - int(stop))
                    print ("distance of 3' end of oligo (stop Position) from end of seq", end_pos)

                if start >= 0 and homopol != "matched":
                    gc_freqs = get_gcfreq(oligo)
                    gc_pct = float(format_gcpct(gc_freqs))
                    if gc_max > gc_pct > gc_min:
                        tm = float(calcTm(oligo, Na, Mg, dNTPs, saltcorr, dnac1, dnac2))
                        if args.verbose:
                            print("....", "GC in bounds:", gc_pct, "Tm,", tm)

                        if tm_max >= tm >= tm_min:
                            if args.verbose:
                                print("....", "....", "....", "....", "....", "Tm in bounds:", tm, "----------------------------------- PASSED")
                            if args.revcomp:
                                rc_start = (int(dnalen) - int(stop))
                                rc_stop = (int(dnalen) - int(start))
                                printlist = [id, '(reverse)', str(dnalen) + 'bp', oligo, length, start, stop, gc_pct, tm, "start-stop in revcomp:", rc_start, rc_stop]
                                printliststrings = [str(integer) for integer in printlist]
                                print ('\t'.join(printliststrings))
                            else:
                                print('\t'.join([id, '(forward)', str(dnalen) + 'bp', oligo, str(length), str(start), str(stop), str(gc_pct), str(tm)]))

                        else:
                            if args.verbose:
                                print("....", "....", "....", "....", "....", "....", "....", "Tm NOT in bounds!!  ----- failed!")
                    else:
                        if args.verbose:
                            print("GC out of bounds:", gc_pct, "percent    ---------------------- failed!")



def parseArgs():
    """Parses commandline arguments.
    :param arg_list: Arguments to parse.
    :type arg_list: list.
    """
    argparser = ArgumentParser(description='Makes/enumerates/generates oligos suitable for PCR application. '
                                           'No particular filtering other than GC/Tm and homopolymer check. '
                                           'NOTE: -f OR -c MUST be specified, for input sequence')
    # the actual arguments:
    argparser.add_argument('-f', '--file', help='Seq file to analyse. Format ID<tab>ACTGTGCATGC...etc, on 1 line. '
                                                'Can handle multiple input seqs in file, each on its own line', type=str, required=False)
    argparser.add_argument('-c', '--stdin', help='(Flag) Sequences on STDIN to analyse. Format ID<tab>ACTGTGCATGC...etc, on 1 line. '
                                                 'Can handle multiple seqs, each onn its own line', action="store_true", required=False)
    argparser.add_argument('-r', '--revcomp', help='(Flag) revcomp the seq to analyse', action="store_true", required=False)
    argparser.add_argument('-v', '--verbose', help='(Flag) verbose output for errror checking', action="store_true", required=False)

    argparser.add_argument('--minlen', type=int, default=17, required=False, help="minimum acceptable oligo length.")
    argparser.add_argument('--maxlen', type=int, default=35, required=False, help='maximum acceptable oligo length')
    argparser.add_argument('--gcmin', type=int, default=20.0, required=False, help='percent GC min oligo parameter')
    argparser.add_argument('--gcmax', type=int, default=80.0, required=False, help='percent GC max oligo parameter')


    argparser.add_argument('--tmmin', type=float, dest='tm_min', default=60.0, required=False, help='Tm min oligo parameter. ')
    argparser.add_argument('--tmmax', type=float, dest='tm_max', default=70.0, required=False, help='Tm max oligo parameter')
    argparser.add_argument('--tmopt', type=float, dest='tm_opt', default=62.5, required=False, help='Tm opt oligo parameter')

    argparser.add_argument('--Na', type=int, dest='Na', default=150, required=False, help='Sodium conc for Tm calculation mM ??')
    argparser.add_argument('--Mg', type=int, dest='Mg', default=0, required=False, help='Magnesium conc for Tm calculation mM ??')
    argparser.add_argument('--dNTPs', type=int, dest='dNTPs', default=0.2, required=False, help='dNTPs conc for Tm calculation')
    argparser.add_argument('--saltcorr', type=int, dest='saltcorr', default=5, required=False, help='Salt correction method for Tm calculation mM ??')
    argparser.add_argument('--dnac1', type=int, dest='dnac1', default=1000, required=False, help='DNA 1 conc for Tm calculation')
    argparser.add_argument('--dnac2', type=int, dest='dnac2', default=250, required=False, help='DNA 2 conc for Tm calculation')

    if len(sys.argv) == 1:   # shows verbose help if no args supplied
        argparser.print_help(sys.stderr)
        sys.exit(1)

    return argparser.parse_args()


if __name__ == '__main__':

    args = parseArgs()

    # input params:
    if args.stdin:
        fh = sys.stdin
    elif args.file:
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

    # oligo params:
    oligolenmin = args.minlen
    oligolenmax = args.maxlen
    gc_min = args.gcmin
    gc_max = args.gcmax

    # Tm params:
    tm_min = args.tm_min
    tm_max = args.tm_max
    tm_opt = args.tm_opt

    # 'Nearest neighbor' Tm calculation params:
    Na = args.Na
    Mg = args.Mg
    dNTPs = args.dNTPs
    saltcorr = args.saltcorr
    dnac1 = args.dnac1
    dnac2 = args.dnac2

    # if args.verbose  ### no need for this; verbose is being accessed as args.verbose in the workflow
    # if args.revcomp  ### no need for this; revcomp is being accessed as args.revcomp in the workflow

    #workflow(fh, Na, Mg, dNTPs, saltcorr, dnac1, dnac2)
    ### don't actually need to specify the above; they are being passed through as globals, per the reassignments above
    workflow()

