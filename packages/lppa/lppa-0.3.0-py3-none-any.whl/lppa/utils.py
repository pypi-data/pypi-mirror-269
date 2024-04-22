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
import requests

from lppa.auth import Session


def ppa_list():
    session = Session().get_session()
    me = session.me
    ppas_url = me.ppas_collection_link
    while ppas_url:
        r = requests.get(ppas_url)
        ppas = r.json()
        ppas_url = ppas.get('next_collection_link')
        for ppa in ppas['entries']:
            yield ppa['name']
