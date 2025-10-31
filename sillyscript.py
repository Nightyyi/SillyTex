import subprocess, argparse, shutil, time, os, ctypes, zipfile, math, platform, json
import pathlib as pl
import script_data.lib.sillyfuzzy as sillyfuzzy

texpack_name = "SillyTex"


if platform.system() == "Windows":
    ctypes.windll.kernel32.SetConsoleMode(
      ctypes.windll.kernel32.GetStdHandle(-11),  # -11 is the console buffer 
      7  # this enables VT processing
    )




class Settings:
    def __init__(self):
        settings_path = pl.Path('script_data/config.json')
        if not settings_path.exists():
            self.source_file_whitelist_extension = ['.png']
            self.whitelist_extension = ['py','target']
            self.target_extension = ['png']
            self.repositories = []
            self.repo_paths = []
        else:
            settings_json = settings_path.read_text()
            self.deserialize(json.loads(settings_json))

    def serialize(self):
        new_dict = {'source_file_whitelist_extension':self.source_file_whitelist_extension,
                'whitelist_extension':self.whitelist_extension,
                'target_extension':self.target_extension,
                'repositories':self.repositories,
                'repo_paths':self.repo_paths,
                }
        return new_dict

    def deserialize(self,a_dict):
        self.source_file_whitelist_extension = a_dict['source_file_whitelist_extension']
        self.whitelist_extension             = a_dict['whitelist_extension'            ]
        self.target_extension                = a_dict['target_extension'               ]
        self.repositories                    = a_dict['repositories'                   ]
        self.repo_paths                      = a_dict['repo_paths'                     ]

    def save(self):
        settings_path = pl.Path('script_data/config.json')
        with settings_path.open("w") as json_file:
            json_file.write(json.dumps(self.serialize()))

    def __str__(self):
        string = ""

        string += colors.yellow+"Repositories: \n"+colors.cyan
        for elem in self.repositories:
            string += "   "+elem+'\n'
        if not len(self.repositories):
            string += colors.red+"   NONE\n"+colors.reset

        string += colors.magenta+"Repository Paths: \n"+colors.cyan
        for elem in self.repo_paths:
            string += "   "+elem+'\n'
        if not len(self.repo_paths):
            string += colors.red+"   NONE\n"+colors.reset

        string+=colors.green+"you can edit these ones.\n\n"+colors.reset

        string += colors.green+"Sourcefile extension whiteist: \n"+colors.cyan
        for elem in self.source_file_whitelist_extension:
            string += "   "+elem+'\n'
        if not len(self.source_file_whitelist_extension):
            string += colors.red+"   NONE\n"+colors.reset


        string += colors.blue+"Extension whitelist: \n"+colors.cyan
        for elem in self.whitelist_extension:
            string += "   "+elem+'\n'
        if not len(self.whitelist_extension):
            string += colors.red+"   NONE\n"+colors.reset
        
        string += colors.blue+"Extension targets: \n"+colors.cyan
        for elem in self.target_extension:
            string += "   "+elem+'\n'
        if not len(self.target_extension):
            string += colors.red+"   NONE\n"+colors.reset


        string+=colors.reset
        string+=colors.red+"only edit these if you know what your doing.\n"+colors.reset
        string+="\n\n"
        string+="     sillyscript.py -c edit_r        to edit repositories, paths\n"
        string+="     sillyscript.py -c edit_sw       to edit sourcefile whitelists\n"
        string+="     sillyscript.py -c edit_w        to edit whitelists\n"
        string+="     sillyscript.py -c edit_te       to edit extension targets\n"


        return string 


SETTINGS_global = Settings()





# whitelist anything with a file extension within this list
source_file_whitelist_extension = ['.png']
# anything with a file extension within this list
whitelist_extension = ['py','target']
# generate a target if the file extension is..
target_extension = ['png']

find_max_suggestions = 5
GLOBAL_PROGRESS_BAR_PRECISION = 4 
GLOBAL_PROGRESS_BAR_SIZE = 30 #characters

repositories =  SETTINGS_global.repositories 
               
