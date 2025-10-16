import subprocess, argparse, shutil, time, os, ctypes, zipfile
from PIL import Image
import pathlib as pl

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('-f', '--folder')
args = parser.parse_args()




path = pl.Path(args.folder) 

size_count = {}

for file in path.rglob('**/*'):
    if not file.is_dir():
        
        file_name = file.name 
        file_stem = file_name.split(".")[0]
        file_extension = file_name.split(".")[-1]
        if file_extension == 'png':
            size = 0
            subfolder = ""
            with Image.open(file) as img:
                size = img.size
                subfolder = "x"+str(img.size[0]) +"_y"+ str(img.size[1])
            key = str(size[0])+"-"+str(size[1])
            count = size_count.get(key,0) 
            dest = "renamed/"+size+"texture_"+str(count)+".aseprite"
            shutil.copyfile(src=file, dst= dest)
            print(file.name," -> ",str(count)+"-texture")
            count[key] = count + 1

