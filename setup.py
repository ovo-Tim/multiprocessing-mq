import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multiprocessing_mq",
    version="0.1",
    author="ovo-tim",
    author_email="ovo-tim@qq.com",
    description="在多进程内维护一个消息队列，更方便的使用多进程 ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ovo-Tim/multiprocessing-mq",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ]
)
