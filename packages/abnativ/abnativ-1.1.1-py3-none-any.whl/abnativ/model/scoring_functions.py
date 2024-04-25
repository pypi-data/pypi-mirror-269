# (c) 2023 Sormannilab and Aubin Ramon
#
# Scoring functions for the AbNatiV model.
#
# ============================================================================

from .abnativ import AbNatiV_Model
from .utils import is_protein
from .onehotencoder import data_loader_masking_bert_onehot_fasta, alphabet
from .alignment.align_and_clean import anarci_alignments_of_Fv_sequences
from .alignment.aho_consensus import cdr1_aho_indices, cdr2_aho_indices, cdr3_aho_indices, fr_aho_indices
from ..update import PRETRAINED_MODELS_DIR

from pkg_resources import resource_filename

from typing import Tuple
from Bio import SeqIO
from collections import defaultdict
from tqdm import tqdm
import math
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import torch
import sklearn


def plot_abnativ_profile(res_scores, full_seq, name_seq, model_type, fig_fp_save):
    '''
    Plot the AbNatiV score profile of a sequence.
    '''
    sns.set(font_scale = 2.2)
    sns.set_style('white', {'axes.spines.right':False, 'axes.spines.top': True, 'axes.spines.bottom': False,
                                    'xtick.bottom': False,'xtick.top': True, 'ytick.left': True, 'xtick.labeltop':True})
    fig, ax = plt.subplots(figsize=(40,8))

    # Plot
    ax.plot(res_scores, linewidth = 5, alpha=0.65, color='darkorange', label=name_seq)

    # Add CDRs
    ax.axvspan(cdr1_aho_indices[0]-1,cdr1_aho_indices[-1]-1, alpha=0.06, color='forestgreen')
    ax.axvspan(cdr2_aho_indices[0]-1,cdr2_aho_indices[-1]-1, alpha=0.06, color='forestgreen')
    ax.axvspan(cdr3_aho_indices[0]-1,cdr3_aho_indices[-1]-1, alpha=0.06, color='forestgreen')

    ax.xaxis.set_ticks(np.arange(0, len(full_seq), 1.0))
    ax.set_xticklabels(full_seq, fontsize=21)
    ax.tick_params(axis='x', which='major', pad=3)
    ax.xaxis.set_label_position('top')
    ax.set_ylabel(f'AbNatiV {model_type}\nResidue Score', fontsize = 28, labelpad =15)
    ax.set_xlabel('Sequence', fontsize = 28, labelpad=15)
    ax.xaxis.tick_top()

    plt.title(f'{name_seq} AbNatiV {model_type} profile', fontsize=31,pad=18)
    plt.tight_layout()
    plt.savefig(fig_fp_save, dpi=200, bbox_inches='tight')



def norm_by_length_no_gap(scores_pposi: list, onehot_encoding: list) -> list:
    '''
    Sum the scores per position of a given sequence. Normalise the result by the
    number of residues (no gaps).

    Parameters
    ----------
        - scores_pposi : list
            Scores of the chosen positions
        - onehot_encoding : list
            One-hot encoding of the chosen given positions
    '''
    length = len(onehot_encoding)
    idx = np.argmax(onehot_encoding, axis=1)
    nb_gaps = np.count_nonzero(idx == 20)
    length -= nb_gaps
    if length == 0:
        print('Length portion equals zero, too many gaps. Evaluates it as np.nan')
        norm = np.nan
    else:
        norm = np.sum(scores_pposi)/length
    return norm

def linear_rescaling(list_scores: list, t_new: int, t_r: int) -> list:
    '''
    Linear rescaling of the scores to translate the threshold t_r (specific to each
    model type as defined in Methods) to the new threshold t_new.
    '''
    rescaled = list()
    for x in list_scores:
        rescaled.append((t_new-1)/(t_r-1)*(x-1) + 1)
    return rescaled

