import logging
import socket
import ssl
from scrippy_remote.ftp.clients.errors import Error
from scrippy_remote.ftp.clients.ftp import FtpSimple, B_CRLF, CRLF, print_line

logger = logging.getLogger("scrippy.main")


class Ftps(FtpSimple):
  """
  Ftp client with implicit TLS support (FTPs).
  """
  def __init__(self, hostname, port=21,
               username='anonymous', password='anonymous',
               ssl_verify=True, ssl_version=None):
    super().__init__(hostname=hostname, port=port,
                     username=username, password=password)
    self.ssl_verify = ssl_verify
    self.ssl_version = ssl.PROTOCOL_TLS_CLIENT
    if ssl_version is not None:
      self.ssl_version = getattr(ssl.TLSVersion, ssl_version)
    self.context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    self._prot_p = False
    if not self.ssl_verify:
      self.context.check_hostname = False
      self.context.verify_mode = ssl.CERT_NONE

  def connect(self):
    logging.debug("[+] Connection (Implicit TLS)")
    if self.hostname is not None:
      self.sock = socket.create_connection((self.hostname, self.port),
                                           self.timeout)
      self.af = self.sock.family
      if not self.ssl_verify:
        logging.warning("[!] Insecure connection: ssl_verify set to False")
      self.sock = self.context.wrap_socket(self.sock,
                                           server_hostname=self.hostname)
      self.file = self.sock.makefile('r', encoding=self.ENCODING)
      logging.debug(f"[WELCOME] {self._getresp()}")
      logging.debug("[=] connected")
      return True
    raise Error("Remote host not defined")

  def ntransfercmd(self, cmd, rest=None):
    conn, size = super().ntransfercmd(cmd, rest)
    if self._prot_p:
      conn = self.context.wrap_socket(conn,
                                      server_hostname=self.hostname,
                                      session=self.sock.session)
    return conn, size

  def storbinary(self, cmd, fp, blocksize=8192, callback=None, rest=None):
    self.prot_p()
    self.voidcmd('TYPE I')
    conn = self.transfercmd(cmd, rest)
    while 1:
      buf = fp.read(blocksize)
      if not buf:
        logging.debug("[STOR] EOF")
        break
      conn.sendall(buf)
      if callback:
        callback(buf)
    conn.unwrap()
    return self._voidresp()

  def storlines(self, cmd, fp, callback=None):
    self.prot_p()
    self.voidcmd('TYPE A')
    conn = self.transfercmd(cmd)
    while 1:
      buf = fp.readline(self.maxline + 1)
      if len(buf) > self.maxline:
        raise Error(f"got more than {self.maxline} bytes")
      if not buf:
        break
      if buf[-2:] != B_CRLF:
        if buf[-1] in B_CRLF:
          buf = buf[:-1]
          buf = buf + B_CRLF
      conn.sendall(buf)
      if callback:
        callback(buf)
    conn.unwrap()
    return self._voidresp()

  def retrbinary(self, cmd, callback, blocksize=8192, rest=None):
    self.prot_p()
    self.voidcmd('TYPE I')
    conn = self.transfercmd(cmd, rest)
    while 1:
      data = conn.recv(blocksize)
      if not data:
        break
      callback(data)
    conn.unwrap()
    return self._voidresp()

  def retrlines(self, cmd, callback=None):
    self.prot_p()
    if callback is None:
      callback = print_line
    resp = self.sendcmd('TYPE A')
    conn = self.transfercmd(cmd)
    with conn.makefile('r', encoding=self.ENCODING) as fp:
      while 1:
        line = fp.readline(self.maxline + 1)
        if len(line) > self.maxline:
          raise Error(f"got more than {self.maxline} bytes")
        logging.debug(f"[RETR] {repr(line)}")
        if not line:
          break
        if line[-2:] == CRLF:
          line = line[:-2]
        elif line[-1:] == '\n':
          line = line[:-1]
        callback(line)
    conn.unwrap()
    return self._voidresp()

  def close(self):
    logging.debug("[CLOSE]")
    self.file.close()
    try:
      self.sock.unwrap()
    except Exception:
      pass
    self.sock.close()

  def ccc(self):
    resp = self.voidcmd('CCC')
    self.sock = self.sock.unwrap()
    return resp

  def prot_p(self):
    self.voidcmd('PBSZ 0')
    resp = self.voidcmd('PROT P')
    self._prot_p = True
    return resp

  def prot_c(self):
    resp = self.voidcmd('PROT C')
    self._prot_p = False
    return resp
