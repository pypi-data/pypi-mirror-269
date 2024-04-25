# (c) 2023 Sormannilab and Aubin Ramon
#     CC BY-NC-SA 4.0
#
# Util functions for humanisation using the AbNatiV model.
#
# ============================================================================

from ..model.alignment.mybio import print_Alignment_pap
from ..model.scoring_functions import (
    abnativ_scoring,
    cdr1_aho_indices,
    cdr2_aho_indices,
    cdr3_aho_indices,
    fr_aho_indices,
)
from ..model.alignment.structs import Gly_X_Gly_sasa_standard_radiiMax, Term_resMax
from ..model.alignment.mybio import ThreeToOne, renumber_Fv_pdb_file
from ..model.onehotencoder import alphabet

from .dms_utils import compute_dms_map

from pkg_resources import resource_filename

from typing import Tuple

from paretoset import paretoset
from collections import defaultdict

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import pandas as pd

import Bio
from Bio.PDB import PDBParser
from Bio.PDB.SASA import ShrakeRupley

from ImmuneBuilder import NanoBodyBuilder2, ABodyBuilder2

from topmodel.check import chirality, clashes, amide_bond
from topmodel.util.utils import ChiralCenters, AmideBonds, Clashes, CoupleIrregularity


def check_predicted_structure(fp_pdb: str) -> Tuple[bool, list, list]:
    """
    Use the TopModel method to check structual liabilties in a generated model:
        - WdV clashes
        - Wrong dihedral angles
        - D-Stereoimetry

    If a structure has either a WdV clash or a D-residue it will be flagged as unreliable.

    Parameters
    ----------
        - fp_pdb : str
            Filepath to the structure

    Returns
    -------
        - is_reliable : bool
            True if reliable, False if a WdV clash or a D-residue
        - list of clashes
        - list of D-residues

    """

    struct = PDBParser().get_structure("WT_framework", fp_pdb)[0]

    ### WdV Clashes ###
    found_clashes = clashes.get_clashes(struct)
    wdv_clashes = found_clashes[Clashes.VDW]

    # Remove disulfide bonds from clashes
    no_cc_wdv_clashes = list()
    for clash in wdv_clashes:
        if isinstance(clash, CoupleIrregularity):
            res_a_name = clash.res_a.code
            a_numb = clash.res_a.number
            res_b_name = clash.res_b.code
            b_numb = clash.res_b.number
            if res_a_name == "C" and res_b_name == "C":
                continue
        no_cc_wdv_clashes.append(clash)

    ### Wrong dihedral angles (amide bond) ###
    found_amides = amide_bond.get_amide_stereo(struct)
    cis = found_amides[AmideBonds.CIS]
    cis_pro = found_amides[AmideBonds.CIS_PROLINE]
    non_plan = found_amides[AmideBonds.NON_PLANAR]

    ### D-Chiralities ###
    found_chiralities = chirality.get_chirality(struct)
    chiral_d = found_chiralities[ChiralCenters.D]

    if len(no_cc_wdv_clashes) > 0 or len(chiral_d) > 0:
        is_reliable = False
    else:
        is_reliable = True

    return is_reliable, no_cc_wdv_clashes, chiral_d


def predict_struct_vhh(
    seq: str,
    name_seq: str,
    o_dir: str,
    scheme: str = "AHo",
    model_ids=[1, 2, 3, 4],
    max_check_iter=10,
) -> Tuple[str, str, bool, list, list, float]:
    """Predict the structure of a nanobody sequence using the NanobodyBuilder2 software.

    Parameters
    ----------
        - seq : str
            Sequence string
        - name seq: str
        - o_dir: str
        - scheme:
            Alignement numbering used to annotate the residues in the prediction
        - model_ids: list of int
            The id of the model to use with ImmuneBuilder
        - max_check_iter: int
            The maximun number of iterations to generate a structure that does not
            show any major liabilities (WdV clashes or D-stereoisomers)

    Returns
    -------
        - filepath to the predicted nanobody structure .pdb
        - chain id
        - struct_quality_flag
        - list of no_cc_wdv_clashes
        - list of chiral_d
        - and error estimate profile from ImmuneBuilder
    """

    seq_dict = {"H": seq}

    struct_quality_flag = False
    count_check = 0

    while struct_quality_flag is False and count_check < max_check_iter:
        predictor = NanoBodyBuilder2(model_ids=model_ids, numbering_scheme=scheme)

        # NanoBodyBuilder2 structure prediction
        nanobody = predictor.predict(seq_dict)
        aho_pdb_file = os.path.join(o_dir, f"{name_seq}_aho_nanobuilder.pdb")
        nanobody.save(aho_pdb_file)
        ch_id = "H"

        index_best_model = nanobody.error_estimates.mean(-1).argmin()
        error_estimate_profile = np.array(nanobody.error_estimates[index_best_model])

        # Check quality of the model with TopModel
        struct_quality_flag, no_cc_wdv_clashes, chiral_d = check_predicted_structure(
            aho_pdb_file
        )
        count_check += 1

    if struct_quality_flag == False and count_check == max_check_iter:
        print(
            f"\n ATTENTION: Could not generate a structure for {name_seq} without liabilities (i.e., VdW clashes or D-stereoisomers)"
        )
        print(f"----> VdW clashes: {no_cc_wdv_clashes}")
        print(f"----> D-stereo: {chiral_d}")

    return (
        aho_pdb_file,
        ch_id,
        struct_quality_flag,
        no_cc_wdv_clashes,
        chiral_d,
        error_estimate_profile,
    )


def predict_struct_vh_vl(
    vh_seq: str,
    vl_seq: str,
    name_seq: str,
    o_dir: str,
    scheme: str = "AHo",
    model_ids=[1, 2, 3, 4],
    max_check_iter=10,
) -> Tuple[str, str, str, bool, list, list, float]:
    """Predict the structure of a paired VH/VL antibody using the ABodyBuilder2 software

    Parameters
    ----------
        - vh_seq: str
            Sequence string of the Heavy chain of the paired Fvs
        - vl_seq: str
            Sequence string of the Light chain of the paired Fvs
        - name seq: str
        - o_dir: str
        - scheme:
            Alignement numbering used to annotate the residues in the prediction
        - model_ids: list of int
            The id of the model to use with ImmuneBuilder
        - max_check_iter: int
            The maximun number of iterations to generate a structure that does not
            show any major liabilities (WdV clashes or D-stereoisomers)

    Returns
    -------
        - filepath to the predicted nanobody structure .pdb
        - id of heavy chain
        - id of light chain
        - struct_quality_flag
        - list of no_cc_wdv_clashes
        - list of chiral_d
        - and error estimate profile from ImmuneBuilder
    """

    seq_dict = {"H": vh_seq, "L": vl_seq}

    struct_quality_flag = False
    count_check = 0

    while struct_quality_flag is False and count_check < max_check_iter:

        # NanoBodyBuilder2 structure prediction
        predictor = ABodyBuilder2(model_ids=model_ids, numbering_scheme=scheme)

        nanobody = predictor.predict(seq_dict)
        aho_pdb_file = os.path.join(o_dir, f"{name_seq}_aho_abodybuilder.pdb")
        nanobody.save(aho_pdb_file)
        ch_id_vh = "H"
        ch_id_vl = "L"

        index_best_model = nanobody.error_estimates.mean(-1).argmin()
        error_estimate_profile = np.array(nanobody.error_estimates[index_best_model])

        # Check quality of the model with TopModel
        struct_quality_flag, no_cc_wdv_clashes, chiral_d = check_predicted_structure(
            aho_pdb_file
        )
        count_check += 1

    if struct_quality_flag == False and count_check == max_check_iter:
        print(
            f"\n ATTENTION: Could not generate a structure for {name_seq} without liabilities (i.e., VdW clashes or D-stereoisomers)"
        )
        print(f"----> VdW clashes: {no_cc_wdv_clashes}")
        print(f"----> D-stereo: {chiral_d}")

    return (
        aho_pdb_file,
        ch_id_vh,
        ch_id_vl,
        struct_quality_flag,
        no_cc_wdv_clashes,
        chiral_d,
        error_estimate_profile,
    )


