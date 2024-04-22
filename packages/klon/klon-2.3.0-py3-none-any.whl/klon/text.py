#!/usr/bin/env python3

# standards
import re
from typing import List, no_type_check

# 3rd parties
import lxml.etree as ET


BLOCK_TAGS = frozenset([
    # This list taken from https://developer.mozilla.org/en-US/docs/Web/HTML/Block-level_elements
    'address', 'article', 'aside', 'blockquote', 'details', 'dialog', 'dd', 'div', 'dl', 'dt', 'fieldset', 'figcaption', 'figure',
    'figcaption', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'hgroup', 'hr', 'li', 'main', 'nav', 'ol', 'p',
    'pre', 'section', 'table', 'ul'
])


NON_CONTENT_TAGS = frozenset([
    'head', 'script', 'style', 'svg',
])


PREFORMATTED_TAGS = frozenset([
    # Inside these tags, newlines will be honoured (up to 2). Horizontal space is still squished, unlike in a browser. That could
    # be implemented but `extract_text` would become significantly more involved, and it didn't seem to be worth the complexity.
    'pre', 'textarea',
])


def extract_text(etree: ET._Element, *, multiline: bool = False) -> str:
    if isinstance(etree, ET._ElementUnicodeResult):
        return normalize_spaces(etree)

    # using a list rather than making _walk() a yielding generator makes it about 5% faster
    parts: List[str] = []
    _walk(etree, parts)
    text = ''.join(parts)

    if multiline:
        return re.sub(
            r'\s+',
            lambda m: '\n\n' if '\n\n' in m.group() else '\n' if '\n' in m.group() else ' ',
            text
        ).strip()
    else:
        return normalize_spaces(text)


@no_type_check  # until lxml-stubs improves
def _walk(node: ET._Element, parts: List[str], preformatted: bool = False) -> None:
    if node.tag in NON_CONTENT_TAGS or isinstance(node, ET._Comment):
        return

    if node.tag == 'br':
        parts.append('\n')
    elif node.tag in BLOCK_TAGS:
        parts.append('\n\n')

    if node.tag in PREFORMATTED_TAGS:
        preformatted = True

    if node.text:
        parts.append(node.text if preformatted else re.sub(r'\s+', ' ', node.text))
    for child in node:
        _walk(child, parts)

        if child.tag in BLOCK_TAGS:
            parts.append('\n\n')
        if child.tail:
            parts.append(child.tail if preformatted else re.sub(r'\s+', ' ', child.tail))


def extract_multiline_text(etree: ET._Element) -> str:
    return extract_text(etree, multiline=True)


def normalize_spaces(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()
