# setup.py

from setuptools import setup, find_packages

packs= find_packages()
print(packs)

setup(
    name='heimdall_tools',
    version='0.1.2',
    packages=find_packages(),
    #packages=['heimdall_tools'],
    install_requires=[
        'boto3',
        'mysql-connector-python',
        # Add any other dependencies here
    ],
    author='Robin Thomas',
    author_email='robin@clockhash.com',
    description='Custom package including all modules required for my application',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your_username/your_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
)
