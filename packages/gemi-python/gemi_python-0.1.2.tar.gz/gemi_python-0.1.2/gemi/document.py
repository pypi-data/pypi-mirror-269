from __future__ import annotations

from pathlib import Path

from .enums import OutputFormat
from .error import ParsingError


HTML_TEMPLATE: str = """<!doctype html>
<html>
	<head>{title}</head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<body>
{contents}
	</body>
</html>
"""


class Element:
	"Represents a single element in a Gemini document"

	pre: str | None = None
	"String to add to the beginning of the text"

	text: str
	"Body of the element"


	def build(self) -> str:
		"Convert the element to a string"

		data = self.text

		if self.pre is not None:
			data = f"{self.pre} {self.text}"

		return data


	def __repr__(self) -> str:
		return f"{type(self).__name__}(text = {repr(self.text)})"


	@staticmethod
	def parse(text: str) -> Element:
		"""
			Parse some text and return the appropriate object

			:param text: String to parse
		"""

		elem: Element
		prefix: str | None
		value: str

		try:
			prefix, value = text.split(" ", 1)

		except ValueError:
			prefix, value = None, text

		if not prefix:
			return Text(value)

		if prefix.startswith("#"):
			return Header(value, len(prefix))

		if prefix == ">":
			return Quote(value)

		if prefix == "*":
			return ListItem(value)

		if prefix == "=>":
			elem = Link("", "")
			elem.text = value
			return elem

		if prefix == "```":
			return Preformatted(value.replace("```", ""))

		return Text(text)


class Header(Element):
	"Represents a header element (starts with '#')"
	pre = "#"


	def __init__(self, label: str, prefix_length: int = 1):
		"""
			Create a new Header element

			:param label: Text to display in the header
			:param prefix_length: Header level to set (min: 1, max: 3)
		"""

		assert 0 < prefix_length < 4, "Prefix length can only be from 1 to 3"

		self.label: str = label
		"Text to display in the header"

		self.pre: str = "#" * prefix_length # type: ignore
		"Header level to set"


	@property
	def text(self) -> str:
		"Body of the element"

		return self.label


	@text.setter
	def text(self, value: str | tuple[str, int]) -> None:
		if isinstance(value, str):
			prefix, label = value.split(" ", 1)

			if set(prefix) != set("#"):
				raise ValueError("Prefix can only include '#' characters")

			value = (label, len(prefix))

		self.label = value[0]
		self.prefix_length = value[1]


	def set_prefix_length(self, length: int) -> None:
		self.pre = "#" * length


class Link(Element):
	"Represents a link element"

	pre = "=>"


	def __init__(self, url: str, label: str | None = None):
		"""
			Create a new link element

			:param label: Text to display in the header
			:param url: Url to direct the user to
		"""

		self.label: str | None = label
		"Text to display in the header"

		self.url: str = url
		"Url to direct the user to"


	def __repr__(self) -> str:
		return f"{type(self).__name__}(url = {repr(self.url)}, label = {repr(self.label)})"


	@property
	def text(self) -> str:
		"Body of the element"

		if self.label is None:
			return self.url

		return f"{self.url} {self.label}"


	@text.setter
	def text(self, value: str | tuple[str, str | None]) -> None:
		if isinstance(value, str):
			try:
				self.url, self.label = tuple(value.split(" ", 1))

			except ValueError:
				self.url, self.label = value, None

			return

		self.label = value[1]
		self.url = value[0]


class ListItem(Element):
	"Represents an item in a list"

	pre: str = "*"


	def __init__(self, text: str):
		"""
			Create a new list item element

			:param text: String to display in the list
		"""

		self.text = text


class Preformatted(Element, list[str]):
	"Represents an unparsed text block"

	pre: str = "```"


	def __init__(self, lines: str | list[str]):
		"""
			Create a new unparsed text block

			:param lines: A single line or list of lines to add to the element
		"""

		self.add_lines(lines)


	def __repr__(self) -> str:
		return f"{type(self).__name__}({list.__repr__(self)})"


	@property
	def text(self) -> str:
		"Body of the element"

		return "\n".join(self)


	@text.setter
	def text(self, value: str | list[str]) -> None:
		self.clear()
		self.add_lines(value)


	def add_lines(self, value: str | list[str]) -> None:
		"""
			Add a line or multiple lines to the end of the element

			:param value: A single line or list of lines to be appended
		"""

		if isinstance(value, str):
			self.extend(value.splitlines())
			return

		self.extend(value)


	def build(self) -> str:
		return f"```\n{self.text}\n```"


