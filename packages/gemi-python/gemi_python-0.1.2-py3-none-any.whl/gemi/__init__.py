__software__ = "Gemi"
__version__ = "0.1.2"

import mimetypes
mimetypes.add_type("text/gemini", ".gmi", strict = True)

from .client import AsyncClient
from .enums import AppType, OutputFormat, StatusCode
from .error import BodyTooLargeError, GeminiError, ParsingError
from .message import Message, Request, Response
from .misc import BaseApp, SslContext, Url, resolve_path
from .server import AsyncServer, Router, BaseRoute, Route, FileRoute, route

from .document import (
	Document,
	Element,
	Header,
	Link,
	ListItem,
	Preformatted,
	Quote,
	Text
)
