from setuptools import setup, find_packages

setup(
    name='PyDL7',
    version='0.0.3',
    description='Python API for parsing DAN Dive Log files.',
    author='Simon Johnston',
    author_email='johnstonskj@gmail.com',
    download_url='https://pypi.python.org/pypi/PyDL7',
    url='https://github.com/johnstonskj/PyDL7',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        ],
    packages=find_packages(exclude=['docs', 'tests']),
    entry_points={
        'console_scripts': [
            'dl7dump=divelog.command_line:main',
            ],
        }
)