def get_abnativ_nativeness_scores(output_abnativ: dict, portion_indices: list, model_type: str) -> list:
    '''
    Give the AbNatiV nativeness scores for given positions (could be full) of the outputs of the
    AbNatiV model.

    Parameters
    ----------
        - output_abnativ : dict
            Output dict of sequences evaluated by AbNatiV
            i.e. {'fp':'/my/path/to/the/dataset.txt', 'recon_error_pbe': [0.2,0.3,0.4]}
        - portion_indices : list
            Position indices to score
            e.g., range(1,150) for the all sequence / range(27,43) for the CDR-1 (AHo numbering)
        - model_type : str
            VH, VHH, VKappa, VLambda

    Returns
    ----------
        - a list of the rescaled AbNatiV nativenees scores
    '''

    humanness_scores = list()
    best_thresholds = {'VH': 0.988047, 'VKappa': 0.992496, 'VLambda': 0.985580, 'VHH': 0.990973}

    # Convert AHo-position into list index
    portion_indices = np.array(portion_indices) - 1

    # Score
    for k, profile in enumerate(output_abnativ['recon_error_pposi']):
        score = norm_by_length_no_gap(profile[portion_indices].cpu().detach().numpy(),
                                      output_abnativ['inputs'][k][portion_indices].cpu().detach().numpy())
        humanness_scores.append(math.exp(-score))

    if model_type not in best_thresholds.keys(): # If scoring your own model
        rescaled_scores = humanness_scores

    else:
        rescaled_scores = linear_rescaling(humanness_scores, 0.8, best_thresholds[model_type])

    return list(rescaled_scores)

