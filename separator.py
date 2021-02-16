import os 
from pathlib import Path
import shutil
import sys
import getopt
import random


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
    remind_diffrent_images = same_folders_count 
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
    same_folders_count = len(os.listdir(others_directory))     
    make_diffrent_folder(same_folders_count, diffrent_images_name,
                        index_directory, diffrent_directory)
    return "Done"

def check_exeist(source_path):
    first_path = os.path.join(source_path, DATASET_ALL_IMAGES_FOLDER)
    second_path = os.path.join(source_path, DATASET_ALL_IMAGES_FOLDER)
    result = (Path(first_path).exists() and Path(second_path).exists())
    return result


def main(argv):
    source_path = ''
    destination_path = ''
    try:
       opts, args = getopt.getopt(argv, "hs:d:", ["spath=", "dpath="])
    except getopt.GetoptError:
        print ('separator.py -s "source_path" -d "destination_path" \n or')
        print('separator.py --spath "source_path" -dpath "destination_path"')
        sys.exit(2)
    if args :
        print ('separator.py -h')
        sys.exit()
    for opt, arg in opts:
       if opt == '-h':
          print ('separator.py -s "source_path" -d "destination_path" \n or')
          print('separator.py --spath "source_path" -dpath "destination_path"')
          sys.exit()
       elif opt in ("-s", "--spath"):
          source_path = arg
       elif opt in ("-d", "--dpath"):
          destination_path = arg
    if source_path !='' and destination_path != '' and check_exeist(source_path):
        print('source path  is ', source_path)
        print('destination path is ', destination_path)
        print('please wait')
        result = separate_images(source_path,destination_path)
    else:
        result = "path is wrong"
    print(result)


if __name__ == "__main__":
    main(sys.argv[1:])