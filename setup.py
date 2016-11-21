from setuptools import setup

setup(name='apicartix',
      version='0.1',
      description='API CARTIX',
      url='https://github.com/rmuhire/apicartix',
      author='exuus',
      author_email='devteam@exuus.com',
      license='exuus',
      packages=['apicartix'],
      install_requires = [
            'Flask',
            'Flask-SQLalchemy',
            'Flask-Migrate'
      ],
      include_package_data=True,
      zip_safe=False)