import sys
import os
import time

# COLORS
from pipcreator.color import red, green, blue, yellow, magenta, cyan, white, black_bg, reset


# CONSTANTS
VERSION = 'v0.1.0'
author = 'Rakesh Kanna'
title = f'\n\t{cyan}PIP CREATOR{reset} {VERSION}\n'

check_directory_err = f"{red}Files exist in the directory. Try another directory or delete these files.{reset}"

readme_success = f"{green}README.md created successfully. ✔{reset}"
setuppy_success = f"{green}setup.py created successfully. ✔{reset}"
setupcfg_success = f"{green}setup.cfg created successfully. ✔{reset}"
pyprojecttoml_success = f"{green}pyproject.toml created successfully. ✔{reset}"
requirements_success = f"{green}requirements.txt created successfully. ✔{reset}"
gitignore_success = f"{green}.gitignore created successfully. ✔{reset}"
license_success = f"{green}License created successfully. ✔{reset}"


files_success = f"\n{green}All files created successfully. ✔{reset}"
ready_to_code = "Your project folder is ready to use."
file_written_check = f"{green}Files Written successfully. ✔{reset}"


crtfd_msg = "Creating folder... → "
crtfd_msg_ovr = f"{green}Folder created successfully. ✔ → "
crtfl_msg = "Creating files... → "
crtfl_msg_ovr = f"{green}Files created successfully. ✔ → "
wrtfl_msg = "Writing files... → "
wrtfl_msg_ovr = f"{green}Files written successfully. ✔ → "
test_end_msg = f"\r{green}Test Folder has been created successfully! ✔{reset}\n"


wrt_prog_remd = "Writing README.md files... → "
wrt_prog_setuppy = "Writing setup.py files... → "
wrt_prog_setupcfg = "Writing setup.cfg files... → "
wrt_prog_pyprojecttoml = "Writing pyproject.toml files... → "
wrt_prog_requirements = "Writing requirements.txt files... → "
wrt_prog_gitignore = "Writing .gitignore files... → "
wrt_prog_license = "Writing LICENSE files... → "

wrt_prog_remd_ovr = f"{green}README.md written successfully. ✔{reset}"
wrt_prog_setuppy_ovr = f"{green}setup.py written successfully. ✔{reset}"
wrt_prog_setupcfg_ovr = f"{green}setup.cfg written successfully. ✔{reset}"
wrt_prog_pyprojecttoml_ovr = f"{green}pyproject.toml written successfully. ✔{reset}"
wrt_prog_requirements_ovr = f"{green}requirements.txt written successfully. ✔{reset}"
wrt_prog_gitignore_ovr = f"{green}.gitignore written successfully. ✔{reset}"
wrt_prog_license_ovr = f"{green}LICENSE written successfully. ✔{reset}"

footer = f"{author}\n{cyan}Happy Coding!{reset}"

invalid_input = f"{red}Invalid input. Please enter 'y' or 'n'.{reset}"
exit_msg = f"{red}Exiting the program.{reset}\n"


gitignore = '''
# Byte-compiled / optimized Python files
__pycache__/
*.pyc
*.pyo
*.pyd

# Virtual environment
venv/
env/
*.env

# Compiled files
*.o
*.class
*.dll
*.exe

# Temporary files
*~
*.swp
*.log

# Miscellaneous
.DS_Store
.idea/
.vscode/
'''

# PROGRESS BAR
def progress_bar(progress, length=50, symbol='█', empty_symbol='-', color_on_completion=green):
    filled_length = int(length * progress)
    bar = symbol * filled_length + empty_symbol * (length - filled_length)
    color = color_on_completion if progress == 1 else ''
    print(f'|{color}{bar}{reset}| {progress:.1%}', end='\r')


def erase_bar(progress, length=50, symbol='█', empty_symbol='-', messages=None):
    messages = messages or []
    filled_length = int(length * progress)
    bar = symbol * filled_length + empty_symbol * (length - filled_length)
    
    if progress == 1:
        time.sleep(0.5)
        sys.stdout.write(f'\r{" " * (length + len(messages[-1]) + 10)}\r')
        sys.stdout.write(reset)
        sys.stdout.flush()

    elif progress == 0.98:
        sys.stdout.write(green)
        sys.stdout.write(f'\r{" " * (length + len(messages[-1]) + 10)}')
        
    else:
        # Determine the current message index based on the progress
        message_index = min(int(progress * len(messages) * 2), len(messages) - 1)
        current_message = messages[message_index]
        
        sys.stdout.write(f'\r|{bar}| {progress:.0%} {current_message}')
        sys.stdout.flush()



