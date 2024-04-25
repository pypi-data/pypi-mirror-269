import os
import re
from scrippy_remote import ScrippyRemoteError, logger


# -----------------------------------------------------------------------------
# Local operations
# -----------------------------------------------------------------------------
def list_local_dir(local_dir, file_type="f", pattern=".*"):
  """
  Get the complete list of files or dirs found in the specified local directory and matching the specified file type (f or d) and the specified regular expression pattern.

  Note:
    - This method is **NOT** recursive.
    - The workflow main workspace directory and workflow session workspace directory component of path will be automatically stripped out from

  Arguments:
    ``local_dir``: String. The full path of the local directory to explore. This option is mandatory and has no default value.
    ``file_type``: String. Optional. If set to ``d``, the returned list will only contain directory names. When set to ``f``, the returned list will contain only file names. Default: ``f``.
    pattern: String. A regular expression to filter returned values. Default to ``.*``
  """
  dirs = list()
  files = list()
  reg = re.compile(pattern)
  logger.debug(f"Exploring {local_dir}")
  try:
    for l_file in os.listdir(local_dir):
      l_full_fname = os.path.join(local_dir, l_file)
      if os.path.isdir(l_full_fname) and re.match(reg, l_full_fname):
        dirs.append(l_full_fname)
      elif os.path.isfile(l_full_fname) and re.match(reg, l_full_fname):
        files.append(l_full_fname)
    if file_type == "f":
      return files
    elif file_type == "d":
      return dirs
  except Exception as err:
    err_msg = f"[LocalOSError] {err.__class__.__name__} {err}"
    logger.critical(err_msg)
    raise ScrippyRemoteError(err_msg) from err


def delete_local_file(local_file, exit_on_error=True):
    """
    Delete specified file from local host.

    Arguments:
      ``local_file``: The local filepath to delete.
      ``exit_on_error``: Boolean. Optional. If set to ``False``, any error encountered will only be logged as a warning. Default: ``True``.
    """
    logger.debug(f"Removing local file: {local_file}")
    try:
      os.remove(local_file)
    except Exception as err:
      err_msg = f"[LocalOSError] {err.__class__.__name__}: {err}"
      if exit_on_error:
        raise ScrippyRemoteError(err_msg) from err
      logger.warning(err_msg)


def delete_local_dir(local_dir, recursive=False, exit_on_error=True):
  """
  Delete specified directory on the local host and its content.
  Whatever the value of the ``recursive``argument, all files within the specified directory will be deleted.
  When ``recursive`` is set to ``True``, all sub directories and their content are deleted.

  Arguments:
    ``local_dir``: The directory to delete.
    ``recursive``: If set to ``True``, delete directory and all its content.
    ``exit_on_error``: Boolean. Optional. If set to ``False``, any error encountered will only be logged as a warning. Default: ``True``.
  """
  logger.debug(f"Removing local dir: {local_dir}")

  try:
    if recursive:
      for l_dir in list_local_dir(local_dir=local_dir, file_type="d"):
        delete_local_dir(local_dir=l_dir,
                         recursive=recursive,
                         exit_on_error=exit_on_error)
    for l_file in list_local_dir(local_dir=local_dir):
      delete_local_file(local_file=l_file, exit_on_error=exit_on_error)
    os.rmdir(local_dir)
  except Exception as err:
    err_msg = f"[LocalOSError] {err.__class__.__name__}: {err}"
    if exit_on_error:
      raise ScrippyRemoteError(err_msg) from err
    logger.warning(err_msg)


def create_local_dirs(remote_file, local_dir):
  """
  Create a copy of the remote directory structure for a remote file path.

  Arguments:
    ``remote_file``: String. A remote file path.
    ``local_dir``: String. The local directory within duplicate the remote directory tree.
  """
  try:
    hierarchy = os.path.join(*remote_file.split("/")[:-1])
    hierarchy = os.path.join(local_dir, hierarchy)
  except TypeError:
    # Remote_file is a single file without a path
    hierarchy = os.path.join(local_dir)
  logger.debug(f"Creating local dir: {hierarchy}")
  try:
    os.makedirs(hierarchy, exist_ok=True)
  except Exception as err:
    err_msg = f"[LocalOSError] {err.__class__.__name__} {err}"
    logger.error(err_msg)
    raise ScrippyRemoteError(err_msg) from err
