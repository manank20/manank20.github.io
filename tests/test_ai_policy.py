"""Integration checks against a freshly built Zola site."""
import os
from pathlib import Path
import unittest
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = Path(os.environ.get("SITE_OUTPUT", ROOT / "public"))


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.stack = []
        self.policy_links = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and (attrs.get("href") or "").endswith("/ai-policy/"):
            self.policy_links.append(tuple(self.stack))
        if tag not in {"meta", "link", "img", "input", "br", "hr", "source", "wbr"}:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.stack:
            self.stack = self.stack[:len(self.stack) - 1 - self.stack[::-1].index(tag)]


class PolicyTests(unittest.TestCase):
    def test_global_and_post_links(self):
        pages = list(PUBLIC.rglob("*.html"))
        self.assertTrue(pages)
        for path in pages:
            # Zola's pagination aliases are redirect stubs, not site pages.
            if '<title>Redirect</title>' in path.read_text():
                continue
            with self.subTest(page=str(path.relative_to(PUBLIC))):
                links = Document(path).policy_links
                self.assertTrue(any("nav" in ancestors for ancestors in links))
                relative = path.relative_to(PUBLIC)
                if relative.parts[0] == "blog" and len(relative.parts) == 3:
                    self.assertTrue(any("article" in ancestors for ancestors in links))
                    self.assertTrue(any("aside" in ancestors for ancestors in links))

    def test_policy_page_exists(self):
        self.assertTrue((PUBLIC / "ai-policy/index.html").is_file())


if __name__ == "__main__":
    unittest.main()
