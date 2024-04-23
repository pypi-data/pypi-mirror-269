from __future__ import annotations

from blib import Enum, IntEnum


class AppType(Enum):
	SERVER = 0
	CLIENT = 1


class OutputFormat(Enum):
	"Text format to use when dumping a document"

	GEMTEXT = 0
	HTML = 1
	MARKDOWN = 2


class StatusCode(IntEnum):
	"Name and value for each code that can be returned from a server"

	INPUT = 10
	SENSITIVE_INPUT = 11

	SUCCESS = 20

	TEMPORARY_REDIRECT = 30
	PERMANENT_REDIRECT = 31

	TEMPORARY_FAILURE = 40
	SERVER_UNAVAILABLE = 41
	CGI_ERROR = 42
	PROXY_ERROR = 43
	SLOW_DOWN = 44

	PERMANENT_FAILURE = 50
	NOT_FOUND = 51
	GONE = 52
	PROXY_REQUEST_REFUSED = 53
	BAD_REQUEST = 59

	CERT_REQUIRED = 60
	CERT_NOT_AUTHORIZED = 61
	CERT_NOT_VALID = 62


	@property
	def reason(self) -> str:
		"Get the human readable name of the status"

		return self.name.replace("_", " ").title()
