from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(filepath: str) -> List[str]:
    '''Read the requirements file and return list of requirements'''
    requirements = []
    with open(filepath) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n',' ') for req in requirements]
                
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
               
    return requirements

setup(
    name='GHMicroclimate_LSTM',
    version='0.1',
    packages=find_packages(),
    author='Niraj Tamrakar',
    author_email='niraj@gnu.ac.kr',
    install_requires= get_requirements('requirements.txt')
 
)