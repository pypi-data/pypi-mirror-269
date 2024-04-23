import os

from setuptools import setup, find_packages

# read the contents of your README file

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version_dev='1.0.0'
version_prod='1.0.11'

run_mode=''

setup(name='m-utilities' + run_mode,
      version='1.0.11',
      description='Mobio Utilities, tổng hợp thư viện được dùng thường xuyên trong các micro-service Mobio.',
      url='',
      author='MOBIO',
      author_email='contact@mobio.vn',
      license='MIT',
      package_dir={'': './'},
      packages=find_packages('./'),
      install_requires=['m-singleton==0.3',
                        'm-monitor==0.6',
                        'm-validator==0.1',
                        'm-filetypes',
                        'm-cipher==1.5.2',
                        'm-schedule==1.0.1',
                        'm-caching==0.1.15',
                        'm-threadpool==0.2',
                        'm-formatter-logging>=1.0.2',
                        'm-kafka-sdk-v2==1.0.1',
                        ],
      long_description=long_description,
      long_description_content_type='text/markdown',
      python_requires='>=3.8'
      )
