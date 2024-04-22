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
import argparse

from lppa.ppa import PPA
import lppa.constants
import lppa.utils


def create(args):
    pocket = 'Updates'
    if args.proposed:
        pocket = 'Proposed'
    arches = args.processors or ['all']
    if 'all' in arches:
        arches = lppa.constants.PROCESSORS
    elif any(arch not in lppa.constants.PROCESSORS for arch in arches):
        argparse.ArgumentParser.exit(
            -1, f'Invalid "{arches}" is not a subset of "{lppa.constants.PROCESSORS}"'
        )
    archive = PPA(args.name, arches, pocket=pocket)
    archive.create()
    print(f'New PPA created: {args.name}')
    print(f'PPA Packages page: {archive.archive.web_link}/+packages')
    print('You can upload packages to this PPA using:')
    print(f'\t{archive.get_dput_str()}')


def delete(args):
    archive = PPA(args.name, None)
    archive.delete()


def list(args):
    for ppa_name in lppa.utils.ppa_list():
        print(ppa_name)


def info(args):
    archive = PPA(args.name, None)
    archive.set_existing_archive()
    if not archive.archive:
        argparse.ArgumentParser.exit(-1, f'"{args.name}" is not a valid PPA')
    print(f'PPA Packages page: {archive.archive.web_link}/+packages')
    print('You can upload packages to this PPA using:')
    print(f'\t{archive.get_dput_str()}')
    if args.verbose:
        print(f'"{archive.name}" is available for arches: {archive.get_processors()}')


def run():
    parser = argparse.ArgumentParser(description=lppa.constants.CLI_DESCRIPTION)
    parser.add_argument('--version', action='version', version=lppa.__version__)

    subparsers = parser.add_subparsers(help='sub-command help')

    parser_create = subparsers.add_parser('create', help='Create new PPA')
    parser_create.add_argument('name', help='Name of the PPA to be created')
    parser_create.add_argument(
        'processors',
        nargs='*',
        # choices=constants.PROCESSORS,
        help=(
            'List of launchpad processors to be enabled in the new PPA. Use "all" to enable all '
            'architectures. If no value is provided, assume all'
        )
    )
    parser_create.add_argument(
        '--proposed',
        help='Prefer build dependencies from the -proposed pocket',
        action=argparse.BooleanOptionalAction,
        default=True
    )
    parser_create.set_defaults(func=create)

    parser_delete = subparsers.add_parser('delete', help='Delete existing PPA')
    parser_delete.add_argument('name', help='Name of the PPA to be deleted')
    parser_delete.set_defaults(func=delete)

    parser_list = subparsers.add_parser('list', help="List user's PPAs")
    parser_list.set_defaults(func=list)

    parser_info = subparsers.add_parser('info', help='Fetch information on existing PPA')
    parser_info.add_argument('name', help='Name of the PPA of interest')
    parser_info.add_argument(
        '-v',
        '--verbose',
        help='Turn on verbose output for additional information about the archive',
        action='store_true'
    )
    parser_info.set_defaults(func=info)

    args = parser.parse_args()
    if not getattr(args, 'func', None):
        argparse.ArgumentParser.exit(-1, parser.format_help())

    args.func(args)
