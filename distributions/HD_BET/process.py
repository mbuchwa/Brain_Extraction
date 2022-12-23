#!/usr/bin/env python
import argparse
import os
from distributions.HD_BET.run import run_hd_bet
from distributions.HD_BET.utils import maybe_mkdir_p, subfiles
from distributions import HD_BET


def hd_bet(input_image, output_image, device):
    """hd bet"""
    hd_parser = argparse.ArgumentParser(description='bet parser')
    hd_parser.add_argument('-mode', type=str, default='accurate', required=False)
    hd_parser.add_argument('-device', default='0', type=str, required=False)
    hd_parser.add_argument('-tta', default=1, required=False, type=int)
    hd_parser.add_argument('-pp', default=1, type=int, required=False)
    hd_parser.add_argument('-s', '--save_mask', default=1, type=int, required=False)
    hd_parser.add_argument('--overwrite_existing', default=1, type=int, required=False)
    hd_parser.add_argument("--data-dir", '-dd', default='/home/marcus/Desktop/Datasets/ADNI2_temp/ADNI/',
                           help='MRI image folder to process', type=str)
    hd_parser.add_argument("--num_saved_slices", '-ns', default=10, help='number of centered MRI slices saved as png')
    args = hd_parser.parse_args()

    if device == 'cpu':
        args.device = 'cpu'
        args.mode = 'fast'
        args.tta = 0

    """Caller function which calculates the brain extraction using HD-BET"""
    input_file_or_dir = input_image
    output_file_or_dir = output_image

    if output_file_or_dir is None:
        output_file_or_dir = os.path.join(os.path.dirname(input_file_or_dir),
                                          os.path.basename(input_file_or_dir).split(".")[0] + "_bet")
    mode = args.mode
    device = args.device
    tta = args.tta
    pp = args.pp
    save_mask = args.save_mask
    overwrite_existing = args.overwrite_existing
    params_file = os.path.join(HD_BET.__path__[0], "model_final.py")
    config_file = os.path.join(HD_BET.__path__[0], "config.py")

    assert os.path.abspath(input_file_or_dir) != os.path.abspath(
        output_file_or_dir), "output must be different from input"

    if device == 'cpu':
        pass
    else:
        device = int(device)

    if os.path.isdir(input_file_or_dir):
        maybe_mkdir_p(output_file_or_dir)
        input_files = subfiles(input_file_or_dir, suffix='.nii.gz', join=False)

        if len(input_files) == 0:
            raise RuntimeError("input is a folder but no nifti files (.nii.gz) were found in here")

        output_files = [os.path.join(output_file_or_dir, i) for i in input_files]
        input_files = [os.path.join(input_file_or_dir, i) for i in input_files]
    else:
        if not output_file_or_dir.endswith('.nii.gz'):
            output_file_or_dir += '.nii.gz'
            assert os.path.abspath(input_file_or_dir) != os.path.abspath(
                output_file_or_dir), "output must be different from input"

        output_files = [output_file_or_dir]
        input_files = [input_file_or_dir]

    if tta == 0:
        tta = False
    elif tta == 1:
        tta = True
    else:
        raise ValueError("Unknown value for tta: %s. Expected: 0 or 1" % str(tta))

    if overwrite_existing == 0:
        overwrite_existing = False
    elif overwrite_existing == 1:
        overwrite_existing = True
    else:
        raise ValueError("Unknown value for overwrite_existing: %s. Expected: 0 or 1" % str(overwrite_existing))

    if pp == 0:
        pp = False
    elif pp == 1:
        pp = True
    else:
        raise ValueError("Unknown value for pp: %s. Expected: 0 or 1" % str(pp))

    if save_mask == 0:
        save_mask = False
    elif save_mask == 1:
        save_mask = True
    else:
        raise ValueError("Unknown value for pp: %s. Expected: 0 or 1" % str(pp))

    run_hd_bet(input_files, output_files, mode, config_file, device, pp, tta, save_mask, overwrite_existing)
