from __future__ import annotations

import ssl
import typing

from OpenSSL import crypto
from pathlib import Path
from urllib.parse import urlparse

from .enums import AppType

if typing.TYPE_CHECKING:
	from collections.abc import Sequence
	from typing import Any, Self
	from .client import AsyncClient
	from .server import AsyncServer


def resolve_path(path: Path | str) -> Path:
	if isinstance(path, str):
		path = Path(path)

	return path.expanduser().resolve()


class BaseApp:
	"Base properties for the client and server classes"

	apptype: AppType
	"Whether the application is a client or server"


	def __init__(self,
				name: str,
				cert: Path | str | None = None,
				key: Path | str | None = None,
				timeout: int = 30):

		if type(self) is BaseApp:
			raise NotImplementedError("This class should not be used by itself")

		self.name: str = name
		"Internal name of the application"

		self.timeout: int = timeout
		"Length in seconds to wait for a network action"

		self.ssl_context: SslContext = SslContext(self, cert, key)
		"Context object used for SSL actions"


class SslContext(ssl.SSLContext):
	client: AsyncClient
	"Client object the context is associated with"

	server: AsyncServer
	"Server object the context is associated with"

	cert: Path
	"Path to the certificate file in PEM format"

	key: Path
	"Path to the key file in PEM format"


	def __init__(self,
				app: BaseApp,
				cert: Path | str | None = None,
				key: Path | str | None = None):

		ssl.SSLContext.__init__(self)

		self.check_hostname: bool = False
		self.verify_mode = ssl.CERT_NONE

		self.cert: Path | None = resolve_path(cert) if cert else None # type: ignore
		self.key: Path | None = resolve_path(key) if key else None # type: ignore

		if app.apptype == AppType.CLIENT:
			self.client = app # type: ignore

		else:
			if not (cert or key):
				raise ValueError("Must set certificate and private key for server")

			self.server = app # type: ignore


	def __new__(cls: type[Self], app: BaseApp, *_: Any) -> Self:
		if app.apptype == AppType.CLIENT:
			protocol = ssl.PROTOCOL_TLS_CLIENT

		else:
			protocol = ssl.PROTOCOL_TLS_SERVER

		return ssl.SSLContext.__new__(cls, protocol)


	def generate_cert(self, hostname: str, overwrite: bool = False) -> None:
		if crypto is None:
			raise RuntimeError("pyOpenSSL module is not installed")

		if not overwrite and (self.cert.exists() or self.key.exists()):
			raise FileExistsError("Not willing to overwrite the key and certificate")

		key = crypto.PKey()
		key.generate_key(crypto.TYPE_RSA, 4096)

		cert = crypto.X509()
		subject = cert.get_subject()
		subject.C = "US"
		subject.ST = "New Jersey"
		subject.L = "Camden"
		subject.O = "Barkshark" # noqa: E741
		subject.OU = "Barkshark"
		subject.CN = hostname
		cert.set_serial_number(1000)
		cert.gmtime_adj_notBefore(0)
		cert.gmtime_adj_notAfter(10*365*24*60*60)
		cert.set_issuer(cert.get_subject())
		cert.set_pubkey(key)
		cert.sign(key, "sha1")

		with self.cert.open("wb") as fd:
			fd.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

		with self.key.open("wb") as fd:
			fd.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))


	def load_cert(self) -> None:
		self.load_cert_chain(certfile = self.cert, keyfile = self.key)


class Url(str):
	"Represents a Gemini or Tital URL with properties for each part"


	def __init__(self,
				domain: str,
				path: str,
				proto: str = "gemini",
				port: int = 0,
				query: Sequence[str] | None = None,
				anchor: str | None = None):
		"""
			Create a new Url object

			:param domain: Domain of the url
			:param path: Path of the url
			:param proto: Protocol of the url
			:param port: Port of the url
			:param query: Mapping of key/value pairs for the query part of the url
			:param anchor: Extra text at the end of the url
		"""

		assert port >= 0, "Port must be at least 0"

		self.parts: tuple[str, str, str, int, tuple[str, ...], str | None] = (
			domain, path, proto, port, tuple(query or []), anchor
		)


	def __new__(cls,
				domain: str,
				path: str,
				proto: str = "gemini",
				port: int = 0,
				query: Sequence[str] | None = None,
				anchor: str | None = None) -> Self:

		if proto.lower() not in {"gemini", "titan"}:
			raise ValueError("Protocol must be 'gemini' or 'titan'")

		url = f"{proto}://{domain}"

		if port:
			url += f":{port}"

		url += "/" + path if not path.startswith("/") else path

		if query:
			url += f"?{'&'.join(query)}"

		if anchor:
			url += f"#{anchor}"

		return str.__new__(cls, url)


	@classmethod
	def parse(cls: type[Self], url: str) -> Self:
		"""
			Parse a URL string

			:param url: URL as a string
		"""

		if isinstance(url, cls):
			return url

		if not url.startswith(("gemini://", "titan://")):
			url = f"gemini://{url}"

		data = urlparse(url)

		if data.scheme.lower() not in {"gemini", "titan"}:
			raise ValueError("Protocol must be 'gemini' or 'titan'")

		if data.hostname is None:
			raise ValueError("Hostname cannot be empty")

		return cls(
			data.hostname,
			data.path or "/",
			data.scheme.lower(),
			data.port or 0,
			data.query,
			data.fragment
		)


	@property
	def domain(self) -> str:
		"Domain of the url"

		return self.parts[0]


	@property
	def path(self) -> str:
		"Path of the url"

		return self.parts[1]


	@property
	def proto(self) -> str:
		"Protocol of the url"

		return self.parts[2]


	@property
	def port(self) -> int:
		"""
			Port of the url. If no port is listed in the url, the default for the protocol will be
			returned
		"""

		return self.parts[3] or 1965


	@property
	def query(self) -> tuple[str, ...]:
		"Mapping of key/value pairs for the query part of the url"

		return self.parts[4]


	@property
	def anchor(self) -> str | None:
		"Extra text at the end of the url"

		return self.parts[5]


	@property
	def hostname(self) -> str:
		"""
			Get the hostname of the url. If the default port for the protocol is used, just return
			the domain.
		"""

		if self.parts[3] < 1:
			return self.domain

		return f"{self.domain}:{self.port}"