def print_chimera_mutations_code(
    wt_seq: str, hum_seq: str, pdb_file: str, ch_id: str, output_dir: str, name_seq: str
) -> Tuple[list, list]:
    """
    Print the chimera code for visualisation in .txt files. See Returns for more details.

    Parameters
    ----------
        - wt_seq: str
            WT sequence
        - hum_seq: str
            Humanised sequence with mutations
        - pdb_file: str
            Filepath to the pdb file to write the visualition code on.
        - ch_id: str
        - o_dir: str
        - name_seq: str

    Returns
    -------
        - chimeratxt: list of str
            Write  the chimera code as follows 'A21.V' for an alanine at PDB position 21
            of the chain V, useful for CamSol combination
        - chimeraXtxt: list of str
            Write chimeraX code as follows '/A:21' fon a residue at PDB position 21 which has
            been mutated, useful for visualisation"""

    chimera_output_dir = os.path.join(output_dir, "chimera_codes")

    if not os.path.exists(chimera_output_dir):
        os.makedirs(chimera_output_dir)

    # Remove alignement if there is
    wt_seq = wt_seq.replace("-", "")
    hum_seq = hum_seq.replace("-", "")

    # Compare sequence with pdb sequence to extract their PDB numbering
    chimera_codes, chimerax_codes = list(), list()
    parser = PDBParser()
    ab_chain = parser.get_structure("struct", pdb_file)[0][ch_id]

    for k, res in enumerate(ab_chain):
        resname = res.resname
        id = res.id[1]

        if resname == "HOH":
            continue

        resletter = ThreeToOne[resname]

        if resletter != wt_seq[k]:
            raise EOFError("PDB seq does not match WT seq, BE CAREFUL")

        if wt_seq[k] != hum_seq[k]:
            chimera_codes.append(resletter + str(id) + "." + ch_id)
            chimerax_codes.append(str(id))

    # Save the chimera codes
    chimera_txt = os.path.join(chimera_output_dir, f"{name_seq}_chimera_mut_codes.txt")
    with open(chimera_txt, "w") as f:
        f.write(",".join(chimera_codes))

    chimerax_txt = os.path.join(
        chimera_output_dir, f"{name_seq}_chimeraX_mut_codes.txt"
    )
    with open(chimerax_txt, "w") as f:
        f.write("/" + ch_id + ":" + ",".join(chimerax_codes))

    return chimera_txt, chimerax_codes


def rasa_selection_posi_to_humanise(
    seq,
    nat,
    is_VHH,
    fp_pdb_file: str = "pdb_file.pdb",
    ch_id: str = "H",
    threshold_rasa_score: float = 0.15,
) -> list:
    """Select the residues with a RASA score >= threshold_rasa_score.

    Parameters
    ----------
        - seq: str
            Unaligned string sequence
        - nat: str
            Type of AbNatiV nativeness to do the study on
        - is_VHH: bool
            If True, considers the VHH seed for the alignment, more suitable when aligning nanobody sequences
        - fp_pdb_file: str
            Path to the pdb file
        - ch_id: str
            Chain id of the protein in the PDB file
        - threshold_rasa_score: float
            Ratio of RASA to use as a cutoff to select residues. The higher the cutoff is
            the more solvent exposed will be the selected residues

    Returns
    -------
        - List of the selected positions"""

    selected_aho_positions = list()

    # Compute AbNatiV profile
    wt_vh_seq_abnativ_df, wt_vh_profile_abnativ_df = abnativ_scoring(
        nat,
        seq,
        batch_size=1,
        mean_score_only=False,
        do_align=True,
        is_VHH=is_VHH,
        verbose=False,
    )

    ng_df_vh_profile = wt_vh_profile_abnativ_df.loc[
        wt_vh_profile_abnativ_df["aa"] != "-"
    ]

    # Compute RASA
    p = PDBParser(QUIET=1)
    sr = ShrakeRupley()

    struct = p.get_structure(wt_vh_profile_abnativ_df["seq_id"][0], fp_pdb_file)
    sr.compute(struct, level="R")

    # Compute rasa of each res in the given pdb
    dict_rasa = dict()
    for res in struct[0][ch_id]:
        aho_id = res.id[1]
        if res.resname == "HOH":
            continue
        if aho_id == 0 or aho_id == 149:
            norm_fact = Term_resMax[res.resname]
        else:
            norm_fact = Gly_X_Gly_sasa_standard_radiiMax[res.resname]
        dict_rasa[aho_id] = (res.sasa / norm_fact, ThreeToOne[res.resname])

    # RASA selection
    for aho_posi in ng_df_vh_profile["AHo position"]:
        abnativ_res = list(
            ng_df_vh_profile[ng_df_vh_profile["AHo position"] == aho_posi]["aa"]
        )[0]
        pdb_res = dict_rasa[aho_posi][1]

        if aho_posi not in dict_rasa:
            print(
                "\n [ATTENTION] Given pdb structure is not complete, could not calculate the RASA of each residue.\n \
                  Missing residues were including by default. Please provide a complete structure or \
                  use the structure prediction option.\n"
            )
        elif abnativ_res != pdb_res:
            raise ValueError(
                f"At AHo position {aho_posi}, the residue {abnativ_res} in al_wt_seq (aligned by AbNatiV) does not match the residue {pdb_res} \
                             in the pdb file. Use the structure prediction option to avoid this problem"
            )
        else:
            if dict_rasa[aho_posi][0] >= threshold_rasa_score:
                # Framework selection
                if aho_posi in fr_aho_indices:
                    selected_aho_positions.append(aho_posi)

    return selected_aho_positions


def get_dict_pposi_allowed_muts(
    low_frequency_cutoff: float,
    nat_to_hum: str,
    is_VHH: str,
    forbidden_mut: list,
    is_brute: bool,
) -> dict:
    """Returns a dict with keys will be AHo numbers, values will be allowed substitutions
    according to the PSSM criteria (i.e., log>=0 and low_freq_cutoof) in both human V nat_to_hum and VHH (if is_VHH and is_brute)

    Parameters
    ----------
        - low_frequency_cutoff: float
        - nat_to_hum: str
            Type of humanness to improve nativeness into (VH, VKappa, VLambda).
        - is_VHH: bool
            If True, considers the VHH seed for the alignment, more suitable when aligning nanobody sequences
        - forbidden_mut: list of strs
            All residues forbidden to mutate into
        - is_brute: bool
            If False, only consider VH-PSSM allowed
            If True, also consider VHH-PSSM allowed mutation which is more restrictive (smaller space sample)

    Returns
    -------
        - dict with keys will be AHo numbers, values will be allowed substitutions
            according to the PSSM criteria

    """

    alphabet_pssm = np.array(
        [
            "-",
            "A",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "K",
            "L",
            "M",
            "N",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "V",
            "W",
            "Y",
        ]
    )

    # Fetch PSSMs data to find pssm-allowed mutations at each position
    pssms_dir = resource_filename(__name__, "pssms")

    if nat_to_hum == "VH":
        with open(os.path.join(pssms_dir, "VH_log2_pssm.npy"), "rb") as f:
            hum_log2_pssm = np.load(f)
        with open(os.path.join(pssms_dir, "VH_pssm.npy"), "rb") as f:
            hum_pssm = np.load(f)

    elif nat_to_hum == "VKappa":
        with open(os.path.join(pssms_dir, "VKappa_log2_pssm.npy"), "rb") as f:
            hum_log2_pssm = np.load(f)
        with open(os.path.join(pssms_dir, "VKappa_pssm.npy"), "rb") as f:
            hum_pssm = np.load(f)

    elif nat_to_hum == "VLambda":
        with open(os.path.join(pssms_dir, "VLambda_log2_pssm.npy"), "rb") as f:
            hum_log2_pssm = np.load(f)
        with open(os.path.join(pssms_dir, "VLambda_pssm.npy"), "rb") as f:
            hum_pssm = np.load(f)

    elif nat_to_hum == "VHH":
        with open(os.path.join(pssms_dir, "VHH_log2_pssm.npy"), "rb") as f:
            hum_log2_pssm = np.load(f)
        with open(os.path.join(pssms_dir, "VHH_pssm.npy"), "rb") as f:
            hum_pssm = np.load(f)

    if is_VHH:
        with open(os.path.join(pssms_dir, "VHH_log2_pssm.npy"), "rb") as f:
            VHH_log2_pssm = np.load(f)
        with open(os.path.join(pssms_dir, "VHH_pssm.npy"), "rb") as f:
            VHH_pssm = np.load(f)

    # keys will be AHo numbers, values will be allowed substitutions according to the PSSM criteria we have
    pssm_allowed_substitutions_at_position = {}

    for AHo in range(1, 150):
        j = AHo - 1  # switch to index
        hum_allowed = alphabet_pssm[
            np.where(
                (hum_log2_pssm[:, j] > 0) & (hum_pssm[:, j] > low_frequency_cutoff)
            )[0]
        ]

        if is_brute and is_VHH:
            VHH_allowed = alphabet_pssm[
                np.where(
                    (VHH_log2_pssm[:, j] > 0) & (VHH_pssm[:, j] > low_frequency_cutoff)
                )[0]
            ]
            pssm_allowed_substitutions_at_position[AHo] = [
                aa
                for aa in hum_allowed
                if aa in VHH_allowed and aa not in forbidden_mut
            ]
        else:
            pssm_allowed_substitutions_at_position[AHo] = [
                aa for aa in hum_allowed if aa not in forbidden_mut
            ]

    return pssm_allowed_substitutions_at_position


