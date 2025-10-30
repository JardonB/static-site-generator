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
        expected_result = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
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
        expected_result = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        self.assertEqual(html, expected_result)

    def test_quoteblock(self):
        md = """
>This
>is a
>quoteblock
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div><blockquote>This\nis a\nquoteblock</blockquote></div>"
        self.assertEqual(html, expected_result)
        
    def test_ul(self):
        md = """
- One
- Two
- Three
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div><ul><li>One</li><li>Two</li><li>Three</li></ul></div>"
        self.assertEqual(html, expected_result)
              
    def test_ul_inline_md(self):
        md = """
- One
- _Two_
- **Three**
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div><ul><li>One</li><li><i>Two</i></li><li><b>Three</b></li></ul></div>"
        self.assertEqual(html, expected_result)
        
    def test_ol(self):
        md = """
1. One
2. Two
3. Three
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div><ol><li>One</li><li>Two</li><li>Three</li></ol></div>"
        self.assertEqual(html, expected_result)
            
    def test_ol_inline_md(self):
        md = """
1. One
2. _Two_
3. **Three**
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div><ol><li>One</li><li><i>Two</i></li><li><b>Three</b></li></ol></div>"
        self.assertEqual(html, expected_result)

    def test_heading(self):
        md = """
# Heading
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div><h1>Heading</h1></div>"
        self.assertEqual(html, expected_result)

    def test_heading2(self):
        md = """
## Heading
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div><h2>Heading</h2></div>"
        self.assertEqual(html, expected_result)

    def test_heading3(self):
        md = """
### Heading
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div><h3>Heading</h3></div>"
        self.assertEqual(html, expected_result)

    def test_heading4(self):
        md = """
#### Heading
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div><h4>Heading</h4></div>"
        self.assertEqual(html, expected_result)

    def test_heading5(self):
        md = """
##### Heading
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div><h5>Heading</h5></div>"
        self.assertEqual(html, expected_result)

    def test_heading6(self):
        md = """
###### Heading
"""
        html = markdown_to_html_node(md).to_html()
        expected_result = "<div><h6>Heading</h6></div>"
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
        expected_result = "<div><h6>Heading</h6><blockquote>This is a <i>very</i>\ndeep quote</blockquote><h3>Heading</h3><pre><code>code\n</code></pre></div>"
        self.assertEqual(html, expected_result)