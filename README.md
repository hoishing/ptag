# ptag

[![ci-badge]][ci-url] [![pypi-badge]][pypi-url] [![MIT-badge]][MIT-url] [![black-badge]][black-url]

> pythonic way to create HTML/XML/SVG tags

- create tags in pure python
- use context manager for tag hierarchy
- no external dependencies
- read the [docs]

## Quick Start

Installation: `pip install ptag`

```python
from ptag import div, img, form, label, input_, del_
from ptag import Tag  # for creating custom element

# === html element ===
tag = div(img(src="url"), id="bar")
print(tag)  # <div id="bar"><img src="url"/></div>

# === custom element ===
my_tag = Tag("MyTag", child="foo", attr="bar")
print(my_tag)  # <MyTag attr="bar">foo</MyTag>

# == ⭐️ context manager ⭐️ ==
with form() as f:
    label("foo", for_="bar")  # python keyword 'for' -> 'for_'
    input_(None, name="bar", type="checkbox", value="baz")

print(f.pretty())
# <form>
#     <label for="bar">foo</label>
#     <input name="bar" type="checkbox" value="baz"/>
# </form>

# === add content and attributes to existing tag ===
# position args -> attribute w/o value
# python keyword 'class' -> 'class_'
tag = div(class_="foo") 
# python keyword 'del' -> 'del_'
tag.add(del_("bar"), "m-2", "rounded", id="baz") 
print(tag)  
# <div m-2 rounded class="foo" id="baz"><del>bar</del></div>
```

more examples could be found on [references] and [tests]

## Limitations

- add trailing underscore to work around python keywords and built-in object
    - tag attributes: `class_`, `for_`
    - tag object: `del_`, `input_`, `map_`, `object_`
- `prettify()` method doesn't support attribute without value
    - use kwargs instead of positional args if prettifying is needed
    - eg. `selected` -> `selected=""`

## Motivation

When working with HTML, instead of separating python and template files like this:

```html
<ul id="navigation">
    {% for item in navigation %}
    <li><a href="{{ item.href }}">{{ item.caption }}</a></li>
    {% endfor %}
</ul>
```

I prefer a pythonic approach like this:

```python
with ul(id="navigation") as nav:
    for item in navigation:
        li(a(item.caption, href=item.href))
```

It provides full intellisense, type checking, and all language supports from the text editor. A much better DX.

## Need Help?

[![git-logo] github issue][github issue]

[![x-logo] posts][x-post]

[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black
[ci-badge]: https://github.com/hoishing/ptag/actions/workflows/ci.yml/badge.svg
[ci-url]: https://github.com/hoishing/ptag/actions/workflows/ci.yml
[docs]: https://hoishing.github.io/ptag
[git-logo]: https://api.iconify.design/bi/github.svg?color=%236FD886&width=20
[github issue]: https://github.com/hoishing/ptag/issues
[MIT-badge]: https://img.shields.io/github/license/hoishing/ptag
[MIT-url]: https://opensource.org/licenses/MIT
[pypi-badge]: https://img.shields.io/pypi/v/ptag
[pypi-url]: https://pypi.org/project/ptag/
[references]: https://hoishing.github.io/ptag/references
[tests]: https://github.com/hoishing/ptag/tree/main/tests
[x-logo]: https://api.iconify.design/ri:twitter-x-fill.svg?width=20&color=DarkGray
[x-post]: https://x.com/hoishing
