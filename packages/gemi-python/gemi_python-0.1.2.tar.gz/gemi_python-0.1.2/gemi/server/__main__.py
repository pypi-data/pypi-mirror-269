#!/usr/bin/env python3
import argparse
import gemi
import platform
import sys

from gemi import logger as logging
from pathlib import Path
from platformdirs import user_config_dir


parser = argparse.ArgumentParser(
	prog = "gemi-server",
	description = "Serve a directory",
)

parser.add_argument("-n", "--hostname"),
parser.add_argument("-a", "--address", default = "0.0.0.0")
parser.add_argument("-p", "--port", type = int, default = 1965)
parser.add_argument("-t", "--timeout", type = int, default = 30)
parser.add_argument("-c", "--config-dir", type = gemi.resolve_path)
parser.add_argument("-s", "--static-dir", type = gemi.resolve_path)
parser.add_argument("-v", "--version", action = "store_true")


def get_config_dir() -> Path:
	if (path := gemi.resolve_path(".")).joinpath("server.cert").is_file():
		return path

	if platform.system() == "Linux":
		if (path := gemi.resolve_path("~/.config/barkshark/gemi-server")).is_dir():
			return path

		if (path := Path("/etc/gemi-server")).is_dir():
			return path

	else:
		if (user := Path(user_config_dir("gemi-server", "barkshark"))).is_dir():
			return user

	return user


def main() -> None:
	args = parser.parse_args()

	if args.version:
		print(f"gemi-server (Gemi/{gemi.__version__})")
		sys.exit()


	config_dir = args.config_dir or get_config_dir()
	config_dir.mkdir(exist_ok = True, parents = True)

	static_dir = args.static_dir or config_dir.joinpath("static")
	static_dir.mkdir(exist_ok = True, parents = True)

	server = gemi.AsyncServer(
		name = "Default",
		cert = config_dir.joinpath("server.cert"),
		key = config_dir.joinpath("server.key"),
		addr = args.address,
		port = args.port,
		host = args.hostname,
		timeout = args.timeout
	)

	server.router.add_static_route(static_dir, "/")

	try:
		server.run()

	except ConnectionError as error:
		logging.error(error)


if __name__ == "__main__":
	main()
