from setuptools import find_packages, setup
from typing import List

import sys

def get_requirements() -> List[str]:
    '''
    This function will return list of requirements.
    '''
    req_list:List[str] = []
    try:
        with open('requirements.txt', 'r') as f:
            req = f.readlines()
        
        for r in req:
            requirement = r.strip()
            if requirement and requirement != "-e .":
                req_list.append(requirement)
                
                
    except FileNotFoundError:
        print("requirements.txt file not found.")
    
    return req_list

setup(
    name = "Network Security",
    version="0.0.0.1",
    author="Anshika Modi",
    author_email="anshikamodi3001@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)