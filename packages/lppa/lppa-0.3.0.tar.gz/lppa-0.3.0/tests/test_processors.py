"""
Copyright (C) 2021 Athos Ribeiro

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
from unittest.mock import Mock, patch

from lppa.processors import Processors


@patch('lppa.auth.Session.get_session', return_value='stub_session')
def test_instance_without_session(MockedSession):
    processors = Processors()
    MockedSession.assert_called_once()
    assert processors.session == 'stub_session'


@patch('lppa.auth.Session.get_session')
def test_instance_with_session(MockedSession):
    session = Mock()
    processors = Processors(session)
    MockedSession.assert_not_called()
    assert processors.session == session


def test_fetch_when_not_set():
    session = Mock(processors='stub_session_processors')
    processors = Processors(session)
    assert processors.processors is None
    processors.fetch()
    assert processors.processors == 'stub_session_processors'


def test_fetch_when_already_set():
    session = Mock(processors='stub_session_processors')
    processors = Processors(session)
    processors.processors = 'existing_data'
    processors.fetch()
    assert processors.processors == 'existing_data'


def test_list_when_not_set():
    mocked_processors = [Mock(), Mock()]
    mocked_processors[0].configure_mock(name='arch1')
    mocked_processors[1].configure_mock(name='arch2')
    session = Mock(processors=mocked_processors)
    processors = Processors(session)
    assert processors.list() == ['arch1', 'arch2']


def test_list_when_already_set():
    session = Mock()
    processors = Processors(session)
    processors.processors = [Mock(), Mock()]
    processors.processors[0].configure_mock(name='arch1')
    processors.processors[1].configure_mock(name='arch2')
    assert processors.list() == ['arch1', 'arch2']


def test_get_by_name_when_not_set():
    mocked_processors = Mock()
    attrs = {'getByName.return_value': 'arch'}
    mocked_processors.configure_mock(**attrs)
    session = Mock(processors=mocked_processors)
    processors = Processors(session)
    arch = processors.get_by_name(name='arch')
    assert arch == 'arch'


def test_get_by_name_when_already_set():
    session = Mock()
    processors = Processors(session)
    processors.processors = Mock()
    attrs = {'getByName.return_value': 'arch'}
    processors.processors.configure_mock(**attrs)
    arch = processors.get_by_name(name='arch')
    assert arch == 'arch'


def test_get_by_name_not_found():
    pass
