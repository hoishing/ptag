"""
Pre-generate HTML and SVG element to `ptag/elements.py`

We take pre-generating approach because `Pylance` cannot infer the type of partial functions dynamically,
failing attempts included:

- update local variable with `locals().update()`
- use `exec()` to create partial functions.
"""

from pathlib import Path
from functools import partial
from typing import TypeVar, Callable, ParamSpec, Concatenate, cast

P = ParamSpec("P")
T = TypeVar("T")


def typed_partial(cls: Callable[Concatenate[str, P], T], tag_name: str) -> Callable[P, T]:
    return cast(Callable[P, T], partial(cls, tag_name))


html_tags = """\
a abbr acronym address applet area article aside audio b base basefont bdi bdo big blockquote body br button \
canvas caption center cite code col colgroup data datalist dd del details dfn dialog dir div dl dt em embed \
fieldset figcaption figure font footer form frame frameset h1 h2 h3 h4 h5 h6 head header hgroup hr html \
i iframe img input ins kbd label legend li link main map mark menu meta meter nav noframes noscript \
object ol optgroup option output p param picture pre progress q rp rt ruby \
s samp script search section select small source span strike strong style sub summary sup svg \
table tbody td template textarea tfoot th thead time title tr track tt u ul var video wbr\
"""
"""source: https://www.w3schools.com/tags/"""


svg_tags = """\
a animate animateMotion animateTransform circle clipPath defs desc ellipse \
feBlend feColorMatrix feComponentTransfer feComposite feConvolveMatrix feDiffuseLighting feDisplacementMap \
feDistantLight feDropShadow feFlood feFuncA feFuncB feFuncG feFuncR feGaussianBlur feImage feMerge feMergeNode \
feMorphology feOffset fePointLight feSpecularLighting feSpotLight feTile feTurbulence filter foreignObject \
g image line linearGradient marker mask metadata mpath path pattern polygon polyline \
radialGradient rect script set stop style svg switch symbol text textPath title tspan use view\
"""
"""source: https://developer.mozilla.org/en-US/docs/Web/SVG/Element"""


all_tags = sorted(set((html_tags + svg_tags).split()))


def generate_elements():
    """generate and write HTML and SVG elements to `elements.py`"""
    with open("ptag/elements.py", "w") as f:
        f.write(f"from .tag import Tag\n")
        f.write(f"from .{Path(__file__).stem} import {typed_partial.__name__}\n\n")
        for tag in all_tags:
            # handle special cases, del is a keyword
            alias = tag + "_" if tag in ["del", "input", "map", "object"] else tag
            f.write(f"{alias} = {typed_partial.__name__}(Tag, '{tag}')\n")


if __name__ == "__main__":
    generate_elements()
