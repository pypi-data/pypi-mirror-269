"""
The scrippy_remote.remote.cifs module implements the client part of the CIFS protocol in the form of the Cifs class.
"""
import os
import socket
import tempfile
from scrippy_remote import ScrippyRemoteError, logger
from scrippy_remote.local import list_local_dir, delete_local_file
from scrippy_remote.local import delete_local_dir, create_local_dirs
from smb.SMBConnection import SMBConnection


class Cifs:
  """The ``Cifs`` class purpose is to provide a CIFS/Samba client able to transfer files using the CIFS/Samba protocol.

  Arguments:
    ``host``: String. The remote host to connect to.
    ``shared_folder``: String. The remote shared folder to use.
    ``username``: String. Optional, default to 'anonymous'.
    ``password``: String. Optional, default to 'anonymous'.
    ``port``: Int. Optional. The TCP remote port to connect to. Default to ``445``.
    ``use_ntlm_v2``: Boolean. Optional, default to True.
    ``is_direct_tcp``: Boolean. Optional, Default to True.
  """

  @property
  def connected(self):
    return self.connection is not None and self._connected

  def __init__(self, host, shared_folder,
               username, password, port=445,
               use_ntlm_v2=True, is_direct_tcp=True):
    logger.debug("[+] Connection initialization:")
    self.username = username
    self.host = host
    self.port = port
    self.shared_folder = shared_folder
    self.password = password
    self.use_ntlm_v2 = use_ntlm_v2
    self.is_direct_tcp = is_direct_tcp
    self.connection = None
    self._connected = False
    self._list_local_dir = list_local_dir
    self._delete_local_file = delete_local_file
    self._delete_local_dir = delete_local_dir
    self._create_local_dirs = create_local_dirs

  def _connect(self):
    """Connect to the remote server using the specified connection information.
    """
    logger.debug(f"Connecting to {self.host}:{self.port}")
    self.connection = SMBConnection(username=self.username,
                                    password=self.password,
                                    my_name=socket.gethostname(),
                                    remote_name=self.host,
                                    use_ntlm_v2=self.use_ntlm_v2,
                                    is_direct_tcp=self.is_direct_tcp)
    self._connected = self.connection.connect(self.host, self.port)

  def _close(self):
    if self.connected:
      self.connection.close()
      self.connection = None
      self._connected = False

  def __enter__(self):
    """Entry point."""
    logger.debug(f"[+] Connecting to {self.username}@{self.host}:{self.port}")
    self._connect()
    return self

  def __exit__(self, type_err, value, traceback):
    """Exit point."""
    logger.debug(f"[+] Closing connection to {self.username}@{self.host}")
    self._close()

# -----------------------------------------------------------------------------
# Basic operations
# -----------------------------------------------------------------------------
  def get_file(self, remote_filepath, local_filepath):
    logger.debug(f"[+] Downloading file {remote_filepath} in {local_filepath}")
    if not self.connected:
      self._connect()
    with open(local_filepath, 'wb') as file_obj:
      self.connection.retrieveFile(self.shared_folder, remote_filepath, file_obj)

  def put_file(self, local_filepath, remote_filepath):
    logger.debug(f"[+] Uploading file {local_filepath} to {remote_filepath}")
    if not self.connected:
      self._connect()
    with open(local_filepath, 'rb') as file_obj:
      self.connection.storeFile(self.shared_folder, remote_filepath, file_obj)

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

# -----------------------------------------------------------------------------
# Remote operations
# -----------------------------------------------------------------------------
  def create_remote_dir(self, path):
    logger.debug(f"[+] Creating folder: {path}")
    if not self.connected:
      self._connect()
    self.connection.createDirectory(self.shared_folder, path)

  def delete_remote_dir_content(self, path):
    logger.debug(f"[+] Deleting all content at path '{path}'")
    if not self.connected:
      self._connect()
    entries = self.connection.listPath(self.shared_folder, path)
    for entry in entries:
      if entry.filename not in (".", ".."):
        if entry.isDirectory:
          self.delete_remote_dir_content(os.path.join(path, entry.filename))
          logger.debug(f"[+] Delete directory: {os.path.join(path, entry.filename)}")
          self.connection.deleteDirectory(self.shared_folder, os.path.join(path, entry.filename))
        else:
          logger.debug(f"[+] Delete file: {os.path.join(path, entry.filename)}")
          self.connection.deleteFiles(self.shared_folder, os.path.join(path, entry.filename))

  def open(self, file, mode):
    if not self.connected:
      self._connect()
    if mode in ["r", "w"]:
      if mode == "w":
        return _CifsFileWritter(self.connection, self.shared_folder, file)
      elif mode == "r":
        file_obj = tempfile.TemporaryFile()
        self.connection.retrieveFile(self.shared_folder, file, file_obj)
        file_obj.seek(0)
        return file_obj
    raise ScrippyRemoteError(f"[UnknownAccessModeError] Unknown file access mode: {mode}")


class _CifsFileWritter:
  def __init__(self, connection, shared_folder, file_path):
    self.connection = connection
    self.shared_folder = shared_folder
    self.file_path = file_path
    self.file_obj = tempfile.TemporaryFile()

  def __enter__(self):
    self.file_obj.__enter__()
    return self.file_obj

  def __exit__(self, type_err, value, traceback):
    if type_err is None:
      self.write()
    self.file_obj.__exit__(type_err, value, traceback)

  def write(self):
    logger.debug(f"[+] Writing file {self.file_path}")
    self.file_obj.seek(0)
    self.connection.storeFile(self.shared_folder, self.file_path, self.file_obj)
