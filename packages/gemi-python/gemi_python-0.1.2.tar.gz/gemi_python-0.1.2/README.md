# Gemi

Utilities for the Gemini protocol

## Client Example

	import asyncio
	import gemi

	async def main():
		client = gemi.AsyncClient()
		response = await client.request("geminiprotocol.net")

		for element in (await response.document()):
			print(repr(element))

	asyncio.run(main())

## Server Example

	import gemi

	@gemi.route("Default", "/")
	async def home(request: gemi.Request) -> gemi.Response:
		return gemi.Response(20, "UvU", "text/plain")

	server = gemi.AsyncServer("Default")
	server.run()

## Document Example

	import gemi

	doc = gemi.Document([
		gemi.Header("Hewwo!", 1),
		gemi.Text(""),
		gemi.Text("im gay"),
		gemi.Text(""),
		gemi.Link("https://git.barkshark.xyz/barkshark/gemi", "Gemi")
	])

	doc.dump("/var/lib/gemi-server/static/text.gmi", gemi.OutputFormat.GEMTEXT)

[Documentation](https://docs.barkshark.xyz/gemi)

[Gemini Protocol](https://geminiprotocol.net/)
