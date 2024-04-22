from setuptools import setup
from os import path


top_level_directory = path.abspath(path.dirname(__file__))
with open(path.join(top_level_directory, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
   name='ya-music-rnd',
   version='1.1.0',
   description='Поиск случайного исполнителя на сайте яндекс музыки',
   long_description=long_description,
   long_description_content_type='text/markdown',
   author='Genzo',
   author_email='genzo@bk.ru',
   url='https://github.com/Genzo4/yandex_rnd',
   project_urls={
           'Bug Tracker': 'https://github.com/Genzo4/yandex_rnd/issues',
       },
   classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3.9',
      'Programming Language :: Python :: 3.10',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      'Intended Audience :: Developers',
      'Intended Audience :: End Users/Desktop',
      'Natural Language :: English',
      'Natural Language :: Russian',
      'Topic :: Scientific/Engineering',
      'Topic :: Software Development',
      'Topic :: Software Development :: Libraries :: Python Modules'
   ],
   keywords=['yandex', 'music', 'yandex_rnd', 'ya_music_rnd', 'ya'],
   license='MIT',
   packages=['ya_music_rnd'],
   install_requires=['urllib3'],
   python_requires='>=3.8'
)