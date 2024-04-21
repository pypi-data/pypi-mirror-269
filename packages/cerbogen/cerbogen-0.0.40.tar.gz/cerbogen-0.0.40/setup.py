from setuptools import setup, find_packages

setup(
    name='cerbogen',
    version = '0.0.40',
    description='A Python package for CerboTech',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Clarence Parmar',
    author_email='git.clarence@gmail.com',
    url='https://github.com/clarenceparmar/cerbogen',
    packages=find_packages(),
    
    package_data={
        '': ['ffmpeg/mac/*', 'data/img/*', 'mod/*']
    },

    install_requires=[
        "matplotlib", "pydub", "numpy", "librosa"
    ],
    
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    # Specify the script to be executed during installation
    scripts=['cerbogen/mod/install_location.py']
)