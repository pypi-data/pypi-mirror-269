# Config Manager (cmgr)
[CHANGELOG](CHANGELOG.md)

[cmgr](https://github.com/kyan001/PyConfigManager) is a command-line tool to manage configurations and packages. It's designed to be simple and easy to use. It's written in Python and can be installed via pip and pipx.

## Get Started

```sh
pip install cmgr  # Install cmgr

cmgr  # Run cmgr.
```

## Installation

```sh
pip install --user cmgr  # install cmgr
pip install --upgrade cmgr # upgrade cmgr
pip uninstall cmgr  # uninstall cmgr

# using pipx
pipx install cmgr  # install cmgr
pipx upgrade cmgr  # upgrade cmgr
pipx uninstall cmgr  # uninstall cmgr
```

## Usage

```sh
# Shell
cmgr --help  # Command-line help message.
cmgr --version  # Show version information.

cmgr  # Run cgmr. Will looking for all cmgr.toml under current folder.
cmgr -p/--profile '/path/to/root/cmgr.toml'  # Run cmgr with specific profile.
cmgr -r/--root '/path/to/root/'  # Run cmgr with specific root folder.
cmgr -n/--name 'my-cmgr.toml'  # Run cmgr with specific profile's filename.

# Install package
cmgr install ping3  # Install a package named ping3. Using default package manager.
cmgr install ping3 -c/--command 'ping3'  # Use specific command to detect if the package is installed before install.
cmgr install ping3 -m/--manager 'pip'  # Use specific package manager to install the package.

# Copy configuration
cmgr config "bash.conf" "~/.bashrc"  # Copy `bash.conf` to `~/` as `.bashrc`.
cmgr config "bash.conf" "~/.bashrc" -n/--name "BASH"  # Copy `bash.conf` to `~/` as `.bashrc` with specific name in output.
```

## Profile
* A cmgr profile example: [cmgr-example.toml](cmgr-example.toml)
* A minimal cmgr profile: [cmgr-minimal.toml](cmgr-minimal.toml)
