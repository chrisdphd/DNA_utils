#! /bin/sh

fastq1=$1
fastq2=$2

### Make sure the Archer-derived fastq's have the SAME number of reads, with the same read ID's
### SORT the fastqs, in prep for read count reconciliation, for paired mapping
for i in $(ls $fastq1 $fastq2); do echo "Making txt version of " $i; awk '{printf substr($0,1,length-2);getline;printf "\t"$0;getline;getline;print "\t"$0}' $i | sort -S 8G -T. > $i.txt; done

### make the reconciled fastqs
for i in $(ls $fastq1.txt $fastq2.txt); do
	echo "";
	echo "Reconciling " $i;
	base=`echo $i | cut -f1-3 -d'_'`;
	echo "Base: " $base;
	echo $base"_R1.txt";
	echo $base"_R2.txt";
	join $fastq1.txt $fastq2.txt | awk '{print $1"\n"$2"\n+\n"$3 > "'$fastq1''.fq'"; print $1"\n"$4"\n+\n"$5 > "'$fastq2''.fq'"}';
done;

gzip *fq *fastq

