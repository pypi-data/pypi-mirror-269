from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='snbpy_assistant',

    version='1.0.0',

    description='snbpy',

    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://github.com/chnyangjie/snbpy-assistant',

    author='chnyangjie',

    author_email='chnyangjie@gmail.com',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='snbpy_assistant',
    package_dir={'snbpy_assistant': 'src/snbpy_assistant'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=['requests', 'snbpy'],
    py_modules=['snbpy_assistant'],
    project_urls={
        'Bug Reports': 'https://github.com/chnyangjie/snbpy-assistant/issues',
        'Funding': 'https://github.com/chnyangjie/snbpy-assistant/issues',
        'Say Thanks!': 'https://github.com/chnyangjie/snbpy-assistant/issues',
        'Source': 'https://github.com/chnyangjie/snbpy-assistant/issues',
    },
)
