from setuptools import setup

with open("README.rst", "r") as f:
    readme = f.read()

setup(
    name='poplar_apcheques',
    version='1.0.29',
    author='Poplar Development',
    url='https://poplars.dev',
    author_email='chris@poplars.dev',
    packages=['poplar_apcheques'],
    package_data={
        '': ['vi/*.vi', 'expi.json' ],
    },
    description=(""),
    long_description=readme,
    include_package_data=True,
    install_requires=[
        'excrypto>=0.1.8',
        'extools>=0.13.44'
        'poplar_workflow>=1.0.4',
        'pdfrw',
        'wheel'
    ],
    # Valid classifiers: https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: End Users/Desktop",
        "License :: Other/Proprietary License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.4",
    ],
    keywords=[
        "Orchid", "Extender", "Sage 300", "Automation",
    ],
    download_url="https://expi.dev/poplar_apcheques/"
)