repo_paths = SETTINGS_global.repo_paths 

parser = argparse.ArgumentParser(
                    prog='Sillyscript',
                    description='Helps you with texturepacks!',
                    epilog='v0.1.0')
parser.add_argument('-r', '--run',   action='store_true')
parser.add_argument('-p', '--pull',   action='store_true')
parser.add_argument('-t', '--target', action='store_true')
parser.add_argument('-b', '--build',  action='store_true')
parser.add_argument('-u', '--update',  action='store_true')
parser.add_argument('-z', '--zip',    action='store_true')
parser.add_argument('-f', '--find',    action='store_true')
parser.add_argument('-c', '--config',nargs='?', const="none")

args = parser.parse_args()




def check_same(check,against,min_len = 1):
    check = check.lower()
    against = against.lower()
    if len(check) < min_len: return 0
    if len(check) > len(against): return 0
    c = 0 
    for let in (check):
        if let != against[c]: return 0
        c+=1
    return 1

def config_ask():
    print("hi")

def is_valid_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def SET_CONFIG():
    show_tip = True

    if args.config.lower() == "edit_w":
        show_tip = False
        in_progress = True
        while in_progress:
            l_count = 0
            c = 0
            for x in SETTINGS_global.whitelist_extension:
                print(str(c)+" "+x)
                l_count+=1
                c += 1
            if len(SETTINGS_global.whitelist_extension) == 0:
                print(colors.red+"none"+colors.reset)
                l_count+=1
            got_text = input("[d-delete] [a-add] [e-exit]\n")
            l_count+=2

            if check_same(got_text, 'delete'):
                delete_index = input("Delete (index), leave empty/non-numeric to exit:\n    ")
                l_count+=2
                if is_valid_integer(delete_index):
                    SETTINGS_global.whitelist_extension.pop(int(delete_index))
                else:
                    print("exited")
                    time.sleep(0.25)
                    l_count+=1

            if check_same(got_text, 'add'):
                new_whitelist = input("Repository path:\n    ")
                l_count+=2
                SETTINGS_global.whitelist_extension.append(new_whitelist)

            if check_same(got_text, 'exit',0):
                in_progress = False

            for x in range(0,l_count):
                print("\r",flush=True,end="")
                print("\b",flush=True,end="")
                print("\033[1A",flush=True,end="")
                print(" "*100,flush=True,end="")
                print("\r",flush=True,end="")

    # not done
    if args.config.lower() == "edit_te":
        show_tip = False
        in_progress = True
        while in_progress:
            l_count = 0
            c = 0
            for x,y in zip(SETTINGS_global.repositories,SETTINGS_global.repo_paths):
                print(str(c)+" "+x+", "+y)
                l_count+=1
                c += 1
            if len(SETTINGS_global.repositories) == 0:
                print(colors.red+"none"+colors.reset)
                l_count+=1
            got_text = input("[d-delete] [a-add] [e-exit]\n")
            l_count+=2

            if check_same(got_text, 'delete'):
                delete_index = input("Delete (index), leave empty/non-numeric to exit:\n    ")
                l_count+=2
                if is_valid_integer(delete_index):
                    SETTINGS_global.repositories.pop(int(delete_index))
                    SETTINGS_global.repo_paths.pop(int(delete_index))
                else:
                    print("exited")
                    time.sleep(0.25)
                    l_count+=1

            if check_same(got_text, 'add'):
                new_repo_name = input("Repository link:\n    ")
                l_count+=2
                new_repo_path = input("Repository path:\n    ")
                l_count+=2
                SETTINGS_global.repositories.append(new_repo_name)
                SETTINGS_global.repo_paths.append(new_repo_path)

            if check_same(got_text, 'exit',0):
                in_progress = False

            for x in range(0,l_count):
                print("\r",flush=True,end="")
                print("\b",flush=True,end="")
                print("\033[1A",flush=True,end="")
                print(" "*100,flush=True,end="")
                print("\r",flush=True,end="")

    # not done
    if args.config.lower() == "edit_sw":
        show_tip = False
        in_progress = True
        while in_progress:
            l_count = 0
            c = 0
            for x,y in zip(SETTINGS_global.repositories,SETTINGS_global.repo_paths):
                print(str(c)+" "+x+", "+y)
                l_count+=1
                c += 1
            if len(SETTINGS_global.repositories) == 0:
                print(colors.red+"none"+colors.reset)
                l_count+=1
            got_text = input("[d-delete] [a-add] [e-exit]\n")
            l_count+=2

            if check_same(got_text, 'delete'):
                delete_index = input("Delete (index), leave empty/non-numeric to exit:\n    ")
                l_count+=2
                if is_valid_integer(delete_index):
                    SETTINGS_global.repositories.pop(int(delete_index))
                    SETTINGS_global.repo_paths.pop(int(delete_index))
                else:
                    print("exited")
                    time.sleep(0.25)
                    l_count+=1

            if check_same(got_text, 'add'):
                new_repo_name = input("Repository link:\n    ")
                l_count+=2
                new_repo_path = input("Repository path:\n    ")
                l_count+=2
                SETTINGS_global.repositories.append(new_repo_name)
                SETTINGS_global.repo_paths.append(new_repo_path)

            if check_same(got_text, 'exit',0):
                in_progress = False

            for x in range(0,l_count):
                print("\r",flush=True,end="")
                print("\b",flush=True,end="")
                print("\033[1A",flush=True,end="")
                print(" "*100,flush=True,end="")
                print("\r",flush=True,end="")
    
    if args.config.lower() == "edit_r":
        show_tip = False
        in_progress = True
        while in_progress:
            l_count = 0
            c = 0
            for x,y in zip(SETTINGS_global.repositories,SETTINGS_global.repo_paths):
                print(str(c)+" "+x+", "+y)
                l_count+=1
                c += 1
            if len(SETTINGS_global.repositories) == 0:
                print(colors.red+"none"+colors.reset)
                l_count+=1
            got_text = input("[d-delete] [a-add] [e-exit]\n")
            l_count+=2

            if check_same(got_text, 'delete'):
                delete_index = input("Delete (index), leave empty/non-numeric to exit:\n    ")
                l_count+=2
                if is_valid_integer(delete_index):
                    SETTINGS_global.repositories.pop(int(delete_index))
                    SETTINGS_global.repo_paths.pop(int(delete_index))
                else:
                    print("exited")
                    time.sleep(0.25)
                    l_count+=1

            if check_same(got_text, 'add'):
                new_repo_name = input("Repository link:\n    ")
                l_count+=2
                new_repo_path = input("Repository path:\n    ")
                l_count+=2
                SETTINGS_global.repositories.append(new_repo_name)
                SETTINGS_global.repo_paths.append(new_repo_path)

            if check_same(got_text, 'exit',0):
                in_progress = False

            for x in range(0,l_count):
                print("\r",flush=True,end="")
                print("\b",flush=True,end="")
                print("\033[1A",flush=True,end="")
                print(" "*100,flush=True,end="")
                print("\r",flush=True,end="")
            





    if show_tip:
        print(str(SETTINGS_global))


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