def get_cdr_aho_indices_ng(al_seq: str) -> Tuple[np.array, np.array, np.array]:
    """Get the cdr positions (starts at 1, not 0) without the gaps of an input AHo aligned sequence"""

    ng_cdr1, ng_cdr2, ng_cdr3 = list(), list(), list()

    nb_pre_gaps = 0
    for k, res in enumerate([*al_seq]):
        aho_k = k + 1
        if res == "-":
            nb_pre_gaps += 1
            continue
        elif aho_k in cdr1_aho_indices:
            ng_cdr1.append(aho_k - nb_pre_gaps)
        elif aho_k in cdr2_aho_indices:
            ng_cdr2.append(aho_k - nb_pre_gaps)
        elif aho_k in cdr3_aho_indices:
            ng_cdr3.append(aho_k - nb_pre_gaps)

    return np.array(ng_cdr1), np.array(ng_cdr2), np.array(ng_cdr3)


## ENHANCED SAMPLING ##


def humanise_enhanced_sampling(
    wt_seq: str,
    name_seq: str,
    nat_to_hum: str,
    is_VHH: str,
    pdb_file: str,
    ch_id: str,
    seq_dir: str,
    allowed_user_aho_positions: list,
    threshold_abnativ_score: float = 0.98,
    threshold_rasa_score: float = 0.15,
    alphabet: list = alphabet,
    perc_allowed_decrease_vhh: float = 1.5e-2,
    forbidden_mut: list = ["C", "M"],
    a: float = 0.8,
    b: float = 0.2,
    seq_ref: str = None,
    name_seq_ref: str = None,
    verbose: bool = True,
) -> str:
    """Humanise a full input WT sequence through AbNatiV with the Enhanced sampling stategy. It iteratively explores
    the mutational space aiming for rapid convergence to generate a single humanised sequence.

        - If is_VHH == True: it employs a dual-control strategy that aims to increase the AbNatiV VH-hummanness of a sequence
    while retaining its VHH-nativeness.

        - If is_VHH == False: it employs a single-control strategy that aims only to improve the AbNAtiV V{nat_to_hum}-humanness.

    See Parameters for further details.

    Parameters
    ----------
        - wt_seq: str
            Unaligned sequence string
        - name_seq: str
        - nat_to_hum: str
            Type of humanness to improve nativeness into (VH, VKappa, VLambda).
        - is_VHH: bool
            If True, considers the dual-control strategy for humanisation, and the VHH seed for the alignment, more suitable for nanobody sequences
        - pdb_file: str
            Filepath to the pdb file of the wt_seq
        - ch_id: str
            Chain id of the pfb pdb_file
        - seq_dir:str
            Directory where to save files
        - allowed_user_aho_positions: list of int
            List of AHo positions allowed by the user to make mutation on
        - threshold_abnativ_score: float
            Bellow the AbNatiV VH threshold score, a position is considered as a liability
        - threshold_rasa_score: float
            Above this threshold, the residue is considered solvent exposed and is considered for mutation
        - alphabet: list
            A list of string with the residues composing the sequences
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
        - The unaligned final humanised sequence

    """

    # Create folder
    dms_dir = os.path.join(seq_dir, "dms")
    if not os.path.exists(dms_dir):
        os.makedirs(dms_dir)

    # Compute the average dependence of mutations with DMS
    _, _, _, dms_avg_dep = compute_dms_map(
        wt_seq, nat_to_hum, is_VHH, dms_dir, alphabet, name_seq
    )

    # Rasa selection of aho positions
    if threshold_rasa_score == 0:
        allowed_rasa_aho_positions = list(range(1, 150))
    else:
        allowed_rasa_aho_positions = rasa_selection_posi_to_humanise(
            wt_seq, nat_to_hum, is_VHH, pdb_file, ch_id, threshold_rasa_score
        )

    # Intersection rasa and user allowed aho positions
    allowed_aho_positions = list(
        set(allowed_rasa_aho_positions) & set(allowed_user_aho_positions)
    )

    # Humanisation
    humanised_seq = enhanced_humanisation_of_selected_posis(
        wt_seq,
        nat_to_hum,
        is_VHH,
        name_seq,
        threshold_abnativ_score,
        allowed_aho_positions,
        dms_avg_dep,
        perc_allowed_decrease_vhh,
        forbidden_mut,
        a,
        b,
        verbose,
    )

    # Plot
    score_and_plot_abnativ_profile_with_ref(
        wt_seq,
        nat_to_hum,
        humanised_seq,
        is_VHH,
        name_seq + f"_{nat_to_hum}",
        seq_ref,
        name_seq_ref,
        seq_dir,
    )

    return humanised_seq


