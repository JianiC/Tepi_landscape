#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
import numpy as np
import sys
from scipy.spatial.distance import cityblock
from progressbar import ProgressBar
import argparse


# In[16]:


def core_tcrf(core):
    core_tcrf = f'___{core[3]}{core[4]}{core[5]}{core[6]}{core[7]}_'
    return core_tcrf


# In[17]:


def seq_mandist(df_epitope,epitope_feature):
    ## get sequence ID
    
    seq = df_epitope.ID.unique()
    ## loop through all seq in seq array to calculate Manhatton distance
    pbar = ProgressBar()
    seq_distance=[]
    for i in pbar(range(len(seq))):
        for j in range(len(seq)):
            if i<j:
                distance = cityblock(epitope_feature[seq[i]], epitope_feature[seq[j]])
                seq_distance.append([seq[i], seq[j], distance])                
                #distance_df = pd.DataFrame(seq_distance, columns=["seq1", "seq2","epitope_distance"])
                    
    return seq_distance


# In[19]:


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required = True)  ## input is the netMPHpan xlsx for multiple sequence but single allel
    parser.add_argument('-o', '--output', required=True) ## output is the distance matrisx for each allele, required output csv name
    args = parser.parse_args()
    print(args.input, 'is input, ', args.output, 'output.')
    
    ## input is the netMPHpan xlsx for multiple sequence but single allel
    ## for single allel, load the xls file and filter by cutoff
    data = pd.read_csv(args.input,sep="\t",skiprows=0)
    data_epitope = data.loc[data['EL_Rank'] <2] 
    data_epitope['core_tcrf'] = data_epitope.apply(lambda x:core_tcrf(x['core']),axis=1)
    data_epitope = data_epitope[["ID","Pos", "core_tcrf","EL-score"]]
    data_epitope=data_epitope.groupby(["ID","Pos", "core_tcrf"])["EL-score"].sum().reset_index()
    ## reshape dataframe
    epitope_feature = data_epitope.pivot_table(index=['core_tcrf'], columns=['ID'],values="EL-score")
    epitope_feature = epitope_feature.fillna(0)

    ## calculate distance
    seq_epidist=seq_mandist(data_epitope,epitope_feature)
    seq_epidist = pd.DataFrame(seq_epidist, columns=["seq1", "seq2","epitope_distance"])
    #allele=get_allele(args.input)
    #seq_epidist['allele']=allele
    seq_epidist.to_csv(args.output,index=False)

main()


# In[ ]:




