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

import lppa.utils


def mocked_request(*args, **kwargs):
    class MockedResponse:
        def __init__(self, json_data):
            self.json_data = json_data

        def json(self):
            return self.json_data

    return MockedResponse({'entries': [{'name': 'ppa1'}, {'name': 'ppa2'}]})


@patch('launchpadlib.launchpad.Launchpad.login_with')
@patch('requests.get', side_effect=mocked_request)
def test_ppa_list(MockedRequest, MockedSession):
    ppas = lppa.utils.ppa_list()
    assert list(ppas) == ['ppa1', 'ppa2']
