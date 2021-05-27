# -*- coding: utf-8 -*-
"""
Created on Wed May 26 20:27:35 2021

@author: axalo
"""

import os

in_dir = input("Image Directory: ")

for subdir, dirs, files in os.walk(in_dir):
    for f in files:
        f = os.path.join(subdir, f)
        if os.path.getsize(f) > 1000000:
            os.remove(f)

print("done")