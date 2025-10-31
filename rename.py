import subprocess, argparse, shutil, time, os, ctypes, zipfile, math
import PIL
from PIL import Image
import pathlib as pl

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('-f', '--folder')
args = parser.parse_args()

path = pl.Path(args.folder) 

spritesheet_max_size = 20
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
            
            files_list[size] = files_list.get(size,[])+[file]

for key in files_list:

    chunks = [[]]
    count = 0
    fcount = 0
    for file in files_list[key]:
        chunks[-1].append(file)
        count+=1
        fcount+=1
        if count >= spritesheet_max_size**2:
            count=0
            chunks.append([])
    chunk_count = 0 
    for chunk in chunks:     
        chunk_count +=1

        amount = len(chunk)
        subfolder = "renamed/x"+str(key[0]) +"_y"+ str(key[1])
        if not pl.Path(subfolder).is_dir(): 
            pl.Path(subfolder).mkdir()

        y_length = math.ceil(math.sqrt(amount))
        x_length = math.ceil(amount/y_length)
        x = x_length * key[0]
        y = y_length * key[1]

        im = Image.new(mode="RGBA",size=[x,y],color=(0,0,0,0))
        x_iter = 0
        y_iter = 0
        for file in chunk:
            im_2 = Image.open(file)
            im.paste(im_2,(x_iter,y_iter))
            x_iter += key[0]
            if x_iter == x:
                x_iter = 0
                y_iter += key[0]
        im.save(subfolder+"/x"+str(x)+'_y'+str(y)+"_"+str(chunk_count)+".png")


        print(len(files_list[key]),str(x_length)+"x"+str(y_length))

        with open(subfolder+"/x"+str(x)+'_y'+str(y)+"_"+str(chunk_count)+".txt",'w') as ref_file:
            for file in chunk:
                ref_file.write(file.name+"\n")






