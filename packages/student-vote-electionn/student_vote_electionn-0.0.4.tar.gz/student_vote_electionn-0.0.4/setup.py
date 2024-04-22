from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='student_vote_electionn',
  version='0.0.4',
  description='This is simple announcement that will show up on the screen.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Yamini x23166401@student.ncirl.ie',
  author_email='x23166401@student.ncirl.ie',
  license='MIT', 
  classifiers=classifiers,
  keywords='studentvoteelectionn', 
  packages=find_packages(),
  install_requires=[
    'django',
    ] 
)
