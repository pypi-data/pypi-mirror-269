from pathlib import Path
import setuptools

def get_long_description():
    long_description=''
    with open(Path(Path(__file__).parent,'README.md'), 'r') as fh:
        long_description=fh.read()
    return long_description

setuptools.setup(
    name='coolML',
    version='0.0.8',
    description='Cool ML is a machine learning workflow developed to optimize thermionic double-assymmetric barrier heterostructures based on semiconductors',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='Julian Garcia Fernandez ',
    author_email='julian.garcia.fernandez2@usc.es',
    url='https://gitlab.citius.usc.es/modev/coolML',
    setup_requires=['setuptools'],
    install_requires=['torch','pytorch_lightning','wandb','numpy','pandas','scikit-learn','pathlib'],
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    classifiers=[
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
    ],
)

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
