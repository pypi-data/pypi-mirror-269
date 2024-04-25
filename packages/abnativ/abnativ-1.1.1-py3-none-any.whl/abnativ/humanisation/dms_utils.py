# (c) 2023 Sormannilab and Aubin Ramon
#
# Util functions for Deep Mutational Scanning of a given sequence using AbNatiV scoring.
#
# ============================================================================

from ..model.scoring_functions import abnativ_scoring

import matplotlib.pyplot as plt

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import pandas as pd



## ENHANCED SAMPLING METHOD ##

def plot_dms_average(dms_average_dependence:list, fp_save:str) -> None:
    '''Plot the average dependence profile on the mutation 
    of all other positions within the sequence of each position obtained
    via a prior deep mutational scanning study'''

    sns.set(font_scale = 1.1)
    sns.set_style('white', {'axes.spines.right':False, 'axes.spines.top': False,
                                'xtick.bottom': True, 'ytick.left': True})

    fig, ax= plt.subplots(figsize=(6,3))

    ax.plot(dms_average_dependence,color = 'C1',alpha=0.8,linewidth = 1.8)
    ax.tick_params(left=True, bottom=True)
    ax.set_xlabel('Residue position', fontsize=15)
    ax.set_ylabel('Average\ninterdependence', fontsize=15)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.11), frameon=False, markerscale=3, fontsize=9)

    plt.tight_layout()

    #Save plots
    plt.savefig(fp_save, dpi=300, bbox_inches='tight')
 

def get_no_gap_idx(al_seq: str) -> list:
    '''Get the gap indexs of an aligned sequence'''
    no_gap_idx = list()
    for k, res in enumerate(al_seq):
        if res != '-':
            no_gap_idx.append(k)
    return no_gap_idx


def compute_dms_map(seq:str, nat: str, is_VHH:bool, fp_folder_deep_mutations:str, 
                    alphabet:list, name_seq:str):
    '''Deep Mutational Scanning study of a given sequence. 

    For a given position, each of the other positions is individually mutated into 
    all available amino acid residues (19 possibilities). Across all mutated positions 
    and all available mutations, the differences between the AbNatiV score of the mutants 
    and of the WT are calculated. These differences are then averaged into a single value 
    quantifying the position under scrutiny dependence on the mutation 
    of all other positions within the sequence. 

    Parameters
    ----------
        - seq: str
            Unaligned string sequence
        - nat: str
            Type of AbNatiV nativeness to do the study on
        - is_VHH: bool
            If True, considers the VHH seed for the alignment, more suitable when aligning nanobody sequences
        - fp_folder_deep_mutations: str
            Path where to save the mutated sequences as a single .fa file in a this folder and figures
        - alphabet: list
            A list of string with the residues composing the sequences
        - name_seq: str 

    Returns
    -------
        - ng_dms_map: np.array
            [NO GAPS] a square matrix of length len(al_wt_seq) with:
                -> rows = how the mutation to this position affect the other ones
                -> columns = how this position is affected whent he other ones are mutated
        - ng_dms_avg_dep: list
            a list of lenght len(dms_map) with the average dependence for each position of dms_map
        - dms_map: np.array
            [NO GAPS] a square matrix of length len(al_wt_seq) with:
                -> rows = how the mutation to this position affect the other ones
                -> columns = how this position is affected whent he other ones are mutated
        - dms_avg_dep: list
            a list of length len(dms_map) with the average dependence for each position of dms_map
    '''

    #Score WT
    wt_vh_seq_abnativ_df, wt_vh_profile_abnativ_df = abnativ_scoring(nat, seq, batch_size=1,mean_score_only=False, 
                                                                    do_align=True, is_VHH=is_VHH, verbose=False)
    wt_vh_bnativ_profile = wt_vh_profile_abnativ_df[f'AbNatiV {nat} Residue Score'].to_list()
    al_wt_seq = ''.join(wt_vh_seq_abnativ_df['aligned_seq'])
    
    #Generate all mutations
    fp_mut_sata = deep_mutate_to_txt(al_wt_seq, fp_folder_deep_mutations, alphabet, name_seq)
    
    #Scoring all mutations of the DMS
    dms_vh_seq_abnativ_df, dms_vh_profile_abnativ_df = abnativ_scoring(nat, fp_mut_sata, batch_size=128,mean_score_only=False, 
                                                                    do_align=False, is_VHH=is_VHH, verbose=True)

    #Remove DMS files
    os.remove(fp_mut_sata)
    os.rmdir(fp_folder_deep_mutations)
    
    #Initialise the scanning
    mean_profile_pposi = list()
    posi=0
    saved_mut_profiles_at_posi = list()
    no_gap_idx = get_no_gap_idx(al_wt_seq)

    #Iterate other mutants not optimal but do the trick
    for aho_posi in range(1,len(al_wt_seq)+1):
        id = aho_posi - 1

        for uniq_id in dms_vh_seq_abnativ_df['seq_id']:
            split = uniq_id.split('_')
            posi_being_mutated = int(split[-2])
            if posi_being_mutated == id:
                vh_mut_profile = dms_vh_profile_abnativ_df[dms_vh_profile_abnativ_df['seq_id']==uniq_id][f'AbNatiV {nat} Residue Score'].to_list()
                saved_mut_profiles_at_posi.append(vh_mut_profile)

        #Saving for each posi a mean of the profiles when being deeply mutated
        mean_profile_pposi.append(np.mean(saved_mut_profiles_at_posi, axis=0))
        #Reset the saved profiles for next position
        saved_mut_profiles_at_posi = list([vh_mut_profile])

    
    wt_baseline = np.array([wt_vh_bnativ_profile for k in range(len(al_wt_seq))])
    dms_map = np.absolute(mean_profile_pposi - wt_baseline)
    ng_dsm_map = dms_map[:,no_gap_idx][no_gap_idx,:] #Remove gaps
    
    #Computing the median dependence when the other positions are mutated
    dms_avg_dep = give_averaged_position_dependence_dms(dms_map)
    ng_dms_avg_dep = give_averaged_position_dependence_dms(ng_dsm_map) #No gaps
    
    #Plot the average dependence profile
    #fp_save = os.path.join(fp_folder_deep_mutations, f'{name_seq}_avg_dms_dep.png')
    #plot_dms_average(ng_dms_avg_dep, fp_save)

    return ng_dsm_map, ng_dms_avg_dep, dms_map, dms_avg_dep


