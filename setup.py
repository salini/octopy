
import os, sys
from distutils.core import setup, Command

import subprocess

import octopy


CWD=os.path.realpath(os.path.dirname(__file__))


cmdclass = {}
try:
    from sphinx.setup_command import BuildDoc # add a command for building the html doc
    cmdclass['build_doc'] = BuildDoc
except ImportError:
    pass


class RunTestCmd(Command):
    description = 'run all tests in tests folder'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        sys.exit(os.system("python "+CWD+"/tests/runAllTests.py"))


cmdclass["run_tests"] = RunTestCmd


class RunPyLintCmd(Command):
    description = 'run pylint on myProject Package'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        sys.exit(os.system("pylint octopy"))

cmdclass["run_pylint"] = RunPyLintCmd




with open('README.md', 'r') as f:
    readme = f.read()


setup(
    name='octopy',
    version=octopy.version(),
    description='A template to manipulate octree',
    long_description=readme,
    license='GPL',
    author=['joseph salini'],
    author_email=['josephsalini@gmail.com'],
    url='https://github.com/salini/octopy',
    packages=['octopy'],
    cmdclass=cmdclass,
)
