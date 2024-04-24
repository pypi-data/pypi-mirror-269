import os
import sys

parent_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)

import my_functions as mf

def resize_image_max(ppath,lim):
    from PIL import Image
    image = Image.open(ppath)
    w = image.size[0]
    h = image.size[1]
    AR = w/h # aspect ratio
    if w > h:
        w = lim
        h = int(w/AR)
    else:
        h = lim
        w = int(h*AR)

    new_image = image.resize((w, h))
    new_image.save(ppath)

def batch_image_resizer(ffiles,lim=2500):
    from PIL import Image
    print(f"Resizing started -- {lim}")
    for img_path in ffiles:
        image = Image.open(img_path)
        w = image.size[0]
        h = image.size[1]
        if max(w,h) > lim:
            resize_image_max(img_path,lim)
            img_name = mf.get_filename_from_whole_path(img_path)
            print(f'--- resized "{img_name}"')
    print("All resized")

def convert_CR2_to_JPG(path_from, path_to):
    from PIL import Image

    image = Image.open(path_from)
    rgb_image = image.convert('RGB')
    rgb_image.save(path_to)

if __name__ == '__main__':
    ppath = None

    while True:
        try:
            size = input("MAX SIZE OR FOLDER: ")
            if size[1:2] == ":":
                ppath = size
                size = 2500
                break
            size = int(size)
            break
        except ValueError:
            print("Необходимо ввести число")

    if ppath is None:
        ppath = input("Ссылка на папку: ")

    ffiles = mf.list_of_files(ppath,True)
    files_to_resize = list(filter(lambda f: (f[-3:] == "jpg" or f[-4:] == "jpeg"), ffiles))
    batch_image_resizer(files_to_resize,lim=size)
