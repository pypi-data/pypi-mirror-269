from setuptools import setup, find_packages
import os

version = '3.0.0'

setup(
    name='collective.MockMailHost',
    version=version,
    description="Used for integration testing with Plone",
    long_description="\n".join([
        open("README.rst").read(),
        open(os.path.join("collective", "MockMailHost", "tests",
                          "SendEmail.txt")).read(),
        open("CHANGES.rst").read(),
    ]),
    # Get more strings from https://pypi.org/classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords='mock mailhost tests',
    author='Suresh V.',
    author_email='suresh@grafware.com',
    url='https://github.com/collective/collective.mockmailhost',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
      'setuptools',
      'Products.GenericSetup',
      'Products.MailHost',
      'Products.CMFCore',
      # -*- Extra requirements: -*-
    ],
    extras_require={
      'test': [
          'plone.app.testing',
          'plone.testing',
          'zope.component',
      ],
    },
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
)
