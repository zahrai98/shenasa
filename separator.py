import os 
from pathlib import Path
import shutil
import sys
import getopt


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


def copy_others_to_diffrent(index_directory, others_directory,
                            diffrent_directory, image_name,
                            silmilar_images_list):
    for image in os.listdir(others_directory):
        folder_name_reverse = image.replace('.jpg', '_') + image_name.replace('.jpg', '')
        if (not Path(make_path(diffrent_directory, folder_name_reverse)).exists() 
                and image not in silmilar_images_list):
            destination_folder_name = image_name.replace('.jpg', '_') + image.replace('.jpg', '')
            print("otherds diff",destination_folder_name)
            destination = make_directory(make_path(diffrent_directory, destination_folder_name))
            shutil.copy(make_path(index_directory,image_name), destination)
            shutil.copy(make_path(others_directory,image), destination)

    
def copy_index_to_diffrent(index_directory, diffrent_directory, image_name):
    for image in os.listdir(index_directory):
        folder_name_reverse = image.replace('.jpg', '_') + image_name.replace('.jpg', '')
        print(Path(make_path(diffrent_directory, folder_name_reverse)).exists())
        if (not Path(make_path(diffrent_directory, folder_name_reverse)).exists()  
                and image != image_name):    
            destination_folder_name = image_name.replace('.jpg', '_') + image.replace('.jpg', '')
            print("index diff",destination_folder_name)
            destination = make_directory(make_path(diffrent_directory, destination_folder_name))
            shutil.copy(make_path(index_directory,image_name), destination)
            shutil.copy(make_path(index_directory,image), destination)


def copy_to_same(index_directory, others_directory,
                same_directory, image_name,
                 silmilar_images_list):
    for image in silmilar_images_list:
        destination_folder_name = image.replace('.jpg', '')
        print("same",destination_folder_name)
        destination = make_directory(make_path(same_directory, destination_folder_name))
        shutil.copy(make_path(index_directory,image_name), destination)
        shutil.copy(make_path(others_directory,image),destination)



# Loop in index folder and find similar images in others folder
def separate_images(source_path, destination_path):
    index_directory = make_path(source_path, DATASET_ALL_IMAGES_FOLDER)
    others_directory = make_path(source_path, DATASET_SOME_IMAGES_FOLDER)
    same_directory = make_directory(make_path(destination_path, DATASET_SAME_FOLDER))
    diffrent_directory = make_directory(make_path(destination_path, DATASET_DIFFERENT_FOLDER))

    for image_name in os.listdir(index_directory):
        image_id = image_name.replace('.jpg', '')
        print(image_id)
        similars_in_others = [
            other_image_name 
            for other_image_name in os.listdir(others_directory) 
            if other_image_name.startswith(image_id + '_')
            ]
        if len(similars_in_others):
            copy_to_same(index_directory, others_directory,
                same_directory, image_name,
                similars_in_others)       
        copy_index_to_diffrent(index_directory, diffrent_directory,
            image_name)
        copy_others_to_diffrent(index_directory, others_directory,
            diffrent_directory, image_name,
            similars_in_others)
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