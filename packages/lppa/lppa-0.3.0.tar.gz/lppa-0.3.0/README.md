# DISCONTINUED

This has been discontinued in favor of
[ppa-dev-tools](https://code.launchpad.net/~bryce/ppa-dev-tools/+git/ppa-dev-tools-1).

While this is still useful for examples, I no longer intend to proceed with
development for this tool. Please, use ppa-dev-tools instead.

# lppa

Command line tool to create Launchpad PPAs and push deb source packages to them.

While this tool is intended to be used by distribution developers who often
need to prepare and push packages to test PPAs, this can also be used by
developers who wish to distribute their software through PPAs. For the latter,
please make sure to check the documentation since the default values are
designed to enhance the former use cases.

## Installation

```
pip install lppa
```

## Usage

lppa ships an `lppa` command line application to interact with Launchpad PPAs.
Run

```
lppa --help
```

for additional information.

### Create a new PPA

To create a new PPA, run

```
lppa create PPA_NAME [all|arch, ...]
```

where arch is a Launchpad processor (you can pass multiple architectures here)
or `all` to enable all available architectures. If no architecture is passed,
`all` is assumed.

The currently available Launchpad processors are

- amd64
- arm64
- s390x
- ppc64el
- armhf
- armel
- i386
- powerpc
- riscv64

### Delete an existing PPA

```
lppa delete PPA_NAME
```

### List user's PPAs

```
lppa list
```

This will print a list with the names of the user's available PPAs

### Fetch PPA information

Often, you may want to retrieve an URL for a PPA packages page or quickly fetch
a dput command to upload packages to a PPA. That can be achieved through the
`info` command.

```
lppa info PPA_NAME
```

Moreover, passing the `-v` option to the info command will also display the
architectures for which the PPA can build packages.

## Development

Run `make devel` to set the development environment up (a python virtual
environment is recommended).

Run `make check` to run the test suite and ensure the development environment
is up to date.

You can use `make coverage` to ensure code coverage is not drastically reduced
by new changes (if proposing changes, try to write some tests for them).

For instance, a complete bootstrap script would look like:

```
# apt install -y python3-virtualenv python3-virtualenvwrapper
$ mkvirtualenv lppa
$ workon lppa
$ make devel
$ make check
```

### Releasing

There is a `make release` target which will

- Change `lppa/__init__.py` to set the version to be published
- Update the CHANGELOG.md file with towncrier entries
- Commit the changes above and tag the repository
- Push the changes to PyPI (login required)
- Add a final commit bumping the package version to a new development one

Finally, a manual `git push` (including tags) is required.
