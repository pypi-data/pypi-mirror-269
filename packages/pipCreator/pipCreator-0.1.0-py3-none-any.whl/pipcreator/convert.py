import subprocess
import os
import sys
import time

from pipcreator.constants import green, red, yellow, reset
from pipcreator.constants import check_folder_contents
from pipcreator.constants import title, footer
from pipcreator.constants import exit_msg, invalid_input

def convert(command):
    loop = True
    while loop:
        conform = input("Are you sure you want to convert to sdist and bdist? [y/n]: ")
        if conform.lower() == 'y':
            try:
                subprocess.run(command, shell=True, check=True)
                print(f"{green}Command executed successfully. ✔{reset}")
                print(f"\n{green}Files Converted successfully. ✔{reset}")
            except Exception as e:
                print(f"{red}Error on converting... {e}{reset}")

            loop = False
        
        elif conform.lower() == 'n':
            print(f"{red}\nCommand cancelled.\n{exit_msg}{reset}")
            loop = False

        else:
            print(invalid_input)




def run_setup_command_convert():
    command = "python setup.py sdist bdist_wheel"

    print(title)

    directory = os.getcwd()
    print(f"Uploading files will happen in current directory: {yellow}{directory}{reset}")

    proj_name = os.path.basename(directory)
    print(f"Project name: {yellow}{proj_name}{reset}\n")


    required_files = [proj_name, '.gitignore', 'LICENSE', 'README.md', 
                      'setup.py', 'setup.cfg', 'pyproject.toml', 
                      'requirements.txt']

    folder_complete, missing_files = check_folder_contents(directory, required_files)



    if folder_complete == False:
        time.sleep(1.0)
        print("Folder is missing the following required files:")
        for file_name in missing_files:
            print(f"{yellow}{file_name}{reset}")

    elif folder_complete == True:
        time.sleep(1.0)
        print(f"{green}Folder contains all required files. ✔{reset}")
        try:
            convert(command)

        except Exception as e:
            print(f"Error on Converting...\nERROR: {e}")

    else: 
        print(f"{red}Something went wrong. {exit_msg}{reset}")

    time.sleep(1.0)
    print(f"\n{footer}")

    
