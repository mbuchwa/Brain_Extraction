from nilearn import datasets
import os
import ants

from utils import save_slices_as_png
from distributions.HD_BET.main import hd_bet

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--data_dir', '-d', default='/home/marcus/Desktop/Datasets/ADNI2_temp/ADNI/',
                        help='MRI image folder to process')
    args = parser.parse_args()

    for filename in os.listdir(args.data_dir):
        print(f'\n ################## processing patient image: {filename} ################## \n')
        ptid_folder = os.path.join(args.data_dir, filename)
        image_names = [x for x in os.listdir(ptid_folder) if x.endswith('.nii')]
        for image_name in image_names:
            image_path = f'{ptid_folder}/{image_name}'
            bet_image_path = f'{image_path}_bet.nii.gz'
            n4_bet_resampled_image_path = f'{image_path}_bet_resampled.nii.gz'

            """Run HD-BET"""
            hd_bet(image_path, bet_image_path)

            """Run BFC"""
            input_image = ants.image_read(bet_image_path)
            print('bias field correction and resampling...')
            bfc_image = ants.n4_bias_field_correction(input_image)

            """Resample Image to MNI152 shape"""
            bfc_image_resampled = ants.resample_image(bfc_image, (197, 233, 189), True, 0)
            mni152 = datasets.load_mni152_template(resolution=1)
            mi = ants.from_nibabel(mni152)

            """Registration using ANTsPy"""
            print('registration to mni152...')
            mytx = ants.registration(fixed=mi, moving=bfc_image_resampled, type_of_transform='SyNRA')
            ants.image_write(mytx['warpedmovout'], n4_bet_resampled_image_path)

            """Save middle slices"""
            save_slices_as_png(n4_bet_resampled_image_path, ptid_folder, slice_number=10)

