import os
import re
import stat
import socket
import logging
import paramiko
from scrippy_remote import ScrippyRemoteError, logger
from scrippy_remote.local import list_local_dir, delete_local_file
from scrippy_remote.local import delete_local_dir, create_local_dirs


logging.captureWarnings(True)
paramiko_logger = paramiko.util.get_logger("paramiko")
paramiko_logger.disabled = True
paramiko_transport_logger = logging.getLogger("paramiko.transport")
paramiko_transport_logger.disabled = True


class Ssh:
  """This class purpose is to provide a SSH/SFTP client able to execute commands and transfer files using the SSH protocol.

  Arguments:

    ``username``: String. The user name to use for authentication on remote host.
    ``password``: String. Optional, the password to use fo authentication on remote host. If the ``key`` argument is provided, then the ``password`` value will be use as the SSH key passphrase.
    ``host``: String. The remote host to connect to.
    ``port``: Int. Optional. The TCP remote port to connect to. Default: ``22``.
    ``key``: String. Optional. The SSH private key file name to use for authentication on remote host.
    ``missing_host_key_policy``: String. Optional. Define the behavior when a remote key is missing and remote host is unknown. This should be one of ``auto``, ``warn``, ``reject``. Default to ``warn`` which automatically add remote host key to the known keys and log a warning.
    ``allow_agent``: Boolean. Optional. Do not use SSH agent if set to ``False``. Default: ``True``.
    ``look_for_keys``: Boolean. Optional. Do not search for discoverable private keys if set to ``False``. Default: ``True``.

    Note:
      - When the ``password`` argument is provided alongside the ``key`` argument then it will be assumed that the provided password is a passphrase for the specified key.
      - The ``missing_host_key_policy`` allow one of the 4 following values:
        - ``auto``: Automatically add remote host key to the known keys.
        - ``warn``: Same as auto and log a warning.
        - ``reject``: Reject the host key, do not proceed to connection and raise an error.
  """
  @property
  def connected(self):
    if self.client is not None and self.client.get_transport() is not None:
      return self.client.get_transport().is_active()
    return False

  @property
  def sftp(self):
    """
    Open a SFTP transport connection to remote host.
    """
    if not self.connected:
      self._connect()
    if self.sftp_client is None:
      self.sftp_client = self.client.open_sftp()
    return self.sftp_client

  def __init__(self, username, host, port=22,
               password=None, key=None, missing_host_key_policy="warn",
               allow_agent=True, look_for_keys=True):
    self.username = username
    self.host = host
    self.port = port
    self.password = password
    self.key = key
    self.allow_agent = allow_agent
    self.look_for_keys = look_for_keys
    self.missing_host_key_policy = missing_host_key_policy
    self.client = None
    self.sftp_client = None
    self._list_local_dir = list_local_dir
    self._delete_local_file = delete_local_file
    self._delete_local_dir = delete_local_dir
    self._create_local_dirs = create_local_dirs

  def __enter__(self):
    self._connect()
    return self

  def __exit__(self, type_err, value, traceback):
    self._close()

  def _connect(self):
    logger.debug(f"Connecting to {self.host}:{self.port}")
    self.client = paramiko.SSHClient()
    self.client.set_log_channel("laboro.ssh_transport")
    self.client.set_missing_host_key_policy(
        self._get_missing_key_policy(
            self.missing_host_key_policy))
    self.client.load_system_host_keys()
    try:
      self.client.connect(hostname=self.host,
                          port=self.port,
                          username=self.username,
                          password=self.password,
                          key_filename=self.key,
                          allow_agent=self.allow_agent,
                          look_for_keys=self.look_for_keys)
    except (paramiko.ssh_exception.BadHostKeyException,
            paramiko.ssh_exception.AuthenticationException,
            paramiko.ssh_exception.SSHException,
            socket.error,
            socket.gaierror,
            paramiko.ssh_exception.NoValidConnectionsError) as err:
      raise ScrippyRemoteError(f"[SshConnectionError] {err.__class__.__name__}: {err}") from err

  def _close(self):
    logger.debug(f"Closing connection to {self.host}:{self.port}")
    if self.connected:
      self.client.close()

  def _get_missing_key_policy(self, key):
    policies = {"auto": paramiko.client.AutoAddPolicy(),
                "warn": paramiko.client.WarningPolicy(),
                "reject": paramiko.client.RejectPolicy()}
    try:
      return policies[key]
    except KeyError as err:
      raise ScrippyRemoteError(f"[SshUnknownPolicyError] Unknown 'missing key policy': {key}") from err

  def _log_line(self, line, buffer, level):
    if len(line) > 0:
      buffer.append(line)
      logger.log(level, line)

