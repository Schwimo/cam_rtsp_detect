#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='rtsp_ws_stream',
      version='0.1',
      description='Python library to provide a rtsp from camera via websocket',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Schwimo',
      author_email='Schwimo@github.com',
      url='www.schwuster.de',
      packages=setuptools.find_packages('include'),
      package_dir={'': 'include'},
      classifiers=[
          'Programming Language :: Python3',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: Ubuntu',
      ],
      install_requires=[
          'opencv-python',
          'numpy',
          'autobahn',
          'twisted'
      ]
      )
