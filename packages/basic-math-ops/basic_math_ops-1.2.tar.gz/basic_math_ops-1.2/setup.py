from setuptools import setup

setup(name="basic_math_ops",
      version="1.2",
      description="This package consists of math operation ",
      long_description="This package performs basic math operations",
      author="Nipun Verma",
      packages=['pcki'],
      install_requires=[],
      extras_require={"dev":["twine>=4.0.2"]}
      )