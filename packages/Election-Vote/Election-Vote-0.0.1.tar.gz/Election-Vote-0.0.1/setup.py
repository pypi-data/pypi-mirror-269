from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Election-Vote',
  version='0.0.1',
  description='Displays the button on the Front endto vote for the students ',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Yamini x23166401@student.ncirl.ie',
  author_email='x23166401@student.ncirl.ie',
  license='MIT', 
  classifiers=classifiers,
  keywords='Election-Vote', 
  packages=find_packages(),
  install_requires=[
    'django',
    ] 
)
