import subprocess, argparse, shutil, time, os, ctypes, zipfile
import pathlib as pl

texpack_name = "SillyTex"

ctypes.windll.kernel32.SetConsoleMode(
  ctypes.windll.kernel32.GetStdHandle(-11),  # -11 is the console buffer 
  7  # this enables VT processing
)

# anything with a file extension with this list
whitelist_extension = ['py','target']
# generate a target if the file extension is..
target_extension = ['png']


repositories = ["https://github.com/GregTech-Odyssey/GTOCore",
                "https://github.com/GregTech-Odyssey/GregTech-Modern"]
repo_paths = ["src/main/resources/assets","src/main/resources/assets"]

parser = argparse.ArgumentParser(
                    prog='Sillyscript',
                    description='Helps you with texturepacks!',
                    epilog='v0.1.0')
parser.add_argument('-p', '--pull',   action='store_true')
parser.add_argument('-t', '--target', action='store_true')
parser.add_argument('-b', '--build',  action='store_true')
parser.add_argument('-z', '--zip',    action='store_true')
parser.add_argument('-f', '--find',    action='store_true')
parser.add_argument('-i', '--idk',    action='store_true')

args = parser.parse_args()

def HELP_cmd():
    print(
"""By default, the program will run all four phases.
Each phase can be done seperately with these

\"py sillytex.py -p\"
\"py sillytex.py -t\"
\"py sillytex.py -b\"
\"py sillytex.py -z\"

if you struggle with naming, you can also use
to help find possible matches for source
targets that are missing targets

\"py sillyscript.py -f\"""")






class colors:
    red = '\x1b[31m'
    green = '\x1b[32m'
    yellow = '\x1b[33m'
    blue = '\x1b[34m'
    reset = '\x1b[0m'
def PULL_phase():
    print("Creating your texturepack!")
    print("Pull Phase.. getting asset directories.")
    for repo, repo_path  in zip(repositories, repo_paths):
        repo_folder_name = repo.split("/")[-1]
        copy = True
        if not os.path.isdir(repo_folder_name):
            print("[\""+repo_folder_name+"\"] downloading..")
            subprocess.call(["git", "clone", "-n", "--depth=1", "--filter=tree:0", repo])
            subprocess.call(["git", "sparse-checkout", "set", "--no-clone", repo_path],cwd=repo_folder_name)
            subprocess.call(["git","checkout", "-q"],cwd=repo_folder_name)
        else:
            print("[\""+repo_folder_name+"\"] exists already.")
            while True:
                out = input("Do you want to check for updates? (y/N)\n")
                if out == "y":
                    break
                elif out == "n":
                    copy = False
                    break
                elif out == "":
                    print("Defaulted (N)",end="\n\n")
                    copy = False
                    break
                else:
                    print("Invalid")
            if copy:
                subprocess.call(["git","pull","-q"],cwd=repo_folder_name)
        if copy:
            shutil.copytree(src=repo_folder_name  + "/"+repo_path,dst="dest",dirs_exist_ok=True)
            print("[\""+repo_folder_name+"\"] moved successfully")

def TARGET_phase():
    print("Starting the \"Target\" phase.")
    targets_directory = pl.Path("dest/")

    file_c = 0 
    dir_c = 0 
    del_c = 0 
    made_c = 0
    for file in targets_directory.rglob('**/*'):
        file_c +=1 
        delete = True
        if file.is_dir(): 
            dir_c += 1
            delete = False
        
        file_name = file.name
        file_stem = file_name.split('.')[0]
        file_extension = file_name.split('.')[-1]
        if file_extension in whitelist_extension: delete = False
        if file_extension in target_extension: 
            new_file = file.parent / f"{file.stem}.target"
            new_file.touch()
            print(colors.green + " + " + new_file.name + colors.reset)
            made_c += 1
        if delete:
            print(colors.red + " - " + file.name + colors.reset)
            file.unlink()
            del_c += 1

    print(colors.blue + "File " + str(file_c) + colors.reset)
    print(colors.blue + "Dir " + str(dir_c) + colors.reset)
    print(colors.red + "-- " + str(del_c) + colors.reset)
    print(colors.green + "++ " + str(made_c) + colors.reset)

    shutil.copytree(src="dest",dst="assets",dirs_exist_ok=True)

def BUILD_phase():
    print("Starting the \"building\" phase") 
    resourcepack_directory = pl.Path("assets/")
    source_directory = pl.Path("source/")
    # get source first
    source_files = {}
    target_files = {}

    print("Gathering Source Files")
    for file in source_directory.rglob('**/*'):
        if not file.is_dir():
            #if file.stem in source_files: source_files[file.stem] += [file]
            #else: source_files[file.stem] = [file]
            source_files[file.stem] = source_files.get(file.stem,[]) + [file]

    print("Shooting Source Files against Targets!")
    hits = 0 
    for file in resourcepack_directory.rglob('**/*'):
        if not file.is_dir():
            if file.stem in source_files:
                for source_file in source_files[file.stem]:
                    shutil.copyfile(source_file, file.parent / source_file.name)
                    del source_files[file.stem]
                    hits += 1
            else:
                target_files[file.stem] = target_files.get(file.stem,[]) + [file]

    if len(source_files) > 0:
        print("Warning, some source files are missing targets:")
        for missing in source_files:
            print(colors.red+missing+colors.reset)

    print(colors.green+"Hits: "+str(hits)              + colors.reset)
    print(colors.red+"Misses: "+str(len(source_files)) + colors.reset)


def ZIP_phase():
    print("Now Packing the resourcepack..")
    resourcepack_directory = pl.Path("assets/")
    texpack = zipfile.ZipFile(texpack_name,'w')
    texpack.write('rsp_dat/pack.mcmeta', 'pack.mcmeta')
    texpack.write('rsp_dat/pack.png', 'pack.png')
    texpack.write('assets')
    for file in resourcepack_directory.rglob('**/*'):
        if file.suffix != 'target':
            texpack.write(file)
    print("Done.")
    texpack.close()



normal_run = not (args.pull or args.target or args.build or args.zip or args.find or args.idk)

if normal_run:
    PULL_phase()
    TARGET_phase()
    BUILD_phase()
    ZIP_phase()

if args.pull: PULL_phase()
if args.target: TARGET_phase()
if args.build: BUILD_phase()
if args.zip: ZIP_phase()
if args.idk: HELP_cmd()
