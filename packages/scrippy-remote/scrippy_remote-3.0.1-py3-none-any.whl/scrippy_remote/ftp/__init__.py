import os
import re
from scrippy_remote import ScrippyRemoteError, logger
from scrippy_remote.ftp.clients.ftp import FtpSimple
from scrippy_remote.ftp.clients.ftps import Ftps
from scrippy_remote.ftp.clients.ftpes import Ftpes
from scrippy_remote.local import list_local_dir, delete_local_file
from scrippy_remote.local import delete_local_dir, create_local_dirs


class Ftp:
  """This class' purpose is to provide a FTP client able to support all type of operations with or without implicit or explicit TLS support.

  Arguments:
    ``username``: String. Optional, default to 'anonymous'.
    ``password``: String. Optional, default to 'anonymous'.
    ``host``: String. The remote host to connect to.
    ``port``: Int. Optional. The TCP remote port to connect to. Default: ``21``.
    ``tls``: Boolean. Optional, default to True. If set to False, the FTP connection will not be encrypted.
    ``explicit``: Boolean. Optional, When set to True (default), the FTP connection will use explicit TLS (FTPes). If set to False, the connection will use implicit TLS (FTPs).
    ``ssl_verify``: Boolean. Optional. Default to True. If set to False, remote server SSL certificate will not be verified.
    ``ssl_version``: String. Optional. A string specifying the TLS version to use (Usually one of ``TLSv1_3`` or ``TLSv1_2``). Default to auto negotiation between client and server for highest possible security.
  """
  @property
  def connected(self):
    return self.client is not None and self._connected

  def __init__(self, host, port, username="anonymous", password="anonymous",
               tls=True, explicit=True, ssl_verify=True, ssl_version=None):
    self.host = host
    self.port = port
    self.username = username
    self.password = password
    self.tls = tls
    self.explicit = explicit
    self.ssl_verify = ssl_verify
    self.ssl_version = ssl_version
    self.client = None
    self._connected = False
    self._list_local_dir = list_local_dir
    self._delete_local_file = delete_local_file
    self._delete_local_dir = delete_local_dir
    self._create_local_dirs = create_local_dirs

  def __enter__(self):
    if self.tls:
      if self.explicit:
        self.client = Ftpes(self.host,
                            self.port,
                            self.username,
                            self.password,
                            self.ssl_verify,
                            self.ssl_version)
      else:
        self.client = Ftps(self.host,
                           self.port,
                           self.username,
                           self.password,
                           self.ssl_verify,
                           self.ssl_version)
    else:
      self.client = FtpSimple(self.host,
                              self.port,
                              self.username,
                              self.password)
    return self

  def __exit__(self, type_err, value, traceback):
    self._close()

  def _connect(self):
    """Connect to the remote server using the specified connection information.
    """
    logger.debug(f"Connecting to {self.host}:{self.port}")
    self._connected = self.client.connect()
    if self.connected:
      self.client.login()

  def _close(self):
    """Close the connection to remote server.
    """
    if self.connected:
      logger.debug(f"Closing connection to {self.host}:{self.port}")
      if self.client is not None:
        self.client.quit()
        self._connected = False

