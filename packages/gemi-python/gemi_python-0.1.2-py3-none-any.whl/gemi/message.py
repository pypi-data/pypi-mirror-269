from __future__ import annotations

import typing

from blib import FileSize

from .document import Document
from .enums import StatusCode
from .error import BodyTooLargeError, GeminiError
from .misc import Url

if typing.TYPE_CHECKING:
	from blib import AsyncTransport
	from typing import Self
	from .server import AsyncServer


class Message:
	"Represents a protocol message"

	transport: AsyncTransport
	"The transport associated with the message"

	url: Url
	"URL of the resource"

	body: bytes
	"Main part of the message"


	async def __aenter__(self) -> Self:
		return self


	async def __aexit__(self, *_: None) -> None:
		try:
			await self.transport.close()

		except Exception:
			pass


	@property
	def local(self) -> str:
		"Address of the local socket"

		return self.transport.local_address


	@property
	def remote(self) -> str:
		"Address of the remote socket"

		return self.transport.remote_address


	def build(self) -> bytes:
		"Convert the message into a bytes object that can be sent via a socket"

		raise NotImplementedError("Message.compile")


	async def read_body(self, limit: FileSize | int = FileSize(256, "MiB")) -> bytes:
		"""
			Read the body of the response

			:param limit: Max body size to be accepted
			:raises BodyTooLargeError: When the length of the body is higher than the limit
		"""

		while len(self.body) < limit:
			chunk = await self.transport.read(256)
			self.body += chunk

			if len(chunk) < 256:
				return self.body

		raise BodyTooLargeError(len(self.body), limit)


	async def text(self) -> str:
		"Read the body of the response as a string"

		body = await self.read_body()
		return body.decode("utf-8")


	async def document(self) -> Document:
		"Read the body and attempt to parse it as a gemtext document"

		text = await self.text()
		return Document.loads(text)


class Request(Message):
	"Represents a client request message"

	server: AsyncServer

	def __init__(self, url: Url | str):
		"""
			Create a new request object

			:param url: URL to send the request to
		"""

		self.url: Url = Url.parse(url)


	@classmethod
	async def from_transport(cls: type[Self],
							server: AsyncServer,
							transport: AsyncTransport) -> Self:
		"""
			Parse an incoming client request

			:param server: Server the request will be related to
			:param transport: The transport of the server the request is being sent to
		"""

		try:
			url = (await transport.readline(1024)).decode("utf-8")

		except ValueError as error:
			if "separator is found" in str(error).lower():
				raise GeminiError(59, "Header too long")

		if url.startswith("/"):
			url = f"gemini://{transport.local_address}:{transport.local_port}{url}"

		request = cls(url)
		request.server = server
		request.transport = transport
		return request


	@property
	def path(self) -> str:
		"Path portion of the url"

		return self.url.path


	@property
	def query(self) -> tuple[str, ...]:
		"Query portion of the url"

		return self.url.query


	@property
	def anchor(self) -> str | None:
		"Anchor portion of the url"

		return self.url.anchor


	@property
	def remote(self) -> str:
		"IP address of the remote socket"

		return self.transport.remote_address


	def build(self) -> bytes:
		return f"{self.url}\r\n".encode("utf-8")


class Response(Message):
	"Represents a server response message"


	def __init__(self,
				status: StatusCode | int,
				body: str | bytes = b"",
				meta: str = ""):
		"""
			Create a new response object

			:param status: Status code of the response
			:param body: Data to be sent
			:param meta: Metadata to be sent
		"""

		self.status: StatusCode = StatusCode.parse(status)
		"Status code of the response"

		self.meta: str = meta
		"Metadata (usually mimetype of the data) to be sent with the response"

		self.body: bytes = body if isinstance(body, bytes) else bytes(body, encoding = "utf-8")
		"Data to be sent with the response"


	@classmethod
	async def from_transport(cls: type[Self], transport: AsyncTransport) -> Self:
		"""
			Parse an incoming client request

			:param transport: The transport of the client the response is being sent to
		"""

		try:
			header = (await transport.readline(1024)).decode("utf-8")

		except ValueError as error:
			if "separator is found" in str(error).lower():
				raise GeminiError(59, "Header too long")

		try:
			status, meta = header.strip().split(" ", 1)

		except ValueError:
			status, meta = header, ""

		response = cls(int(status.strip()), meta = meta.strip())
		response.transport = transport
		return response


	@classmethod
	def new_text(cls: type[Self],
				status: StatusCode | int,
				body: str,
				meta: str = "text/plain") -> Self:
		"""
			Create a new response with a text body

			:param status: Status code of the response
			:param body: Text to be sent as the body
			:param meta: Metadata of the response
		"""

		return cls(status, body.encode("utf-8"), meta)


	def build(self) -> bytes:
		if not self.meta:
			header = str(self.status.value)

		else:
			header = f"{self.status.value} {self.meta}"

		return (header + "\r\n").encode("utf-8") + self.body
