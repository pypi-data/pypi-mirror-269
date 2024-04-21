from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

# Define a custom install class that inherits from setuptools' install command
class CustomInstall(install):
    def run(self):
        
        install.run(self)
        self.custom_code()
    
    def custom_code(self):
        subprocess.run(['python', '-m', 'cerbogen.install.setup'])

setup(
    name='cerbogen',
    version = '0.0.45',
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

    # Use the custom install class
    cmdclass={'install': CustomInstall},
)