# -----------------------------------------------------------------------------
# Basic operations
# -----------------------------------------------------------------------------
  def exec(self, command, exit_on_error=True):
    """
    Execute the specified command on the remote host.

    Arguments:
    ``command``: String. The command to be executed on the remote host.
    ``exit_on_error``: Boolean. Optional,  Boolean. Optional. If set to ``False``, any error encountered will only be logged as a warning. Default: ``True``.

    Returns:
      ``dict``: A dictionary containing the following items:
                - ``exit_code``: The exit code returned by the command.
                - ``stdout``: A list containing each line of the standard output returned by the command.
                - ``stderr``: A list containing each line of the standard error returned by the command.
    """
    if not self.connected:
      self._connect()
    logger.debug(f"Running command: {command}")
    try:
      exit_code = None
      stdin, stdout, stderr = self.client.exec_command(command)
      channel = stdout.channel
      stdout_content = list()
      stderr_content = list()
      while True:
        while channel.recv_ready():
          self._log_line(line=stdout.readline().strip(),
                         buffer=stdout_content,
                         level=logging.DEBUG)
        while channel.recv_stderr_ready():
          self._log_line(line=stderr.readline().strip(),
                         buffer=stderr_content,
                         level=logging.ERROR)
        if channel.exit_status_ready():
          self._log_line(line=stdout.readline().strip(),
                         buffer=stdout_content,
                         level=logging.DEBUG)
          self._log_line(line=stderr.readline().strip(),
                         buffer=stderr_content,
                         level=logging.ERROR)
          exit_code = channel.recv_exit_status()
          break
      if exit_code > 0:
        raise ScrippyRemoteError(f"[SshExecError] {' '.join(stderr_content)}")
      return {"exit_code": exit_code,
              "stdout": stdout_content,
              "stderr": stderr_content}
    except ScrippyRemoteError as err:
      logger.error(str(err))
      if not exit_on_error:
        return {"exit_code": exit_code,
                "stdout": stdout_content,
                "stderr": stderr_content}
      raise ScrippyRemoteError(str(err)) from err
    except paramiko.SSHException as err:
      err_msg = f"[SshExecError] {err.__class__.__name__}: {err}"
      if exit_on_error:
        raise ScrippyRemoteError(err_msg) from err
      logger.warning(err_msg)

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
    local_dir = local_dir.rstrip("/")
    local_fname = os.path.join(local_dir, os.path.basename(remote_file))
    if create_dirs:
      local_fname = os.path.join(local_dir, remote_file.lstrip("/"))
      create_local_dirs(remote_file, local_dir)
    logger.debug(f"Getting remote file: {remote_file}")
    try:
      self.sftp.get(remote_file, local_fname)
    except Exception as err:
      err_msg = f"[SftpTransferError] {err.__class__.__name__} {err}"
      if exit_on_error:
        logger.critical(err_msg)
        raise ScrippyRemoteError(err_msg) from err
      logger.warning(err_msg)

  def put_file(self, local_file, remote_dir,
               create_dirs=False, exit_on_error=True):
    """
    Send local file ``local_file`` to remote directory ``remote_dir``.
    If ``create_dirs`` is set to ``True``, a directory structure matching the local directory hierarchy will be created on the remote host.

    Arguments:
      ``local_file``: String. Local filename full path.
      ``remote_dir``: String. Remote directory where to store the file.
      ``create_dirs``: Boolean. Optional. Create all missing directory components found in ``remote_dir``. Default: ``False``.
      ``exit_on_error``: Boolean. Optional. If set to ``False``, any error encountered will only be logged as a warning. Default: ``True``.
    """
    remote_dir = remote_dir.rstrip("/")
    remote_fname = os.path.join(remote_dir, os.path.basename(local_file))
    logger.debug(f"Sending file to: {remote_fname}")
    if create_dirs:
      self._create_remote_dirs(remote_dir=remote_dir,
                               exit_on_error=exit_on_error)
    try:
      self.sftp.put(local_file, remote_fname, confirm=True)
    except Exception as err:
      err_msg = f"[SftpTransferError] {err.__class__.__name__} {err}"
      if exit_on_error:
        logger.critical(err_msg)
        raise ScrippyRemoteError(err_msg) from err
      logger.warning(err_msg)

