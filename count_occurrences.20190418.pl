#!/usr/bin/perl

use strict;
use Getopt::Long;
use warnings;

### Description:  Counts all the frequencies of a string (or an n-mer/k-mer) in a given field
### usage:  cat the file thru the script, designating -f the field to look at for n-mers (or STRINGS) and -n the freq (with count) above which to output.


my ($verbose);
my ($field) = ('');
my ($freq) = ('0');  ### default value

unless (GetOptions("verbose:i"  => \$verbose,
		"f|field=n"   => \$field,
		"n|freq=n"   => \$freq,  ### cutoff of frequency, ABOVE which to output (i.e., >, gt). So can only see frequent strings/seqs, if desired
		  )) {die "GetOptions error\n";}

unless ($field) {die "Must supply --field, 1-based \n";}

if (defined $verbose and not $verbose) {$verbose = 1;}

my %hash;
my $count1=0;
my $count2=0;


while (my $input_line = <STDIN>) {
    
    $count2++;
    if ($input_line =~ /^\#/) {
        #print "skip\t$input_line";
    	next;}
  	chomp $input_line;
    my @F = split(/\t/, $input_line);

    $count1++;   #### debug/info  - counting the total number of lines processed

    my $count_field = ($field -1);
	#print $F[$count_field],"\n";
    ### add to hash:
    my ($key, $value) = split /\s+/, "$F[$count_field] 1";
    $hash{$key}++;
                    #    print "$key running total: $hash{$key} \n";   #### debug
    }


### done building hash; now output results
### print "===================\n";  #### debug
print "$count1 non-hash lines processed out of $count2\n";
#print "$count2 valid nmers counted - correct case and non-N\n";
foreach my $key (sort keys %hash) {
    #    print "$key appears $hash{$key} times\n";   #### debug
    print "$key\t$hash{$key}\n" if $hash{$key} > $freq;
	
}
