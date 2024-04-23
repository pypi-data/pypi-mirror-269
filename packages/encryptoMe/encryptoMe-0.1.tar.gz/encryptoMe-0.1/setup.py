from setuptools import setup, find_packages

setup(
    name='encryptoMe',
    version='0.1',
    packages=find_packages(),
    description='A simple encryption library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Praneeth Raghava Vadrevu',
    author_email='x23211946@student.ncirl.ie',
    license='MIT',
    install_requires=[
        'cryptography',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