def abnativ_scoring(model_type: str, fp_fa_or_seq: str, batch_size: int=128, mean_score_only: bool=True,
                    do_align: bool=True, is_VHH: bool=False, is_plotting_profiles: bool=False,
                    output_dir: str='temp_abnativ_scoring', output_id: str='antibody', verbose: bool=True) -> Tuple[pd.DataFrame,pd.DataFrame]:
    '''
    Infer on a fasta file, or directly a sequence, the AbNatiV loaded model with the
    selected model type. Returns a dataframe with the scored sequences.
    Alignement (AHo numbering) is performed if asked. If not asked, the sequences must have been
    beforehand aligned on the AHo scheme.
    All files saved within the function are meant to be temporary.

    Parameters
    ----------
        - model_type : str
            e.g., - VH, VHH, VKappa, VLambda (for default AbNatiV trained models),
                  - or, filepath to the custom checkpoint .ckpt (no linear rescaling will be applied)
        - fp_fa_or_seq : str
            Filepath to the fasta file with AHo aligned sequences to evaluate or directly an aligned sequence input
                e.g., 'seqs.fa' or 'QVE-VSS'
        - batch_size: int
        - mean_score_only: bool
            If True, provide only the mean nativeness score at the sequence level
        - do_align: bool
            If True, do the alignment with the AHo numbering by ANARCI #Coming update. A column
            will be added with the aligned_seq
        - is_VHH: bool
            If True, considers the VHH seed for the alignment, more suitable when aligning nanobody sequences
        - is_plotting_profiles: bool
            If True, plot the profile of every sequence
        - output_dir: str
            Filepath to the folder whre all files are saved
        - id: str
            Preffix of all saved files
        - verbose: bool
            If False, do not print anything except exceptions and errors

    Returns
    -------
        - df_mean: pd.DataFrame
            Dataframe composed of the id, the aligned sequence, the AbNatiV overall score,
            and in particular the CDR-1, CDR-2, CDR-3, Framework scores for a each sequences of the fasta file
        - df_profile: pd_DataFrame
            If not mean_score_only: Dataframe composed of the residue level Abnativ score with the score of each residue at each position.
            Else: Empty Dataframe

    '''

    # Set the device
    if torch.cuda.is_available():
        device_type = 'cuda'
    else:
        device_type = 'cpu'

    if verbose: print(f'\nCalculations on device {device_type}\n')

    device = torch.device(device_type)

    model_dir = PRETRAINED_MODELS_DIR

    fr_trained_models = {'VH': os.path.join(model_dir, 'vh_model.ckpt'), 'VHH': os.path.join(model_dir, 'vhh_model.ckpt'),
                         'VKappa': os.path.join(model_dir, 'vkappa_model.ckpt'), 'VLambda': os.path.join(model_dir, 'vlambda_model.ckpt')}

    # Create folder is not existing
    flag_existing_folder = True
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        flag_existing_folder=False

    # Write a temp fasta file for a single seq
    if not os.path.isfile(fp_fa_or_seq):
        if is_protein(fp_fa_or_seq, alphabet):
            fp_fa = os.path.join(output_dir, f'{output_id}_temp_1seq.fa')
            with open(fp_fa, 'w') as tmp_1fa:
                    tmp_1fa.write('>single_seq\n')
                    tmp_1fa.write(fp_fa_or_seq + '\n')
        else:
            raise Exception(f'Can not find the input file {fp_fa_or_seq} or if you gave a single protein sequence make sure it is composed only of {alphabet}')
    else:
        fp_fa = fp_fa_or_seq

    ## ALIGNMENT ##
    if do_align:
        if verbose: print(f'\n### ANARCI alignment of {fp_fa_or_seq}###\n')
        VH,VK,VL,failed,mischtype = anarci_alignments_of_Fv_sequences(fp_fa, isVHH=is_VHH, verbose=verbose)
        VH.add(VK)
        VH.add(VL)
        if len(VH)==0:
            raise Exception(f'All sequences have been discarded during alignement.')
        # Saving aligned sequences in a fasta file
        fp_aligned_fa = os.path.join(output_dir, f'{output_id}_temp_al_seqs.fa')
        VH.Print(fp_aligned_fa, print_header_definition_files=False)
    else:
        fp_aligned_fa = fp_fa

    ## MODEL LOADING ##
    if model_type not in fr_trained_models.keys():
        try:
            if verbose: print(f'\n### AbNatiV scoring of {fp_fa_or_seq} from checkpoint {model_type} ###\n')
            loaded_model = AbNatiV_Model.load_from_checkpoint(model_type, map_location=device)
            name_type = 'Custom'
        except:
            print(f'Cannnot load the checkpoint {model_type}, you might use the default models: VH, VKappa, VLambda, or VHH.')

    else:
        if verbose: print(f'\n### AbNatiV {model_type}-ness scoring of {fp_fa_or_seq} ###\n')
        loaded_model = AbNatiV_Model.load_from_checkpoint(fr_trained_models[model_type], map_location=device)
        name_type = model_type

    loaded_model.eval()
    loader = data_loader_masking_bert_onehot_fasta(fp_aligned_fa, batch_size, perc_masked_residues=0, is_masking=False)

    # Save ids with aligned seqs and original sequences
    list_ids, list_seqs, list_al_seqs = list(), list(), list()
    original_seqs = SeqIO.to_dict(SeqIO.parse(fp_fa, 'fasta'))
    for record in SeqIO.parse(fp_aligned_fa, 'fasta'):
        id = record.id
        seq = str(original_seqs[id].seq)
        list_ids.append(id)
        list_seqs.append(seq)
        if do_align:
            al_seq = str(record.seq)
            if len(al_seq)!=149:
                raise Exception(f'Sequence {id} is too short (length={len(al_seq)}<149), make sure all sequences are aligned on the AHo numbering.')
            list_al_seqs.append(al_seq)

    nb_of_iterations = math.ceil(len(list_ids)/batch_size)

    scored_data_dict_mean = defaultdict(list)
    scored_data_dict_mean.update({'seq_id': list_ids, 'input_seq': list_seqs})
    if do_align:
        scored_data_dict_mean.update({'aligned_seq': list_al_seqs})

    scored_data_dict_profile = defaultdict(list)

    ## MODEL EVALUATION ##
    try:
        for count, batch in enumerate(tqdm(loader, total=nb_of_iterations, disable=not verbose)):
            batch = [s_data.to(device) for s_data in batch]
            output_abnativ = loaded_model(batch)

            # Sequence-level scores
            humanness_scores = get_abnativ_nativeness_scores(output_abnativ, range(149), model_type)
            cdr1_scores = get_abnativ_nativeness_scores(output_abnativ, cdr1_aho_indices, model_type)
            cdr2_scores = get_abnativ_nativeness_scores(output_abnativ, cdr2_aho_indices, model_type)
            cdr3_scores = get_abnativ_nativeness_scores(output_abnativ, cdr3_aho_indices, model_type)
            fr_scores = get_abnativ_nativeness_scores(output_abnativ, fr_aho_indices, model_type)

            scored_data_dict_mean[f'AbNatiV {name_type} Score'].extend(humanness_scores)

            scored_data_dict_mean[f'AbNatiV CDR1-{name_type} Score'].extend(cdr1_scores)
            scored_data_dict_mean[f'AbNatiV CDR2-{name_type} Score'].extend(cdr2_scores)
            scored_data_dict_mean[f'AbNatiV CDR3-{name_type} Score'].extend(cdr3_scores)
            scored_data_dict_mean[f'AbNatiV FR-{name_type} Score'].extend(fr_scores)

            # Residue-level scores
            if not mean_score_only:
                for k, input in enumerate(output_abnativ['inputs']):
                    input = input.cpu()
                    seq_id = list_ids[count*batch_size + k]
                    res_scores, full_seq = list(), list()
                    for i, res in enumerate(input):
                        scored_data_dict_profile['seq_id'].extend([seq_id])
                        scored_data_dict_profile['AHo position'].extend([i+1])
                        scored_data_dict_profile['aa'].extend([alphabet[np.argmax(res)]])
                        score = math.exp(-output_abnativ['recon_error_pposi'][k][i])
                        scored_data_dict_profile[f'AbNatiV {name_type} Residue Score'].extend([score])
                        res_scores.append(score)
                        full_seq.append(alphabet[np.argmax(res)])
                        for n, alpha in enumerate(alphabet):
                            scored_data_dict_profile[alpha].extend([output_abnativ['x_recon'].cpu().detach().numpy()[k][i][n]])
                    if is_plotting_profiles:
                        dir_save = os.path.join(output_dir, f'{output_id}_profiles')
                        if not os.path.exists(dir_save):
                            os.makedirs(dir_save)
                        # Plotting
                        fig_save_fp = os.path.join(dir_save, f'{seq_id}_abnativ_profile.png')
                        plot_abnativ_profile(res_scores, full_seq, seq_id, name_type, fig_save_fp)
    finally:
        # Remove temporary files
        if is_protein(fp_fa_or_seq, alphabet): #temp single seq
            if verbose: print(f'\nAbNatiV {name_type} Score: {humanness_scores[0]}\n')
            os.remove(fp_fa)
        if do_align: #temp alignment
            os.remove(fp_aligned_fa)
        if not flag_existing_folder and not is_plotting_profiles:
            os.rmdir(output_dir)

    df_mean = pd.DataFrame.from_dict(scored_data_dict_mean)
    df_profile = pd.DataFrame.from_dict(scored_data_dict_profile)

    return df_mean, df_profile



