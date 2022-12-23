from nilearn import datasets
import os
import ants
import argparse

from utils import save_slices_as_png
from distributions.HD_BET.process import hd_bet


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", '-dd', default='/home/marcus/Desktop/Datasets/test/',
                        help='MRI image folder to process', type=str)
    parser.add_argument("--num_saved_slices", '-ns', default=10,
                        help='number of centered MRI slices saved as png, if None than all slices are saved as png.')
    parser.add_argument('-device', default='0', type=str, required=False)

    args, unknown = parser.parse_known_args()
    data_dir = args.data_dir
    num_slices = args.num_saved_slices
    device = args.device
    for filename in os.listdir(data_dir):
        print(f'\n ################## processing patient image: {filename} ################## \n')
        ptid_folder = os.path.join(data_dir, filename)
        image_names = [x for x in os.listdir(ptid_folder) if x.endswith('.nii')]
        for image_name in image_names:
            image_path = f'{ptid_folder}/{image_name}'
            bet_image_path = f'{image_path}_bet.nii.gz'
            bet_bfc_image_path = f'{image_path}_bet_bfc.nii.gz'
            n4_bet_resampled_image_path = f'{image_path}_bet_bfc_registered.nii.gz'

            """Run HD-BET"""
            hd_bet(image_path, bet_image_path, device)

            """Run BFC"""
            input_image = ants.image_read(bet_image_path)
            print('bias field correction and resampling...')
            bfc_image = ants.n4_bias_field_correction(input_image)
            ants.image_write(bfc_image, bet_bfc_image_path)

            """Resample Image to MNI152 shape"""
            bfc_image_resampled = ants.resample_image(bfc_image, (197, 233, 189), True, 0)
            mni152 = datasets.load_mni152_template(resolution=1)
            mi = ants.from_nibabel(mni152)

            """Registration using ANTsPy"""
            print('registration to mni152...')
            mytx = ants.registration(fixed=mi, moving=bfc_image_resampled, type_of_transform='SyNRA')
            ants.image_write(mytx['warpedmovout'], n4_bet_resampled_image_path)

            """Save middle slices"""
            print('saving slices as png...')
            save_slices_as_png(n4_bet_resampled_image_path, ptid_folder, image_name, slice_number=num_slices)
