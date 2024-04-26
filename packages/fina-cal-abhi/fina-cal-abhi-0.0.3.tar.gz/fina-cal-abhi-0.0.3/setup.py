from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'A finance calculation package'
LONG_DESCRIPTION = 'A package that makes it easy to do finance calculation'

setup(
    name="fina-cal-abhi",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Abhishek Vyas",
    author_email="abhishek.vyas@gmail.com",
    license='NEXT',
    packages=find_packages(),
    install_requires=[],
    keywords='finance-calculation',
    # classifiers= [
    #     "Development Status :: 1 - Alpha",
    #     "Intended Audience :: Developers",
    #     'License :: OSI Approved :: NEXT License',
    #     "Programming Language :: Python :: 3",
    # ]
)