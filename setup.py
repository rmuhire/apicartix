from setuptools import setup

setup(name='cartix',
      version='0.1',
      description='CARTIX',
      url='https://github.com/rmuhire/apicartix',
      author='exuus',
      author_email='devteam@exuus.com',
      license='exuus',
      packages=['cartix'],
      install_requires = [
            'Flask',
            'Flask-SQLalchemy',
            'Flask-Migrate',
            'marshmallow'
      ],
      include_package_data=True,
      zip_safe=False)