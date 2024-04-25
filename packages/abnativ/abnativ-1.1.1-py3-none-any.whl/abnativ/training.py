# (c) 2023 Sormannilab and Aubin Ramon
#
# Training of the AbNatiV model with the Pytorch Lightning module.
#
# ============================================================================

from .model.abnativ import AbNatiV_Model
from .model.onehotencoder import data_loader_masking_bert_onehot_fasta
from .model.alignment.align_and_clean import anarci_alignments_of_Fv_sequences

import os
import argparse
import yaml

import pytorch_lightning as pl
from pytorch_lightning.loggers import MLFlowLogger
from pytorch_lightning.callbacks import ModelCheckpoint


def run(args: argparse.Namespace):

      ## BUILDING MODULES ##
      with open(args.hparams, 'r') as f: 
            hparams = yaml.safe_load(f)

      model = AbNatiV_Model(hparams)
      
      ## ALIGNMENT ##
      if args.do_align:
            #Train
            print(f'\n### ANARCI alignment of {args.train_filepath}###\n')
            VH,VK,VL,failed,mischtype = anarci_alignments_of_Fv_sequences(args.train_filepath, isVHH=args.is_VHH, del_cyst_misalign=True)
            VH.add(VK)
            VH.add(VL)
            fp_al_train_fa = 'temp_al_train_seqs.fa'
            VH.Print(fp_al_train_fa)

            #Val
            print(f'\n### ANARCI alignment of {args.val_filepath}###\n')
            VH,VK,VL,failed,mischtype = anarci_alignments_of_Fv_sequences(args.val_filepath, isVHH=args.is_VHH, del_cyst_misalign=True)
            VH.add(VK)
            VH.add(VL)
            fp_al_val_fa = 'temp_al_val_seqs.fa'
            VH.Print(fp_al_val_fa)
      else:
            fp_al_train_fa = args.fp_train_data
            fp_al_val_fa = args.fp_val_data


      ## DATA LOADING ##
      train_loader = data_loader_masking_bert_onehot_fasta(fp_al_train_fa, hparams['batch_size'],
                        hparams['perc_masked_residues'], is_masking=True)
      val_loader = data_loader_masking_bert_onehot_fasta(fp_al_val_fa, hparams['batch_size'],
                        perc_masked_residues=0, is_masking=False)

      ## TRAINING ##
      # fix seed for reproductibility
      pl.seed_everything(11)

      # Logging
      logger = MLFlowLogger(experiment_name=args.model_name, run_name=args.run_name)

      # Checkpointing
      ckpt_root_dir = os.path.join('checkpoints', args.run_name)
      ckpt_callback = ModelCheckpoint(ckpt_root_dir, save_top_k=-1) # to save every epoch

      trainer = pl.Trainer(limit_train_batches=1, limit_val_batches=hparams['limit_val_batches'], max_epochs=hparams['max_epochs'], 
                              deterministic=True, accelerator='auto', logger=logger, callbacks=[ckpt_callback])

      # Training 
      trainer.fit(model, train_dataloaders=train_loader, val_dataloaders=val_loader)

      # Remove temporary files
      if args.do_align:
            os.remove(fp_al_train_fa)
            os.remove(fp_al_val_fa)