def list_pull(iterable):
    accumil = []
    for x in iterable:
        accumil.append(x)
    return accumil

def ProgressBar(iterable, length = None):
    if length is None:
        count_max = len(iterable)
    else:
        count_max = length
    count_max -=1
    count = 0
    start = time.perf_counter_ns()
    time_since_start = 0
    for x in iterable:
        if count_max > 0:
            ratio = count/count_max
            size = GLOBAL_PROGRESS_BAR_SIZE
            time_since_start = (time.perf_counter_ns()-start)/1_000_000_000
            if ratio != 0:
                ETA = time_since_start*(1/ratio)
            else:
                ETA = 0
            str_0 = colors.red 
            if ratio > 1/3: 
                str_0 = colors.yellow
            if ratio > 2/3:
                str_0 = colors.green 
            if ratio == 1: 
                str_0 = colors.cyan
            str_1 = "["+"#"*math.floor(ratio*size)+" "*(size-math.floor(ratio*size))+"]  "
            str_2 = ""+str(count)+"/"+str(count_max)+" "
            str_3 = f'({ratio:.2%})'
            str_4 = colors.blue+"   "+f'{time_since_start:.4f}s'
            str_5 = colors.magenta+"   ETA:"+f'{ETA:.4f}s'+colors.reset
            print("\r",end="",flush=True)
            print(str_0+str_1+str_2+str_3+str_4+str_5,end="",flush=True)
            count += 1 

        yield x
    
    print("\r"+" "*100,end="",flush=True)
    print("\r"+colors.reset,end="",flush=True)

