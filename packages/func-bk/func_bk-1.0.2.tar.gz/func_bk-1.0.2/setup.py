from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='func_bk',
      version='1.0',
      description='add function for normal python and add class(for inheritance) for django',
      packages=['func_bk'],
      author_email='lilo.pio147@mail.ru',
      zip_safe=False,
      long_description=long_description,
      long_description_content_type='text/markdown')