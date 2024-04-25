from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='wrapper-analytics',
    version='0.0.1',
    license='',
    author='Lucas Martim',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='',
    keywords='',
    description=u'Teste',
    packages=['lib_analytics_cofco'],
    install_requires=[''],)