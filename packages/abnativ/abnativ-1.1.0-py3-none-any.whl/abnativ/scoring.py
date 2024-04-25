# (c) 2023 Sormannilab and Aubin Ramon
#
# Lightning testing of the AbNatiV model.
#
# ============================================================================

from .model.scoring_functions import abnativ_scoring
import argparse
import os

from .update import PRETRAINED_MODELS_DIR

def run(args: argparse.Namespace):

    # Check that models are downloaded
    if not os.path.exists(PRETRAINED_MODELS_DIR):
        raise Exception("Models not found. Please run 'abnativ update' to download the models.")

    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)

    ## DATA SCORING ##
    batch_size = 128
    abnativ_df_mean, abnativ_df_profile = abnativ_scoring(args.nativeness_type, args.input_filepath_or_seq, batch_size, args.mean_score_only,
                                                          args.do_align, args.is_VHH, args.is_plotting_profiles, args.output_directory, args.output_id)

    ## DATA SAVING ##
    #print(f'\n-> Scores being saved in {args.output_directory}\n')
    abnativ_df_mean.to_csv(os.path.join(args.output_directory, f'{args.output_id}_abnativ_seq_scores.csv'))
    if not args.mean_score_only:
        abnativ_df_profile.to_csv(os.path.join(args.output_directory, f'{args.output_id}_abnativ_res_scores.csv'))
    if args.is_plotting_profiles:
        save_profile_fp = os.path.join(args.output_directory, f'{args.output_id}_profiles')
        #print(f'\n-> Profile plots saved in {save_profile_fp}\n')






