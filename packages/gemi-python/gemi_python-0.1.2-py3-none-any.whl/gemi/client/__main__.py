#!/usr/bin/env python3
import argparse
import asyncio
import gemi
import sys


parser = argparse.ArgumentParser(
	prog = "gurl",
	description = "Fetch a resource at a Gemini URL",
)

parser.add_argument("url"),
parser.add_argument("-i", "--include-response-info", action = "store_true")
parser.add_argument("-I", "--only-response-info", action = "store_true")
parser.add_argument("-t", "--timeout", type = int, default = 30)
parser.add_argument("-v", "--version", action = "store_true")


async def async_main(args: argparse.Namespace) -> None:
	client = gemi.AsyncClient(args.timeout)
	resp = await client.request(args.url)

	if args.only_response_info or args.include_response_info:
		print("url:", resp.url)
		print("status:", resp.status, resp.status.reason)
		print("metadata:", resp.meta)

		if args.only_response_info:
			return

		print("----------------------\n")

	print(await resp.text())


def main() -> None:
	args = parser.parse_args()

	if args.version:
		print(f"GURL (Gemi/{gemi.__version__})")
		sys.exit()

	asyncio.run(async_main(args))


if __name__ == "__main__":
	main()
