from setuptools import setup, find_packages

setup(name='keycloak-oid-client',
      version='0.0.1',
      description='Simple OpenID client',
      url='https://git.ocherepanov.ru/ocherepanov/oid-client',
      author='O.S. Cherepanov',
      author_email='ocherepanov@inbox.ru',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'python-keycloak-client',
          'xmltodict',
      ]
)