def abnativ_embeddings_extraction(model_type: str, fp_fa_or_seq: str, batch_size: int=128,
                    do_align: bool=True, is_VHH: bool=False,
                    output_dir: str='temp_abnativ_scoring', output_id: str='antibody', verbose: bool=True) -> dict:
    '''
    Infer embedding on a fasta file, or directly a sequence, the AbNatiV loaded model with the
    selected model type. Returns a dataframe with the scored sequences.
    Alignement (AHo numbering) is performed if asked. If not asked, the sequences must have been
    beforehand aligned on the AHo scheme.
    All files saved within the function are meant to be temporary.

    Parameters
    ----------
        - model_type : str
            e.g., - VH, VHH, VKappa, VLambda (for default AbNatiV trained models),
                  - or, filepath to the custom checkpoint .ckpt (no linear rescaling will be applied)
        - fp_fa_or_seq : str
            Filepath to the fasta file with AHo aligned sequences to evaluate or directly an aligned sequence input
                e.g., 'seqs.fa' or 'QVE-VSS'
        - batch_size: int
        - do_align: bool
            If True, do the alignment with the AHo numbering by ANARCI #Coming update. A column
            will be added with the aligned_seq
        - is_VHH: bool
            If True, considers the VHH seed for the alignment, more suitable when aligning nanobody sequences
        - output_dir: str
            Filepath to the folder whre all files are saved
        - id: str
            Preffix of all saved files
        - verbose: bool
            If False, do not print anything except exceptions and errors

    Returns
    -------
        - dict with saved embs
    '''
    # Set the device
    if torch.cuda.is_available():
        device_type = 'cuda'
    else:
        device_type = 'cpu'

    model_dir = PRETRAINED_MODELS_DIR

    fr_trained_models = {'VH': f'{model_dir}/vh_model.ckpt', 'VHH': f'{model_dir}/vhh_model.ckpt',
                         'VKappa': f'{model_dir}/vkappa_model.ckpt', 'VLambda': f'{model_dir}/vlambda_model.ckpt'}

    # Create folder is not existing
    flag_existing_folder = True
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        flag_existing_folder=False

    # Write a temp fasta file for a single seq
    if not os.path.isfile(fp_fa_or_seq):
        if is_protein(fp_fa_or_seq, alphabet):
            fp_fa = os.path.join(output_dir, f'{output_id}_temp_1seq.fa')
            with open(fp_fa, 'w') as tmp_1fa:
                    tmp_1fa.write('>single_seq\n')
                    tmp_1fa.write(fp_fa_or_seq + '\n')
        else:
            raise Exception(f'Can not find the input file {fp_fa_or_seq} or if you gave a single protein sequence make sure it is composed only of {alphabet}')
    else:
        fp_fa = fp_fa_or_seq

    ## ALIGNMENT ##
    if do_align:
        if verbose: print(f'\n### ANARCI alignment of {fp_fa_or_seq}###\n')
        VH,VK,VL,failed,mischtype = anarci_alignments_of_Fv_sequences(fp_fa, isVHH=is_VHH, verbose=verbose)
        VH.add(VK)
        VH.add(VL)
        if len(VH)==0:
            raise Exception(f'All sequences have been discarded during alignement.')
        # Saving aligned sequences in a fasta file
        fp_aligned_fa = os.path.join(output_dir, f'{output_id}_temp_al_seqs.fa')
        VH.Print(fp_aligned_fa, print_header_definition_files=False)
    else:
        fp_aligned_fa = fp_fa

    ## MODEL LOADING ##
    if model_type not in fr_trained_models.keys():
        try:
            if verbose: print(f'\n### AbNatiV scoring of {fp_fa_or_seq} from checkpoint {model_type} ###\n')
            loaded_model = AbNatiV_Model.load_from_checkpoint(model_type, map_location=device_type)
            name_type = 'Custom'
        except:
            print(f'Cannnot load the checkpoint {model_type}, you might use the default models: VH, VKappa, VLambda, or VHH.')

    else:
        if verbose: print(f'\n### AbNatiV {model_type}-ness scoring of {fp_fa_or_seq} ###\n')
        loaded_model = AbNatiV_Model.load_from_checkpoint(fr_trained_models[model_type], map_location=device_type)
        name_type = model_type

    loaded_model.eval()
    loader = data_loader_masking_bert_onehot_fasta(fp_aligned_fa, batch_size, perc_masked_residues=0, is_masking=False)

    # Save ids with aligned seqs and original sequences
    list_ids, list_seqs, list_al_seqs = list(), list(), list()
    original_seqs = SeqIO.to_dict(SeqIO.parse(fp_fa, 'fasta'))
    for record in SeqIO.parse(fp_aligned_fa, 'fasta'):
        id = record.id
        seq = str(original_seqs[id].seq)
        list_ids.append(id)
        list_seqs.append(seq)
        if do_align:
            al_seq = str(record.seq)
            if len(al_seq)!=149:
                raise Exception(f'Sequence {id} is too short (length={len(al_seq)}<149), make sure all sequences are aligned on the AHo numbering.')
            list_al_seqs.append(al_seq)

    nb_of_iterations = math.ceil(len(list_ids)/batch_size)

    data_dict_embs = defaultdict(list)
    data_dict_embs.update({'id': list_ids, 'input_seq': list_seqs})

    ## MODEL EVALUATION ##
    try:
        for count, batch in enumerate(tqdm(loader, total=nb_of_iterations, disable=not verbose)):
            output_abnativ = loaded_model(batch)
            if count==0:
                for key in output_abnativ:
                    if key in ['perplexity']:
                        continue
                    data_dict_embs[key] = list(output_abnativ[key].detach().numpy())
            else:
                for key in output_abnativ:
                    if key in ['perplexity']:
                        continue
                    data_dict_embs[key].extend(list(output_abnativ[key].detach().numpy()))

    finally:
        # Remove temporary files
        if is_protein(fp_fa_or_seq, alphabet): #temp single seq
            os.remove(fp_fa)
        if do_align: #temp alignment
            os.remove(fp_aligned_fa)
        if not flag_existing_folder:
            os.rmdir(output_dir)

    return data_dict_embs

