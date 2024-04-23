from __future__ import annotations

import os
import re
import typing

from functools import lru_cache
from mimetypes import guess_type
from pathlib import Path

from ..error import GeminiError
from ..message import Response
from ..misc import resolve_path

if typing.TYPE_CHECKING:
	from collections.abc import Callable
	from typing import Any, Self

	from ..message import Request

	class RouteHandler(typing.Protocol):
		async def __call__(self, request: Request, **params: Any) -> Response: ...


ROUTERS: dict[str, Router] = {}


def route(name: str, path: str) -> Callable[[RouteHandler], RouteHandler]:
	def wrapper(handler: RouteHandler) -> RouteHandler:
		Router.get(name, create = True).add_route(path, handler)
		return handler

	return wrapper


class Router:
	"Stores and dispatches routes for an HTTP server"


	def __init__(self, name: str = "Default", trailing_slash: bool = False):
		"""
			Create a new ``Router`` object

			:param name: Internal identifier
			:param register: Add this router to the global router list
			:param types: Mapping of type names and their converter functions
		"""

		self.name: str = name
		"Internal identifier"

		self.routes: dict[str, BaseRoute] = {}
		"Routes handled by this router"

		self.trailing_slash: bool = trailing_slash
		"If ``True``, append a forward slash at the end of the path if doesn't end with one"

		Router.set(self)


	def __repr__(self) -> str:
		return f"Router('{self.name}', trailing_slash={self.trailing_slash})"


	@staticmethod
	def get(name: str, create: bool = False) -> Router:
		"""
			Get a router with the specified name

			:param name: Internal name of the router to get
			:param create: If ``True``, create a new router if it doesn't exist'=
			:raises KeyError: If ``create`` is ``False`` and a router cannot be found
		"""

		if name not in ROUTERS and create:
			ROUTERS[name] = Router(name)

		return ROUTERS[name]


	@staticmethod
	def set(router: Router) -> None:
		"""
			Add a router to the global router list

			:raises KeyError: If a router by the same name exists
		"""

		if router.name in ROUTERS:
			raise KeyError(router.name)

		ROUTERS[router.name] = router


	def add_route(self, path: str, handler: RouteHandler) -> Route:
		"""
			Add a route to be handled by the router

			:param handler: Function to be called for the route
			:param path: Path to handle
		"""

		route = Route.parse_path(path, self, handler)

		if route.path in self.routes:
			raise ValueError(f"Path already exists: {route.path}")

		self.routes[route.path] = route
		return route


	def add_static_route(self, directory: Path | str, path: str) -> FileRoute:
		"""
			Add a route that serves static files

			:param directory: Base filesystem directory to use for returning paths
			:param path: Virtual path to handle
		"""

		route = FileRoute(self, directory, path)

		if route.path in self.routes:
			raise ValueError(f"Path already exists: {route.path}")

		self.routes[route.path] = route
		return route


	def del_route(self, path: str) -> None:
		"""
			Delete a route

			:param path: Path of the route
		"""

		del self.routes[path]


	@lru_cache(maxsize = 256)
	def match(self, path: str) -> Match:
		"""
			Parse a path from a request

			:param path: Path of the request
			:raises GeminiError: If the route could not be found
		"""

		path = _parse_path(path, self.trailing_slash)

		try:
			return self.routes[path].match(path)

		except KeyError:
			pass

		for route in self.routes.values():
			try:
				return route.match(path)

			except GeminiError as error:
				if error.status.value == 51:
					continue

				raise error

		raise GeminiError(51, path)


	def route(self, path: str) -> Callable[[RouteHandler], RouteHandler]:
		"""
			Decorator for adding a new route

			:param path: Path to handle
			:raises ValueError: A handler for the path exists
		"""

		def wrapper(func: RouteHandler) -> RouteHandler:
			self.add_route(path, func)
			return func

		return wrapper


class BaseRoute:
	"Base class for all route classes"

	router: Router
	"Router the route is associated with"

	path: str
	"Path the route will handle"

	regex: re.Pattern[str]
	"Regex pattern to use when matching paths"


	def __repr__(self) -> str:
		return f"{type(self).__name__}('{self.path}')"


	def match(self, path: str) -> Match:
		"""
			Parse a path from a request

			:param path: Path of the request
			:raises GeminiError: If the route could not be found
		"""

		raise NotImplementedError(f"Method not implemented: {type(self).__name__}.match")


