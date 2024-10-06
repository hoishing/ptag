# ptag

[![ci-badge]][ci-url] [![pypi-badge]][pypi-url] [![MIT-badge]][MIT-url] [![black-badge]][black-url]

> pythonic way to create HTML/XML/SVG tags

- create tags in pure python
- use **context manager** to create tag hierarchy
- create value-less(boolean) attributes with positional argument
    - handy for using with [UnoCSS] attributify mode
- all standard html and svg elements are exported as functions
- pure python, no external dependencies
- high test coverage

## Quick Start

- Installation: `pip install ptag`
- base signature
    - `element(content = None, *args, **kwargs) -> Tag`

```python
# common elements
from ptag import div, img, p, ul, li, label, input_,
# for creating custom element
from ptag import Tag  
# for pretty print
from ptag import prettify  

# empty tag
print(div())
# <div />

# None content is ignored
print(div(None))
# <div />

# empty string content creates closing tag
print(div(""))
# <div></div>

# tag as content
print(div(img(src="url"), id="bar"))  
# <div id="bar"><img src="url"/></div>

# content mix with strings and tags
print(div(["foo", img(src="url"), "bar")])
# <div>foo<img src="url"/>bar</div>
```

- use with context manager

```python
with ul() as bullets:
    li("foo")
    li("bar")

print(bullets)
# <ul><li>foo</li><li>bar</li></ul>
```

- pretty print

```python
print(bullets.prettify())
# <ul>
#     <li>foo</li>
#     <li>bar</li>
# </ul>
```

- use trailing underscore to work around python keyword and built-in functions
- attributes:
    - `class_` -> `class`
    - `for_` -> `for`
- elements:
    - `del_` -> `del`
    - `input_` -> `input`
    - `map_` -> `map`
    - `object_` -> `object`

```python
print(label("foo", for_="bar"))
# <label for="bar">foo</label>

print(input_(None, class_="foo", name="bar", type="checkbox", value="baz"))
# <input name="bar" type="checkbox" value="baz"/>
```

- position args -> value-less attribute.
    - boolean attribute: eg. `checked`, `disabled`, `selected`
    - assign tailwind classes with [UnoCSS] attributify mode

```python
print(div("foo", "clear-both", "m-2", "rounded", id="baz"))
# <div clear-both m-2 rounded id="baz">foo</div>
```

- keyword argument with value None is ignored

```python
tag = div(None, "m-2", "rounded", id="baz", style=None) 
print(tag)  
# <div m-2 rounded id="baz" />
```

- append content and attributes to existing tag

```python
tag = div()
tag.affix(p("bar"), "m-2", "rounded", id="baz") 
print(tag)  
# <div m-2 rounded id="baz"><p>bar</p></div>
```

- create custom element
- signature:
    - `Tag(name: str, content = None, *args, **kwargs) -> str`

```python
my_tag = Tag("MyTag", "foo", "bar", "corge", id="baz", class_="qux")
print(my_tag)  
# <MyTag bar corge id="baz" class="qux">foo</MyTag>
```

- more examples could be found in [tests] package

## Limitations

- `prettify()` method doesn't support attribute without value
    - use kwargs instead of positional args if prettifying is needed
    - eg. `selected` -> `selected=""`

## Need Help?

- [github issue]
- [x.com posts]
- [contact the author]

[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black
[ci-badge]: https://github.com/hoishing/ptag/actions/workflows/ci.yml/badge.svg
[ci-url]: https://github.com/hoishing/ptag/actions/workflows/ci.yml
[contact the author]: https://hoishing.github.io
[github issue]: https://github.com/hoishing/ptag/issues
[MIT-badge]: https://img.shields.io/github/license/hoishing/ptag
[MIT-url]: https://opensource.org/licenses/MIT
[pypi-badge]: https://img.shields.io/pypi/v/ptag
[pypi-url]: https://pypi.org/project/ptag/
[tests]: https://github.com/hoishing/ptag/tree/main/tests
[UnoCSS]: https://github.com/unocss/unocss
[x.com posts]: https://x.com/hoishing