class Item:
    def __init__(self, value, string):
        self.v = value
        self.str = string
    
    def __str__(self):
        return "item " + str(self.v) +" "+ str(self.str)
    

class Itemsort:
    def __init__(self, value, string):
        self.items = []
        for index,string in enumerate(string):
            new_item = Item(value[index],string)
            self.items.append(new_item)

    def sort(self):
        return self.quick_sort(self.items)

    def quick_sort(self, arr, depth=0):
        if len(arr) <= 1:
            return arr, depth+1
        mid = len(arr)//2 
        mid_item = arr[mid]
        arr.pop(mid)
        lower = []
        higher = []
        lows = 0
        highs = 0
        for item in arr:
            if mid_item.v > item.v:
                lower.append(item)
                lows  += 1
            else:
                higher.append(item)
                highs +=1
        print(depth, len(arr), lows, highs)

        if lows == 0:
            return lower+[mid_item]+higher, depth+1

        if highs == 0:
            return lower+[mid_item]+higher, depth+1


        lower, depth_1 = self.quick_sort(lower,depth) 
        higher, depth_2 = self.quick_sort(higher,depth)
        if depth_1 >= depth_2:
            depth = depth_1 
        else: 
            depth = depth_2
        return lower+[mid_item]+higher, depth+1


class colors:
    red = '\x1b[31m'
    green = '\x1b[32m'
    yellow = '\x1b[33m'
    blue = '\x1b[34m'
    magenta = '\x1b[35m'
    cyan = '\x1b[36m'
    reset = '\x1b[0m'

def PULL_phase():
    for repo, repo_path  in zip(repositories, repo_paths):
        repo_folder_name = repo.split("/")[-1]
        copy = True
        if not os.path.isdir(repo_folder_name):
            print("[\""+repo_folder_name+"\"] downloading..")
            subprocess.call(["git", "clone", "-n", "--depth=1", "--filter=tree:0", repo])
            subprocess.call(["git", "sparse-checkout", "set", "--no-clone", repo_path],cwd=repo_folder_name)
            subprocess.call(["git","checkout", "-q"],cwd=repo_folder_name)
        else:
            if args.update:
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
    flist = list_pull(targets_directory.rglob('**/*')) 
    for file in ProgressBar(flist):
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
            made_c += 1
        if delete:
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
    flist = list_pull(source_directory.rglob('**/*')) 
    for file in ProgressBar(flist):
        if not file.is_dir():
            if file.suffix in source_file_whitelist_extension:
                #if file.stem in source_files: source_files[file.stem] += [file]
                #else: source_files[file.stem] = [file]
                source_files[file.stem] = source_files.get(file.stem,[]) + [file]

    print("Shooting Source Files against Targets!")
    hits = 0 
    flist = list_pull(resourcepack_directory.rglob('**/*')) 
    for file in ProgressBar(flist):
        if not file.is_dir():
            if file.stem in source_files:
                for source_file in ProgressBar(source_files[file.stem]):
                    shutil.copyfile(source_file, file.parent / source_file.name)
                    del source_files[file.stem]
                    hits += 1
            else:
                target_files[file.stem] = target_files.get(file.stem,[]) + [file]

    if len(source_files) > 0:
        print("Warning, some source files are missing targets:")
        for missing in source_files:
            print(colors.red+missing+colors.reset)

        delete = False
        while True:
            out = input("Do you want to delete missed source files? permanently! (y/N)\n")
            out = out.lower()
            if out == "y":
                delete = True
                break
            elif out == "n":
                break
            elif out == "":
                print("Defaulted (N)",end="\n\n")
                break
            else:
                print("Invalid")
        if delete:
            for missing in source_files:
                for file in source_files[missing]:
                    file.unlink()

    print(colors.green+"Hits: "+str(hits)              + colors.reset)
    print(colors.red+"Misses: "+str(len(source_files)) + colors.reset)


