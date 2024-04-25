#!/usr/bin/env python
# coding=utf-8
import re
import hashlib

from setuptools import setup, find_packages


def read(file_name):
    with open(file_name, 'r') as f:
        content = f.read()
    return content


version = re.search("__version__ = ['\"]([^'\"]+)['\"]", read('py_enum/__init__.py')).group(1)

read_me = read('README.md')
# 替换文档的相对路径为绝对路径地址
read_me = read_me.replace('(./docs/', '(https://github.com/SkylerHu/py-enum/blob/master/docs/')

read_me_b = read_me.encode('utf-8')
blake2b_hash = hashlib.blake2b(read_me_b, digest_size=32).hexdigest()
sha256_hash = hashlib.sha256(read_me_b).hexdigest()
print(f"BLAKE2b-256: {blake2b_hash}\nSHA256: {sha256_hash}")


setup(
    name='py-enum',
    version=version,
    url='https://github.com/SkylerHu/py-enum.git',
    author='SkylerHu',
    author_email='skylerhu@qq.com',
    description='enums for choices fields',
    long_description=read_me,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests*', 'tests']),
    license='MIT Licence',
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'six>=1.12.0',
    ],
    python_requires=">=2.7",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

    ],
)
