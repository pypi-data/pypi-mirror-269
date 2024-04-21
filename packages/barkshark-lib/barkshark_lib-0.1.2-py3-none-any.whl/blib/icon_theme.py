from abc import ABC, abstractmethod
from typing import Any

from .errors import FileError
from .path import File


class Icon(dict[int, Any]):
	"Represents an icon"

	__slots__ = ("name",)


	def __init__(self, name: str, icons: dict[int, Any] | None = None) -> None:
		"""
			Create a new ``Icon`` object

			:param name: Name of the icon
			:param icons: Icon data and their sizes
		"""

		dict.__init__(self, icons or {})

		self.name: str = name


	def __repr__(self) -> str:
		sizes = ",".join(repr(size) for size in self.sizes)
		return f"Icon({repr(self.name)}, sizes={sizes})"


	@property
	def sizes(self) -> tuple[int, ...]:
		"Return a tuple of the available icon sizes"

		return tuple(sorted(self.keys()))


	@property
	def small(self) -> Any:
		"Return a 16x16 icon if available"

		return self[16]


	@property
	def normal(self) -> Any:
		"Return a 32x32 icon if available"

		return self[32]


	@property
	def large(self) -> Any:
		"Return a 64x64 icon if available"

		return self[64]


	@property
	def extra_large(self) -> Any:
		"Return a 128x128 icon if available"

		return self[128]


	@property
	def scalable(self) -> Any:
		"Return a scalable (usually svg) icon if available"

		return self[0]


class IconTheme(ABC):
	"Base class for icon themes"

	name: str
	"Name of the icon theme"

	@abstractmethod
	def get_icon(self, name: str) -> Icon: ...


class IconThemes(dict[str, IconTheme]):
	"Represets a collection of icon themes"


	def __init__(self, base_path: str = "/usr/share/icons", default: str = "hicolor") -> None:
		"""
			Create a new ``IconThemes`` object

			:param base_path: Filesystem path to search for icon themes
			:param default: Fallback theme to use when searching for icons
			:raises ValueError: When the default theme cannot be found
		"""

		self.base_path: File = File(base_path).resolve()
		"Filesystem path to search for icon themes"

		self.themes: dict[str, IconTheme] = {}
		"Loaded icon themes"

		self.default: IconTheme = MemoryIconTheme("default")
		"Fallback icon theme"

		self.load(default)


	def get_icon(self, theme: str, name: str) -> Icon:
		"""
			Get an icon. If the icon cannot be found in the specified theme, the default theme
			will get searched.

			:param theme: Icon theme to search
			:param name: Name of the icon (case-insensitive)
			:raises KeyError: If the icon cannot be found
		"""

		try:
			self.themes[theme].get_icon(name)

		except KeyError:
			pass

		return self.default.get_icon(name)


	def load(self, default: str = "hicolor") -> None:
		"""
			Load themes from the base path

			:params defualt: Fallback theme to use when searching for icons
		"""

		themes: dict[str, IconTheme] = {}
		fallback: IconTheme | None = None

		for path in self.base_path.glob():
			if path.isdir:
				themes[path.name] = FileIconTheme(path)

				if path.name.lower() == default.lower():
					fallback = themes[path.name]

		if fallback is None:
			raise ValueError(f"Cannot find default theme: {default}")

		self.default = fallback
		self.themes = themes


class FileIconTheme(IconTheme):
	"Represents an icon theme in a directory"

	__slots__ = ("path", "name", "default", "_cache")


	def __init__(self, base_path: str, name: str | None = None) -> None:
		"""
			Create a new ``FileIconTheme`` object

			:param base_path: Path to the icon theme
			:param name: Name of the icon theme
			:raises blib.FileError: If the path is not a directory or does not exist
		"""

		self.path: File = File(base_path).resolve()
		self.name: str = name or self.path.name
		self._cache: dict[str, Icon | None] = {}

		if not self.path.isdir:
			raise FileError.IsFile(self.path)

		if not self.path.exists:
			raise FileError.NotFound(self.path)


	def clear_cache(self) -> None:
		"Clear the cached icon results"

		self._cache.clear()


	def get_icon(self, name: str) -> Icon:
		if name in self._cache:
			if (cached := self._cache[name]) is None:
				raise KeyError(name)

			return cached

		icon = Icon(name)

		for path in self.path.glob(recursive = True, ext = ["png", "svg", "svgz"]):
			if name.lower() == path.stem.lower():
				size_str = path.split(self.name)[1].split("/")[1]

				if size_str != "scalable":
					icon[int(size_str.split("x")[0])] = path

				else:
					icon[0] = path

		if len(icon) == 0:
			self._cache[name] = None
			raise KeyError(name)

		self._cache[name] = icon
		return icon


class MemoryIconTheme(IconTheme):
	__slots__ = ("name", "icons",)

	def __init__(self, name: str, *icons: Icon) -> None:
		"""
			Create a new ``MemoryIconTheme`` object

			:param name: Name of the icon theme
			:param icons: List of icons to be included in the theme
		"""

		self.name: str = name
		self.icons: dict[str, Icon] = {icon.name: icon for icon in icons}


	def get_icon(self, name: str) -> Icon:
		return self.icons[name]


	def set_icon(self, name: str, size: int, data: bytes) -> None:
		"""
			Add an icon to the theme

			:param name: Name of the icon
			:param size: Size of the icon. Use ``0`` for scalable.
			:param data: Raw data of the icon
		"""

		if name not in self.icons:
			self.icons[name] = Icon(name)

		self.icons[name][size] = data
