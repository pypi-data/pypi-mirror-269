from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

# Readme and changelog content
try:
    with open('README.txt', 'r') as readme_file:
        readme_content = readme_file.read()
except FileNotFoundError:
    readme_content = 'No README available.'

try:
    with open('CHANGELOG.txt', 'r') as changelog_file:
        changelog_content = changelog_file.read()
except FileNotFoundError:
    changelog_content = 'No changelog available.'

setup(
  name='sbmp',
  version='4.0.3',
  description='SBMP',
  long_description=readme_content + '\n\n' + changelog_content,
  url='',  
  author='Jainam Barbhaya',
  author_email='jainambarbhaya1509@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['sbmp'], 
  packages=find_packages(),
)
