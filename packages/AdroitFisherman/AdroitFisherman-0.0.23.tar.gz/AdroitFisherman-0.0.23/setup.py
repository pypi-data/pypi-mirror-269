from setuptools import setup,Extension
import os
SeqList=Extension("AdroitFisherman.Utilities",sources=['AdroitFisherman/includes/SeqList.c'])

read_me = open('README.md', 'r',encoding='utf-8')
setup(
    name="AdroitFisherman",
    version="0.0.23",
    author="adroit_fisherman",
    author_email="1295284735@qq.com",
    platforms="Windows",
    description="This is a simple package about Data Structure packed by C/C++ language.",
    long_description_content_type="text/markdown",
    long_description=read_me.read(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities"
    ],
    include_package_data=True,
    packages=['AdroitFisherman.SequentialList'],
    ext_modules=[SeqList]
)
read_me.close()
