from setuptools import setup, find_packages
from os import path
import sys

from io import open

here = path.abspath(path.dirname(__file__))
sys.path.insert(0, path.join(here, 'oscb'))
from version import __version__

print('version')
print(__version__)

# Get the long description from the README file
long_description = ''
readme_path = path.join(here, 'README.md')
try:
    with open(readme_path, encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    print(f"README.md not found at '{readme_path}'. No long description provided.")

package_data_list = []

setup(name='oscb',
      version=__version__,
      description='oscb',
      url='https://github.com/cirisjl/Machine-learning-development-environment-for-single-cell-sequencing-data-analyses.git',
      author='OSCB Team',
      author_email='',
      keywords=['pytorch', 'graph machine learning', 'graph representation learning', 'graph neural networks'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      install_requires = [
        'torch>=1.6.0',
        'numpy>=1.16.0',
        'tqdm>=4.29.0',
        'scikit-learn>=0.20.0',
        'pandas>=0.24.0',
        'six>=1.12.0',
        'urllib3>=1.24.0',
        'outdated>=0.2.0',
        'joblib>=1.3.2'
      ],
      license='MIT',
      packages=find_packages(exclude=['dataset', 'examples', 'docs']),
      package_data={'oscb': package_data_list},
      include_package_data=True,
      classifiers=[
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
)