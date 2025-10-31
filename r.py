import subprocess 
quick_rename = "C:\\programmingprojects\\sillytextest\\GregTech-Modern\\src\\main\\resources\\assets\\gtceu\\textures\\item\\material_sets"
#quick_rename = 'C:\\programmingprojects\\voltages\\block2\\gtnh\\modular_armor\\modular items'

subprocess.call(['py','rename.py','-f',quick_rename])
subprocess.call(['py','s.py'])
