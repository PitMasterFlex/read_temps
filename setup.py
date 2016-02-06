#   Copyright 2016 Michael Rice <michael@michaelrice.org>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import os
from setuptools import setup, find_packages

import pitmaster


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fn:
        return fn.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('test-requirements.txt') as f:
    required_for_tests = f.read().splitlines()

setup(
    name='read_temps',
    version=pitmaster.__version__,
    packages=find_packages(exclude=["tests", "*.tests", "tests.*", "*.tests.*"]),
    url=pitmaster.__url__,
    license='License :: OSI Approved :: Apache Software License',
    author=pitmaster.__author__,
    author_email=pitmaster.__email__,
    long_description=read('README.rst'),
    description='BBQ thing for Raspberry Pi',
    zip_safe=False,
    include_package_data=True,
    setup_requires=[required_for_tests],
    install_requires=required,
    test_suite='tests',
    tests_require=required_for_tests,
    entry_points={
        "console_scripts": [
            "read_temps = pitmaster.executable:execute"
        ]
    }
)