def enhanced_humanisation_of_selected_posis(
    wt_seq: str,
    nat_to_hum: str,
    is_VHH: bool,
    name_seq: str,
    threshold_abnativ_score: float,
    allowed_aho_positions: list,
    dms_average_dependence: list,
    perc_allowed_decrease_vhh: float,
    forbidden_mut: list = ["C", "M"],
    a: float = 0.8,
    b: float = 0.2,
    verbose: bool = False,
) -> str:
    """
    Run the sampling on a set of positions allowed_aho_positions flagged for mutation.

    Allowed mutations are PSSM-Human enriched residues.
    We mutate the positions ordered by their average dependence on other positions being mutated to
    guide the convergence towards good mutants.

    If is_VHH, employs the dual-control strategy to humanise the nanobody.
    The final sequence generated is the one which improves the most the humanness without impacting too much the
    VHH-nativeness (see single_point_mutation criteria)

    Parameters
    ----------
        - wt_seq: str
            Unaligned string sequence
        - nat_to_hum: str
            Type of humanness to improve nativeness into (VH, VKappa, VLambda).
        - is_VHH: bool
            If True, considers the dual-control strategy for humanisation, and the VHH seed for the alignment, more suitable for nanobody sequences
        - name_seq: str
        - threshold_abnativ_score: float
            Bellow the AbNatiV VH threshold score, a position is considered as a liability
        - allowed_aho_positions: list
            List of int, being the allowed AHo positions to do the mutation on
        - dms_average_dependence: list
            A list of length len(dms_map) with the average dependence for each position of dms_map
        - perc_allowed_decrease_vhh:float
            Maximun ΔVHH score decrease allowed for a mutation
        - forbidden_mut: list
            List of residues to ban for mutation i.e. ['C','M']
        - a: float
            Used in multi-objective selection function: aΔVH+bΔVHH
        - b: float
            Used in multi-objective selection function: aΔVH+bΔVHH
        - verbose: bool

    Returns
    -------
        - str: final unaligned humanised sequence

    """
    # VH assessment
    wt_vh_seq_abnativ_df, wt_vh_profile_abnativ_df = abnativ_scoring(
        nat_to_hum,
        wt_seq,
        batch_size=1,
        mean_score_only=False,
        do_align=True,
        is_VHH=is_VHH,
        verbose=False,
    )
    al_wt_seq = "".join(wt_vh_seq_abnativ_df["aligned_seq"])
    wt_vh_score = wt_vh_seq_abnativ_df[f"AbNatiV {nat_to_hum} Score"][0]
    saved_original_wt_vh_score = wt_vh_score

    # VHH assessement
    if is_VHH:
        wt_vhh_seq_abnativ_df, wt_vhh_profile_abnativ_df = abnativ_scoring(
            "VHH",
            al_wt_seq,
            batch_size=1,
            mean_score_only=False,
            do_align=False,
            verbose=False,
        )
        wt_vhh_score = wt_vhh_seq_abnativ_df["AbNatiV VHH Score"][0]
        saved_original_wt_vhh_score = wt_vhh_score

    saved_original_seq = wt_seq

    # Compute PSSM-allowed mutations at each position
    forbidden_mut += ["-"]
    low_frequency_cutoff_pssm = 0.01
    pssm_allowed_substitutions_per_aho_position = get_dict_pposi_allowed_muts(
        low_frequency_cutoff_pssm, nat_to_hum, is_VHH, forbidden_mut, is_brute=False
    )

    # Check positions with AbNatiV-VH scores
    to_mutate_aho_positions, to_mutate_dms_average_dependence = list(), list()
    for aho_posi in allowed_aho_positions:
        posi = aho_posi - 1
        if (
            wt_vh_profile_abnativ_df[f"AbNatiV {nat_to_hum} Residue Score"][posi]
            <= threshold_abnativ_score
        ):
            to_mutate_aho_positions.append(aho_posi)
            to_mutate_dms_average_dependence.append(dms_average_dependence[posi])

    flag_tried_everything = False

    nb_mut_accepted = 0
    ori_nb_pois_to_mutate = len(to_mutate_aho_positions)

    # Iterate over positions to mutate and update them when a mutation is accepted
    while len(to_mutate_aho_positions) > 0 and not flag_tried_everything:

        sorted_to_mutate_aho_positions = [
            x
            for _, x in sorted(
                zip(to_mutate_dms_average_dependence, to_mutate_aho_positions)
            )
        ]

        if verbose:
            print("To mutate positions ", sorted_to_mutate_aho_positions)

        # Mutate the positions ordered by their average depedence on other positions being mutated
        # if a mutation is accepted, update the sequence and starts the while loop again
        # if no mutations are accepted at one position, goes to the next one until the end of the list
        # and terminates humanisation (flag_tried_everything)
        for k, aho_posi in enumerate(sorted_to_mutate_aho_positions):
            print(f"AHO position being mutated {aho_posi}")
            if is_VHH:
                is_posi_mutated, al_mut_seq, mut_vh_score_best, mut_vhh_score_best = (
                    single_point_mutation(
                        al_wt_seq,
                        nat_to_hum,
                        is_VHH,
                        aho_posi,
                        wt_vh_score,
                        pssm_allowed_substitutions_per_aho_position,
                        wt_vhh_score,
                        perc_allowed_decrease_vhh,
                        a,
                        b,
                        verbose,
                    )
                )
            else:
                is_posi_mutated, al_mut_seq, mut_vh_score_best, mut_vhh_score_best = (
                    single_point_mutation(
                        al_wt_seq,
                        nat_to_hum,
                        is_VHH,
                        aho_posi,
                        wt_vh_score,
                        pssm_allowed_substitutions_per_aho_position,
                        verbose=verbose,
                    )
                )
            # Update the new WT sequence
            al_wt_seq, wt_vh_score, wt_vhh_score = (
                al_mut_seq,
                mut_vh_score_best,
                mut_vhh_score_best,
            )

            if is_posi_mutated:
                nb_mut_accepted += 1
                wt_vh_seq_abnativ_df, wt_vh_profile_abnativ_df = abnativ_scoring(
                    nat_to_hum,
                    al_wt_seq,
                    batch_size=1,
                    mean_score_only=False,
                    do_align=False,
                    verbose=False,
                )

                # Re-assess the laibles posiiotns with a low humanness score, in case a new position has now a low humanness
                to_mutate_aho_positions, to_mutate_dms_average_dependence = (
                    list(),
                    list(),
                )
                for allowed_aho_posi in allowed_aho_positions:
                    allowed_posi = allowed_aho_posi - 1
                    if (
                        wt_vh_profile_abnativ_df[f"AbNatiV {nat_to_hum} Residue Score"][
                            allowed_posi
                        ]
                        <= threshold_abnativ_score
                    ):
                        to_mutate_aho_positions.append(allowed_aho_posi)
                        to_mutate_dms_average_dependence.append(
                            dms_average_dependence[allowed_posi]
                        )

                break

            elif k + 1 == len(sorted_to_mutate_aho_positions):
                flag_tried_everything = True

    final_seq = "".join(al_wt_seq).replace("-", "")

    # Print results
    if verbose:
        print(
            f"\n{nb_mut_accepted} position(s) mutated (Could be several time at the same position) out of {ori_nb_pois_to_mutate} positions originally"
        )

    if is_VHH:
        print(
            f"\n{name_seq} WT sequence (VH: {saved_original_wt_vh_score}, VHH: {saved_original_wt_vhh_score})\n{saved_original_seq}"
        )
        print(
            f"\n{name_seq} AbNatiV humanised sequence (VH: {wt_vh_score}, VHH: {wt_vhh_score})\n{final_seq}"
        )
    else:
        print(
            f"\n{name_seq} WT sequence ({nat_to_hum}: {saved_original_wt_vh_score})\n{saved_original_seq}"
        )
        print(f"\n{name_seq} AbNatiV humanised sequence ({nat_to_hum}: {wt_vh_score})")

    count_mut = sum(1 for a, b in zip(saved_original_seq, final_seq) if a != b)

    print(f"=====> Final number of mutations {count_mut}")

    return final_seq


def single_point_mutation(
    al_wt_seq: str,
    nat_to_mut: str,
    is_VHH: str,
    aho_posi: int,
    wt_vh_score: float,
    allowed_substitutions_per_aho_position: dict,
    wt_vhh_score: float = None,
    perc_allowed_decrease_vhh: float = 1.5e-2,
    a: float = 0.8,
    b: float = 0.2,
    verbose: bool = True,
) -> Tuple[bool, str, float, float]:
    """Single point mutation of a aligned sequence scoring the AbNatiV VHH and VH nativeness.

    We select the mutant which increases the most the VH-AbNatiV score (i.e., highest ΔVH)
    and which does not decrease the VHH-AbNatiV score by more than perc_allowed_decrease_vhh decrease
    (i.e., perc_allowed_decrease_vhh decrease tolerance of ΔVHH) when is_VHH is True.

    This selection process is governed by the multi-objective function: aΔVH+bΔVHH when is_VHH is True.

    If no better mutant is found, the procedure continues to the next position.

    If a mutant is found, the sequence is updated and the process of selecting positions for mutation
    recommences to ensure no over positions are depreciated by this new mutation.

    Parameters
    ----------
        - al_wt_seq: str
            Aligned string sequence
        - nat_to_hum: str
            Type of humanness to improve nativeness into (VH, VKappa, VLambda).
        - is_VHH: bool
            If True, considers the dual-control strategy for humanisation, and the VHH seed for the alignment, more suitable for nanobody sequences
        - aho_posi: int
            AHo position to try mutations on
        - wt_vh_score: float
            AbNatiV VH sequence score, for comparison at the very end
        - allowed_substitutions_per_aho_position: dict
            Dict with keys will be AHo numbers, values will be allowed substitutions
            according to the PSSM criteria
        - wt_vhh_score: float
            AbNatiV VHH sequence score, for comparison at the very end
        - perc_allowed_decrease_vhh:float
            Maximun ΔVHH score decrease allowed for a mutation
        - a: float
            Used in multi-objective selection function: aΔVH+bΔVHH
        - b: float
            Used in multi-objective selection function: aΔVH+bΔVHH
        - verbose: bool

    Returns
    -------
        - is_posi_mutated: bool
            Flag to know if position has been mutated
        - al_mut_seq: str
            Aligned sequence of the new mutant sequence
        - mut_vh_score_best: float
            New AbNatiV VH score
        - mut_vhh_score_best: float
            New AbNatiV VHH score, it's None if is_VHH is True

    """

    posi = aho_posi - 1
    res_wt = [*al_wt_seq][posi]

    # Init with the WT as best
    res_best, ΔVH_best, ΔVHH_best, mut_vh_score_best, mut_vhh_score_best = (
        res_wt,
        0,
        0,
        wt_vh_score,
        wt_vhh_score,
    )

    for mut in allowed_substitutions_per_aho_position[aho_posi]:
        if res_wt == mut:
            continue

        mut_seq = [*al_wt_seq]
        mut_seq[posi] = mut
        mut_seq = "".join(mut_seq)

        # Score mutant
        mut_vh_seq_abnativ_df, mut_vh_profile_abnativ_df = abnativ_scoring(
            nat_to_mut,
            mut_seq,
            batch_size=1,
            mean_score_only=True,
            do_align=False,
            verbose=False,
        )
        mut_vh_score = mut_vh_seq_abnativ_df[f"AbNatiV {nat_to_mut} Score"][0]
        ΔVH = mut_vh_score - wt_vh_score
        if verbose:
            print(f"\n{res_wt} (WT) at posi {posi} tries {mut}, gives ΔVH: {ΔVH}")

        if is_VHH:
            mut_vhh_seq_abnativ_df, mut_vhh_profile_abnativ_df = abnativ_scoring(
                "VHH",
                mut_seq,
                batch_size=1,
                mean_score_only=True,
                do_align=False,
                verbose=False,
            )
            mut_vhh_score = mut_vhh_seq_abnativ_df["AbNatiV VHH Score"][0]
            ΔVHH = mut_vhh_score - wt_vhh_score
            if verbose:
                print(f'\nand gives ΔVHH" {ΔVHH}')

        # Condition acceptance the mutation
        if ΔVH >= 0:
            # Metropolis acceptance criterion
            if is_VHH:
                if ΔVHH >= 0:
                    if ΔVH >= ΔVH_best:
                        (
                            res_best,
                            ΔVH_best,
                            ΔVHH_best,
                            mut_vh_score_best,
                            mut_vhh_score_best,
                        ) = (mut, ΔVH, ΔVHH, mut_vh_score, mut_vhh_score)
                else:
                    if abs(ΔVHH) <= perc_allowed_decrease_vhh * wt_vhh_score:
                        # Select best mutation
                        if a * ΔVH + b * ΔVHH >= a * ΔVH_best + b * ΔVHH_best:
                            (
                                res_best,
                                ΔVH_best,
                                ΔVHH_best,
                                mut_vh_score_best,
                                mut_vhh_score_best,
                            ) = (mut, ΔVH, ΔVHH, mut_vh_score, mut_vhh_score)
            else:
                if ΔVH >= ΔVH_best:
                    res_best, ΔVH_best, mut_vh_score_best = mut, ΔVH, mut_vh_score

    # Print results
    if res_best == res_wt:
        if verbose:
            print(
                f"\n=> For AHo-position {posi+1}, can not find a better res with a higher humanness score than {res_wt}"
            )
        is_posi_mutated = False
    else:
        if verbose:
            print(
                f"\n=> Mutation at AHo-position {posi+1} accepted from {res_wt} to {res_best} accepted"
            )
        is_posi_mutated = True

    # Update sequence
    al_mut_seq = [*al_wt_seq]
    al_mut_seq[posi] = res_best
    al_mut_seq = "".join(al_mut_seq)

    return is_posi_mutated, al_mut_seq, mut_vh_score_best, mut_vhh_score_best


