# CLI
from .main import cli

# WRITER
from .writer import pip_creator

# OTHER FUNCTIONS
from .writer import create_gitignore, create_license
from .writer import create_pyprojecttoml, create_readme
from .writer import create_requirements, create_setupcfg, create_setuppy

# List files
from .writer import list_files

# CONVERT
from .convert import run_setup_command_convert

# UPLOAD
from .upload import run_setup_command_upload

# GUIDE
from .guide import guide_learn

__cli__ = ["pip_creator"]

__others__ = ["create_gitignore", "create_license", 
              "create_pyprojecttoml", "create_readme", 
              "create_requirements", "create_setupcfg", "create_setuppy"]

__list_files__ = ["list_files"]

__convert__ = ["run_setup_command"]

__upload__ = ["run_setup_command_upload"]

__guide__ = ["guide_learn"]

__all__ = __cli__ + __others__ + __list_files__ + __convert__ + __upload__ + __guide__