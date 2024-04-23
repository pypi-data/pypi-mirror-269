from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='AresHook',
    version='0.1',  # 初始版本号，如果使用自动版本管理，这个值可以是任意值
    author='369',
    author_email='luck.yangbo@gmail.com',
    description='A simple hook library.',
    long_description=long_description,
    packages=find_packages(),  # 自动查找并包含所有包
    install_requires=[
        'frida',
        'frida-tools',
    ],
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
