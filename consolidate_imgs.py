# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 19:13:33 2021
@author: axalo
"""

import os, shutil, zipfile, random

class Tools: #provide basic mechanisms
    def adding_images(self, dirpath, loc):
        exists = False
        cur = os.getcwd()
        os.chdir(loc)
        if os.path.exists(dirpath):
            exists = True
        os.chdir(cur)
        return exists
    
    def dir_len(self, dirpath):
        return sum(len(files) for _, _, files in os.walk(dirpath)) - 1

class Imgs: #class to house rest of functions
    def __init__(self):
        # Windows: "C:/Users/username/.../project/"
        # Linux/MacOS: "/Users/username/.../project/"
        self.tools = Tools()
        self.image_folders = []
        self.in_dir = "C:/Users/axalo/OneDrive/Documents/aicamp_project/image_folders_2/" #directory with your image folders goes here
        self.out_dir = "C:/Users/axalo/OneDrive/Documents/aicamp_project/" #directory to place cleaned image folder in
        
        print("Images will be taken from folders in {} and a new folder will be placed in {}".format(self.in_dir, self.out_dir))
        proceed = input("Proceed? (y/n): ")
        if proceed != "y":
            raise Exception("Mistake in user input")
        
        self.new_folder = os.path.join(self.out_dir, "all_images/")
        self.unzipped_folders = os.path.join(self.out_dir, "unzipped_img_folders/")
        if not self.tools.adding_images(self.new_folder, self.out_dir):
            os.mkdir(self.new_folder)
            self.count_imgs = 0
            self.adding_imgs = False
        else:
            self.count_imgs = self.tools.dir_len(self.new_folder)
            self.adding_imgs = True
        
        os.mkdir(self.unzipped_folders)
            
    def extract(self): #unzip images into temporary folders
        def delete_non_imgs():
            for s, _, tmpfiles in os.walk(pathname):
                for tmpfile in tmpfiles:
                    if not tmpfile.startswith("default"):
                        os.remove(os.path.join(s, tmpfile))
                        
        for subdir, _, files in os.walk(self.in_dir):
            num = 0
            for f in files:
                pathname = os.path.join(self.unzipped_folders, "images" + str(num))
                self.image_folders.append(pathname)
                f = os.path.join(subdir, f)
                with zipfile.ZipFile(f, 'r') as z:
                    z.extractall(pathname)
                    delete_non_imgs()
                num += 1
    
    def consolidate(self): #consolidate images from folders into one
        def get_new_name():
            imgnum = random.choice(numlist)
            numlist.remove(imgnum)
            return os.path.join(subdir, "impressionist_" + str(imgnum) + ".jpg") #put your art style here
        
        numlist = [i for i in range(self.count_imgs, self.tools.dir_len(self.unzipped_folders) + 1 + self.count_imgs)]
        
        for subdir, _, files in os.walk(self.unzipped_folders):
            for f in files:
                old_name = os.path.join(subdir, f)
                new_name = get_new_name()
                os.rename(old_name, new_name)
                shutil.copy(new_name, self.new_folder)
    
    def delete_dups(self): #delete duplicate images based on bit size    
        for subdir, _, files in os.walk(self.unzipped_folders):
            for f in files:
                if f.endswith(".png") or f.endswith(".jpg"):
                    path = os.path.join(subdir, f)
                    if os.path.getsize(path) > 1000000:
                        os.remove(path)
                else:
                    raise Exception("Non-png/jpg item found in directory")
    
    def display_paths(self): #return new path folders for train/test/valid
        print("\n" + "New Folder: " + self.new_folder[:-1]) #returns path to be used with structure_data.py
    
    def clear_tmp_folders(self): #remove preexisting folderss
        shutil.rmtree(self.unzipped_folders)
    
    def clean(self): #wrapper
        self.display_paths()
        self.extract()
        self.delete_dups()
        self.consolidate()
        self.clear_tmp_folders()

if __name__ == "__main__":
    imgs = Imgs()
    imgs.clean()
    print("done")
