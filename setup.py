from setuptools import setup  # , find_packages
import emailage

LONG_DESCRIPTION = open('README.rst').read()

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

KEYWORDS = 'emailAge api wrapper'

setup(
    name='emailage',
    # packages=find_packages(),
    include_package_data=True,
    version=emailage.__version__,
    description='A Python EmailAge API Wrapper',
    long_description=LONG_DESCRIPTION,
    author='radzhome',
    download_url='http://pypi.python.org/pypi/emailage/',
    url='http://www.github.com/radzhome',
    packages=['emailage', ],
    package_dir={'emailage': 'emailage'},
    platforms=['Platform Independent'],
    license='BSD',
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    requires=['requests'],
    install_requires=['requests'],
)
