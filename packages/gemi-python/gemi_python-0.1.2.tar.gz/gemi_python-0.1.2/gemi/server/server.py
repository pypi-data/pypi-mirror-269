from __future__ import annotations

import asyncio
import platform
import signal
import socket
import ssl
import traceback
import typing

from asyncio.exceptions import CancelledError
from blib import AsyncTransport
from pathlib import Path
from typing import Any

from .router import Router

from .. import logger as logging
from ..enums import AppType
from ..error import GeminiError
from ..message import Request, Response
from ..misc import BaseApp

if typing.TYPE_CHECKING:
	from asyncio import StreamReader, StreamWriter
	from collections.abc import Callable
	from .router import RouteHandler


IS_WINDOWS: bool = platform.system() == "Windows"
SERVERS: dict[str, AsyncServer] = {}
SIGNALS: list[str] = [
		"SIGHUP",
		"SIGILL",
		"SIGTERM",
		"SIGINT"
	]


class AsyncServer(BaseApp, dict[str, Any]):
	"Server for the Gemini protocol"

	apptype: AppType = AppType.SERVER


	def __init__(self,
				name: str = "Default",
				addr: str = "0.0.0.0",
				port: int = 1965,
				cert: Path | str = "server.crt",
				key: Path | str = "server.pem",
				host: str | None = None,
				timeout: int = 30):
		"""
			Create a new server

			:param name: Internal name of the server
			:param addr: IP address for the server to listen on
			:param port: Port number for the server to listen on
			:param cert: Certificate to load into the SSL context
			:param key: Private key to load into the SSL context
			:param host: Hostname the server is associated with
			:param timeout: Number of seconds to wait for network actions
		"""

		BaseApp.__init__(self, name, cert, key, timeout)
		dict.__init__(self)

		self.addr: str = addr
		"IP address for the server to listen on"

		self.port: int = port
		"Port number for the server to listen on"

		self.host: str | None = host or addr
		"Hostname the server is associated with"

		self.router: Router = Router.get(name, create = True)
		"Router object that handles dispatching routes"

		try:
			self.ssl_context.generate_cert(self.host or self.addr, overwrite = False)

		except FileExistsError:
			pass

		self.ssl_context.load_cert()
		self.ssl_context.sni_callback = self.handle_client_ssl
		self._server: asyncio.Server | None = None

		AsyncServer.set_server(self)


	@staticmethod
	def get_server(name: str, create: bool = False) -> AsyncServer:
		"""
			Get a server with the specified name

			:param name: Internal name of the server to get
			:param create: If ``True``, create a new server if it doesn't exist'
			:raises KeyError: If ``create`` is ``False`` and a server cannot be found
		"""

		if name not in SERVERS:
			SERVERS[name] = AsyncServer(name)

		return SERVERS[name]


	@staticmethod
	def set_server(server: AsyncServer) -> None:
		"""
			Add a server to the global server list

			:param server: Server object to append to the global ``dict``
			:raises KeyError: If a server by the same name exists
		"""

		if server.name in SERVERS:
			raise KeyError(server.name)

		SERVERS[server.name] = server


	def add_route(self, path: str, handler: RouteHandler) -> None:
		"""
			Add a handler for a route

			:param path: Virtual path to be handled
			:param handler: Async method to be called
		"""

		self.router.add_route(path, handler)


	def route(self, path: str) -> Callable[[RouteHandler], RouteHandler]:
		"""
			Decorator for adding route handlers

			:param path: Virtual path to be handled
		"""

		return self.router.route(path)


	def run(self) -> None:
		"Start the server and wait for it to close"

		asyncio.run(self.start())


	def set_signal_handler(self, handler: Callable[..., Any] | None) -> None:
		loop = asyncio.get_event_loop()

		for sig in SIGNALS:
			try:
				if IS_WINDOWS:
					signal.signal(getattr(signal, sig), handler or signal.SIG_DFL)
					continue

				loop.add_signal_handler(
					getattr(signal, sig),
					handler or signal.SIG_DFL # type: ignore
				)

			except AttributeError:
				logging.verbose("Cannot handle signal: %s", sig)


	async def start(self) -> None:
		"Start the server"

		if self._server is not None:
			return

		if port_in_use(self.addr, self.port):
			raise ConnectionError(f"Address and port already in use: {self.addr}:{self.port}")

		logging.info(f"Starting server @ gemini://{self.addr}:{self.port}")

		self.set_signal_handler(self.stop)
		self._server = await asyncio.start_server(
			client_connected_cb = self.handle_client,
			host = self.addr,
			port = self.port,
			ssl = self.ssl_context,
			reuse_address = True,
			reuse_port = not IS_WINDOWS,
			ssl_handshake_timeout = self.timeout,
			ssl_shutdown_timeout = self.timeout,
			start_serving = True
		)

		try:
			await self._server.serve_forever()

		except CancelledError:
			pass

		self.set_signal_handler(None)
		await self._server.wait_closed()

		logging.info("Shutting down...")

		self._server = None


	def stop(self, *_: Any) -> None:
		"Tell the server to stop"

		if self._server is None:
			return

		self._server.close()


	async def handle_client(self, reader: StreamReader, writer: StreamWriter) -> None:
		"""
			Callback for client connections

			:param reader: Reader object for reading client data
			:param writer: Writer object for sending data to the client
		"""

		transport = AsyncTransport(reader, writer, self.timeout)
		request = Request(f"{self.addr}:{self.port}/")

		try:
			request = await Request.from_transport(self, transport)
			handler = self.router.match(request.path)
			response = await handler(request)

			if not isinstance(response, Response):
				raise GeminiError(50, "Invalid response")

		except GeminiError as error:
			response = Response(
				error.status,
				(f"{error.status.reason}: {error.message}").encode("utf-8"),
				"text/plain"
			)

		except Exception:
			response = Response(50, b"Server Error :/", "text/plain")
			traceback.print_exc()

		try:
			await transport.write(response.build())
			logging.info(
				"ip: %s, path: %s, status: %i, length: %i",
				transport.remote_address,
				request.path,
				response.status,
				len(response.body)
			)

		except Exception:
			traceback.print_exc()

		await transport.close()


	def handle_client_ssl(self,
						socket: ssl.SSLObject,
						name: str,
						context: ssl.SSLContext) -> int | None:
		"""
			Callback for client ssl connections

			:param socket: Socket object of the connection
			:param name: Hostname sent by the client
			:param context: SSL context associated with the connection
		"""

		# return int is ssl.ALTER_DESCRIPTION_[HANDSHAKE_FAILURE | INTERNAL_ERROR]

		# set context here: socket.context = context
		return None


def port_in_use(host: str, port: int) -> bool:
	if host == "0.0.0.0":
		host = "127.0.0.1"

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		return s.connect_ex((host, port)) == 0
