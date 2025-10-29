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
files_list = {}

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
            dest_folder = pl.Path("renamed/"+subfolder)
            if not dest_folder.is_dir(): 
                dest_folder.mkdir()

            dest = "renamed/"+subfolder+"/texture_"+str(count)+".png"
            shutil.copyfile(src=file, dst= dest)
            print(file.name," -> ",str(count)+"-texture")
            ref_line = file.stem+"\n"
            files_list[size] = files_list.get(size,"")+ref_line
            size_count[key] = count + 1
    
for key in files_list:
    subfolder = "x"+str(key[0]) +"_y"+ str(key[1])
    with open('renamed/'+subfolder+"/ref.txt",'w') as ref_file:
        ref_file.write(files_list[key])

