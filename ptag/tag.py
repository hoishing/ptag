from typing import Self
from xml.dom.minidom import Document, parseString
from typing import NamedTuple


class Tag:
    """HTML / SVG element generation class

    Examples:

        - void element, child=None (default)
        >>> Tag('br')
        <br />

        - void Tag w/ attr
        >>> Tag("img", src="http://img.url")
        <img src="http://img.url" />

        - empty string child -> Tag with end tag but no content
        >>> Tag("script", child="", src="url")
        <script src="url"></script>

        - boolean attribute(attribute w/o value)
        >>> Tag("option", "a", "selected")
        <option selected>a</option>

        - mix of boolean attribute and normal attribute
        >>> Tag('a', 'foo', 'm-2', 'rounded', 'text-teal-400', href='bar')
        <a m-2 rounded text-teal-400 href="bar">foo</a>

        - nested Tag
        >>> Tag("div", Tag("i", "x"))
        <div><i>x</i></div>

    Args:
        tag_name (str): tag name
        child (str | Tag | None): inner text or other Tag, default None
        args (list[str], optional): names of value-less attributes
            - eg. `defer`, `selected`
            - useful for UnoCSS attributify mode
        kwargs (dict): tag attributes, in form of `key="val"`

    """

    tag_name: str
    args: list[str] = []
    kwargs: dict[str, str] = {}
    parent: Self | None = None
    children: list[Self | str] | None = None
    context_stack: list[Self] = []  # context stack for context manager

    def __init__(
        self,
        tag_name: str | None,
        child: str | Self | None = None,
        *args,
        **kwargs,
    ):
        """initialize Tag, append to current context stack if exists"""
        self.tag_name = tag_name
        self.args = args
        self.kwargs = kwargs
        self.children = self.prepare_child(child)

        if Tag.context_stack:
            Tag.context_stack[-1].add(self)

    def prepare_child(self, child: str | Self | None) -> list[Self | str] | None:
        """utils, prepare children for the Tag"""
        if child is None:
            return None
        if isinstance(child, Tag):
            child.parent = self
        return [child]

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
        correct_keys = [
            (
                key.removesuffix("_")
                if key in ("class_", "for_")
                else key.replace("_", "-")
            )
            for key in self.kwargs.keys()
        ]

        kwargs_tuple = zip(correct_keys, self.kwargs.values())

        kwargs = [f'{key}="{val}"' for key, val in kwargs_tuple]
        attr = [self.tag_name] + list(self.args) + kwargs
        attr_str = " ".join(attr)

        content = None if self.children is None else "".join(map(str, self.children))

        # void element with self closing tag
        if content is None:
            return f"<{attr_str} />"

        return f"<{attr_str}>{content}</{self.tag_name}>"

    def add(self, child: str | Self, *args, **kwargs) -> Self:
        """add child and attributes to current Tag

        Examples:
            >>> opt = Tag('option')
            >>> opt.add('hello', 'selected', value='world')
            <option selected value="world">hello</option>
        """
        tail = self.prepare_child(child)
        self.children = tail if self.children is None else self.children + tail
        self.args += args
        self.kwargs.update(kwargs)
        return self

    def prettify(self, indent="    ") -> str:
        """prettify the Tag with indentation"""
        dom = parseString(str(self))
        return dom.childNodes[0].toprettyxml(indent=indent)

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
