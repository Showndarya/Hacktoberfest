from setuptools import setup
from SurpriseMe import __version__

dependencies=['pyttsx3']
long_description=""
with open("README.md",'r') as f:
    long_description=f.read()
    
setup(
        name='SurpriseMe',
        description='A command line tool which chooses a random word to generate audio',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/Showndarya/Hacktoberfest',
        author='Showndarya',
        author_email='showndarya.m@somaiya.edu',
        packages=[
            'SurpriseMe'
        ],
        version=__version__,
        install_requires=dependencies,
        entry_points={
            'console_scripts':[
                'SurpriseMe = SurpriseMe.SurpriseMe:main'
            ],
        },
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Operating System :: POSIX',
            'Programming Language :: Python',
        ],
    )
