from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='pgpyui',
  version='0.0.2',
  author='Memdved',
  author_email='mixail.vilyukov@icloud.com',
  description='The package is an add-on for Pygame to create a user interface on the screen.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://pypi.org/project/pgpyui/',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='ui gui pgpyui pygame',
  project_urls={
    'GitHub': 'https://github.com/Memdved'
  },
  python_requires='>=3.6'
)
