from setuptools import setup, find_packages

setup(
    name='cerbogen',
    version = '0.0.39',
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

    # Specify the entry point to execute the install_location function
    entry_points={
        'console_scripts': [
            'install_cerbogen=cerbogen.mod.install_location:install_location',
        ],
    }
)