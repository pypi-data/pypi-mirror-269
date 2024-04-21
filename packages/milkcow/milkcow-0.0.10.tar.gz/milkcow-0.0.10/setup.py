from setuptools import find_packages, setup


with open('milkcow/README.md', 'r') as f:
    long_description = f.read()


setup(
        name='milkcow',
        version='0.0.10',
        description='A tool to building middleware for the multiprocessing of data',
        packages=find_packages(),
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/SamReynoso/milkcow',
        author='SamReynoso',
        license='MIT',
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            ]
        )
