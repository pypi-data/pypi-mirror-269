#!/usr/bin/env python3

# 3rd parties
import pytest

# klon
from klon import extract_text, parse_html_etree


@pytest.mark.parametrize(
    'html, expected_default, expected_multiline',
    [
        (
            '<p>This is a   <b>test!</b></p>   And it works.',
            'This is a test! And it works.',
            'This is a test!\n\nAnd it works.',
        ),
        (
            '<ul><li>one<li>two</ul>',
            'one two',
            'one\n\ntwo',
        ),
        (
            '''
              <p>One paragraph</p>
              <p>two paragraphs</p>
              three and<br>
              four
              <p>and five<br></p>
              and six and<br>
              <p>seven</p>
            ''',
            'One paragraph two paragraphs three and four and five and six and seven',
            'One paragraph\n\ntwo paragraphs\n\nthree and\nfour\n\nand five\n\nand six and\n\nseven',
        ),
        (
            '''
            <html>
              <head><title><Test</title></head>
              <body>
                <script> alert("Boo!") </script>
                <p>Dr Livingstone, I presume?</p>
              </body>
            </html>
            ''',
            'Dr Livingstone, I presume?',
            'Dr Livingstone, I presume?',
        ),
        (
            '<p>It was <!-- not --> a dark stormy night</p>',
            'It was a dark stormy night',
            'It was a dark stormy night',
        ),
        (
            '<p>It was <style> p { font-weight: bold; } </style> a dark stormy night</p>',
            'It was a dark stormy night',
            'It was a dark stormy night',
        ),
        (
            '<p>It was a <span id="root">dark stormy</span> night</p>',
            'dark stormy',
            'dark stormy',
        ),
        (
            '''
              <h1>A poem</h1>
              <pre>
This is a haiku

This verse
           is the longer one


\t  This one is shorter
</pre>
            ''',
            'A poem This is a haiku This verse is the longer one This one is shorter',
            # note that in the current implementation we honour newlines inside <pre> tags but horizontal space is lost
            'A poem\n\nThis is a haiku\n\nThis verse\nis the longer one\n\nThis one is shorter',
        ),
        (
            '<p>A single <textarea>preformatted</textarea> word</p>',
            'A single preformatted word',
            'A single preformatted word',
        ),
    ]
)
def test_extract_text(html, expected_default, expected_multiline):
    etree = parse_html_etree(html)
    roots = etree.xpath('//*[@id="root"]')
    if roots:
        etree, = roots
    assert repr(extract_text(etree)) == repr(expected_default)
    assert repr(extract_text(etree, multiline=True)) == repr(expected_multiline)