def give_averaged_position_dependence_dms(dms_map: np.array) -> list:
    '''Average at each position their dependence when everyother positions 
    are mutated (so no diag)

    Parameters
    ----------
        - dms_map : np.array
            Deep mutational scanning map, a square matrix with
                -> rows = how the mutation to this position affect the other ones
                -> columns = how this position is affected whent he other ones are mutated

    Returns
    -------
        - a list of lenght len(dms_map) 
        with the average dependence for each position of dms_map
    '''

    # Exclude the diagonal
    mask_diag=~np.eye(len(dms_map),dtype=bool)

    # loop on columns
    vals= [c[mask_diag.T[j]] for j,c in enumerate(dms_map.T)]
    means=[np.mean(va) for va in vals]

    return means

def deep_mutate_to_txt(seq_aligned_wt:str, save_deep_mut_folder:str, 
                       alphabet:list, name_seq:str) -> str:
    
    '''Deep mutate a given aligned sequence over the whole alphabet and save it 
    as a fasta file in a folder

    Parameters
    ----------
        - seq_aligned_wt: a string sequence
        - save_deep_mut_folder: a string path to save the mutated sequences as a single .fa file in a this folder
        - alphabet: a list of string with the residues composing the sequences
        - name_seq: str nme of the sequence

    Returns
    -------
        - the filename of the saved fasta file
    '''
    
    if not os.path.exists(save_deep_mut_folder):
        os.makedirs(save_deep_mut_folder)

    mutated_seqs = []
    mutated_seqs.append(seq_aligned_wt)
    len_seq_aligned = len(seq_aligned_wt)

    fp_mut_data =  os.path.join(save_deep_mut_folder, 'dms_' + name_seq + '.fa')
    
    with open(fp_mut_data, 'w') as f:
        for i in range(len_seq_aligned):
            single_mut_seq = list(seq_aligned_wt)
            wt_res = single_mut_seq[i]
            if wt_res != '-':
                for k, res in enumerate(alphabet):
                    if res != wt_res and res != '-':
                        single_mut_seq[i] = res
                        f.write(f'>{name_seq}_{i}_{k}\n')
                        f.write(''.join(single_mut_seq) + '\n')
    
    return fp_mut_data





