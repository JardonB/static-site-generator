import unittest
from markdown_to_html_node import markdown_to_html_node

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_result = "<div>\n<p>\nThis is <b>bolded</b> paragraph text in a p tag here\n</p>\n<p>\nThis is another paragraph with <i>italic</i> text and <code>code</code> here\n</p>\n</div>\n"
        self.assertEqual(html, expected_result)

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_result = "<div>\n<pre>\n<code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code>\n</pre>\n</div>\n"
        self.assertEqual(html, expected_result)

    def test_quoteblock(self):
        md = """
>This
>is a
>quoteblock
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div>\n<blockquote>\nThis\nis a\nquoteblock\n</blockquote>\n</div>\n"
        self.assertEqual(html, expected_result)
        
    def test_ul(self):
        md = """
- One
- Two
- Three
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div>\n<ul>\n<li>One</li>\n<li>Two</li>\n<li>Three</li>\n</ul>\n</div>\n"
        self.assertEqual(html, expected_result)
              
    def test_ul_inline_md(self):
        md = """
- One
- _Two_
- **Three**
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div>\n<ul>\n<li>One</li>\n<li><i>Two</i></li>\n<li><b>Three</b></li>\n</ul>\n</div>\n"
        self.assertEqual(html, expected_result)
        
    def test_ol(self):
        md = """
1. One
2. Two
3. Three
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div>\n<ol>\n<li>One</li>\n<li>Two</li>\n<li>Three</li>\n</ol>\n</div>\n"
        self.assertEqual(html, expected_result)
            
    def test_ol_inline_md(self):
        md = """
1. One
2. _Two_
3. **Three**
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div>\n<ol>\n<li>One</li>\n<li><i>Two</i></li>\n<li><b>Three</b></li>\n</ol>\n</div>\n"
        self.assertEqual(html, expected_result)

    def test_heading(self):
        md = """
# Heading
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div>\n<h1>Heading</h1>\n</div>\n"
        self.assertEqual(html, expected_result)

    def test_heading2(self):
        md = """
## Heading
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div>\n<h2>Heading</h2>\n</div>\n"
        self.assertEqual(html, expected_result)

    def test_heading3(self):
        md = """
### Heading
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div>\n<h3>Heading</h3>\n</div>\n"
        self.assertEqual(html, expected_result)

    def test_heading4(self):
        md = """
#### Heading
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div>\n<h4>Heading</h4>\n</div>\n"
        self.assertEqual(html, expected_result)

    def test_heading5(self):
        md = """
##### Heading
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div>\n<h5>Heading</h5>\n</div>\n"
        self.assertEqual(html, expected_result)

    def test_heading6(self):
        md = """
###### Heading
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div>\n<h6>Heading</h6>\n</div>\n"
        self.assertEqual(html, expected_result)

    def test_multi_type(self):
        md = """
###### Heading

> This is a _very_
> deep quote

### Heading

```
code
```
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div>\n<h6>Heading</h6>\n<blockquote>\nThis is a <i>very</i>\ndeep quote\n</blockquote>\n<h3>Heading</h3>\n<pre>\n<code>\ncode\n</code>\n</pre>\n</div>\n"
        self.assertEqual(html, expected_result)