#!/bin/bash
######################################
## purpose: run netMHC pan

## requirement: local: need to have netMHCpan installed https://services.healthtech.dtu.dk/service.php?NetMHCpan-4.1
## input: Aligned protein sequence file
## parameters: HLA allele, spe by space
## output: Epitope binding prediction for each seq
## parallel: netMHCpan could take hours with large amount seqs
## to run this scripts on a server( gacrc) see scerver setup scripts

######################################

## example to run: run_netMHCpan.sh -i "input_protein_file" -l "length_of_epitope" -A "list_of_Allel(sep by space -o output")
print_usage() {
  printf "Usage: run_netMHCpan.sh -i input_protein_file -l length_of_epitope -A list_of_Allel(sep by space -o output"
}


#mkdir netMHCpan_out
## Shell script to run NetMHCpan


#####################################################
##### take command line args
#######################################################

while getopts 'i:l:A:o:' flag

do
	case "${flag}" in
        i) seq_pep=${OPTARG} ;;
        l) epitope_len=${OPTARG} ;;
        A) A_list=${OPTARG} ;;
        o) samplexls=${OPTARG} ;;
        *) echo "Invalid option: -$flag"
 #       	print_usage
  #      	exit 1 ;;
    esac
done


#####################################################
##### default paramters to run netMHCpan
#######################################################
## for multiple allele use allele supetertype
A_supertype_full=()
#A_supertype_short=(HLA-A01:01 HLA-A02:01 HLA-A03:01 HLA-A24:02 HLA-B07:02 HLA-B44:03)
A_supertype_short=(HLA-A01:01 HLA-A02:01)



## no args use default
: ${epitope_len:="8,9,10,11"}

if [ -z "$A_list" ]
then
	A_list=("${A_supertype_short[@]}")
fi

mkdir ./results
#####################################################
##### run netMHCpan command line
#######################################################

for allele in "${A_list[@]}"
do
	out=$(sed 's|[-*:]||g' <<< $allele)
	outxls="results/$out.xls"
	#input="data/$seq_pep"

	#echo "netMHCpan -f $input" -l $epitope_len -a $allele -xls -xlsfile $outxls  	##test

	netMHCpan -f $seq_pep -l $epitope_len -a $allele -xls -xlsfile $outxls
done


#####################################################
##### combine all xls file
#######################################################
#sample=$(sed 's|_al.pep||g' <<< $seq_pep)
#samplexls="$sample.xls"
#echo "$samplexls"

# echo "now do combine test"

## remove the first line of Allele info
for FILE in $(find ./results -type f -name 'HLA*xls')
do
	echo $FILE
	tail -n +2 "$FILE" > "$FILE.tmp"
	mv "$FILE.tmp" "$FILE"
done

## concatenate output from different allele with same header
awk '(NR == 1) || (FNR > 1)' ./results/HLA*xls > $samplexls
