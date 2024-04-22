from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='hsr_pic_parcer',
  version='1.0.2',
  author='vano979797',
  author_email='vano979797@gmail.com',
  description='parser to get images from hsr mana',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/vano979797/hsr_pic_parser',
  packages=find_packages(),
  install_requires=['requests>=2.25.1', 'beautifulsoup4>=4.12.3'],
  classifiers=[
    'Programming Language :: Python :: 3.12',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='python parse hsr',
  project_urls={
    'Documentation': 'https://github.com/vano979797/hsr_pic_parser/blob/4a0309d617f93c56714fe206753119f690109219/README.md'
  },
  python_requires='>=3.7'
)