from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='PyDL7',
    version='0.0.3',
    description='Python API for parsing DAN Dive Log files.',
    long_description=readme(),
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
    packages=['divelog'],
    setup_requires=['pytest-runner'],
    tests_require=[
          'pytest',
          'pytest-cov',
          'pytest-pep8'
      ],
    entry_points={
        'console_scripts': [
            'dl7dump=divelog.command_line:main',
            ],
        }
)
