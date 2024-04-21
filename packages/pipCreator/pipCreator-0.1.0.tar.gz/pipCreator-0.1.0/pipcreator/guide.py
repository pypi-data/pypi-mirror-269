from pipcreator.constants import title, author, footer
from pipcreator.color import *

guide_text = f"""{title}
Author:{author}

Let's get started!

1.  On first let create the project folder.
    USE: {magenta}pipcreator create <location>{reset}
    this command will create the project folder in the location specified.

2.  Edit the inner folder files that as same name as the project folder.

3.  Edit the folder as you want and have a {green}__init__.py{reset} file, to initiate the project.

4.  Also Edit the README.md, setup.py, setup.cfg, pyproject.toml and requirements.txt file.
    for more metadata information and setup details.

5.  Convert the project folder to python package. 
    USE: {magenta}pipcreator convert{reset}
    this will create the wheel and sdist for the project.

6.  Upload the project folder to pypi. 
    USE: {magenta}pipcreator upload{reset}
    this will upload the project folder to pypi. 
    this command uses twine. to upload the project folder to pypi.
    {yellow}make sure you have an account on https://pypi.org .{reset}


GitHub  : {blue}https://github.com/rakeshkanna-rk/pipCreator{reset}
PyPI    : {blue}https://pypi.org/project/pipcreator/{reset}

{footer}"""

def guide_learn():
    print(guide_text)