def ZIP_phase():
    print("Now Packing the resourcepack..")
    resourcepack_directory = pl.Path("assets/")
    texpack = zipfile.ZipFile(texpack_name+".zip",'w')
    texpack.write('rsp_dat/pack.mcmeta', 'pack.mcmeta')
    texpack.write('rsp_dat/pack.png', 'pack.png')
    texpack.write('assets')
    flist = list_pull(resourcepack_directory.rglob('**/*')) 
    for file in ProgressBar(flist):
        if file.suffix != 'target':
            texpack.write(file)
    texpack.close()


global_find_target = []
def GET_SCORE(keywords):
    score = 0
    c = 0
    for word in keywords:
        if word in global_find_target:
            score +=25 
        for global_word in global_find_target:
            if word[0] == global_word[0]:
                score+=5
            if word[-1] == global_word[-1]:
                score+=5
        if c < len(global_find_target):
            if keywords[c] == global_find_target[c]:
                c2 = 0
                for let in keywords[c]:
                    if c2 < len(global_find_target[c]):
                        if let == global_find_target[c][c2]:
                            score+=3
                    c2+=1
                score+=5
            else:
                score-=10
        c+=1
    score -= (len(keywords)-len(global_find_target))*10
    score -= sillyfuzzy.compare(''.join(global_find_target),''.join(keywords)) * 3
    return score

def FIND_cmd():
    print("Finding matches..") 
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
                    del source_files[file.stem]
                    hits += 1
            else:
                target_files[file.stem] = target_files.get(file.stem,[]) + [file]
    
    print(colors.green+"Hits: "+str(hits)              + colors.reset)
    print(colors.red+"Misses: "+str(len(source_files)) + colors.reset + '\n')

    if len(source_files) > 0:
        for missing in source_files:
            print(colors.red+missing+colors.reset)

    print("\nUnhit targets: "+str(len(target_files)))
    
    targets_processed = []
    for target in target_files:
        target_processed = [*target.split('_')]
        targets_processed.append(target_processed)

    if len(source_files) > 0:
        for missing in source_files:
            print(colors.red+missing) 
            missing_processed = [*(missing.split('_'))]
            filtered_missing = []
            for keyword in missing_processed:
                if len(keyword) > 0:
                    filtered_missing.append(keyword)
            missing_processed = filtered_missing
            global global_find_target
            global_find_target = missing_processed
            sorted_targets = reversed(sorted(targets_processed,key=GET_SCORE))
            count = 0 
            print(colors.cyan,end="")
            for sorted_target in sorted_targets:
                reconstructed_name=""
                c2 = 0
                for keyword in sorted_target:
                    reconstructed_name += keyword
                    if c2 < len(sorted_target)-1:
                        reconstructed_name +="_"
                    c2+=1
                print(" "*70+"Score: "+str(GET_SCORE(sorted_target)),end="",flush=True)
                print("\r",end="",flush=True)
                print(reconstructed_name)
                
                count +=1 
                if count > 5:
                    break
            print()
        print(colors.reset,"\n")


give_help = not (args.pull or args.target or args.build or args.zip or args.find or args.run or args.config)

if args.run:
    PULL_phase()
    TARGET_phase()
    BUILD_phase()
    ZIP_phase()

if args.pull: PULL_phase()
if args.target: TARGET_phase()
if args.build: BUILD_phase()
if args.zip: ZIP_phase()
if args.find: FIND_cmd()
if args.config: SET_CONFIG()

if give_help: HELP_cmd()


SETTINGS_global.save()
