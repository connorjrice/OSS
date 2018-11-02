from setuptools import setup, find_packages

import pip

pip.main(['install', 'pandas'])
pip.main(['install', 'tornado'])
pip.main(['install', 'bcrypt'])
pip.main(['install', 'faker'])
pip.main(['install', 'requests'])

setup(
    name="astral-oss",
    version="0.0.1",
    packages=find_packages(),
    install_requires=['tornado', 'selenium', 'pytest', 'requests', 'bcrypt'],
)
