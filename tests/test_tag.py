from ptag import Tag
from textwrap import dedent


def test_void_element():
    assert Tag("br").str == "<br />"
    assert Tag("br", None).str == "<br />"


def test_empty_str_content():
    assert Tag("br", "").str == "<br></br>"


def test_str_content():
    assert Tag("p", "hello").str == "<p>hello</p>"


def test_tag_content():
    p = Tag("p", Tag("span", "world"))
    assert p.str == "<p><span>world</span></p>"


def test_affix_str():
    p = Tag("p").affix("hello")
    assert p.str == "<p>hello</p>"


def test_affix_tag():
    p = Tag("p").affix(Tag("i", "hello"))
    assert p.str == "<p><i>hello</i></p>"


def test_affix_multiple_tags():
    p = Tag("p")
    p.affix([Tag("i", "hello"), Tag("i", "world")])
    assert p.str == "<p><i>hello</i><i>world</i></p>"


def test_str_tag_mix():
    with Tag("p") as p:
        p.affix([Tag("i", "hello"), "world"])
    assert p.str == "<p><i>hello</i>world</p>"


def test_affix_from_none():
    p = Tag("p")
    p.affix("hello")
    assert p.str == "<p>hello</p>"


def test_affix_from_str():
    p = Tag("p", "hello-")
    p.affix("world")
    assert p.str == "<p>hello-world</p>"


def test_pretty_basic():
    p = Tag("p", "hello").affix(Tag("i", "world"))
    assert p.prettify() == "<p>\n    hello\n    <i>world</i>\n</p>\n"


def test_context_manager():
    with Tag("div", "hello") as div:
        Tag("p", "world")
        Tag("p", "🎉")

    assert div.str == "<div>hello<p>world</p><p>🎉</p></div>"


def test_2_level_context():
    with Tag("div") as div:
        Tag("p", "hello")
        with Tag("p", "shing") as p:
            Tag("span", "world")

    assert div.str == "<div><p>hello</p><p>shing<span>world</span></p></div>"


def test_2_level_context_with_str():
    with Tag("div") as div:
        Tag("p", "hello")
        with Tag("p"):
            Tag("span", "world")
        div.affix("shing")

    assert div.str == "<div><p>hello</p><p><span>world</span></p>shing</div>"


def test_restricted_attribute_name():
    with Tag("div", id="foo", class_="bar") as div:
        Tag("p", "rock", for_="baz")

    assert div.str == '<div id="foo" class="bar"><p for="baz">rock</p></div>'


def test_boolean_attribute():
    input = Tag("input", None, "checked", type="checkbox")
    assert input.str == '<input checked type="checkbox" />'
    # boolean should be treated as string
    input2 = Tag("input", None, checked=True, type="checkbox")
    assert input2.str == '<input checked="True" type="checkbox" />'
    # int should be converted to string
    input3 = Tag("input", None, checked=1, type="checkbox")
    assert input3.str == '<input checked="1" type="checkbox" />'


def test_none_kwarg():
    t = Tag("div", None, id=3, class_=None, selected="")
    assert t.str == '<div id="3" selected="" />'


def test_prettify():
    with Tag("html") as html:
        div = Tag("div", "hello")
        div.affix(Tag("p", "world"))
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


def test_multiple_content():
    with Tag("html") as html:
        t1 = Tag("i", "hello")
        t2 = Tag("p", "world")
        Tag("div", [t1, t2])
        with Tag("p", "something"):
            Tag("span", "yeah")

    assert (
        html.str
        == "<html><div><i>hello</i><p>world</p></div><p>something<span>yeah</span></p></html>"
    )


def test_args_order():
    t = Tag("div", "hello", "world", "foo", "bar")
    assert t.args == ["bar", "foo", "world"]
    # omit duplicate args
    t2 = Tag("div", "hello", "world", "foo", "bar", "foo")
    assert t2.args == ["bar", "foo", "world"]
    # append should not add duplicate args, and keep order
    t3 = Tag("div", "hello", "foo")
    t3.affix("world", "baz", "bar", "foo")
    assert t3.args == ["bar", "baz", "foo"]
