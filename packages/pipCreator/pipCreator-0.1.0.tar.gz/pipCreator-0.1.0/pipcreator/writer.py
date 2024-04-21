import os
import sys
import time
from string import ascii_lowercase, ascii_uppercase, digits

# CONSTANTS
from pipcreator.constants import *


# CHECK DIRECTORY
def check_directory(directory, proj_name):

    # Check if directory exists
    if not os.path.exists(directory):
        # options()
        description, keywords, author, author_mail, licence = options()
        print(f"{yellow}Directory doesn't exist.{reset}")

        dir_loop = True
        while dir_loop:
            dir_crt = input("Do you want to create the directory? (y/n) ")
            if dir_crt.lower() == 'y':
                os.makedirs(directory)
                print(f"{green}Directory created successfully. ✔{reset}")
                time.sleep(0.5)
                create_files_and_folders(directory, description, keywords, author, author_mail, proj_name, licence)
                dir_loop = False

            elif dir_crt.lower() == 'n':
                print(f"{red}Creating project aborted.{reset}")
                print(f"\n{footer}")
                dir_loop = False
                sys.exit(1)

            else:
                print(invalid_input)

    else:
        # Check if directory is empty
        if not os.listdir(directory):
            description, keywords, author, author_mail, licence = options()
            print("Directory is empty. Creating files and folders...")
            create_files_and_folders(directory, description, keywords, author, author_mail, proj_name, licence)
        else:
            print(check_directory_err)
            list_files(directory)


# CREATE README.MD
def create_readme(directory, description, proj_name):
    # Create README.md
    with open(os.path.join(directory, 'README.md'), 'w') as f:
        readme = f'''
# {proj_name}
{description}
'''
        f.write(readme)
    print(readme_success)
    return readme


# CREATE SETUP.PY
def create_setuppy(directory, description, keywords, author, author_mail, proj_name, licence="MIT"):
    keywords = keywords.split()

    with open(os.path.join(directory, 'setup.py'), 'w') as f:
        setuppy = setuppy_writer(description, keywords, author, author_mail, proj_name, licence)
        f.write(setuppy)
    print(setuppy_success)
    return setuppy


# CREATE SETUP.CFG
def create_setupcfg(directory, description, keywords, author, author_mail, proj_name, licence="MIT"):
    with open(os.path.join(directory, 'setup.cfg'), 'w') as f:
        setupcfg = setupcfg_writer(description, keywords, author, author_mail, proj_name, licence)
        f.write(setupcfg)
    print(setupcfg_success)
    return setupcfg


# CREATE PYPROJECT.TOML
def create_pyprojecttoml(directory, description, keywords, author, author_mail, proj_name, licence="MIT"):
    with open(os.path.join(directory, 'pyproject.toml'), 'w') as f:
        pyprojecttoml = pyprojecttoml_writer(description, keywords, author, author_mail, proj_name, licence)
        f.write(pyprojecttoml)
    print(pyprojecttoml_success)
    return pyprojecttoml


# CREATE REQUIREMENTS.TXT
def create_requirements(directory):
    with open(os.path.join(directory, 'requirements.txt'), 'w') as f:
        requirements = '# your requirements here\n'
        f.write(requirements)
    print(requirements_success)
    return requirements


# .GITIGNORE
def create_gitignore(directory):
    with open(os.path.join(directory, '.gitignore'), 'w') as f:
        f.write(gitignore)
    print(gitignore_success)
    return gitignore


# LICENSE
def create_license(directory):
    with open(os.path.join(directory, 'LICENSE'), 'w') as f:
        license = '# your license here\n'
        f.write(license)
    print(license_success)
    return license