class Quote(Element):
	"Represents quoted line of text"

	pre: str = ">"

	def __init__(self, text: str):
		"""
			Create a new quote element

			:param text: String to display in the quote
		"""

		self.text = text


class Text(Element):
	"Represents a block of text"


	def __init__(self, line: str):
		"""
			Create a new text element

			:param line: A string object
		"""

		self.text = line


class Document(list[Element]):
	"Represents a collection of elements in a Gemini document"

	@classmethod
	def load(cls, path: Path | str) -> Document:
		"""
			Load a document from a path

			:param path: Path to the file
		"""

		with open(path) as fd:
			return cls.loads(fd.read())


	@classmethod
	def loads(cls, data: str | bytes, _filename: str | None = None) -> Document:
		"""
			Load a document from a string or bytes object

			:param data: Data to be parsed
			:param _filename: Internal use
		"""
		data = data.decode("utf-8") if isinstance(data, bytes) else data

		items = cls()
		preformat: Preformatted | None = None

		for idx, raw_line in enumerate(data.splitlines()):
			line = raw_line.strip()

			if preformat is not None:
				if "```" in raw_line:
					if len(raw_line) > (end_index := raw_line.index("```") + 3):
						raise ParsingError(
							message = "Text after preformatted text block ending",
							line = raw_line,
							lineno = idx,
							offset = end_index,
							filename = _filename
						)

					preformat = None
					continue

				preformat.append(raw_line)
				continue

			if "```" in line:
				if raw_line.startswith("```"):
					if len(raw_line) > 3:
						raise ParsingError(
							message = "Text after Indicator for preformatted block",
							lineno = idx,
							offset = 3,
							line = raw_line,
							filename = _filename
						)

					preformat = Preformatted("")
					items.append(preformat)
					continue

				raise ParsingError(
					message = "Indicator for preformatted block not at start of line",
					line = raw_line,
					lineno = idx,
					offset = raw_line.index("```"),
					filename = _filename
				)

			items.append(Element.parse(line))

		return items


	@property
	def title(self) -> str | None:
		if len(self) > 0 and isinstance((element := self[0]), Header):
			return element.text

		return None


	def dump(self, path: Path | str, format: OutputFormat | str = "gemtext") -> None:
		"""
			Save the document as a file

			:param path: File to save the document to
			:param format: Text format to dumps the document to
		"""

		with open(path, "r", encoding = "utf8") as fd:
			fd.write(self.dumps(format = format))


	def dumps(self, format: OutputFormat | str = "gemtext") -> str:
		"""
			Convert the document to a string

			:param format: Text format to dumps the document to
		"""

		format = OutputFormat.parse(format)

		if format == OutputFormat.GEMTEXT:
			return "\n".join(elem.build() for elem in self) + "\n"

		if format == OutputFormat.HTML:
			return _dump_to_html(self)

		if format == OutputFormat.MARKDOWN:
			return _dump_to_markdown(self)

		raise ValueError("n_n")


def _dump_to_html(document: Document) -> str:
	data: list[str] = []

	for idx, element in enumerate(document):
		if isinstance(element, Text):
			if not element.text:
				continue

			data.append(f"<p>{element.text}</p>")

		elif isinstance(element, Quote):
			data.append(f"<blockquote>{element.text}</blockquote>")

		elif isinstance(element, Preformatted):
			text = "\n".join(f"\t{line}" for line in element)
			data.append(f"<pre>\n{text}\n</pre>")

		elif isinstance(element, ListItem):
			if idx > 0 and not isinstance(document[idx - 1], ListItem):
				data.append("<ul>")

			data.append(f"\t<li>{element.text}")

			if document[-1] != element and not isinstance(document[idx + 1], ListItem):
				data.append("</ul>")

		elif isinstance(element, Link):
			data.append(f'<a href="{element.url}">{element.label}</a>')

		elif isinstance(element, Header):
			data.append(f"<h{len(element.pre)}>{element.text}</h{len(element.pre)}>")

	return HTML_TEMPLATE.format(
		contents = "\n".join(f"\t\t{line}" for line in data) + "\n",
		title = document.title or "Gemtext Document"
	)


def _dump_to_markdown(document: Document) -> str:
	data: list[str] = []

	for element in document:
		if isinstance(element, Text):
			data.append(element.text)

		elif isinstance(element, Quote):
			data.append(f"> {element.text}")

		elif isinstance(element, Preformatted):
			data.extend(f"\t{line}" for line in element)

		elif isinstance(element, (ListItem, Header)):
			data.append(element.build())

		elif isinstance(element, Link):
			if not element.label:
				data.append(f"[{element.url}]({element.url})")

			else:
				data.append(f"[{element.label}]({element.url})")

	return "\n".join(data) + "\n"
