from ptag import *
from textwrap import dedent


def test_br():
    assert str(br()) == "<br />"


def test_div():
    assert str(div("hello")) == "<div>hello</div>"


def test_bool_attr():
    with form() as f:
        label("Agree to terms", for_="agree")
        input_(None, "checked", name="agree", type="checkbox")

    assert (
        str(f)
        == '<form><label for="agree">Agree to terms</label><input checked name="agree" type="checkbox" /></form>'
    )


def test_update_args():
    l = label("Agree to terms")
    l.add("🎉", class_="some class", for_="foo-input", data_columns="3")

    assert (
        str(l)
        == '<label class="some class" for="foo-input" data-columns="3">Agree to terms🎉</label>'
    )


def test_pretty():
    with html() as doc:
        div("hello").add(p("world"))
        with p("something"):
            span("yeah")

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

    assert doc.prettify() == dedent(output)