# FOLDERS
def folders(directory, proj_name, folder_name):
    os.makedirs(os.path.join(directory, folder_name))
    with open(os.path.join(directory, folder_name, '__init__.py'), 'w') as f:
        init = init_writer()
        f.write(init)
        print(f"{green}{proj_name}/__init__.py created successfully. ✔{reset}")
        time.sleep(0.5)

    with open(os.path.join(directory, folder_name, 'main.py'), 'w') as f:
        main = main_writer()
        f.write(main)
        print(f"{green}{proj_name}/main.py created successfully. ✔{reset}\n")
        time.sleep(0.5)

    return init, main


# CREATE FILES AND FOLDERS
def create_files_and_folders(directory, description, keywords, author, author_mail, proj_name, licence="MIT"): 

    print()
    messages = [wrt_prog_remd + directory, wrt_prog_setuppy + directory, 
                wrt_prog_setupcfg + directory, wrt_prog_pyprojecttoml + directory, 
                wrt_prog_gitignore + directory, wrt_prog_license + directory, 
                wrt_prog_requirements + directory]
    for i in range(101):
        progress = i / 100
        erase_bar(progress, messages=messages)
        time.sleep(0.05)

    # Create files
    readme = create_readme(directory, description, proj_name)
    time.sleep(0.5)
    setuppy = create_setuppy(directory, description, keywords, author, author_mail, proj_name, licence)
    time.sleep(0.5)
    setupcfg = create_setupcfg(directory, description, keywords, author, author_mail, proj_name, licence)
    time.sleep(0.5)
    pyprojecttoml = create_pyprojecttoml(directory, description, keywords, author, author_mail, proj_name, licence)
    time.sleep(0.5)
    gitignore_fh = create_gitignore(directory)
    time.sleep(0.5)
    licence = create_license(directory)
    time.sleep(0.5)
    requirements = create_requirements(directory)
    time.sleep(0.5)

    # Folder name
    folder_name = os.path.basename(directory)

    # CREATING FOLDERS
    init, main = folders(directory, proj_name, folder_name)


    print(file_written_check)
    written_file_check = input("\nDo you want to check files? (y/n): ")
    if written_file_check.lower() == 'y':
        file_printer(readme, setuppy, setupcfg, pyprojecttoml, requirements, gitignore_fh, init, main, proj_name)
    print(files_success)
    print(ready_to_code)
    print(f"\n\t {yellow}cd{reset} {directory}\n")
    print(footer)


def list_files(directory):
    # List files in the directory
    files = os.listdir(directory)
    for file_name in files:
        print(file_name)



# MAIN (PIP CREATOR)
def pip_creator():
    print(title)

    if len(sys.argv) != 3:
        print("Usage: pipcreator create <directory>")
        sys.exit(1)

    folder_name = ascii_lowercase + ascii_uppercase + digits + '_./'

    directory = sys.argv[2]

    if "-" in directory:
        print(f"{yellow}The ' - ' will be replaced as '_' in the folder name{reset}")
        directory = directory.replace("-", "_")

    if any(char not in folder_name for char in directory):
        print(f"{red}Invalid directory name{reset}")
        print(f"{yellow}Directory name must contain only the following characters:{reset}")
        print("A-Z a-z 0-9 _ \n")
        print(footer)
        sys.exit(1)

    if directory == '.' or directory == './':
        directory = os.getcwd()
        print(f"Creating project in current directory: {directory}")

    proj_name = os.path.basename(directory)

    file_content = f'''\n
    {proj_name}/__init__.py
    {proj_name}/main.py
    .gitignore
    LICENSE
    README.md
    setup.py
    setup.cfg
    pyproject.toml
    requirements.txt
    '''
    print(f'The folder will be created in {directory} \n{file_content}')

    check = True
    while check:
        file_check = input(f"Are you sure you want to create the following files in {directory}? (y/n) ")

        if file_check.lower() == 'y':
            check_directory(directory, proj_name)
            check = False
        elif file_check.lower() == 'n':
            print(exit_msg)
            print(footer)
            sys.exit(0)
        else:
            print(invalid_input)

