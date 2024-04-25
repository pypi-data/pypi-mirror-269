# (c) 2023 Sormannilab and Aubin Ramon
#
# Humanisation pipelines of nanobodies of AbNatiV VH and VHH assesments
#
# ============================================================================

import os

from ..model.alignment.align_and_clean import anarci_alignments_of_Fv_sequences
from ..model.onehotencoder import alphabet
from ..model.alignment.mybio import print_Alignment_pap
from ..model.alignment.mybio import renumber_Fv_pdb_file
from ..model.scoring_functions import abnativ_scoring, fr_aho_indices

from .humanisation_utils import humanise_enhanced_sampling, humanise_exhaustive_sampling, print_chimera_mutations_code, predict_struct_vh_vl



def abnativ_vh_vl_humanisation(vh_wt_seq: str, vl_wt_seq:str, name_seq: str, output_dir: str='abnativ_humanisation', pdb_file: str=None, ch_id_vh: str=None,
                               ch_id_vl: str=None, allowed_user_positions_h:list=fr_aho_indices, allowed_user_positions_l:list=fr_aho_indices, is_brute: bool=False, threshold_abnativ_score:float=.98,
                             threshold_rasa_score:float=0.15, forbidden_mut: list=['C','M'], seq_ref: str=None, name_seq_ref: str=None, verbose: bool=True) -> None: 
    '''Run AbNatiV humanisation pipeline on paired VH/VL Fv sequences that aims
      to increase the AbNatiV VH- and VL- hummanness of each sequence separately.

    Two sampling methods are available:
        - enhanced sampling (is_brute=False): iteratively explores
            the mutational space aiming for rapid convergence to generate a single humanised sequence.
        - exhaustive sampling (is_brute=True): It assesses all mutation combinations within 
            the available mutational space (PSSM-allowed mutations) and selects the best sequences (Pareto Front).

    See parameters for further details. 
    
    Parameters
    ----------
        - vh_wt_seq: str
            Unaligned heavy sequence string
        - vl_wt_seq: str
            Unaligned light sequence string 
        - name_seq: str
        - output_dir:str
            Directory where to save files
        - pdb_file: str
            Filepath to the pdb file of the wt_seq
        - ch_id_vh: str
            Chain id of the heavy chain in the pfb pdb_file
        - ch_id_vl: str
            Chain id of the light chain in the pfb pdb_file
        - allowed_user_aho_positions: list of int
            List of AHo positions allowed by the user to make mutation on (default: framework positions)
        - is_brute: bool
            If True, runs brute method rather than the enhanced sampling method
        - threshold_abnativ_score: float 
            Bellow the AbNatiV VH threshold score, a position is considered as a liability
        - threshold_rasa_score: float 
            Above this threshold, the residue is considered solvent exposed and is considered for mutation
        - forbidden_mut: list
            List of residues to ban for mutation i.e. ['C','M']
        - seq_ref: str 
            If None, does not plot any references in the profiles. If str, will plot it. 
        - name_seq_ref: str
        - verbose: bool
            
    Returns
    -------
        - dict with keys will be AHo numbers, values will be allowed substitutions 
            according to the PSSM criteria '''
    

    # Create folders
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    seq_dir = os.path.join(output_dir, name_seq)
    if not os.path.exists(seq_dir): os.makedirs(seq_dir)

    pdb_dir = os.path.join(seq_dir, 'structures')
    if not os.path.exists(pdb_dir): os.makedirs(pdb_dir)

    # Find Fv chain type
    fp_light_fa = os.path.join(seq_dir, f'temp_light_1seq.fa')
    with open(fp_light_fa, 'w') as tmp_1fa:
            tmp_1fa.write('>single_seq\n')
            tmp_1fa.write(vl_wt_seq + '\n')
    VH,VK,VL,failed,mischtype = anarci_alignments_of_Fv_sequences(fp_light_fa, isVHH=False, verbose=False)

    if len(VK)>0:
        light_Fv_type = 'VKappa'
    elif len(VL)>0:
        light_Fv_type = 'VLambda'
    else:
        raise ValueError(f'Could not compute automtically the light_Fv_type (VKappa, VLambda) of the input light sequence')

    # Aligned WT sequence to take into account additional terminal residues added during the alignment process
    wt_vh_seq_abnativ_df, wt_vh_profile_abnativ_df = abnativ_scoring('VH', vh_wt_seq, batch_size=1,mean_score_only=False, 
                                                                    do_align=True, is_VHH=True, verbose=False)
    al_vh_wt_seq = ''.join(wt_vh_seq_abnativ_df['aligned_seq'])

    wt_vl_seq_abnativ_df, wt_vl_profile_abnativ_df = abnativ_scoring(light_Fv_type, vl_wt_seq, batch_size=1,mean_score_only=False, 
                                                                    do_align=True, is_VHH=True, verbose=False)
    al_vl_wt_seq = ''.join(wt_vl_seq_abnativ_df['aligned_seq'])

    # Predict no pdb available, use NanoBuilder2
    if pdb_file is None:
        aho_pdb_file, ch_id_vh, ch_id_vl, flag, _, _, _ = predict_struct_vh_vl(al_vh_wt_seq.replace('-',''), al_vl_wt_seq.replace('-',''), name_seq + '_abnativ_wt', pdb_dir)

    # Renumber PDB file into AHo numbering, not very robust yet 
    else: 
        aho_pdb_file = os.path.join(pdb_dir, os.path.basename(pdb_file).split('.')[0] + '_aho.pdb')
        try: 
            renumber_Fv_pdb_file(pdb_file, ch_id_vh, ch_id_vl, scheme='AHo', outfilename=aho_pdb_file)
        except ValueError: 
            print('Difficulties to read PDB, please make sure it is as cleaned as possible or use the structure prediction option\
                   by writing "None" in the pdb_file option')

    try:
        # Run AbNatiV humanisation
        if not is_brute: 
            fp_vh_hum_fa = os.path.join(seq_dir, f'abnativ_humanised_heavy_{name_seq}.fa')
            with open(fp_vh_hum_fa, 'w') as f:
                if verbose: print(f'\n>> ENHANCED SAMPLING <<\n\n## Humanise VH of {name_seq} ##\n')
                id_vh_wt = name_seq + '_abnativ_heavy_wt'
                f.write(f'>{id_vh_wt}\n')
                f.write(al_vh_wt_seq.replace('-','') + '\n')

                vh_seq_hum =  humanise_enhanced_sampling(al_vh_wt_seq.replace('-',''), name_seq, 'VH', False, aho_pdb_file, ch_id_vh, seq_dir, allowed_user_positions_h,
                                                threshold_abnativ_score, threshold_rasa_score, forbidden_mut=forbidden_mut, seq_ref=seq_ref, name_seq_ref=name_seq_ref, verbose=verbose)
                                                
                
                id_vh_hum = name_seq + '_abnativ_heavy_hum'
                f.write(f'>{id_vh_hum}\n')
                f.write(vh_seq_hum + '\n')

            fp_vl_hum_fa = os.path.join(seq_dir, f'abnativ_humanised_light_{name_seq}.fa') 
            with open(fp_vl_hum_fa, 'w') as f:
                if verbose: print(f'\n## Humanise VL of {name_seq} ##\n')
                id_vl_wt = name_seq + '_abnativ_light_wt'
                f.write(f'>{id_vl_wt}\n')
                f.write(al_vl_wt_seq.replace('-','') + '\n')
                
                vl_seq_hum = humanise_enhanced_sampling(al_vl_wt_seq.replace('-',''), name_seq, light_Fv_type, False, aho_pdb_file, ch_id_vl, seq_dir, allowed_user_positions_l,
                                                threshold_abnativ_score, threshold_rasa_score, forbidden_mut=forbidden_mut, seq_ref=seq_ref, name_seq_ref=name_seq_ref, verbose=verbose)
                
                id_vl_hum = name_seq + '_abnativ_light_hum'
                f.write(f'>{id_vl_hum}\n')
                f.write(vl_seq_hum + '\n')
            

            # Final AbNatiV score and save
            vh_abnativ_df_mean, vh_abnativ_df_profile = abnativ_scoring('VH', fp_vh_hum_fa, batch_size=1, mean_score_only=False, do_align=True, is_VHH=True)
            vl_abnativ_df_mean, vl_abnativ_df_profile = abnativ_scoring(light_Fv_type, fp_vl_hum_fa, batch_size=1, mean_score_only=False, do_align=True, is_VHH=True)

            vh_abnativ_df_mean.to_csv(os.path.join(seq_dir, f'{name_seq}_hum_heavy_abnativ.csv'))
            vl_abnativ_df_mean.to_csv(os.path.join(seq_dir, f'{name_seq}_hum_light_abnativ.csv'))

            # Print pap file 
            dict_all_seqs = {id_vh_wt:al_vh_wt_seq.replace('-',''), id_vh_hum:vh_seq_hum}
            print_Alignment_pap(dict_all_seqs, os.path.join(seq_dir,f'abnativ_humanised_heavy_{name_seq}.pap'), nchar_id=18)

            dict_all_seqs = {id_vl_wt:al_vl_wt_seq.replace('-',''), id_vl_hum:vl_seq_hum}
            print_Alignment_pap(dict_all_seqs, os.path.join(seq_dir,f'abnativ_humanised_light_{name_seq}.pap'), nchar_id=18)

            # Model WT/HUM structures
            if pdb_file is not None : 
                pred_pdb_file, pred_ch_id_vh, pred_ch_id_vl, flag, _, _, _ = predict_struct_vh_vl(al_vh_wt_seq.replace('-',''), al_vl_wt_seq.replace('-',''), name_seq + '_wt', pdb_dir)
            else:
                pred_pdb_file, pred_ch_id_vh, pred_ch_id_vl = aho_pdb_file, ch_id_vh, ch_id_vl

            predict_struct_vh_vl(vh_seq_hum, vl_seq_hum, name_seq + 'abnativ_hum', pdb_dir)
            print_chimera_mutations_code(al_vh_wt_seq.replace('-',''), vh_seq_hum, pred_pdb_file, pred_ch_id_vh, pdb_dir, name_seq + '_pred_heavy_pdb')
            print_chimera_mutations_code(al_vl_wt_seq.replace('-',''), vl_seq_hum, pred_pdb_file, pred_ch_id_vl, pdb_dir, name_seq + '_pred_light_pdb')

            if pdb_file is not None:
                try:
                    print_chimera_mutations_code(al_vh_wt_seq.replace('-',''), vh_seq_hum, pdb_file, ch_id_vh, pdb_dir, name_seq + '_real_heavy_pdb')
                    print_chimera_mutations_code(al_vl_wt_seq.replace('-',''), vl_seq_hum, pdb_file, ch_id_vl, pdb_dir, name_seq + '_real_light_pdb')
                except:
                    print('Could not print the chimera code for the real pdb. To be adressed.')

        else:
            # Run Brute force optimisation
            if verbose: print(f'\n>> EXHAUSTIVE SAMPLING <<\n\n## Humanise VH of {name_seq} ##\n')
            humanise_exhaustive_sampling(al_vh_wt_seq.replace('-',''), 'VH', False, name_seq + '_heavy', aho_pdb_file, ch_id_vh, seq_dir, pdb_dir, allowed_user_positions_h,
                                      threshold_abnativ_score, threshold_rasa_score, forbidden_mut=forbidden_mut,seq_ref=seq_ref, name_seq_ref=name_seq_ref)
            
            if verbose: print(f'\n## Humanise VL of {name_seq} ##\n')
            humanise_exhaustive_sampling(al_vl_wt_seq.replace('-',''), light_Fv_type, False, name_seq + '_light', aho_pdb_file, ch_id_vl, seq_dir, pdb_dir, allowed_user_positions_l,
                                      threshold_abnativ_score, threshold_rasa_score, forbidden_mut=forbidden_mut,seq_ref=seq_ref, name_seq_ref=name_seq_ref)

    finally: 
        if pdb_file is not None: os.remove(aho_pdb_file)
        os.remove(fp_light_fa)