## EXHAUSTIVE SAMPLING ##


def humanise_exhaustive_sampling(
    wt_seq: str,
    nat_to_hum: str,
    is_VHH: bool,
    name_seq: str,
    pdb_file: str,
    ch_id: str,
    output_dir: str,
    pdb_dir: str,
    allowed_user_aho_positions: list,
    threshold_abnativ_score: float,
    threshold_rasa_score: float,
    perc_allowed_decrease_vhh: float = 1.5e-2,
    forbidden_mut: list = ["C", "M"],
    seq_ref: str = None,
    name_seq_ref: str = None,
    verbose: bool = True,
) -> None:
    """
    Humanise a full input WT sequence through AbNatiV with the Exhaustive sampling stategy. It assesses all mutation combinations within
    the available mutational space (PSSM-allowed mutations) and selects the best sequences (Pareto Front). It is much more computationally demanding than the
    Enhanced method. It is not recommended to use if it as to explore a lot of liable positions.

        - If is_VHH == True: it employs a dual-control strategy that aims to increase the AbNatiV VH-hummanness of a sequence
    while retaining its VHH-nativeness.

        - If is_VHH == False: it employs a single-control strategy that aims only to improve the AbNAtiV V{nat_to_hum}-humanness.

    See Parameters for further details.

    Parameters
    ----------
        - wt_seq: str
            Unaligned sequence string
        - nat_to_hum: str
            Type of humanness to improve nativeness into (VH, VKappa, VLambda).
        - is_VHH: bool
            If True, considers the dual-control strategy for humanisation, and the VHH seed for the alignment, more suitable for nanobody sequences
        - name_seq: str
        - pdb_file: str
            Filepath to the pdb file of the wt_seq
        - ch_id: str
            Chain id of the pfb pdb_file
        - output_dir:str
            Directory where to save files
        - pdb_dir: str
            Directory where to save predicted pdb structures
        - allowed_user_aho_positions: list of int
            List of AHo positions allowed by the user to make mutation on
        - threshold_abnativ_score: float
            Bellow the AbNatiV VH threshold score, a position is considered as a liability
        - threshold_rasa_score: float
            Above this threshold, the residue is considered solvent exposed and is considered for mutation
        - alphabet: list
            A list of string with the residues composing the sequences
        - perc_allowed_decrease_vhh: float
            Maximun ΔVHH score decrease allowed for a mutation
        - forbidden_mut: list
            List of residues to ban for mutation i.e. ['C','M']
        - seq_ref: str
            If None, does not plot any references in the profiles. If str, will plot it
        - name_seq_ref: str
        - verbose: bool

    Returns
    -------
        - dict with keys will be AHo numbers, values will be allowed substitutions
            according to the PSSM criteria
    """

    # Create folder
    fig_fp_save = os.path.join(output_dir, "profiles")
    if not os.path.exists(fig_fp_save):
        os.makedirs(fig_fp_save)

    # Get allowed mutations at every AHo number
    forbidden_mut += ["-"]
    low_frequency_cutoff_pssm = 0.01
    pssm_allowed_substitutions_at_position = get_dict_pposi_allowed_muts(
        low_frequency_cutoff_pssm, nat_to_hum, is_VHH, forbidden_mut, is_brute=True
    )

    # Score WT
    wt_vh_seq_abnativ_df, wt_vh_profile_abnativ_df = abnativ_scoring(
        nat_to_hum,
        wt_seq,
        batch_size=1,
        mean_score_only=False,
        do_align=True,
        is_VHH=is_VHH,
        verbose=False,
    )
    al_wt_seq = "".join(wt_vh_seq_abnativ_df["aligned_seq"])

    if is_VHH:
        wt_vhh_seq_abnativ_df, wt_vhh_profile_abnativ_df = abnativ_scoring(
            "VHH",
            wt_seq,
            batch_size=1,
            mean_score_only=False,
            do_align=True,
            is_VHH=is_VHH,
            verbose=False,
        )
    else:
        wt_vhh_seq_abnativ_df, wt_vhh_profile_abnativ_df = None, None

    # Rasa selection of aho positions
    if threshold_rasa_score == 0:
        allowed_rasa_aho_positions = list(range(1, 150))
    else:
        allowed_rasa_aho_positions = rasa_selection_posi_to_humanise(
            wt_seq, nat_to_hum, is_VHH, pdb_file, ch_id, threshold_rasa_score
        )

    # Intersection rasa and user allowed aho positions
    allowed_aho_positions = list(
        set(allowed_rasa_aho_positions) & set(allowed_user_aho_positions)
    )

    # Look at all the mutants possible based on PSSM and abnativ liabilities (VH and VHH)
    allowed_mutations_pposi = exhaustive_selection_mutation_pposi_to_humanise(
        pssm_allowed_substitutions_at_position,
        al_wt_seq,
        nat_to_hum,
        is_VHH,
        wt_vh_profile_abnativ_df,
        wt_vhh_profile_abnativ_df,
        threshold_abnativ_score,
        allowed_aho_positions,
        verbose,
    )

    inds_that_may_have_mutaitons = [
        j for j, muts in enumerate(allowed_mutations_pposi) if len(muts) > 1
    ]
    options_at_inds = [allowed_mutations_pposi[j] for j in inds_that_may_have_mutaitons]

    generator = xuniqueCombinationsPOSITIONALstr(
        options_at_inds
    )  # the only drawback of the generator approach is that it does not tell you directly how many mutations away from wt each generated sequence is
    all_seqs = [
        full_sequence_from_mut_option(muts, al_wt_seq, inds_that_may_have_mutaitons)
        for muts in generator
    ]

    fp_all_mut = os.path.join(output_dir, f"{name_seq}_all_mut_brute.fa")
    with open(fp_all_mut, "w") as f:
        for k, seq in enumerate(all_seqs):
            seq = seq[0]
            f.write(f">{k}_brute_mut\n")
            f.write(seq + "\n")

    try:
        brute_vh_seq_abnativ_df, brute_vh_profile_abnativ_df = abnativ_scoring(
            nat_to_hum,
            fp_all_mut,
            batch_size=128,
            mean_score_only=True,
            do_align=False,
            is_VHH=is_VHH,
            verbose=True,
        )

        if is_VHH:
            brute_vhh_seq_abnativ_df, brute_vhh_profile_abnativ_df = abnativ_scoring(
                "VHH",
                fp_all_mut,
                batch_size=128,
                mean_score_only=True,
                do_align=False,
                is_VHH=is_VHH,
                verbose=True,
            )
        else:
            brute_vhh_seq_abnativ_df, brute_vhh_profile_abnativ_df = None, None

        # Pareto select and plot all mutants
        exhaustive_selection_of_mutants(
            name_seq,
            nat_to_hum,
            is_VHH,
            wt_vh_seq_abnativ_df,
            wt_vhh_seq_abnativ_df,
            brute_vh_seq_abnativ_df,
            brute_vhh_seq_abnativ_df,
            perc_allowed_decrease_vhh,
            output_dir,
            pdb_dir,
            fig_fp_save,
            pdb_file,
            ch_id,
            seq_ref,
            name_seq_ref,
            verbose,
        )

    finally:
        os.remove(fp_all_mut)
    return


