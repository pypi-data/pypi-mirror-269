from setuptools import setup

setup(name='thriftify',
      version='0.1.5',
      description='Converts xlsx files into thrift binary or json blobs',
      long_description='Uses thrift-generated python reflection classes to match spreadsheet data with your thrift file. You can then load the resulting blob in any language supported by thrift.',
      long_description_content_type='text/x-rst',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
      ],
      keywords='thrift config',
      url='http://github.com/ohthepain/thriftify',
      author='Paul Wilkinson',
      author_email='paul@thisco.co',
      license='MIT',
      packages=['thriftify'],
      install_requires=[
            'openpyxl',
            'datetime',
            'thrift',
            'argparse',
            'datetime',
      ],
      # scripts=['bin/thriftify_cli'],
      entry_points = {
        'console_scripts': [
          'thriftify=thriftify.command_line:main',
        ],
      },
      zip_safe=False)

