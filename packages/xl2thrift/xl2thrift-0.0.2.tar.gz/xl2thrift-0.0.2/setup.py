from setuptools import setup

setup(name='xl2thrift',
      version='0.0.2',
      description='Converts xlsx files into thrift files that can be deserialized in many programming languages',
      long_description='Uses thrift-generated python reflection classes to match spreadsheet data with your thrift file. You can then load the resulting blob in any language supported by thrift.',
      long_description_content_type='text/x-rst',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
      ],
      keywords='thrift config',
      url='http://github.com/ohthepain/xl2thrift',
      author='Paul Wilkinson',
      author_email='paul@thisco.co',
      license='MIT',
      packages=['xl2thrift'],
      install_requires=[
            'openpyxl',
            'datetime',
            'thrift',
            'argparse',
            'datetime',
      ],
      entry_points = {
        'console_scripts': [
          'xl2thrift=xl2thrift.command_line:main',
        ],
      },
      zip_safe=False)

