#!/bin/bash

#SBATCH --job-name=jobname
#SBATCH --partition=bahl_p
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=5gb
#SBATCH --cpus-per-task=4
#SBATCH --time=150:00:00
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

cd $SLURM_SUBMIT_DIR

netMHCpan -f RSVA_F_epicc.pep -l 8,9,10,11 -a HLA-B*44:03 -xls -xlsfile ./netMHCpan_out/HLAB4403.xls