#
def options():
    desc = True
    while desc:
        description = input(f"{cyan}Enter a description for your project: {reset}")
        desc = False

    keyw = True
    while keyw:
        keywords = input(f"{cyan}Enter keywords for your project: {reset}")
        keyw = False

    auth = True
    while auth:
        author = input(f"{cyan}Enter author name: {reset}")
        auth = False

    auth_mail = True
    while auth_mail:
        author_mail = input(f"{cyan}Enter author email: {reset}")
        auth_mail = False

    lic = True
    while lic:
        licence = input(f"{cyan}Enter license for your project: {reset}")
        lic = False

    return description, keywords, author, author_mail, licence


def check_folder_contents(folder_path, required_files):
    
    folder_files = os.listdir(folder_path)

    missing_files = [file_name for file_name in required_files if file_name not in folder_files]

    if not missing_files:
        return True, None
    else:
        return False, missing_files


def file_printer(readme, setuppy, setupcfg, pyprojecttoml, requirements, gitignore_fh, init, main, proj_name):
    print(f'''
--------------------------------
README.md
{readme}
--------------------------------

--------------------------------
setup.py
{setuppy}
--------------------------------

--------------------------------
setup.cfg
{setupcfg}
--------------------------------

--------------------------------
pyproject.toml
{pyprojecttoml}
--------------------------------

--------------------------------
requirements.txt
{requirements}

--------------------------------
.gitignore
{gitignore_fh}
--------------------------------

--------------------------------
{proj_name}/__init__.py
{init} 
--------------------------------

--------------------------------
{proj_name}/main.py
{main}
--------------------------------
''')
    


def setuppy_writer(description, keywords, author, author_mail, proj_name, licence):
    setuppy = f'''
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="{proj_name}",
    version="0.1.0",
    description="{description}",
    author="{author}",
    author_email='{author_mail}',
    licence="{licence}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords={keywords},
)
'''
    return setuppy

def setupcfg_writer(description, keywords, author, author_mail, proj_name, licence):
    keywords = ', '.join(keywords.split())
    setupcfg = f'''
[metadata]
name = {proj_name}
version = 0.1.0
description = {description}
author = {author}
author_email = {author_mail}
license = {licence}
keywords = {keywords}

[options]
packages = find:
python_requires = >=3.6
'''
    return setupcfg

def pyprojecttoml_writer(description, keywords, author, author_mail, proj_name, licence):
    keywords = keywords.split()
    pyprojecttoml = f'''
[tool.poetry]
name = "{proj_name}"
version = "0.1.0"
description = "{description}"
author = "{author}"
author_email = "{author_mail}"
license = "{licence}"
keywords = {keywords}
[tool.poetry.dependencies]
python = ">=3.6"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
'''

    return pyprojecttoml


# FOLDERS
def init_writer():
    init = f'''
from .main import main

__all__ = ["main"]
'''
    return init

def main_writer():
    main = f'''
def main():
    print("Hello, World!")
'''
    return main


# test/test.py
def test_writer(proj_name):
    test = f'''
import unittest
from {proj_name} import hello 

# Define a test class
class TestHelloFunction(unittest.TestCase):

    # Define a test method to test hello() function
    def test_hello(self):
        # Call the hello() function
        result = hello()

        # Assert the result
        self.assertEqual(result, "Hello, World!")

if __name__ == '__main__':
    unittest.main()

'''
    return test

def test_show_writer(proj_name):
    test_show =f'''
--------------------------------
test/test.py
--------------------------------
import unittest
from {proj_name} import hello 

# Define a test class
class TestHelloFunction(unittest.TestCase):

    def test_hello(self):
        # Call the hello() function
        result = hello()

        # Assert the result
        self.assertEqual(result, "Hello, World!")

if __name__ == '__main__':
    unittest.main()
--------------------------------
'''
    return test_show