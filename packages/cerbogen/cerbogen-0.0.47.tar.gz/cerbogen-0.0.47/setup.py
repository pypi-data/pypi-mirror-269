from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import shutil
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        self.custom_code()
    
    def custom_code(self):
        # Run the install.py script located in the 'install' directory
        install_script_path = os.path.join(os.path.dirname(__file__), 'cerbogen', 'install', 'install.py')
        subprocess.run(['python', install_script_path])
        

setup(
    name='cerbogen',
    version='0.0.47',
    description='A Python package for CerboTech',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Clarence Parmar',
    author_email='git.clarence@gmail.com',
    url='https://github.com/clarenceparmar/cerbogen',
    packages=find_packages(),
    install_requires=["matplotlib", "pydub", "numpy", "librosa"],
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    # Include all files from the 'data' directory
    package_data={'': ['data/*/*']},

    # Use the custom install class
    cmdclass={'install': CustomInstall},
)