class Route(BaseRoute):
	"Represents a route handler"

	def __init__(self,
				router: Router,
				path: str,
				path_regex: re.Pattern[str] | str,
				handler: RouteHandler,
				has_params: bool):
		"""
			Create a new route

			:param router: Router the route will be attached to
			:param path: Path the route will handle
			:param path_regex: Regex pattern to use when matching paths
			:param handlers: Functions to be called for the route
			:param has_params: Whether or not the path has parameters
		"""

		if isinstance(path_regex, str):
			path_regex = re.compile(path_regex)

		self.router: Router = router
		self.path: str = path
		self.handler: RouteHandler = handler
		self.regex: re.Pattern[str] = path_regex
		self.has_params: bool = has_params


	@classmethod
	def parse_path(cls: type[Self], path: str, router: Router, handler: RouteHandler) -> Self:
		"""
			Parse a path

			:param path: Path to parse
			:param trailing_slash: Make sure the path ends with a ``/``
		"""
		path = _parse_path(path, router.trailing_slash)
		path_regex = str(path)
		keys = []

		try:
			keys = re.findall('{' + r'([A-Za-z0-9_\-]+)' + '}', path)

			for key in keys:
				param_str = f"{{{key}}}"
				path_regex = path_regex.replace(param_str, rf'(?P<{key}>[A-Za-z0-9_\-:@.%+]+)')

		except IndexError:
			pass

		return cls(router, path, path_regex, handler, len(keys) > 0)


	def match(self, path: str) -> Match:
		path = _parse_path(path, self.router.trailing_slash)
		params: dict[str, Any] = {}

		if self.has_params:
			if not (re_match := self.regex.fullmatch(path)):
				raise GeminiError(51, path)

			params = re_match.groupdict(default = {})

		else:
			if self.path != path:
				raise GeminiError(51, path)

		return Match(path, self.handler, **params)


class FileRoute(BaseRoute):
	"Route for static files"


	def __init__(self,
				router: Router,
				directory: Path | str,
				path: str):
		"""
			Create a new static file route

			:param router: Router the route will be attached to
			:param directory: Filesystem path to fetch files from
			:param path: Virtual path to handle
		"""

		directory = resolve_path(directory)

		if not directory.exists():
			raise FileNotFoundError(directory)

		if not directory.is_dir():
			raise ValueError(f"Path is not a directory: {directory}")

		self.directory = directory
		"Filesystem path to fetch files from"

		self.router = router
		self.path: str = path
		self.regex = None # type: ignore


	def match(self, path: str) -> Match:
		path = _parse_path(path, self.router.trailing_slash)

		if not path.startswith(self.path):
			raise GeminiError(51, path)

		path = path.replace(self.path, "")
		file_path: Path = self.directory.joinpath(path[1:]) if path != "/" else self.directory

		if file_path.is_dir():
			file_path = file_path.joinpath("index.gmi")

		if not file_path.is_file():
			raise GeminiError(51, path)

		return Match(path, self.handler, file_path = file_path) # type: ignore


	# todo: stream responses
	async def handler(self, request: Request, file_path: Path) -> Response:
		mimetype = guess_type(file_path)[0] or "application/octet+stream"

		if mimetype.startswith("text"):
			mimetype += "; charset=UTF-8"

		with file_path.open("rb") as fd:
			return Response(20, fd.read(), mimetype)


class Match:
	"Represents a path match"


	def __init__(self, path: str, handler: RouteHandler, **kwargs: Any):
		"""
			Create a new match

			:param path: Path of the request
			:param handler: Function to be ran
			:param params: Parsed url parameters
		"""

		self.path = path
		"Path of the request"

		self.handler = handler
		"Function to be called"

		self.params = kwargs
		"Parsed url parameters"


	async def __call__(self, request: Request) -> Response:
		"""
			Call the handler with ``params`` as keyword arguments

			:param args: Arguments to pass to the handler
			:param kwargs: Keyword arguments to pass to the handler
		"""

		return await self.handler(request, **self.params)


	def __repr__(self) -> str:
		return f'Match("{self.path}", handler="{self.handler}")'


def _parse_path(path: str, trailing_slash: bool) -> str:
	"Make sure a path starts and ends with ``/``"

	path = os.path.normpath(path)

	if path == "/":
		return path

	if not path.startswith('/'):
		path = '/' + path

	if not path.endswith('/') and trailing_slash:
		path += '/'

	elif path.endswith("/") and not trailing_slash:
		path = path[:-1]

	return path
