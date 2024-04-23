from .enums import StatusCode


class BodyTooLargeError(Exception):
	"Raised when the size of the body goes over the limit"


	def __init__(self, limit: int, size: int):
		"""
			Create a new ``BodyTooLargeError`` exception

			:param limit: Maximum size in bytes the body can be
			:param size: Size of the body when the error was raised
		"""

		Exception.__init__(self, f"Body larger than limit ({limit}): {size}")

		self.limit = limit
		"Maximum size in bytes the body can be"

		self.size = size
		"Size of the body when the error was raised"


class GeminiError(Exception):
	"Raised when an error occurs in a server handler"

	def __init__(self, status: StatusCode | int, message: str):
		"""
			Create a new ``GeminiError`` exception

			:param status: Status code to set for the response
			:param message: Text to send to the client
		"""

		status = StatusCode.parse(status)

		Exception.__init__(self, f"Gemini Error {status} {status.reason}: {message}")

		self.status: StatusCode = status
		"Status code to set for the response"

		self.message: str = message
		"Text to send to the client"



class ParsingError(SyntaxError):
	"Raised when a Gemini document cannot be parsed"


	def __init__(self,
				message: str,
				lineno: int,
				offset: int,
				line: str,
				filename: str | None = None):
		"""
			Create a new ``ParsingError`` exception

			:param message: Text to display to the console
			:param lineno: Line number of where the error occured
			:param offset: Character number of where the error occured
			:param line: Text of the line where the error occured
			:param filename: Filename of the document
		"""

		params = (filename or "--inline--", lineno, offset, line, lineno, offset)

		SyntaxError.__init__(self, message, params)
