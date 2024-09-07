import argparse
import re
import os
import typing
from dataclasses import dataclass
from typing import Literal, ClassVar, Generator
from contextlib import contextmanager
import logging
log = logging.getLogger('skin')
@contextmanager
def sublog(name:str):
    global log
    parent_log = log
    try:
        log = parent_log.getChild(name)
        yield
    finally:
        log = parent_log

class ParametricRegexCache(dict[str, re.Pattern]):
    def __init__(self, pattern:str, *args, **kwargs):
        self.pattern = pattern
        self.args = args
        self.kwargs = kwargs
    def __missing__(self, key:str) -> re.Pattern:
        regex_string = self.pattern.format(key=key)
        regex = re.compile(regex_string, *self.args, **self.kwargs)
        self[key] = regex
        return regex

ElementName = Literal[
    'skin',
    'skinname',
    'date',
    'macros',
    'stylesheet',
    'templates',
    'wrappers',
]
ELEMENT_NAMES: tuple[ElementName,...] = typing.get_args(ElementName)
ELEMENT_REGEX: dict[ElementName, re.Pattern] = ParametricRegexCache(
    r"<{key}>(?P<body>.*)</{key}>", re.DOTALL|re.MULTILINE
)
ITEMS_REGEX: dict[str, re.Pattern] = ParametricRegexCache(
    r"<item name='{key}'>(?P<body>.*?)</item>", re.DOTALL|re.MULTILINE
)

@dataclass(repr=False)
class SkinNode:
    _data: str
    _pos: int = 0
    _endpos: int = -1

    def __post_init__(self):
        if self._endpos == -1:
            self._endpos = len(self._data)

    def __getattr__(self, name:ElementName) -> 'SkinNode':
        assert name in ELEMENT_NAMES
        regex = ELEMENT_REGEX[name]
        matches = list(regex.finditer(self._data, pos=self._pos, endpos=self._endpos))
        if len(matches) != 1:
            raise AttributeError(f"{regex=} {matches=!r}", name=name, obj=self)
        match, = matches
        return SkinNode(self._data, match.start('body'), match.end('body'))
    
    def items(self) -> 'Generator[tuple[str, SkinNode]]':
        regex = ITEMS_REGEX[r"(?P<name>[^']*?)"]
        matches = regex.finditer(self._data, pos=self._pos, endpos=self._endpos)
        for match in matches:
            yield (match.group('name'), SkinNode(self._data, match.start('body'), match.end('body')))
    
    def __getitem__(self, name:str) -> 'SkinNode':
        regex = ITEMS_REGEX[name]
        matches = list(regex.finditer(self._data, pos=self._pos, endpos=self._endpos))
        if len(matches) != 1:
            raise KeyError(f"{regex=} {matches=!r}")
        match, = matches
        return SkinNode(self._data, match.start('body'), match.end('body'))
    
    @property
    def text(self):
        return str(self)

    def __dir__(self) -> list[str]:
        return list(ELEMENT_NAMES) + list(super().__dir__())
    
    def __str__(self) -> str:
        return self._data[self._pos:self._endpos]
    
    def __repr__(self) -> str:
        _data = f"<str at {id(self._data):#x}>"
        _pos = self._pos
        _endpos = self._endpos
        return f"{self.__class__.__name__}({_data=!s}, {_pos=}, {_endpos=})"

def load(filename: str) -> SkinNode:
    with open(filename, 'r', encoding='utf8', errors='surrogateescape') as f:
        node = SkinNode(f.read())

    log.info("loaded %s", filename)
    try:
        log.info("name: %s", node.skinname.text)
    except AttributeError:
        log.warning("input file does not contain a name")
    try:
        log.info("date: %s", node.date.text)
    except AttributeError:
        log.warning("input file does not contain a date")

    return node

def load_or_default(filename: str, default:SkinNode) -> SkinNode:
    if filename:
        return load(filename)
    else:
        return default

def write_item_files(node: SkinNode, path: str, suffix: str = ".html", headmatter: str = ""):
    for name, body in node.items():
        filepath = os.path.join(path, name) + suffix
        write_node_file(body, filepath, headmatter=headmatter)

def write_node_file(node: SkinNode, path: str, headmatter: str = ""):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf8', errors='surrogateescape') as f:
            f.write(headmatter)
            f.write(node.text)
    except:
        log.exception("error writing file")
        raise
    log.info("wrote %s", path)

def main(full:str, macros:str, stylesheet:str, templates:str, wrapper:str, out:str, **kwargs):
    with sublog('full'):
        full_data = load_or_default(full, None)

    with sublog('macros'):
        data = load_or_default(macros, full_data)
        try:
            node = data.skin.macros
        except AttributeError:
            log.warning("element not found")
        else:
            write_item_files(
                node = node,
                path = os.path.join(out, "macros"),
                suffix = ".html",
                headmatter = '---\nlayout: macro\n---\n',
            )

    with sublog('templates'):
        data = load_or_default(templates, full_data)
        try:
            node = data.skin.templates
        except AttributeError:
            log.warning("element not found")
        else:
            write_item_files(
                node = node,
                path = os.path.join(out, "templates"),
                suffix = ".html",
                headmatter = '---\nlayout: template\n---\n',
            )

    with sublog('stylesheet'):
        data = load_or_default(stylesheet, full_data)
        try:
            node = data.skin.stylesheet
        except AttributeError:
            log.warning("element not found")
        else:
            write_node_file(
                node = node,
                path = os.path.join(out, "stylesheet") + ".css",
            )

    with sublog('wrapper'):
        data = load_or_default(wrapper, full_data)
        try:
            node = data.skin.wrappers
        except AttributeError:
            log.warning("element not found")
        else:
            write_node_file(
                node = data.skin.wrappers,
                path = os.path.join(out, "wrapper") + ".html",
                headmatter = '---\nlayout: wrapper\n---\n',
            )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", help="Path to skinset.xml.")
    parser.add_argument("--macros", help="Path to macros.xml.")
    parser.add_argument("--stylesheet", help="Path to stylesheet.xml.")
    parser.add_argument("--templates", help="Path to templates.xml.")
    parser.add_argument("--wrapper", help="Path to wrapper.xml.")
    parser.add_argument("--out", default=os.curdir, help="Output directory. default: current directory")
    parser.add_argument("--loglevel", default="info", help="Provide logging level. default: info" )
    
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel.upper())

    main(**vars(args))