"""
Copyright 2016 Brandon Michael Hoffman

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from setuptools import setup

setup(name='python-fossil',
      version='0.0.1',
      author='Brandon Hoffman',
      author_email='brandon.michael.hoffman@gmail.com',
      license="MIT",
      packages=['fossil'],
      install_requires=[
          "jinja2"
      ],
      install_develop=[
          "flake8",
          "pep8-naming",
          "tox",
          "coverage",
          "pytest",
          "pytest-cov",
          "isort",
          "wheel"
      ])
