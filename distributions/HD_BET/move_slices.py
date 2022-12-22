import os

adni_images_path = '/home/marcus/Desktop/Datasets/ADNI2/ADNI/'
adni_slices_path = '/home/marcus/Desktop/Datasets/ADNI2/slices/'
os.mkdir(adni_slices_path)

"""Move brain slice images to new directory"""
for filename in os.listdir(adni_images_path):
    print(f'\n ################## processing patient image: {filename} ################## \n')
    ptid_folder = os.path.join(adni_images_path, filename)
    png_names = [x for x in os.listdir(ptid_folder) if x.endswith('.png')]
    os.mkdir(os.path.join(ptid_folder, f'brain_slices'))
    for png_name in png_names:
        os.rename(os.path.join(ptid_folder, png_name), os.path.join(os.path.join(ptid_folder, f'brain_slices'), png_name))

for filename in os.listdir(adni_images_path):
    ptid_folder = os.path.join(adni_images_path, filename)
    os.rename(os.path.join(ptid_folder, f'brain_slices'), os.path.join(adni_slices_path, filename))
