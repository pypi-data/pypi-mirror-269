"""Module de test scrippy_remote.remote.Ftp."""
import os
import hashlib
from scrippy_remote import ScrippyRemoteError
from scrippy_remote.ftp import Ftp
from tests import common


def set_env():
  common.env["remote_host"] = "vsftpd"
  common.env["remote_port"] = 2990
  common.env["remote_user"] = "luiggi.vercotti"
  common.env["remote_dir"] = "dead/parrot"
  common.env["password"] = "d34dp4rr0t"
  common.env["ftp_tls"] = True
  common.env["ftp_explicit_tls"] = True
  common.env["ftp_ssl_verify"] = False


def compare_dirs(host, remote_dir, local_dir):
  r_files = list()
  l_files = list()
  for r_file in host.list_remote_dir(remote_dir=remote_dir,
                                     file_type="f"):
    r_files.append(r_file)
  for r_dir in host.list_remote_dir(remote_dir=remote_dir,
                                    file_type="d"):
    for r_file in host.list_remote_dir(remote_dir=r_dir,
                                       file_type="f"):
      r_files.append(r_file)
  for l_file in host.list_local_dir(local_dir=common.working_dir,
                                    file_type="f"):
    l_files.append(l_file.replace(common.working_dir, remote_dir))
  for l_dir in host.list_local_dir(local_dir=common.working_dir,
                                   file_type="d"):
    for l_file in host.list_local_dir(local_dir=l_dir,
                                      file_type="f"):
      l_files.append(l_file.replace(common.working_dir, remote_dir))
  assert sorted(r_files) == sorted(l_files)


def test_list_local_dir():
  set_env()
  with Ftp(username=common.env.get("remote_user"),
           host=common.env.get("remote_host"),
           port=common.env.get("remote_port"),
           password=common.env.get("password"),
           tls=common.env.get("ftp_tls"),
           explicit=common.env.get("ftp_explicit_tls"),
           ssl_verify=common.env.get("ftp_ssl_verify")) as host:
    local_files = host.list_local_dir(local_dir=common.env.get("working_dir"),
                                      file_type="f",
                                      pattern=common.env.get("pattern"))
    assert common.env.get("local_file") in local_files
    local_files = host.list_local_dir(local_dir=common.env.get("working_dir"),
                                      file_type="f",
                                      pattern=r".*\.exe")
    assert local_files == list()
    try:
      local_files = host.list_local_dir(local_dir="/inexistent",
                                        file_type="f",
                                        pattern=r".*\.exe")
    except ScrippyRemoteError as err:
      expected = "[LocalOSError] FileNotFoundError [Errno 2] No such file or directory"
      assert str(err).startswith(expected)


def test_remote_mirror():
  """Mirror local_dir in remote_dir."""
  set_env()
  with Ftp(username=common.env.get("remote_user"),
           host=common.env.get("remote_host"),
           port=common.env.get("remote_port"),
           password=common.env.get("password"),
           tls=common.env.get("ftp_tls"),
           explicit=common.env.get("ftp_explicit_tls"),
           ssl_verify=common.env.get("ftp_ssl_verify")) as host:
    host.remote_mirror(local_dir=common.env.get("working_dir"),
                       remote_dir=common.env.get("remote_dir"),
                       exit_on_error=True)
    compare_dirs(host=host, remote_dir=common.env.get("remote_dir"), local_dir=common.env.get("working_dir"))


def test_local_mirror():
  set_env()
  with Ftp(username=common.env.get("remote_user"),
           host=common.env.get("remote_host"),
           port=common.env.get("remote_port"),
           password=common.env.get("password"),
           tls=common.env.get("ftp_tls"),
           explicit=common.env.get("ftp_explicit_tls"),
           ssl_verify=common.env.get("ftp_ssl_verify")) as host:
    host.local_mirror(local_dir=common.env.get("local_dir"),
                      remote_dir=common.env.get("remote_dir"),
                      exit_on_error=True)
    compare_dirs(host=host, remote_dir=common.env.get("remote_dir"), local_dir=common.env.get("local_dir"))


def test_get_remote_file():
  set_env()
  with Ftp(username=common.env.get("remote_user"),
           host=common.env.get("remote_host"),
           port=common.env.get("remote_port"),
           password=common.env.get("password"),
           tls=common.env.get("ftp_tls"),
           explicit=common.env.get("ftp_explicit_tls"),
           ssl_verify=common.env.get("ftp_ssl_verify")) as host:
    remote_file = os.path.join(common.env.get("remote_dir"),
                               os.path.basename(common.env.get("local_file")))
    host.get_file(remote_file=remote_file,
                  local_dir=common.env.get("local_dir"),
                  create_dirs=True)
    l_file = os.path.join(common.env.get("local_dir"),
                          common.env.get("remote_dir"),
                          os.path.basename(common.env.get("local_file")))
    assert os.path.isfile(l_file)
    md5_l_file = hashlib.md5(open(l_file, "rb").read()).hexdigest()
    assert md5_l_file == common.env.get("md5_local_file")


def test_delete_remote_file():
  set_env()
  with Ftp(username=common.env.get("remote_user"),
           host=common.env.get("remote_host"),
           port=common.env.get("remote_port"),
           password=common.env.get("password"),
           tls=common.env.get("ftp_tls"),
           explicit=common.env.get("ftp_explicit_tls"),
           ssl_verify=common.env.get("ftp_ssl_verify")) as host:
    remote_file = os.path.join(common.env.get("remote_dir"),
                               os.path.basename(common.env.get("local_file")))
    host.delete_remote_file(remote_file)
    files = host.list_remote_dir(remote_dir=common.env.get("remote_dir"),
                                 pattern=common.env.get("pattern"))
    assert os.path.join(common.env.get("remote_dir"),
                        os.path.basename(common.env.get("local_file"))) not in files


def test_delete_remote_dir():
  set_env()
  with Ftp(username=common.env.get("remote_user"),
           host=common.env.get("remote_host"),
           port=common.env.get("remote_port"),
           password=common.env.get("password"),
           tls=common.env.get("ftp_tls"),
           explicit=common.env.get("ftp_explicit_tls"),
           ssl_verify=common.env.get("ftp_ssl_verify")) as host:
    r_dir = os.path.dirname(common.env.get("remote_dir"))
    host.delete_remote_dir(common.env.get("remote_dir"), recursive=True)
    dirs = host.list_remote_dir(remote_dir=r_dir,
                                file_type="d",
                                pattern=".*")
    assert common.env.get("remote_dir") not in dirs
