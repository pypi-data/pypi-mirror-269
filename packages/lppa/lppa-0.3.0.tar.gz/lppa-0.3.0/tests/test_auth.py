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
from unittest.mock import patch

import pytest

from lppa import auth


@patch('launchpadlib.launchpad.Launchpad.login_with')
@patch('launchpadlib.launchpad.Launchpad.login_anonymously')
def test_anonymous_session(MockedAnon, MockedAuth):
    session = auth.Session(anonymous=True)
    session.get_session()
    MockedAuth.assert_not_called()
    MockedAnon.assert_called_once()


@patch('launchpadlib.launchpad.Launchpad.login_with')
@patch('launchpadlib.launchpad.Launchpad.login_anonymously')
def test_authenticated_session(MockedAnon, MockedAuth):
    session = auth.Session()
    session.get_session()
    MockedAnon.assert_not_called()
    MockedAuth.assert_called_once()


@patch('launchpadlib.launchpad.Launchpad.login_with', side_effect=auth.AuthenticationError)
@patch('launchpadlib.launchpad.Launchpad.login_anonymously')
def test_auth_error_no_fallback(MockedAnon, MockedAuth):
    session = auth.Session()
    with pytest.raises(auth.AuthenticationError):
        session.get_session()
    MockedAuth.assert_called_once()
    MockedAnon.assert_not_called()


@patch('launchpadlib.launchpad.Launchpad.login_with', side_effect=auth.AuthenticationError)
@patch('launchpadlib.launchpad.Launchpad.login_anonymously')
def test_auth_error_with_fallback(MockedAnon, MockedAuth):
    session = auth.Session()
    session.get_session(anonymous_fallback=True)
    MockedAuth.assert_called_once()
    MockedAnon.assert_called_once()
