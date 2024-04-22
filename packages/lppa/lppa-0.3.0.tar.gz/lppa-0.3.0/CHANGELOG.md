lppa 0.3.0 (2024-04-21)
=======================

### Features

- Add RiscV to supported architectures
- If no architectures are provided when creating a new PPA, lppa will create a
  PPA with all supported architectures enables. This changes the previous default
  behavior where only x86_64 and i386 would be enabled by default.
- The --proposed PPA creation option is now the default value for the create
  subcommand. A new --no-proposed option was added to disable the -proposed
  pocked in the created PPA.
- A new --version option was added to display the current lppa version

### Bugfixes

- Support PPA list pagination. The PPA lists are paginated. To correctly fetch
  the list of PPAs, we need to keep iterating over the paginated lists.

### Improved Documentation

- Make it explicit that this tool is intended for distribution developers and
  therefore, all default values are designed to enhance their experience

### Misc

- 


lppa 0.2.1 (2022-01-30)
=======================

Features
--------

- Add --proposed option to the create command to create a PPA for the proposed
  pocket


Bugfixes
--------

- Print CLI help when no args are passed


Improved Documentation
----------------------

- Update development documentation
- Update documented pip installation method
- Add CHANGELOG.md file


lppa 0.2.0 (2021-08-24)
=======================

- Rename project to avoid PyPI packaging conflicts

Features
--------

- Add new `delete` command
- Add new `list` command
- Add new `info` command
- Set default log level to warning
- Do not allow `create` requests with invalid architectures


ppa 0.1.0 (2021-06-22)
======================

- Initial release
