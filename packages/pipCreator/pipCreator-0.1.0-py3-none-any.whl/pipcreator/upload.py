import os
import subprocess
import time
import sys

from pipcreator.constants import green, reset, magenta, yellow, red
from pipcreator.constants import check_folder_contents
from pipcreator.constants import title, footer
from pipcreator.constants import exit_msg, invalid_input


def uploader(command):
    try:
        conform = input(f"{yellow}This will use twine to upload the package.{reset} \nAre you sure you want to proceed? (y/n): ")
        loop = True
        while loop:
            if conform.lower() == "y":
                subprocess.run(command, shell=True, check=True)
                print(f"{green}\nCommand executed successfully. ✔\n")
                loop = False

            elif conform.lower() == "n":
                print(f"{red}\nCommand cancelled. \n")
                loop = False

            else:
                print(invalid_input)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")



def run_setup_command_upload():
    command = "twine upload dist/*"

    print(title)

    directory = os.getcwd()
    print(f"Uploading files will happen in current directory: {yellow}{directory}{reset}")

    proj_name = os.path.basename(directory)
    print(f"Project name: {yellow}{proj_name}{reset}\n")

    print(f"\n{yellow}Make sure you have an account and genrate a API key at https://pypi.org{reset}")

    loop = True
    while loop:
        conform = input("Did you convert the files to sdist and bdist? (y/n): ")
        if conform.lower() == 'y':
            loop = False
        
        elif conform.lower() == 'n':
            print(f"USE: {magenta}pipcreator convert{reset}")
            print(f"{red}\nCommand cancelled.\n{exit_msg}{reset}")
            print(f"\n{footer}")
            loop = False  
            sys.exit()      

        else:
            print(invalid_input)

    required_files = [proj_name, '.gitignore', 'LICENSE', 'README.md', 
                      'setup.py', 'setup.cfg', 'pyproject.toml', 
                      'requirements.txt', 'dist', 'build', f'{proj_name}.egg-info']

    folder_complete, missing_files = check_folder_contents(directory, required_files)


    if folder_complete == False:
        time.sleep(1.0)
        print("Folder is missing the following required files:")
        for file_name in missing_files:
            print(f"{yellow}{file_name}{reset}")

    elif folder_complete == True:
        time.sleep(1.0)
        print(f"\n{green}Folder contains all required files. ✔{reset}")
        try:
            uploader(command)
            print(f"{magenta}Twine Operation Completed...{reset}")

        except Exception as e:
            print(f"Error on Uploading...\nERROR: {e}")

    else: 
        print(f"{red}Something went wrong. Please try again.{reset}")

    time.sleep(1.0)
    print(f"\n{footer}")



