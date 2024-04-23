import asyncio
import sys

from blib import AsyncTransport

from ..enums import AppType
from ..message import Request, Response
from ..misc import BaseApp, Url


class AsyncClient(BaseApp):
	"Client for the Gemini protocol"

	apptype: AppType = AppType.CLIENT

	timeout: int
	"Time in seconds to wait before giving up on connecting or reading data"


	def __init__(self, name: str = "Default", timeout: int = 30):
		"""
			Create a new client object

			:param name: Internal name of the client
			:param timeout: Time in seconds to wait before giving up
		"""

		BaseApp.__init__(self, name, timeout = timeout)


	async def request(self, url: Url | str) -> Response:
		"""
			Create a new request and send it to a server

			:param url: Url of the resource to fetch
		"""

		return await self.send_request(Request(url))


	async def send_request(self, request: Request) -> Response:
		"""
			Send a request to a server

			:param request: The request to be sent
		"""

		reader, writer = await asyncio.open_connection(
			host = request.url.domain,
			port = request.url.port,
			ssl = self.ssl_context,
			ssl_handshake_timeout = self.timeout,
			ssl_shutdown_timeout = self.timeout
		)

		transport = AsyncTransport(reader, writer, self.timeout)
		await transport.write(request.build())

		response = await Response.from_transport(transport)
		response.url = request.url

		# todo: handle redirects

		return response


async def main(timeout: int) -> None:
	client = AsyncClient()

	try:
		url = sys.argv[1]

		if not url.startswith("gemini://"):
			url = "gemini://" + url

	except IndexError:
		print("Please provide a url")
		sys.exit(1)

	resp = await client.request(url)
	print(await resp.text())


if __name__ == "__main__":
	asyncio.run(main(5))
