from typing import Self
from xml.dom.minidom import Document, parseString
from typing import Iterable

ChildrenType = Iterable[Self | str] | None
ContentType = str | Self | ChildrenType


class Tag:
    """HTML / SVG element generation class

    Examples:

        - void element, content=None (default)
        >>> Tag('br')
        <br />

        - void Tag w/ attr
        >>> Tag("img", src="http://img.url")
        <img src="http://img.url" />

        - empty string content -> Tag with end tag but no content
        >>> Tag("script", content="", src="url")
        <script src="url"></script>

        - boolean attribute(attribute w/o value)
        >>> Tag("option", "a", "selected")
        <option selected>a</option>

        - mix of boolean attribute and normal attribute
        >>> Tag('a', 'foo', 'm-2', 'rounded', 'text-teal-400', href='bar')
        <a m-2 rounded text-teal-400 href="bar">foo</a>

        - none attribute will be omitted
        >>> Tag('a', 'foo', href=None, target='_blank')
        <a target="_blank">foo</a>

        - nested Tag
        >>> Tag("div", Tag("i", "x"))
        <div><i>x</i></div>

    Args:
        tag_name (str | None): tag name
        content (ContentType, optional): inner text, other Tag(s), or iterable of str/Tag, default None
        **kwargs (dict[str, str | bool | None]): tag attributes, in form of `key=value`
            - Use `key=None` to omit an attribute
            - Use underscores for attribute names with hyphens (e.g., `data_attr="value"`)

    Returns:
        Tag: An instance of the Tag class representing the HTML/SVG element
    """

    tag_name: str
    children: ChildrenType = None
    args: list[str] = []
    kwargs: dict[str, str] = {}
    parent: Self | None = None
    context_stack: list[Self | "Text"] = []  # context stack for context manager

    def __init__(
        self,
        tag_name: str | None,
        content: ContentType = None,
        *args: list[str],
        **kwargs: dict[str, str],
    ):
        """initialize Tag, append to current context stack if exists"""
        self.tag_name = str(tag_name)
        self.args = sorted(set(args))
        self.kwargs = kwargs
        self.children = self.normalize(content)

        if Tag.context_stack:
            Tag.context_stack[-1].affix(self)

    def normalize(self, content: ContentType) -> ChildrenType:
        """normalize content of different types to ChildrenType"""
        if content is None:
            return None

        if isinstance(content, (str, Tag)):
            return [self._create_child(content)]

        if hasattr(content, "__iter__"):
            return [self._create_child(item) for item in content]

        raise ValueError(f"Invalid content type: {type(content)}")

    def _create_child(self, item: str | Self) -> Self | "Text":
        """create child node from string or Tag"""
        match item:
            case str():
                child = Text(item)
            case Tag():
                child = item
            case _:
                raise ValueError(f"Invalid content type: {type(item)}")

        child.parent = self
        return child

    def __enter__(self):
        """enter context manager, append self to current context stack

        Examples:
            >>> with Tag("div", "hello") as div: # doctest: +SKIP
            ...     Tag("p", "world")
            >>> div                              # doctest: +SKIP
            <div>hello<p>world</p></div>
        """

        Tag.context_stack.append(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """exit context manager, pop self from current context stack"""
        tag = Tag.context_stack.pop()
        # accept children if their parent is itself only
        self.children = [
            child
            for child in self.children
            if isinstance(child, str) or child.parent is self
        ]

    def __repr__(self):
        """string representation of the Tag"""

        # handle python naming restriction
        amended_keys = [
            (
                key.removesuffix("_")
                if key in ("class_", "for_")
                else key.replace("_", "-")
            )
            for key in self.kwargs.keys()
        ]

        kwargs_tuple = zip(amended_keys, self.kwargs.values())

        kwargs = [f'{key}="{val}"' for key, val in kwargs_tuple if val is not None]
        attr = [self.tag_name] + list(self.args) + kwargs
        attr_str = " ".join(attr)

        content = None if self.children is None else "".join(map(str, self.children))

        # void element with self closing tag
        if content is None:
            return f"<{attr_str} />"

        return f"<{attr_str}>{content}</{self.tag_name}>"

    def affix(self, content: ContentType, *args, **kwargs) -> Self:
        """append child and attributes to current Tag"""
        children = self.normalize(content)
        if children:
            old_children = self.children or []
            new_children = [child for child in children if child not in old_children]
            self.children = old_children + new_children

        self.args = sorted(set(self.args) | set(args))
        self.kwargs.update(kwargs)
        return self

    def prettify(self, indent="    ") -> str:
        """prettify the Tag with indentation"""
        dom = parseString(str(self))
        return dom.childNodes[0].toprettyxml(indent=indent)

    @property
    def str(self) -> str:
        """string representation of the Tag"""
        return str(self)

    @staticmethod
    def comment(comment: str) -> str:
        """comment element

        Examples:
            >>> Tag.comment("hello")
            '<!--hello-->'
        """
        return Document().createComment(comment).toxml()

    @staticmethod
    def doctype(kind: str = "html") -> str:
        """DOCTYPE element

        Examples:
            >>> Tag.doctype()
            '<!DOCTYPE html>'
        """
        return f"<!DOCTYPE {kind}>"


class Text(str):
    """text node"""

    def __init__(self, content: str):
        self.content = content
