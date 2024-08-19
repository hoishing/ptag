from ptag import Tag
from textwrap import dedent


def test_void_element():
    assert str(Tag("br")) == "<br />"


def test_str_child():
    assert str(Tag("p", "hello")) == "<p>hello</p>"


def test_tag_child():
    p = Tag("p", Tag("span", "world"))
    assert str(p) == "<p><span>world</span></p>"


def test_add_str():
    p = Tag("p").add("hello")
    assert str(p) == "<p>hello</p>"


def test_add_tag():
    p = Tag("p").add(Tag("i", "hello"))
    assert str(p) == "<p><i>hello</i></p>"


def test_add_from_none():
    p = Tag("p")
    p.add("hello")
    assert str(p) == "<p>hello</p>"


def test_add_from_str():
    p = Tag("p", "hello-")
    p.add("world")
    assert str(p) == "<p>hello-world</p>"


def test_pretty_basic():
    p = Tag("p", "hello").add(Tag("i", "world"))
    assert p.prettify() == "<p>\n    hello\n    <i>world</i>\n</p>\n"


def test_context_manager():
    with Tag("div", "hello") as div:
        Tag("p", "world")
        Tag("p", "🎉")

    assert str(div) == "<div>hello<p>world</p><p>🎉</p></div>"


def test_2_level():
    with Tag("div") as div:
        Tag("p", "hello")
        with Tag("p", "shing") as p:
            Tag("span", "world")

    assert str(div) == "<div><p>hello</p><p>shing<span>world</span></p></div>"


def test_2_level_with_str():
    with Tag("div") as div:
        Tag("p", "hello")
        with Tag("p"):
            Tag("span", "world")
        div.add("shing")

    assert str(div) == "<div><p>hello</p><p><span>world</span></p>shing</div>"


def test_restricted_attribute_name():
    with Tag("div", id="foo", class_="bar") as div:
        Tag("p", "rock", for_="baz")

    assert str(div) == '<div id="foo" class="bar"><p for="baz">rock</p></div>'


def test_boolean_attribute():
    input = Tag(
        "input",
        None,
        "checked",
        type="checkbox",
    )
    assert str(input) == '<input checked type="checkbox" />'


def test_none_kwarg():
    t = Tag("div", None, id=3, class_=None, selected="")
    assert str(t) == '<div id="3" selected="" />'


def test_pretty():
    with Tag("html") as html:
        div = Tag("div", "hello")
        div.add(Tag("p", "world"))
        with Tag("p", "something"):
            Tag("span", "yeah")

    output = """\
        <html>
            <div>
                hello
                <p>world</p>
            </div>
            <p>
                something
                <span>yeah</span>
            </p>
        </html>
        """

    assert html.prettify() == dedent(output)