# -----------------------------------------------------------------------------
# Basic operations
# -----------------------------------------------------------------------------
  def get_file(self, remote_file, local_dir,
               create_dirs=False, exit_on_error=True):
    """
    Get file from remote server ``remote_file`` and store it to ``local_dir``.
    If ``create_dir`` is set to ``True``, a directory structure matching the remote directory hierarchy will be created locally.

    Arguments:
      ``remote_file``: The remote filepath to get the file from.
      ``local_dir``: The local directory where to store the local copy of the file.
      ``create_dirs``: Boolean. Optional. Create an exact copy of the remote directory structure. Default: ``False``
      ``exit_on_error``: Boolean. Optional. If set to ``False``, any error encountered will only be logged as a warning. Default: ``True``.
    """
    if not self.connected:
      self._connect()
    local_fname = os.path.join(local_dir, os.path.basename(remote_file))
    if create_dirs:
      local_fname = os.path.join(local_dir, remote_file.lstrip("/"))
      create_local_dirs(remote_file, local_dir)
    logger.debug(f"Getting remote file: {remote_file} => {local_fname} ")
    try:
      self.client.retrbinary(f"RETR {remote_file}",
                             open(local_fname, 'wb').write)
    except Exception as err:
      err_msg = f"[FtpTransferError] {err.__class__.__name__} {err}"
      if exit_on_error:
        logger.critical(err_msg)
        raise ScrippyRemoteError(err_msg) from err
      logger.warning(err_msg)

  def put_file(self, local_file, remote_dir="/",
               create_dirs=False, exit_on_error=True):
    """
    Send local file ``local_file`` to remote directory ``remote_dir``.
    If ``create_dirs`` is set to ``True``, a directory structure matching the local directory hierarchy will be created on the remote host.

    Arguments:
      ``local_file``: String. Local filename full path.
      ``remote_dir``: String. Optional. Remote directory where to store the file. Default to the remote root directory.
      ``create_dirs``: Boolean. Optional. Create all missing directory components found in ``remote_dir``. Default: ``False``.
      ``exit_on_error``: Boolean. Optional. If set to ``False``, any error encountered will only be logged as a warning. Default: ``True``.
    """
    if not self.connected:
      self._connect()
    remote_dir = remote_dir.lstrip("/")
    remote_file = os.path.basename(local_file)
    remote_fname = os.path.join(remote_dir, remote_file)
    if create_dirs:
      self._create_remote_dirs(remote_dir=remote_dir,
                               exit_on_error=exit_on_error)
    logger.debug(f"Sending file to: {remote_fname}")
    try:
      self.client.storbinary(f"STOR {remote_fname}", open(local_file, "rb"))
    except Exception as err:
      err_msg = f"[FtpTransferError] {err.__class__.__name__} {err}"
      if exit_on_error:
        logger.critical(err_msg)
        raise ScrippyRemoteError(err_msg) from err
      logger.warning(err_msg)

# -----------------------------------------------------------------------------
# Local operations
# -----------------------------------------------------------------------------
  def local_mirror(client, remote_dir, local_dir, exit_on_error=True):
    """Make a local copy of a remote directory recursively.

    Arguments:
      ``remote_dir``: String. The remote directory full path.
      ``local_dir``: String. The local directory full path.
      ``skip``: Int. Number of path subdirectory to skip. Default to ``0``.
      ``exit_on_error``: Boolean. When set to ``False``, transfer errors are ignored. If set to ``True``, raise error at first transfer error. Default to ``True``.
    """
    if not client.connected:
      client._connect()
    for r_file in client.list_remote_dir(remote_dir=remote_dir,
                                         file_type="f",
                                         pattern=".*"):
      client.get_file(remote_file=r_file,
                      local_dir=local_dir,
                      create_dirs=True,
                      exit_on_error=exit_on_error)
    for r_dir in client.list_remote_dir(remote_dir=remote_dir,
                                        file_type="d",
                                        pattern=".*"):
      client.local_mirror(remote_dir=r_dir,
                          local_dir=local_dir,
                          exit_on_error=exit_on_error)

  def list_local_dir(self, local_dir, file_type="f", pattern=".*"):
    return self._list_local_dir(local_dir=local_dir,
                                file_type=file_type,
                                pattern=pattern)

  def delete_local_file(self, local_file, exit_on_error=True):
    self._delete_local_file(local_file=local_file, exit_on_error=exit_on_error)

  def delete_local_dir(self, local_dir, recursive=False, exit_on_error=True):
    self._delete_local_dir(local_dir=local_dir,
                           recursive=False,
                           exit_on_error=exit_on_error)

  def create_local_dirs(self, remote_file, local_dir):
    self._create_local_dirs(remote_file=remote_file, local_dir=local_dir)