def exhaustive_selection_mutation_pposi_to_humanise(
    pssm_allowed_substitutions_at_position: dict,
    al_wt_seq: str,
    nat_to_hum: str,
    is_VHH: bool,
    df_vh_abnativ_profile: pd.DataFrame,
    df_vhh_abnativ_profile: pd.DataFrame,
    threshold_abnativ_score: float,
    allowed_aho_positions: list = fr_aho_indices,
    verbose: bool = True,
) -> list:
    """Returns a list of str of mutation options for each position on AbNatiV liabilities (VHH and VH) and PSMM (VHH and VH)
    allowed mutations is is_VHH. It works only on v{nat_to_hum} for other versions.

    At least return the WT res for each position. If there are potential mutants, for a position it will
    be for instance : 'AGV'.

    Parameters
    ----------
        - pssm_allowed_substitutions_at_position: dict
            dict with keys will be AHo numbers, values will be allowed substitutions
            according to the PSSM criteria
        - al_wt_seq: str
            Aligned WT sequence
        - nat_to_hum: str
            Type of humanness to improve nativeness into (VH, VKappa, VLambda).
        - is_VHH: bool
            If True, considers the VHH seed for the alignment, more suitable when aligning nanobody sequences
        - df_vh_abnativ_profile: pd.DataFrame
            AbNatiV dataframe profile of VH-assessment
        - df_vhh_abnativ_profile: pd.DataFrame
            AbNatiV dataframe profile of VHH-assessment
        -threshold_abnativ_score: float
            Bellow the AbNatiV VH threshold score, a position is considered as a liability
        - allowed_aho_positions: list
            List of int, being the allowed AHo positions to do the mutation on
        - verbose: bool

    Returns
    -------
        - dict with keys will be AHo numbers, values will be allowed substitutions
            according to the PSSM criteria
    """

    # get available mutations
    absolute_max_number_of_seqs = 1e5

    mutation_options = []
    combinatorial_space_size = 1
    liabilities_skipped_no_pssm_options = []
    flagged_as_AbNativ_liability, flagged_as_pssm_liability = [], []

    not_aho_posi = 0
    for AHo in range(1, 150):
        j = AHo - 1  # switch to index
        wt_res = al_wt_seq[j]
        mutation_options += [
            wt_res
        ]  # this is done so that at the very least there is the WT sequence as an option
        if wt_res == "-":
            continue
        not_aho_posi += 1
        if AHo not in allowed_aho_positions:
            continue
        # potentially mutable because exposed and poor humanness/nativeness

        if is_VHH:
            condition = (
                df_vh_abnativ_profile[f"AbNatiV {nat_to_hum} Residue Score"][j]
                < threshold_abnativ_score
                or df_vhh_abnativ_profile["AbNatiV VHH Residue Score"][j]
                < threshold_abnativ_score
            )
        else:
            condition = (
                df_vh_abnativ_profile[f"AbNatiV {nat_to_hum} Residue Score"][j]
                < threshold_abnativ_score
            )

        if condition:
            flagged_as_AbNativ_liability += [AHo]
            # at least one pssm allowed mutation at this liability site
            if len(pssm_allowed_substitutions_at_position[AHo]) > 0:
                mutation_options[-1] += "".join(
                    [
                        aa
                        for aa in pssm_allowed_substitutions_at_position[AHo]
                        if aa != al_wt_seq[j]
                    ]
                )  # add those that are different from WT residues
                combinatorial_space_size *= len(mutation_options[-1])
            else:
                liabilities_skipped_no_pssm_options += [AHo]
        # not a CDR position, where WT residue is not among pssm-allowed
        elif (
            len(pssm_allowed_substitutions_at_position[AHo]) > 0
            and AHo in fr_aho_indices
            and al_wt_seq[j] not in pssm_allowed_substitutions_at_position[AHo]
        ):
            flagged_as_pssm_liability += [AHo]
            mutation_options[-1] += "".join(
                [
                    aa
                    for aa in pssm_allowed_substitutions_at_position[AHo]
                    if aa != al_wt_seq[j]
                ]
            )  # add those that are different from WT residues
            combinatorial_space_size *= len(mutation_options[-1])
    if verbose:
        print("Mutation options per posi:\n", mutation_options)
        print("\ncombinatorial_space_size = %d\n" % (combinatorial_space_size))
        print(
            "flagged_as_AbNativ_liability",
            len(flagged_as_AbNativ_liability),
            flagged_as_AbNativ_liability,
        )
        print(
            "flagged_as_pssm_liability",
            len(flagged_as_pssm_liability),
            flagged_as_pssm_liability,
        )

    if combinatorial_space_size > absolute_max_number_of_seqs:
        print(
            "Exceeded absolute_max_number_of_seqs=%d recommend to abort with control+C"
            % (absolute_max_number_of_seqs)
        )

    return mutation_options


