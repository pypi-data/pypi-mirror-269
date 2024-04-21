import os
import sys
import time

from pipcreator.color import *
from pipcreator.constants import title, footer, green, reset
from pipcreator.constants import  test_end_msg , crtfd_msg, crtfl_msg, wrtfl_msg, wrtfl_msg_ovr, crtfd_msg_ovr, crtfl_msg_ovr
from pipcreator.constants import test_writer, test_show_writer
from pipcreator.constants import erase_bar
from pipcreator.constants import check_folder_contents


def create_test_folder(proj_name, folder_name):
    os.makedirs(folder_name, exist_ok=True)
    with open(os.path.join(folder_name, 'test.py'), 'w') as f:
        test = test_writer(proj_name)
        f.write(test)

    return test


def test_folder():
    print(title)
    directory = os.getcwd()
    print(f"Test folder will be created in current directory: {yellow}{directory}{reset}")

    proj_name = os.path.basename(directory)
    print(f"Project name: {yellow}{proj_name}{reset}\n")

    print(f"{cyan}Checking folder contents...{reset}", end="\r")

    required_files = [proj_name, '.gitignore', 'LICENSE', 'README.md', 'setup.py', 'setup.cfg', 'pyproject.toml']

    folder_complete, missing_files = check_folder_contents(directory, required_files)

    time.sleep(1.0)

    if folder_complete == False:
        print("Folder is missing the following required files:")
        for file_name in missing_files:
            print(f"{yellow}{file_name}{reset}")
        time.sleep(1.0)
        print(f"\n{footer}")
        sys.exit(1)

        


    folder_path = 'test'
    if os.path.exists(folder_path):
        time.sleep(0.5)
        print(f"{green}Folder contains all required files. ✔{reset}")
        print(f"{red}The folder '{proj_name}/{folder_path}' exists.{reset}")
    else:
        print(f"{green}Folder contains all required files. ✔{reset}")
        print(f"The folder '{proj_name}/{folder_path}' does not exist.", end="\r")
        messages = [crtfd_msg + proj_name , 
            crtfd_msg_ovr + proj_name + reset, 
            crtfl_msg + proj_name , 
            crtfl_msg_ovr + proj_name + reset, 
            wrtfl_msg + proj_name , 
            wrtfl_msg_ovr + proj_name + reset]
    
        for i in range(101):
            progress = i / 100
            erase_bar(progress, messages=messages)
            time.sleep(0.05)

        create_test_folder(proj_name, "test")
        print(f"{green}{proj_name}/test.py created successfully. ✔{reset}")

        time.sleep(0.5)
        print(test_end_msg)

        test_loop = True
        while test_loop:
            check_test = input("Do you want to check the test folder? (y/n): ")
            if check_test.lower() == 'y':
                test_show = test_show_writer(proj_name)
                print(test_show)
                test_loop = False

            elif check_test.lower() == 'n':
                test_loop = False

            else:
                print("Invalid input. Please enter 'y' or 'n'.")


    time.sleep(1.0)
    print(f"\n{footer}")


