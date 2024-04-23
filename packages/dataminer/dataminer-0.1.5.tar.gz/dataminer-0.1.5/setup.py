from setuptools import setup, find_packages

setup(
    name='dataminer',
    version='0.1.5',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy',
        'oracledb',
    ],
    author='javaite',
    author_email='javaite@126.com',
    description='A set of data processing tools.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitee.com/javaite_code/dataminer.git',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.10',
)
