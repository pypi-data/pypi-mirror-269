from setuptools import setup, find_packages

setup(
    name='odsbtree',
    version='0.1.0',
    packages=find_packages(),
    description='An efficient binary search tree implementation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='hgs',
    author_email='2523310240@qq.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    test_suite='tests',
)
