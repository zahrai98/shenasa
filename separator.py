import os 
import argparse
from pathlib import Path
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('source_path', metavar='S', type=Path,
                    help='source path for getting images')
parser.add_argument("destination_path", metavar='D', type=Path,
                    help='destination path for images')
path_args = parser.parse_args()

source_path = path_args.source_path
index_directory = Path(source_path) / Path("index")
others_directory = Path(source_path) / Path("others")

destination_path = path_args.destination_path
diffrent_directory = Path(destination_path) / Path("diffrent")
same_directory = Path(destination_path) / Path("same")

# Make diffrent directory directory in destination path if dosn't exist
diffrent_directory.mkdir(parents=True, exist_ok=True)
# Make same directory in destination path if dosn't exist
same_directory.mkdir(parents=True, exist_ok=True)

def copy_to_diffrent(image_name):
    shutil.copy(Path(index_directory) / Path(image_name), diffrent_directory)

def copy_to_same(image_name, silmilar_images_list):
    shutil.copy(Path(index_directory) / Path(image_name), same_directory)
    for image_name in silmilar_images_list:
        shutil.copy(Path(others_directory) / Path(image_name), same_directory)

# Loop in index folder and find similar images in others folder
for image_name in os.listdir(index_directory): 
    image_id = image_name.replace('.jpg', '')
    similars_in_others = [
        other_image_name 
        for other_image_name in os.listdir(others_directory) 
        if other_image_name.startswith(image_id + '_')
        ]
    if len(similars_in_others):
        copy_to_same(image_name, similars_in_others)       
    else:
        copy_to_diffrent(image_name)
        