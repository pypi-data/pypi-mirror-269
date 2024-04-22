"""
Copyright (C) 2024 Athos Ribeiro

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from argparse import Namespace
from unittest.mock import patch

import lppa.cli


@patch('lppa.cli.PPA')
def test_create(MockedPPA):
    SUPPORTED_ARCHES = [
        'amd64', 'arm64', 's390x', 'ppc64el', 'armhf', 'armel', 'i386',
        'powerpc', 'riscv64'
    ]
    args = Namespace(proposed=True, processors=["all"], name="testppa")
    lppa.cli.create(args)
    MockedPPA.assert_called_with("testppa", SUPPORTED_ARCHES, pocket="Proposed")


@patch('lppa.cli.PPA')
def test_create_with_default_values(MockedPPA):
    SUPPORTED_ARCHES = [
        'amd64', 'arm64', 's390x', 'ppc64el', 'armhf', 'armel', 'i386',
        'powerpc', 'riscv64'
    ]
    args = Namespace(name="testppa", proposed=True, processors=None)
    lppa.cli.create(args)
    MockedPPA.assert_called_with("testppa", SUPPORTED_ARCHES, pocket="Proposed")


@patch('lppa.cli.PPA')
def test_create_with_no_proposed(MockedPPA):
    SUPPORTED_ARCHES = [
        'amd64', 'arm64', 's390x', 'ppc64el', 'armhf', 'armel', 'i386',
        'powerpc', 'riscv64'
    ]
    args = Namespace(name="testppa", proposed=False, processors=None)
    lppa.cli.create(args)
    MockedPPA.assert_called_with("testppa", SUPPORTED_ARCHES, pocket="Updates")


def test_delete():
    pass


def test_list():
    pass


def test_info():
    pass


def test_run():
    pass
