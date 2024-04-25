# (c) 2023 Sormannilab and Aubin Ramon
#
# Humanisation of VHH sequences using AbNatiV VH and VHH assesments.
#
# ============================================================================

from .model.scoring_functions import fr_aho_indices
from .humanisation.vh_vl_humanisation_functions import abnativ_vh_vl_humanisation

import argparse

def run(args: argparse.Namespace):

    abnativ_vh_vl_humanisation(args.input_seq_vh,args.input_seq_vl, args.output_id, args.output_directory, args.pdb_file, args.ch_id_vh,
                               args.ch_id_vl, fr_aho_indices, args.is_Exhaustive, args.threshold_abnativ_score, args.threshold_rasa_score, 
                               args.forbidden_mut, verbose=True)

    

    

    





