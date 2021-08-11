# -*- coding: utf-8 -*-
"""
Created on Wed May 19 22:01:19 2021
@author: axalo
"""

import os, shutil, math

class Checks:
    def check_exists(self, dirpath, loc):
        exists = False
        cur = os.getcwd()
        os.chdir(loc)
        if os.path.exists(dirpath):
            exists = True
        os.chdir(cur)
        return exists
    
    def dir_check(self, dirpath, loc):
        if self.check_exists(dirpath, loc):
            shutil.rmtree(dirpath)
    
    def file_check(self, filepath, loc):
        if self.check_exists(filepath, loc):
            os.remove(filepath)
    
    def round_to_even(self, val):
        return math.ceil(val / 2.) * 2

class Cleaner:
    def __init__(self, in_dir, img_dir, c, cur_dir):
        self.checks = Checks()
        self.in_dir = in_dir
        self.style = c;
        
        if cur_dir == '':
            self.cur_dir = os.getcwd()
        else:
            self.cur_dir = cur_dir

        def makeImgDir():
            path = os.path.join(self.cur_dir, img_dir)
            self.checks.dir_check(path, self.cur_dir)
            os.mkdir(path)
            return path
        
        self.img_dir = makeImgDir()
    
    def getInDir(self):
        return self.in_dir
    
    def getCurDir(self):
        return self.cur_dir
    
    def getImgDir(self):
        return self.img_dir
    
    def addImgFiles(self, subdir, f):
        og_filename = os.path.join(subdir, f)
        new_filename = os.path.join(self.img_dir, f[:-3]+"txt")
        shutil.copy(og_filename, self.img_dir)
        with open(new_filename, 'w') as txt:
            txt.write(str(self.style) + " 0.5 0.5 1 1")


class Data:
    def __init__(self):
        self.checks = Checks()
        styles = ["Impressionist", "Baroque", "Spanish Southwest", 
                  "Renaissance", "Post Impressionist", "Realist"]
        
        # This is where you put in the directory
        # [style of art, path to image directory, name of new folder, directory you want the python file to work in]
        # For the last spot, leave it blank if this file is in the same directory as your image folder
        # Below is an example/template:
        
        test = ["Impressionist", "C:/Users/axalo/OneDrive/Documents/aicamp_project/all_images", "all_imgtxt", ""]
    
        style, in_dir, img_dir, cur_dir = tuple(test)
        
        
        self.action = Cleaner(in_dir, img_dir, styles.index(style), cur_dir)
        
    def clean(self):
        for subdir, _, files in os.walk(self.action.getInDir()):
            for f in files:
                if f.endswith(".jpg"):
                    self.action.addImgFiles(subdir, f)
        return self.action.getImgDir()
    

class Split:
    def __init__(self, img_dir):
        self.checks = Checks()
        self.img_dir = img_dir
        
        #input("Path Of Split Folder Directory: ")
        tmp = ''
        
        self.loc = os.getcwd() if tmp == '' else tmp
            
        def generate_folder(folder):
            tmp = os.path.join(self.loc, folder)
            self.checks.dir_check(tmp, self.loc)
            os.mkdir(tmp)
            return tmp
                    
        self.train = generate_folder("train")
        self.valid = generate_folder("validate")
        self.test = generate_folder("test")
    
    #def addToMasterList(self, path, f):
        #with open(self.master, 'a') as master:
            #master.write(os.path.join(path, f) + "\n")
    
    def move_files(self, percentages, dest_folders):
        for _, _, files in os.walk(self.img_dir):
            n = x = 0
            length = self.checks.round_to_even((len(files) / 2) * percentages[x])
            for f in files:
                if n >= length:
                    x += 1
                    length += self.checks.round_to_even((len(files) / 2) * percentages[x])
                shutil.copy(os.path.join(self.img_dir, f), dest_folders[x])
                #self.addToMasterList(dest_folders[x], f)
                n += 0.5
    
    def fill_dirs(self):
        folders = [self.train, self.valid, self.test]
        self.move_files([0.6, 0.2, 0.2], folders)
        print("Training Images:", folders[0])
        print("Validate Images:", folders[1])
        print("Test Images:", folders[2])

if __name__ == "__main__":
    data = Data()
    src = data.clean()
    split = Split(src)
    split.fill_dirs()
    print("done")
