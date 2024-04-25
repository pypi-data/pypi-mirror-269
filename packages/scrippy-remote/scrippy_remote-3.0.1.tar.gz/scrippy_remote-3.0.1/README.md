
![Build Status](https://drone-ext.mcos.nc/api/badges/scrippy/scrippy-remote/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)

![Scrippy, my scrangourou friend](./scrippy-remote.png "Scrippy, my scrangourou friend")

# `scrippy_remote`

SSH/SFTP/FTP client for the [`Scrippy`](https://codeberg.org/scrippy) framework.

## Prerequisites

### Python modules

#### List of necessary modules

The modules listed below will be automatically installed.

- paramiko
- pysmb

## Installation

### Manual

```bash
git clone https://codeberg.org/scrippy/scrippy-remote.git
cd scrippy-remote
python -m pip install -r requirements.txt
make install
```

### With `pip`

```bash
pip install scrippy-remote
```

### Usage

### `scrippy_remote`

This module offers all the objects, methods, and functions for operations on remote hosts accessible via _SSH/SFTP_ or _FTP_ and a limited support of _CIFS_:
- Execution of commands on a remote host
- Copying directories/files to a remote host
- Deleting directories/files on a remote host
- Copying files between remote hosts (with the local machine acting as a buffer)
- ...

The `scrippy_remote` module provides several objects for transferring files via SFTP, FTP, FTPS, or CIFS, and for remote command execution via SSH.

The source code for the `scrippy_remote.remote` module and its sub-modules is also extensively commented and remains the best source of documentation.

A HTML version of the documentation can be generated using sphinx:

```shell
pip3 install sphinx
cd scrippy-remote
make doc
```

The resulting documentation will be generated in the `docs/build/html` directory.

#### Local operations

Each of the `Ssh`, `Ftp`, `Cifs` classes comes with some helper functions to operate on the local host such as :

- [List a local directory content with a pattern filter](README/local.md#list-a-local-directory-content-with-a-pattern-filter)
- [Delete a local file](README/local.md#delete-a-local-file)
- [Delete a local directory recursively](README/local.md#delete-a-local-directory-recursively)


#### SSH/SFTP Operations

The `Ssh` class provides specific methods to execute commands and handle files and directory handling such as :

- [Execute a command on a remote host](README/ssh.md#execute-a-command-on-a-remote-host)
- [Retrieve a remote file](README/ssh.md#retrieve-a-remote-file)
- [Mirror a remote directory to a local directory](README/ssh.md#mirror-a-remote-directory-to-a-local-directory)
- [Transfer a file to a remote host](README/ssh.md#transfer-a-file-to-a-remote-host)
- [Mirror a local directory to a remote directory](README/ssh.md#mirror-a-local-directory-to-a-remote-directory)
- [List remote directory content](README/ssh.md#list-remote-directory-content)
- [Delete a remote file](README/ssh.md#delete-a-remote-file)
- [Delete a remote directory recursively](README/ssh.md#delete-a-remote-directory-recursively)


#### FTP

The `Ftp` class provides specific methods to execute commands and handle files and directory handling such as :

- [Retrieve a remote file](README/ftp.md#retrieve-a-remote-file)
- [Mirror a remote directory to a local directory](README/ftp.md#mirror-a-remote-directory-to-a-local-directory)
- [Transfer a file to a remote host](README/ftp.md#transfer-a-file-to-a-remote-host)
- [Mirror a local directory to a remote directory](README/ftp.md#mirror-a-local-directory-to-a-remote-directory)
- [List remote directory content](README/ftp.md#list-remote-directory-content)
- [Delete a remote file](README/ftp.md#delete-a-remote-file)
- [Delete a remote directory recursively](README/ftp.md#delete-a-remote-directory-recursively)


#### CIFS

The `Cifs` class provides specific methods to transfer files using the *CIFS/Samba* protocol such as:

- [Retrieve a remote file](README/cifs.md#retrieve-a-remote-file)
- [Transfer a file to a remote host](README/cifs.md#transfer-a-file-to-a-remote-host)
- [Open a file in write mode](README/cifs.md#open-a-file-in-write-mode)
- [Open a file in read mode](README/cifs.md#open-a-file-in-read-mode)
- [Delete remote directory content](README/cifs.md#delete-remote-directory-content)
