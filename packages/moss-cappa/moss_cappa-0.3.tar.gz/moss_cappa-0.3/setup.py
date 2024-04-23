from setuptools import setup, find_packages

try:
   import pypandoc
   long_description = pypandoc.convert_file('README.md', 'rst')
   long_description = long_description.replace("\r","")  
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='moss_cappa',
    version='0.3',
    description='Python-клиент Moss, предназначенный для использования в комплексе автоматической проверки программ CAPPA',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='shroud007',
    url='https://github.com/Shroud007/moss_cappa',
    download_url='https://github.com/Shroud007/moss_cappa/releases',
    keywords=['cappa', 'moss', 'plagiarism'],
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'lxml'
    ],
)