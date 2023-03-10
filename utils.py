import os.path
import nibabel as nib
import numpy as np
import cv2


def save_slices_as_png(n4_bet_resampled_image_name, save_folder, image_name, slice_number=None):
    """Save *slice_number* middle slices.
    If flag slice_number == None, then all slices are saved"""
    image = nib.load(n4_bet_resampled_image_name)
    image_array = np.array(image.dataobj)
    image_array = image_array[:, :, :]
    image_array_pixels = (255 * image_array / image_array.max()).astype(np.int32)
    n_slices = image_array_pixels.shape[2]
    save_folder = f"{save_folder}/slices_{image_name.rstrip('.nii')}/"
    if not os.path.isdir(save_folder):
        os.mkdir(save_folder)
    if slice_number == 'None' or slice_number is None:
        for z_slice_number in range(n_slices):
            slice = image_array_pixels[:, :, z_slice_number]
            cv2.imwrite(f"{save_folder}{z_slice_number}.png", slice)
    elif int(slice_number) > 0:
        slice_number = int(slice_number)
        print(f'save {slice_number} middle slices...')
        middle_slices = image_array_pixels[:, :, int(n_slices / 2) - int(slice_number/2):int(n_slices / 2) + int(slice_number/2) + 1]
        for z_slice_number in range(middle_slices.shape[2]):
            slice = middle_slices[:, :, z_slice_number]
            cv2.imwrite(f"{save_folder}{z_slice_number}.png", slice)
    else:
        assert ValueError('slice_number must be an integer > 0 or None')

