# this file 'builds' the application
# it tells python the project is a package, so it can be installed with pip and used outside
# this env or directory; it allows you to do e.g. from mlproject import somefunction, just as
# you would with from numpy import sqrt()

# also adds some metadata

from setuptools import setup, find_packages #looks for folders with __init__.py
from typing import List

# we can run pip install mlproject, but if we create a requirements.txt file ans include the 
# command '-e .', we can run pip install requirements.txt to install all packages in the env
# and trigger the activation of setup.py
HYPEN_E_DOT="-e ."
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''

    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        #we need to remove -e, we want it to trigger setup.py but not in this list
        if HYPEN_E_DOT in requirements: 
            requirements.remove(HYPEN_E_DOT)

    return requirements

setup(
name='biomlproject',
version='0.0.1',
author='me',
author_email='jorguzjma07@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')
)