# -----------------------------------------------------------------------------
# Local operations
# -----------------------------------------------------------------------------
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

  def local_mirror(self, remote_dir, local_dir, exit_on_error=True):
    """Make a local copy of a remote directory recursively.

    Arguments:
      ``remote_dir``: String. The remote directory full path.
      ``local_dir``: String. The local directory full path.
      ``skip``: Int. Number of path subdirectory to skip. Default to ``0``.
      ``exit_on_error``: Boolean. When set to ``False``, transfer errors are ignored. If set to ``True``, raise error at first transfer error. Default to ``True``.
    """
    for r_file in self.list_remote_dir(remote_dir=remote_dir,
                                       file_type="f", pattern=".*"):
      self.get_file(remote_file=os.path.join(remote_dir, r_file),
                    local_dir=local_dir,
                    create_dirs=True,
                    exit_on_error=exit_on_error)
    for r_dir in self.list_remote_dir(remote_dir=remote_dir,
                                      file_type="d", pattern=".*"):
      self.local_mirror(remote_dir=os.path.join(remote_dir, r_dir),
                        local_dir=local_dir,
                        exit_on_error=exit_on_error)

# -----------------------------------------------------------------------------
# Remote operations
# -----------------------------------------------------------------------------
  def list_remote_dir(self, remote_dir, file_type="f", pattern=".*"):
    """
    Get the complete list of files or dirs found in the specified remote directory and matching the specified file type (f or d) and the specified regular expression pattern.

    Note: This method is **NOT** recursive.

    Arguments:
      ``remote_dir``: String. Optional. The full path of the remote directory to explore.
      ``file_type``: String. Optional. If set to ``d``, the returned list will only contain directory names. When set to ``f``, the returned list will contain only file names. Default: ``f``.
      pattern: String. A regular expression to filter returned values. Default to ``.*``
    """
    dirs = list()
    files = list()
    if len(remote_dir) > 1:
      remote_dir = remote_dir.rstrip("/")
    reg = re.compile(pattern)
    logger.debug(f"Exploring {remote_dir}")
    try:
      for f in self.sftp.listdir_attr(remote_dir):
        if re.match(reg, f.filename):
          if stat.S_ISDIR(f.st_mode):
            dirs.append(f.filename)
          elif stat.S_ISREG(f.st_mode):
            files.append(f.filename)
          elif stat.S_ISLNK(f.st_mode):
            l_stat = self.sftp.stat(os.path.join(remote_dir, f.filename))
            if stat.S_ISDIR(l_stat.st_mode):
              dirs.append(f.filename)
            elif stat.S_ISREG(l_stat.st_mode):
              files.append(f.filename)
      if file_type == "f":
        return files
      elif file_type == "d":
        return dirs
    except Exception as err:
      err_msg = f"[SshRemoteOSError] {err.__class__.__name__} {err}"
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
    for l_file in self.list_local_dir(local_dir=local_dir,
                                      file_type="f",
                                      pattern=".*"):
      self.put_file(local_file=l_file,
                    remote_dir=remote_dir,
                    create_dirs=True,
                    exit_on_error=exit_on_error)
    for l_dir in self.list_local_dir(local_dir=local_dir,
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
    logger.debug(f"Deleting remote file: {remote_file}")
    try:
      self.sftp.remove(remote_file)
    except Exception as err:
      err_msg = f"[SftpRemoteOSError] {err.__class__.__name__} {err}"
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
    logger.debug(f"Deleting remote directory: {remote_dir}")
    try:
      for r_file in self.list_remote_dir(remote_dir=remote_dir):
        r_file = os.path.join(remote_dir, r_file)
        self.delete_remote_file(remote_file=r_file)
      if recursive:
        for r_dir in self.list_remote_dir(remote_dir=remote_dir, file_type="d"):
          r_dir = os.path.join(remote_dir, r_dir)
          self.delete_remote_dir(remote_dir=r_dir,
                                 recursive=recursive,
                                 exit_on_error=exit_on_error)
      self.sftp.rmdir(remote_dir)
    except Exception as err:
      err_msg = f"[SftpRemoteOSError] {err.__class__.__name__} {err}"
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
    hierarchy = [d for d in remote_dir.split("/") if len(d) > 0]
    logger.debug(f"Creating remote dir: {remote_dir}")
    r_dir = "/"
    while len(hierarchy) > 0:
      r_dir = os.path.join(r_dir, hierarchy.pop(0))
      rmt_dir = os.path.dirname(r_dir)
      if os.path.basename(r_dir) not in self.list_remote_dir(remote_dir=rmt_dir,
                                                             file_type="d"):
        try:
          self.sftp.mkdir(r_dir)
        except Exception as err:
          err_msg = f"[SftpRemoteOSError] {err.__class__.__name__}: {err}"
          if exit_on_error:
            logger.critical(err_msg)
            raise ScrippyRemoteError(err_msg) from err
          logger.warning(err_msg)
