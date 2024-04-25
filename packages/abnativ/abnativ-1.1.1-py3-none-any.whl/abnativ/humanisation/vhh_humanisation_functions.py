# (c) 2023 Sormannilab and Aubin Ramon
#
# Humanisation pipelines of nanobodies of AbNatiV VH and VHH assesments
#
# ============================================================================

import os

from ..model.alignment.mybio import print_Alignment_pap
from ..model.alignment.mybio import renumber_Fv_pdb_file
from ..model.scoring_functions import abnativ_scoring, fr_aho_indices

from .humanisation_utils import humanise_enhanced_sampling, humanise_exhaustive_sampling,  print_chimera_mutations_code, predict_struct_vhh



def abnativ_vhh_humanisation(wt_seq: str, name_seq: str, output_dir: str='abnativ_humanisation', pdb_file: str=None, ch_id: str=None, 
                             allowed_user_positions:list=fr_aho_indices, is_brute: bool=False, threshold_abnativ_score:float=.98,
                             threshold_rasa_score:float=0.15, perc_allowed_decrease_vhh:float=2e-2, forbidden_mut:list=['C','M'],
                             a:float=.8,b:float=.2, seq_ref: str=None, name_seq_ref: str=None, verbose: bool=True) -> None: 
    '''Run AbNatiV humanisation pipeline on a nanobody sequence with a dual-control strategy 
    that aims to increase the AbNatiV VH-hummanness of a sequence
    while retaining its VHH-nativeness.

    Two sampling methods are available:
        - enhanced sampling (is_brute=False): iteratively explores
            the mutational space aiming for rapid convergence to generate a single humanised sequence.
        - exhaustive sampling (is_brute=True): It assesses all mutation combinations within 
            the available mutational space (PSSM-allowed mutations) and selects the best sequences (Pareto Front).

    See parameters for further details. 
    
    Parameters
    ----------
        - wt_seq: str
            Unaligned sequence string 
        - name_seq: str
        - output_dir:str
            Directory where to save files
        - pdb_file: str
            Filepath to the pdb file of the wt_seq
        - ch_id: str
            Chain id of the pfb pdb_file
        - allowed_user_aho_positions: list of int
            List of AHo positions allowed by the user to make mutation on (default: framework positions)
        - is_brute: bool
            If True, runs brute method rather than the enhanced sampling method
        - threshold_abnativ_score: float 
            Bellow the AbNatiV VH threshold score, a position is considered as a liability
        - threshold_rasa_score: float 
            Above this threshold, the residue is considered solvent exposed and is considered for mutation
        - perc_allowed_decrease_vhh: float
            Maximun ΔVHH score decrease allowed for a mutation
        - forbidden_mut: list
            List of residues to ban for mutation i.e. ['C','M']
        - a: float
            Used in multi-objective selection function: aΔVH+bΔVHH
        - b: float
            Used in multi-objective selection function: aΔVH+bΔVHH
        - seq_ref: str 
            If None, does not plot any references in the profiles. If str, will plot it
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

    # Aligned WT sequence to take into account additional terminal residues added during the alignment process
    wt_vh_seq_abnativ_df, wt_vh_profile_abnativ_df = abnativ_scoring('VH', wt_seq, batch_size=1,mean_score_only=False, 
                                                                    do_align=True, is_VHH=True, verbose=False)
    al_wt_seq = ''.join(wt_vh_seq_abnativ_df['aligned_seq'])

    # Predict no pdb available, use NanoBuilder2
    if pdb_file is None:
        aho_pdb_file, ch_id, _, _, _, _ = predict_struct_vhh(al_wt_seq.replace('-',''), name_seq + '_abnativ_wt', pdb_dir)

    # Renumber PDB file into AHo numbering, not very robust yet 
    else: 
        aho_pdb_file = os.path.join(pdb_dir, os.path.basename(pdb_file).split('.')[0] + '_aho.pdb')
        try: 
            renumber_Fv_pdb_file(pdb_file, ch_id, None, scheme='AHo', outfilename=aho_pdb_file)
        except ValueError: 
            print('Difficulties to read PDB, please make sure it is as cleaned as possible or use the structure prediction option\
                   by writing "None" in the pdb_file option')

    try:
        # Run AbNatiV humanisation
        if not is_brute: 
            fp_hum_fa = os.path.join(seq_dir, f'abnativ_humanised_{name_seq}.fa')
            with open(fp_hum_fa, 'w') as f:
                if verbose: print(f'\n>> ENHANCED SAMPLING <<\n\n## {name_seq} ##\n')
                id_wt = name_seq + '_abnativ_wt'
                f.write(f'>{id_wt}\n')
                f.write(al_wt_seq.replace('-','') + '\n')

                seq_hum =  humanise_enhanced_sampling(al_wt_seq.replace('-',''), name_seq, 'VH', True, aho_pdb_file, ch_id, seq_dir, allowed_user_positions,
                                                threshold_abnativ_score, threshold_rasa_score, perc_allowed_decrease_vhh=perc_allowed_decrease_vhh, forbidden_mut=forbidden_mut,
                                                a=a, b=b, seq_ref=seq_ref, name_seq_ref=name_seq_ref, verbose=verbose)
            
                id_hum = name_seq + '_abnativ_hum'
                f.write(f'>{id_hum}\n')
                f.write(seq_hum + '\n')

            # Final AbNatiV score and save
            vh_abnativ_df_mean, vh_abnativ_df_profile = abnativ_scoring('VH', fp_hum_fa, batch_size=1, mean_score_only=False, do_align=True, is_VHH=True)
            vhh_abnativ_df_mean, vhh_abnativ_df_profile = abnativ_scoring('VHH', fp_hum_fa, batch_size=1, mean_score_only=False, do_align=True, is_VHH=True)
            merge_abnativ_df = vh_abnativ_df_mean.merge(vhh_abnativ_df_mean, how='inner')
            merge_abnativ_df.to_csv(os.path.join(seq_dir, f'{name_seq}_hum_abnativ.csv'))

            # Print pap file 
            dict_all_seqs = {id_wt:wt_seq, id_hum:seq_hum}
            print_Alignment_pap(dict_all_seqs, os.path.join(seq_dir,f'abnativ_humanised_{name_seq}.pap'), nchar_id=18)

            # Model WT/HUM structures
            if pdb_file is not None : 
                pred_pdb_file, pred_ch_id, _, _, _, _ = predict_struct_vhh(al_wt_seq.replace('-',''), id_wt, pdb_dir)
            else:
                pred_pdb_file, pred_ch_id = aho_pdb_file, ch_id
            predict_struct_vhh(seq_hum, id_hum, pdb_dir)
            
            print_chimera_mutations_code(al_wt_seq.replace('-',''), seq_hum, pred_pdb_file, pred_ch_id, pdb_dir, name_seq + '_pred_pdb')

            if pdb_file is not None:
                try:
                    print_chimera_mutations_code(al_wt_seq.replace('-',''), seq_hum, pdb_file, ch_id, pdb_dir, name_seq + '_real_pdb')
                except:
                    print('Could not print the chimera code for the real pdb. To be adressed.')

        else:
            # Run Brute force optimisation
            if verbose: print(f'\n>> EXHAUSTIVE SAMPLING <<\n\n## {name_seq} ##\n')
            humanise_exhaustive_sampling(al_wt_seq.replace('-',''),'VH', True, name_seq, aho_pdb_file, ch_id, seq_dir, pdb_dir, allowed_user_positions,
                                      threshold_abnativ_score, threshold_rasa_score, perc_allowed_decrease_vhh, forbidden_mut,
                                      seq_ref, name_seq_ref)


    finally: 
        if pdb_file is not None: os.remove(aho_pdb_file)