def exhaustive_selection_of_mutants(
    name_seq: str,
    nat_to_hum: str,
    is_VHH: bool,
    wt_vh_seq_abnativ_df: pd.DataFrame,
    wt_vhh_seq_abnativ_df: pd.DataFrame,
    brute_vh_seq_abnativ_df: pd.DataFrame,
    brute_vhh_seq_abnativ_df: pd.DataFrame,
    perc_allowed_decrease_vhh: float,
    output_dir: str,
    pdb_dir: str,
    fig_fp_save: str,
    pdb_file: str,
    ch_id: str,
    seq_ref: str = None,
    name_seq_ref: str = None,
    verbose: bool = True,
):
    """Select the best sequences trhough a Pareto front search that seeks to increase the V{nat_to_hum}-humanness and to
    decrease the number of mutations.

    It plots the Pareto Front results.

    If is_VHH, will apply a hard cut-off and remove all mutants with a ΔVHH decrease >= perc_allowed_decrease_vhh*VHH(WT).

    Parameters
    ----------
        - name_seq: str
        - nat_to_hum: str
            Type of humanness to improve nativeness into (VH, VKappa, VLambda).
        - is_VHH: bool
            If True, considers the dual-control strategy for humanisation, and the VHH seed for the alignment, more suitable for nanobody sequences
        - wt_vh_seq_abnativ_df: pd.DataFrame
            AbNatiV dataframe profile of VH-assessment of WT
        - wt_vhh_seq_abnativ_df: pd.DataFrame
            AbNatiV dataframe profile of VHH-assessmentv of WT
        - brute_vh_seq_abnativ_df: pd.DataFrame
            AbNatiV dataframe profile of VH-assessment of all brute sequences
        - brute_vhh_seq_abnativ_df: pd.DataFrame
            AbNatiV dataframe profile of VHH-assessmentv of all brute sequences
        - perc_allowed_decrease_vhh: float
            Maximun ΔVHH score decrease allowed for a mutation
        - output_dir:str
            Directory where to save files
        - pdb_dir: str
            Directory where to save predicted pdb structures
        -fig_fp_save: str
            Folder where to save the profiles of pareto set
        - pdb_file: str
            Filepath to the pdb file of the wt_seq
        - ch_id: str
            Chain id of the pfb pdb_file
        - seq_ref: str
            If None, does not plot any references in the profiles. If str, will plot it
        - name_seq_ref: str
        - verbose: bool

    Returns
    -------
        - dict with keys will be AHo numbers, values will be allowed substitutions
            according to the PSSM criteria
    """

    wt_seq = wt_vh_seq_abnativ_df["aligned_seq"][0]
    wt_vh_score = wt_vh_seq_abnativ_df[f"AbNatiV {nat_to_hum} Score"][0]
    if is_VHH:
        wt_vhh_score = wt_vhh_seq_abnativ_df["AbNatiV VHH Score"][0]

    allowed_hum_seqs = defaultdict(list)
    for k, id in enumerate(brute_vh_seq_abnativ_df["seq_id"]):

        ΔVH = round(
            brute_vh_seq_abnativ_df[f"AbNatiV {nat_to_hum} Score"][k] - wt_vh_score, 5
        )
        if is_VHH:
            ΔVHH = round(
                brute_vhh_seq_abnativ_df["AbNatiV VHH Score"][k] - wt_vhh_score, 5
            )

        count_mut = sum(
            1 for a, b in zip(wt_seq, brute_vh_seq_abnativ_df["input_seq"][k]) if a != b
        )

        if is_VHH and id != brute_vhh_seq_abnativ_df["seq_id"][k]:
            raise Exception("ID VH not the same than ID VHH")

        if ΔVH >= 0:
            if is_VHH:
                if ΔVHH >= -perc_allowed_decrease_vhh * wt_vhh_score:
                    allowed_hum_seqs["seq_id"].extend([id])
                    allowed_hum_seqs["VH"].extend(
                        [brute_vh_seq_abnativ_df["AbNatiV VH Score"][k]]
                    )
                    allowed_hum_seqs["VHH"].extend(
                        [brute_vhh_seq_abnativ_df["AbNatiV VHH Score"][k]]
                    )
                    allowed_hum_seqs["Diff-VH"].extend([ΔVH])
                    allowed_hum_seqs["Diff-VHH"].extend([ΔVHH])
                    allowed_hum_seqs["count_mut"].extend([count_mut])
                    allowed_hum_seqs["aligned_seq"].extend(
                        [brute_vh_seq_abnativ_df["input_seq"][k]]
                    )
            else:
                allowed_hum_seqs["seq_id"].extend([id])
                allowed_hum_seqs[f"{nat_to_hum}"].extend(
                    [brute_vh_seq_abnativ_df[f"AbNatiV {nat_to_hum} Score"][k]]
                )
                allowed_hum_seqs[f"Diff-{nat_to_hum}"].extend([ΔVH])
                allowed_hum_seqs["count_mut"].extend([count_mut])
                allowed_hum_seqs["aligned_seq"].extend(
                    [brute_vh_seq_abnativ_df["input_seq"][k]]
                )

    df_allowed_hum_seqs = pd.DataFrame.from_dict(allowed_hum_seqs)

    # paretoplot
    df_pareto = df_allowed_hum_seqs[[f"Diff-{nat_to_hum}", "count_mut"]]
    mask = paretoset(df_pareto, sense=["max", "min"])

    df_pareto = df_allowed_hum_seqs
    df_pareto_set = df_allowed_hum_seqs[mask]
    df_pareto_set.to_csv(os.path.join(output_dir, f"{name_seq}_pareto_set.csv"))
    df_pareto_set = df_pareto_set.sort_values("count_mut")

    # Print all png and structures of the pareto set
    dict_all_seqs = {name_seq + "_wt": wt_seq}
    if is_VHH:
        predict_struct_vhh(wt_seq.replace("-", ""), name_seq + "_wt", pdb_dir)

    fp_pareto_mut = os.path.join(output_dir, f"{name_seq}_pareto_mut_brute.fa")
    if verbose:
        print(
            f"\n> Select best mutant from the pareto set on ΔVH and nb of mutations space and save them in {fp_pareto_mut}.\n"
        )
    with open(fp_pareto_mut, "w") as f:
        for k, hum_seq in enumerate(df_pareto_set["aligned_seq"]):
            f.write(f">{name_seq} +{str(k)}\n")
            f.write(hum_seq.replace("-", "") + "\n")

            dict_all_seqs[name_seq + f"_{count_mut}"] = hum_seq
            count_mut = list(df_pareto_set["count_mut"])[k]
            if is_VHH:
                predict_struct_vhh(
                    hum_seq.replace("-", ""),
                    name_seq + "_exhaustive_" + str(k),
                    pdb_dir,
                )
            print_chimera_mutations_code(
                wt_seq, hum_seq, pdb_file, ch_id, pdb_dir, name_seq + str(k)
            )
            score_and_plot_abnativ_profile_with_ref(
                wt_seq.replace("-", ""),
                nat_to_hum,
                hum_seq.replace("-", ""),
                is_VHH,
                name_seq + nat_to_hum + str(count_mut),
                seq_ref,
                name_seq_ref,
                fig_fp_save,
            )

    sns.set_theme()
    sns.set(font_scale=1)
    sns.set_style(
        "white",
        {
            "axes.spines.right": True,
            "axes.spines.top": True,
            "xtick.bottom": True,
            "ytick.left": True,
        },
    )
    fig, ax = plt.subplots(figsize=(6, 6))

    cm = plt.cm.get_cmap("RdYlBu")
    plt.scatter(
        df_pareto_set["count_mut"],
        df_pareto_set[f"Diff-{nat_to_hum}"],
        color="black",
        s=80,
        label="Pareto set",
    )

    if is_VHH:
        sc = plt.scatter(
            df_pareto["count_mut"],
            df_pareto[f"Diff-{nat_to_hum}"],
            c=df_pareto["Diff-VHH"],
            s=20,
            cmap=cm,
        )
        plt.colorbar(sc, label="ΔVHH AbNatiV")

    else:
        sc = plt.scatter(
            df_pareto["count_mut"],
            df_pareto[f"Diff-{nat_to_hum}"],
            c="darkorange",
            alpha=0.7,
            s=20,
        )

    plt.xlabel("Number of mutations")
    plt.ylabel(f"ΔV{nat_to_hum} AbNatiV")
    plt.legend()
    plt.title(f"Pareto optimal set {name_seq}")
    plt.savefig(
        os.path.join(fig_fp_save, f"{name_seq}_brute_pareto_plot.png"),
        dpi=800,
        bbox_inches="tight",
    )

    # Print pap file
    print_Alignment_pap(
        dict_all_seqs, os.path.join(output_dir, f"{name_seq}_hums.pap"), nchar_id=18
    )

    return


def xuniqueCombinationsPOSITIONALstr(list_of_strings, n=None):
    """
    xuniqueCombinationsPOSITIONALstr(['abc', 'AB'] ) -->['aA', 'bA', 'cA', 'aB', 'bB', 'cB']
    N= product([len(l) for l in list_of_list_items ])
    """
    if n is None:
        n = len(list_of_strings)
    if n == 0:
        yield ""
    else:
        for i in range(len(list_of_strings)):
            for cc in xuniqueCombinationsPOSITIONALstr(list_of_strings[i + 1 :], n - 1):
                j = -1
                while j < len(list_of_strings[i]) - 1:
                    j += 1
                    yield list_of_strings[i][j] + cc


def full_sequence_from_mut_option(mut_option, wt_seq, inds_of_mutations):
    """
    # generate the full sequence for an option like 'KENAFQREVNQ', 'QENAFQREVNQ', 'KQNAFQREVNQ', ...
    # and also return number of mutations from wt
    assumes inds_of_mutations is sorted (which it should be)
    probably would be faster with a Biopython mutable_str or a list, but this should be good enough
    """
    seq = ""
    oldj = 0
    nmuts = 0
    for i, j in enumerate(inds_of_mutations):
        seq += (
            wt_seq[oldj:j] + mut_option[i]
        )  # replace in str of WT the mutation at the index
        oldj = j + 1
        if mut_option[i] != wt_seq[j]:
            nmuts += 1
    seq += wt_seq[oldj:]
    return seq, nmuts


## PLOTTING ##


