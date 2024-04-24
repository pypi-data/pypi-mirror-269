# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
setup(
    name='hebill',
    version='1.2.4',
    description='Python Hebill',
    long_description=open(r'D:\SDK\GitHub\python_hebill\hebill\README.MD', encoding='utf-8').read(),
    long_description_content_type='text/plain',
    packages=find_packages(),
    install_requires=[
        'psutil==5.9.8',
        'pillow==10.3.0',
        'requests==2.31.0',
        'wxpython==4.2.1',
        'reportlab==4.1.0',
        'PyMySQL==1.1.0',
        'DBUtils==3.1.0',
    ],
    python_requires='>=3.12',
)
