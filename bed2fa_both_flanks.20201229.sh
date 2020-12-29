#! /bin/sh

# This script pulls a target sequence from a (2bit-indexed) genome, with flanks, so it can (for example) be re-mapped to a new genome by alignment.

# $1 is a bed file to analyse and extract positions to feed to twoBitToFa
# $2 is the org (so that we can create the correct path to the 2bit files)
# $3 is the amount of flanking sequence to add .... to the 5' side
# $4 is the amount of flanking sequence to add to the 3' side
# Output is a tab-delimited file that can easily be converted to fastA

org=$2

### remove existing commas, then tabs to commas, spaces to underscores:
cat $1 | tr -d '\054' | tr '\011' '\054' | tr '\040' '\137' > $1.tmp.csv

for i in $(cat $1.tmp.csv); do
	ID=`echo $i | cut -f4 -d','`
	chr=`echo $i | cut -f1 -d','`
	Tstart=`echo $i | cut -f2 -d','`
	Tstop=`echo $i | cut -f3 -d','`
	alt=`echo $i | cut -f4 -d',' | cut -f1 -d'|'`     #### putting the desired ALT allele into the first "|" delimited field of the ID

#	echo $chr $Tstart $Tstop $ID

	echo $chr $Tstart $Tstop $ID | perl -e 'while ($line=<STDIN>){chomp $line; @F=split/\ /,$line; print $F[0],":",($F[1]-'$3'),"-",$F[1],"\n"}' > tmp.2bitTofa.instr
	~/bin/UCSC.bin1/twoBitToFa -noMask -seqList=tmp.2bitTofa.instr ~/designer_data_resource.dir/$org/2bit_data.dir/$org.2bit 2bit.OUT
	left_flank=`cat 2bit.OUT | tail -n +2 | tr -d '\012'`
#	echo $left_flank

	rm 2bit.OUT.target
	echo $chr $Tstart $Tstop $ID | perl -e 'while ($line=<STDIN>){chomp $line; @F=split/\ /,$line; print $F[0],":",($F[1]),"-",$F[2],"\n"}' > tmp.2bitTofa.instr
	~/bin/UCSC.bin1/twoBitToFa -noMask -seqList=tmp.2bitTofa.instr ~/designer_data_resource.dir/$org/2bit_data.dir/$org.2bit 2bit.OUT.target
	if [ -s 2bit.OUT.target ]
	then
	 	target_seq=`cat 2bit.OUT.target | tail -n +2 | tr -d '\012'`
	else
		target_seq="-"
	fi



	echo $chr $Tstart $Tstop $ID | perl -e 'while ($line=<STDIN>){chomp $line; @F=split/\ /,$line; print $F[0],":",$F[2],"-",($F[2]+'$4'),"\n"}' > tmp.2bitTofa.instr
	~/bin/UCSC.bin1/twoBitToFa -noMask -seqList=tmp.2bitTofa.instr ~/designer_data_resource.dir/$org/2bit_data.dir/$org.2bit 2bit.OUT
	right_flank=`cat 2bit.OUT | tail -n +2 | tr -d '\012'`
#	echo $right_flank

echo $chr $Tstart $Tstop $ID $left_flank $target_seq "ALT-"$alt $right_flank

done



