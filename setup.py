from setuptools import setup, find_packages

setup(
    name='awseb-fab-tasks',
    packages=find_packages(),
    install_requires=['requests', ],
    include_package_data=True,
    version='0.0.1',
    description='Python EmailAge Wrapper',
    long_description='A python wrapper for EmailAge API',
    author='radlws',
    url='http://www.github.com/radlws',
    license='BSD',
    zip_safe=False,
)
