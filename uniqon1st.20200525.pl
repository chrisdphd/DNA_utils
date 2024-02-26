#!/usr/bin/perl

use strict;
use warnings;
use Getopt::Long;

use constant USAGE =><<END;

DESCRIPTION:  makes a file unique on the first instance of the column designated
SYNOPSIS:
cat file0 | template.pl --file1 <the 1st file type> --file2 <the 2nd file type> > OUTFILE   (seq_gene.md is a convenient input test file)
example:
	cat a_file.tx | ~/bin/this_script.pl -c 1 | less

OPTIONS:
--help    Prints this help.
-c or --column   (required) field to uniq on, in 1-base

AUTHOR:
cd

COPYRIGHT:
This program is free software. You may copy and redistribute it under the same terms as Perl itself.

END

my $help = 0;
my ($field) = ('');

GetOptions(
"c|column=n"   => \$field,  ## the field, in 1-base
#"2|file2=s"   => \$file2,  #string  (=n would be numeric)
"help"      => \$help,     #flag
) or die $!, USAGE;

$help and die USAGE;

#unless ($file2) {die USAGE}
### get the date and time
#$my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);

### Open file handles.
#my $FH1 = new FileHandle("$file1") || die "Could not open file \"$file1\" for reading\n";



my %rows;

while (my $line = <STDIN>) {
    my @F = split (/\t/,$line);
    my $uniq_field = $F[$field-1];

	if (defined($rows{$uniq_field})) {next}
    $rows{$uniq_field} = $line; # (else...)

	print $line;
}
