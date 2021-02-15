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


def make_directory(directory_name):
    directory_name.mkdir(parents=True, exist_ok=True)
    return directory_name


def make_path(first_part, second_part):
    result_path = Path(first_part) / Path(second_part)
    return result_path


    
def copy_index_to_diffrent(index_directory, diffrent_directory,
                         image_name, random_images):
    created_folders_count = 0
    for image in random_images:
        folder_name_reverse = image.replace('.jpg', '_') + image_name.replace('.jpg', '')
        if (not Path(make_path(diffrent_directory, folder_name_reverse)).exists()  
                and image != image_name):    
            destination_folder_name = image_name.replace('.jpg', '_') + image.replace('.jpg', '')
            destination = make_directory(make_path(diffrent_directory, destination_folder_name))
            shutil.copy(make_path(index_directory,image_name), destination)
            shutil.copy(make_path(index_directory,image), destination)
            created_folders_count += 1
    return created_folders_count


def copy_to_same(index_directory, others_directory,
                same_directory, image_name,
                 silmilar_images_list):
    for image in silmilar_images_list:
        destination_folder_name = image.replace('.jpg', '')
        destination = make_directory(make_path(same_directory, destination_folder_name))
        shutil.copy(make_path(index_directory,image_name), destination)
        shutil.copy(make_path(others_directory,image),destination)


def make_diffrents_folder(same_folders_count, diffrent_images_name,
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
            random_images = random.sample(os.listdir(index_directory), 1)
            remind_diffrent_images -= copy_index_to_diffrent(index_directory,
                     diffrent_directory, image_name, random_images)
            if remind_diffrent_images <= 0:
                break


# Loop in index folder and find similar images in others folder
def separate_images(source_path, destination_path):
    index_directory = make_path(source_path, DATASET_ALL_IMAGES_FOLDER)
    others_directory = make_path(source_path, DATASET_SOME_IMAGES_FOLDER)
    same_directory = make_directory(make_path(destination_path, DATASET_SAME_FOLDER))
    diffrent_directory = make_directory(make_path(destination_path, DATASET_DIFFERENT_FOLDER))

    diffrent_images_name = []

    for image_name in os.listdir(index_directory):
        image_id = image_name.replace('.jpg', '')
        similars_in_others = [
            other_image_name 
            for other_image_name in os.listdir(others_directory) 
            if other_image_name.startswith(image_id + '_')
            ]
        if len(similars_in_others):
            copy_to_same(index_directory, others_directory,
                same_directory, image_name,
                similars_in_others)
        else:
            diffrent_images_name.append(image_name)       
    same_folders_count = len(os.listdir(same_directory))
    make_diffrents_folder(same_folders_count, diffrent_images_name,
                        index_directory, diffrent_directory)
    return "Done"

def check_exeist(source_path):
    first_path = make_path(source_path, DATASET_ALL_IMAGES_FOLDER)
    second_path = make_path(source_path, DATASET_ALL_IMAGES_FOLDER)
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