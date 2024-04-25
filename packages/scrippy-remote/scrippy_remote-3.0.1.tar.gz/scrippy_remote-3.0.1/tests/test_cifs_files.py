"""Module de test scrippy_remote.remote.Ftp."""
import os
import hashlib
from scrippy_remote.cifs import Cifs
from tests import common


def set_env():
  common.env["remote_host"] = "samba"
  common.env["remote_user"] = "luiggi.vercotti"
  common.env["password"] = "d34dp4rr0t"
  common.env["remote_dir"] = "storage"
  common.env["remote_user_dir"] = "luiggi.vercotti"
  common.env["remote_file"] = "luiggi.vercotti/parrot.txt"


def test_put_file():
  """Test d'envoi de fichier."""
  set_env()
  with Cifs(username=common.env.get("remote_user"),
            host=common.env.get("remote_host"),
            shared_folder=common.env.get("remote_dir"),
            password=common.env.get("password")) as cifs:
    cifs.create_remote_dir(common.env.get("remote_user_dir"))
    cifs.put_file(local_filepath=common.env.get("local_file"),
                  remote_filepath=common.env.get("remote_file"))


def test_get_remote_file():
  set_env()
  l_file = os.path.join(common.env.get("local_dir"), "parrot.txt")
  with Cifs(username=common.env.get("remote_user"),
            host=common.env.get("remote_host"),
            shared_folder=common.env.get("remote_dir"),
            password=common.env.get("password")) as cifs:
    cifs.create_local_dirs(remote_file=common.env.get("remote_file"),
                           local_dir=common.env.get("local_dir"))
    cifs.get_file(remote_filepath=common.env.get("remote_file"),
                  local_filepath=l_file)
    assert os.path.isfile(l_file)
    md5_l_file = hashlib.md5(open(l_file, "rb").read()).hexdigest()
    assert md5_l_file == common.env.get("md5_local_file")


def test_read_write_files():
  set_env()
  r_file = os.path.join(common.env.get("remote_user_dir"), "inquisition.txt")
  with Cifs(username=common.env.get("remote_user"),
            host=common.env.get("remote_host"),
            shared_folder=common.env.get("remote_dir"),
            password=common.env.get("password")) as cifs:
    with cifs.open(r_file, mode="w") as w_file:
      w_file.write(b'None expect the Spannish inquisition')
    with cifs.open(r_file, mode="r") as rr_file:
      assert rr_file.readlines() == [b'None expect the Spannish inquisition']


def test_delete_remote_dir():
  set_env()
  with Cifs(username=common.env.get("remote_user"),
            host=common.env.get("remote_host"),
            shared_folder=common.env.get("remote_dir"),
            password=common.env.get("password")) as cifs:
    cifs.delete_remote_dir_content(common.env.get("remote_user_dir"))
