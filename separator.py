import os 
from pathlib import Path
import shutil
import random
import argparse


DATASET_ALL_IMAGES_FOLDER = "index"
DATASET_SOME_IMAGES_FOLDER = "others"
DATASET_DIFFERENT_FOLDER = "different"
DATASET_SAME_FOLDER = "same"


def copy_index_to_diffrent(index_directory, diffrent_directory,
                         image_name, random_images):
    created_folders_count = 0
    for image in random_images:
        folder_name_reverse = image.replace('.jpg', '_') + image_name.replace('.jpg', '')
        if (not Path(os.path.join(diffrent_directory, folder_name_reverse)).exists()  
                and image != image_name):    
            destination_folder_name = image_name.replace('.jpg', '_') + image.replace('.jpg', '')
            destination = os.path.join(diffrent_directory, destination_folder_name)
            Path(destination).mkdir(parents=True, exist_ok=True)
            shutil.copy(os.path.join(index_directory, image_name), destination)
            shutil.copy(os.path.join(index_directory, image), destination)
            created_folders_count += 1
    return created_folders_count


def make_diffrent_folder(same_folders_count, diffrent_images_name,
                         index_directory, diffrent_directory):
    diffrent_image_count = int(same_folders_count/len(diffrent_images_name))
    remind_diffrent_images = same_folders_count + 1
    if diffrent_image_count != 0 :
        for image_name in diffrent_images_name:
            random_images = random.sample(os.listdir(index_directory), diffrent_image_count)
            remind_diffrent_images -= copy_index_to_diffrent(index_directory,
                     diffrent_directory, image_name, random_images)
    if diffrent_image_count == 0 or remind_diffrent_images != 0:
        for image_name in diffrent_images_name:
            if remind_diffrent_images <= 0:
                break
            random_images = random.sample(os.listdir(index_directory), 1)
            remind_diffrent_images -= copy_index_to_diffrent(index_directory,
                     diffrent_directory, image_name, random_images)

# Loop in index folder and find similar images in others folder
def separate_images(source_path, destination_path):
    index_directory = os.path.join(source_path, DATASET_ALL_IMAGES_FOLDER)
    others_directory = os.path.join(source_path, DATASET_SOME_IMAGES_FOLDER)
    same_directory = os.path.join(destination_path, DATASET_SAME_FOLDER)
    Path(same_directory).mkdir(parents=True, exist_ok=True)
    diffrent_directory = os.path.join(destination_path, DATASET_DIFFERENT_FOLDER)
    Path(diffrent_directory).mkdir(parents=True, exist_ok=True)

    diffrent_images_name = []
    for image_name in os.listdir(index_directory):
        similar_image = False
        image_id = image_name.replace('.jpg', '')
        for other_image_name in os.listdir(others_directory):
            if other_image_name.startswith(image_id + '_'):
                similar_image = True
                destination_folder_name = other_image_name.replace('.jpg', '')
                destination = os.path.join(same_directory, destination_folder_name)
                Path(destination).mkdir(parents=True, exist_ok=True)
                shutil.copy(os.path.join(index_directory,image_name), destination)
                shutil.copy(os.path.join(others_directory,other_image_name), destination)
        if not similar_image:
            diffrent_images_name.append(image_name)  
    make_diffrent_folder(len(os.listdir(others_directory)), diffrent_images_name,
                        index_directory, diffrent_directory)

def check_exeist(source_path):
    first_path = os.path.join(source_path, DATASET_ALL_IMAGES_FOLDER)
    second_path = os.path.join(source_path, DATASET_SOME_IMAGES_FOLDER)
    result = (Path(first_path).exists() and Path(second_path).exists())
    return result

def parse_argument():
    source_path, destination_path = None, None
    parser = argparse.ArgumentParser()
    parser.add_argument("SourcePath", help="source path that contain index and others")
    parser.add_argument("DestinationPath",
                        help="destination path that same and different will create")
    args = parser.parse_args()
    if check_exeist(args.SourcePath):
        source_path, destination_path = args.SourcePath, args.DestinationPath
    else:
        print("Index or others folder does not exist or")
        print("You have not entered the quotation mark for paths")
        print("command:separator.py 'source_path' 'destination_path'")
    return source_path, destination_path


if __name__ == "__main__":
    source_path, destination_path = parse_argument()
    if source_path and destination_path:
        separate_images(source_path, destination_path)