# -----------------------------------------------------------------------------
# Remote operations
# -----------------------------------------------------------------------------
  def list_remote_dir(self, remote_dir="/", file_type="f", pattern=".*"):
    """
    Get the complete list of files or dirs found in the specified remote directory and matching the specified file type (f or d) and the specified regular expression pattern.

    Note: This method is **NOT** recursive.

    Arguments:
      ``remote_dir``: String. Optional. The full path of the remote directory to explore. Default to remote root dir.
      ``file_type``: String. Optional. If set to ``d``, the returned list will only contain directory names. When set to ``f``, the returned list will contain only file names. Default: ``f``.
      pattern: String. A regular expression to filter returned values. Default to ``.*``
    """
    if not self.connected:
      self._connect()
    content = list()
    logger.debug(f"Exploring {remote_dir}")
    try:
      self.client.retrlines(f"LIST {remote_dir}", content.append)
      if file_type == 'f':
        reg = re.compile("^-.*")
      elif file_type == 'd':
        reg = re.compile("^d.*")
      content = [os.path.join(remote_dir, f.split()[-1]) for f in content if re.match(reg, f)]
      reg = re.compile(pattern)
      return [f.split()[-1] for f in content if re.match(reg, f)]
    except Exception as err:
      err_msg = f"[FtpRemoteError] {err.__class__.__name__} {err}"
      logger.critical(err_msg)
      raise ScrippyRemoteError(err_msg) from err

  def remote_mirror(self, local_dir, remote_dir, exit_on_error=True):
    """Make a remote copy of a local directory recursively.

    Arguments:
      ``local_dir``: String. The local directory full path.
      ``remote_dir``: String. The remote directory full path.
      ``exit_on_error``: Boolean. When set to ``False``, transfer errors are ignored. If set to ``True``, raise error at first transfer error. Default to ``True``.
    """
    if not self.connected:
      self._connect()
    for l_file in list_local_dir(local_dir=local_dir,
                                 file_type="f",
                                 pattern=".*"):
      self.put_file(local_file=l_file,
                    remote_dir=remote_dir,
                    create_dirs=True,
                    exit_on_error=exit_on_error)
    for l_dir in list_local_dir(local_dir=local_dir,
                                file_type="d",
                                pattern=".*"):
      r_dir = os.path.join(remote_dir, l_dir.split("/")[-1])
      self.remote_mirror(local_dir=l_dir,
                         remote_dir=r_dir,
                         exit_on_error=exit_on_error)

  def delete_remote_file(self, remote_file, exit_on_error=True):
    """
    Delete specified file from remote server.

    Arguments:
      ``remote_file``: The remote filepath to delete.
      ``exit_on_error``: Boolean. Optional. If set to ``False``, any error encountered will only be logged as a warning. Default: ``True``.
    """
    if not self.connected:
      self._connect()
    logger.debug(f"Deleting remote file: {remote_file}")
    try:
      self.client.delete(remote_file)
    except Exception as err:
      err_msg = f"[FtpTransferError] {err.__class__.__name__} {err}"
      if exit_on_error:
        logger.critical(err_msg)
        raise ScrippyRemoteError(err_msg) from err
      logger.warning(err_msg)

  def delete_remote_dir(self, remote_dir, recursive=False, exit_on_error=True):
    """
    Delete specified  directory from remote server.

    Arguments:
      ``remote_dir``: The remote directory to delete.
      ``recursive``: If set to ``True``, delete directory and all its content.
      ``exit_on_error``: Boolean. Optional. If set to ``False``, any error encountered will only be logged as a warning. Default: ``True``.
    """
    if not self.connected:
      self._connect()
    logger.debug(f"Deleting remote directory: {remote_dir}")
    try:
      for r_file in self.list_remote_dir(remote_dir=remote_dir):
        self.delete_remote_file(remote_file=r_file)
      if recursive:
        for r_dir in self.list_remote_dir(remote_dir=remote_dir, file_type="d"):
          self.delete_remote_dir(remote_dir=r_dir,
                                 recursive=recursive,
                                 exit_on_error=exit_on_error)
      self.client.rmd(remote_dir)
    except Exception as err:
      err_msg = f"[FtpTransferError] {err.__class__.__name__} {err}"
      if exit_on_error:
        logger.critical(err_msg)
        raise ScrippyRemoteError(err_msg) from err
      logger.warning(err_msg)

  def _create_remote_dirs(self, remote_dir, exit_on_error=True):
    """
    Create the specified directory structure on the remote host.

    Arguments:
      ``remote_dir``: String. The remote directory full path to create.
    """
    if not self.connected:
      self._connect()
    hierarchy = [d for d in remote_dir.split("/") if len(d) > 0]
    logger.debug(f"Creating remote dir: {remote_dir}")
    r_dir = "/"
    while len(hierarchy) > 0:
      r_dir = os.path.join(r_dir, hierarchy.pop(0))
      rmt_dir = os.path.dirname(r_dir)
      if f"{r_dir}" not in self.list_remote_dir(remote_dir=rmt_dir,
                                                file_type="d"):
        try:
          self.client.mkd(r_dir)
        except Exception as err:
          err_msg = f"[FtpCreateDirError] {err.__class__.__name__}: {err}"
          if exit_on_error:
            logger.critical(err_msg)
            raise ScrippyRemoteError(err_msg) from err
          logger.warning(err_msg)