def score_and_subplot_profile_with_ref(
    axs: plt.axes,
    id_subplot: int,
    seq_wt: str,
    seq_hum: str,
    seq_ref: str,
    model_type: str,
    name_seq: str,
    name_seq_ref: str,
    is_VHH: bool,
    keep_gaps: bool = False,
    legend_type: str = "HUM",
) -> None:
    """
    Plot for given plt.axes, the AbNatiV VHH and VH profiles of the WT and humanised sequences
    along with a ref sequence if provided.
    """

    df_mean_wt, df_profile_wt = abnativ_scoring(
        model_type,
        seq_wt,
        batch_size=1,
        mean_score_only=False,
        do_align=True,
        is_VHH=is_VHH,
        verbose=False,
    )
    df_mean_hum, df_profile_hum = abnativ_scoring(
        model_type,
        seq_hum,
        batch_size=1,
        mean_score_only=False,
        do_align=True,
        is_VHH=is_VHH,
        verbose=False,
    )

    seq_wt = "".join(df_profile_wt["aa"].tolist())
    seq_hum = "".join(df_profile_hum["aa"].tolist())

    scores_wt = df_profile_wt[f"AbNatiV {model_type} Residue Score"].tolist()
    scores_hum = df_profile_hum[f"AbNatiV {model_type} Residue Score"].tolist()

    # Add CDRs
    if not keep_gaps:
        cdr1, cdr2, cdr3 = get_cdr_aho_indices_ng(seq_wt)

        seq_wt = seq_wt.replace("-", "")
        seq_hum = seq_hum.replace("-", "")

        scores_wt = df_profile_wt[df_profile_wt["aa"] != "-"][
            f"AbNatiV {model_type} Residue Score"
        ].tolist()
        scores_hum = df_profile_hum[df_profile_hum["aa"] != "-"][
            f"AbNatiV {model_type} Residue Score"
        ].tolist()
    else:
        cdr1, cdr2, cdr3 = cdr1_aho_indices, cdr2_aho_indices, cdr3_aho_indices

    axs[id_subplot].axvspan(cdr1[0] - 1, cdr1[-1] - 1, alpha=0.06, color="forestgreen")
    axs[id_subplot].axvspan(cdr2[0] - 1, cdr2[-1] - 1, alpha=0.06, color="forestgreen")
    axs[id_subplot].axvspan(cdr3[0] - 1, cdr3[-1] - 1, alpha=0.06, color="forestgreen")

    wt_nativ = round(df_mean_wt[f"AbNatiV {model_type} Score"][0], 3)
    hum_nativ = round(df_mean_hum[f"AbNatiV {model_type} Score"][0], 3)

    # Add Ref sequence if required
    if seq_ref is not None:
        df_mean_ref, df_profile_ref = abnativ_scoring(
            model_type,
            seq_ref,
            batch_size=1,
            mean_score_only=False,
            do_align=True,
            is_VHH=is_VHH,
            verbose=False,
        )
        seq_ref = "".join(df_profile_ref["aa"].tolist())
        scores_ref = df_profile_ref[f"AbNatiV {model_type} Residue Score"].tolist()

        ref_nativ = round(df_mean_ref[f"AbNatiV {model_type} Score"][0], 3)
        axs[id_subplot].plot(
            scores_ref,
            linestyle="-.",
            linewidth=5,
            alpha=0.15,
            color="black",
            label=f"{name_seq_ref} (REF): {ref_nativ} AbNatiV",
        )
        axs[id_subplot].annotate(
            "$\\bf{REF~-}$",
            xy=(-4.64, 1.0175),
            xycoords="data",
            annotation_clip=False,
            fontsize=18,
        )

    axs[id_subplot].plot(
        scores_wt,
        linewidth=5,
        alpha=0.65,
        color="darkorange",
        label=f"Precursor (WT): {wt_nativ} AbNatiV",
    )
    name_legend = "Humanised"
    if legend_type == "GFT":
        name_legend = "Grafted"
    axs[id_subplot].plot(
        scores_hum,
        linestyle="--",
        linewidth=5,
        alpha=0.95,
        color="mediumpurple",
        label=f"{name_legend} ({legend_type}): {hum_nativ} AbNatiV",
    )

    # Bold selected residues mutated
    axs[id_subplot].xaxis.set_ticks(np.arange(0, len(seq_wt), 1.0))
    both_seqs = list()
    if seq_ref is not None:
        for i, res in enumerate(seq_wt):
            if res != seq_hum[i]:
                both_seqs.append(
                    seq_ref[i]
                    + "\n$\\bf{"
                    + seq_wt[i]
                    + "}$"
                    + "\n"
                    + "$\\bf{"
                    + seq_hum[i]
                    + "}$"
                )
            else:
                both_seqs.append(seq_ref[i] + "\n" + seq_wt[i] + "\n" + seq_hum[i])
    else:
        for i, res in enumerate(seq_wt):
            if res != seq_hum[i]:
                both_seqs.append(
                    "$\\bf{" + seq_wt[i] + "}$" + "\n" + "$\\bf{" + seq_hum[i] + "}$"
                )
            else:
                both_seqs.append(seq_wt[i] + "\n" + seq_hum[i])

    axs[id_subplot].set_xticklabels(both_seqs, fontsize=18)
    axs[id_subplot].tick_params(axis="x", which="major", pad=3)
    axs[id_subplot].xaxis.set_label_position("top")
    axs[id_subplot].set_ylabel(
        f"AbNatiV {model_type}\nResidue Score", fontsize=25, labelpad=14
    )
    axs[id_subplot].set_xlabel("Sequence", fontsize=25, labelpad=14)

    axs[id_subplot].xaxis.tick_top()

    # Add WT/HUM annotation
    axs[id_subplot].annotate(
        "$\\bf{(WT)}$",
        xy=(-4.65, 1.01215),
        xycoords="data",
        annotation_clip=False,
        fontsize=18,
    )
    axs[id_subplot].annotate(
        "$\\bf{(" + legend_type + ")}$",
        xy=(-5.2, 1.0075),
        xycoords="data",
        annotation_clip=False,
        fontsize=18,
    )

    if model_type == "VHH":
        subtitle = "$\\bf{VHH-Nativeness~Profiles}$"
    else:
        subtitle = "$\\bf{Humanness~Profiles}$"

    axs[id_subplot].set_title(subtitle, fontsize=28, pad=10)

    leg = axs[id_subplot].legend()
    for legobj in leg.legendHandles:
        legobj.set_linewidth(8.0)
    title_legend = "$\\bf{" + name_seq.replace("_", "~") + "}$"
    axs[id_subplot].legend(
        loc="lower left",
        title=title_legend,
        frameon=True,
        edgecolor="w",
        title_fontsize=28,
        fontsize=25,
        framealpha=0.5,
    )


def score_and_plot_abnativ_profile_with_ref(
    seq_wt: str,
    nat_to_hum: str,
    seq_hum: str,
    is_VHH: bool,
    name_seq: str,
    seq_ref: str,
    name_seq_ref: str,
    folder_save: str,
    keep_gaps: bool = False,
    legend_type: str = "HUM",
) -> None:
    """
    Plot the AbNatiV VHH and VH profiles of the WT and humanised sequences
    along with a ref sequence if provided.

    Parameters
    ----------
        - seq_wt: str
            Unaligned WT sequence
        - nat_to_hum: str
            Type of humanness to improve nativeness into (VH, VKappa, VLambda).
        - seq_hum: str
            Unaligned humanised sequence
        - is_VHH: bool
            If True, considers the VHH seed for the alignment, more suitable when aligning nanobody sequences
        - name_seq: str
        - seq_ref: str
            If None, does not plot any references in the profiles. If str, will plot it
        - name_seq_ref: str
        - folder_save: str
            Directory where to save the figures
        - keep_gaps: bool
            If True will plot with gaps
        - legend_type: str
            'HUM' or 'GRAFT'

    """

    sns.set(font_scale=2.2)
    sns.set_style(
        "white",
        {
            "axes.spines.right": False,
            "axes.spines.top": True,
            "axes.spines.bottom": False,
            "xtick.bottom": False,
            "xtick.top": True,
            "ytick.left": True,
            "xtick.labeltop": True,
        },
    )

    nb_plots = 1
    if is_VHH:
        nb_plots = 2
    if seq_ref is not None:
        fig, axs = plt.subplots(nb_plots, figsize=(40, 8 * nb_plots))
    else:
        l = len(seq_wt.replace("-", ""))
        length = 40 * l / 149
        fig, axs = plt.subplots(nb_plots, figsize=(length, 8 * nb_plots))

    # Plot VH
    if not is_VHH:
        score_and_subplot_profile_with_ref(
            [axs],
            0,
            seq_wt,
            seq_hum,
            seq_ref,
            nat_to_hum,
            name_seq,
            name_seq_ref,
            is_VHH,
            keep_gaps=keep_gaps,
            legend_type=legend_type,
        )
    else:
        score_and_subplot_profile_with_ref(
            axs,
            0,
            seq_wt,
            seq_hum,
            seq_ref,
            nat_to_hum,
            name_seq,
            name_seq_ref,
            is_VHH,
            keep_gaps=keep_gaps,
            legend_type=legend_type,
        )
        score_and_subplot_profile_with_ref(
            axs,
            1,
            seq_wt,
            seq_hum,
            seq_ref,
            "VHH",
            name_seq,
            name_seq_ref,
            is_VHH,
            keep_gaps=keep_gaps,
            legend_type=legend_type,
        )

    plt.tight_layout()
    plt.savefig(
        os.path.join(folder_save, f"abnativ_hum_profiles_{name_seq}.png"),
        dpi=250,
        bbox_inches="tight",
    )
