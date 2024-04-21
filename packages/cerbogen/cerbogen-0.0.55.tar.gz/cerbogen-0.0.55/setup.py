from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess

class CustomInstall(install):
    def run(self):
        install.run(self)
        self.post_install()

    def post_install(self):
        print("Running post-installation script...")
        for i in range(0, 100):
            print("Hello World")

        install_script_path = os.path.join(os.path.dirname(__file__), 'install', 'install.py')
        subprocess.run(['python', install_script_path])

setup(
    name='cerbogen',
    version = '0.0.55',
    description='A Python package for CerboTech',
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
    package_data={'': ['data/*/*']},
    cmdclass={'install': CustomInstall},
)
