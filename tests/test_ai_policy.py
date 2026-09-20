"""Parent-site integration checks for the extracted DeepThought theme."""
from html.parser import HTMLParser
import re
import subprocess
from pathlib import Path
import os
import unittest

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = Path(os.environ.get("SITE_OUTPUT", ROOT / "public"))
MOVED_TEMPLATES = (
    "templates/base.html",
    "templates/index.html",
    "templates/page.html",
    "templates/policy.html",
    "templates/section.html",
    "templates/404.html",
    "templates/tags/list.html",
    "templates/tags/single.html",
    "templates/categories/list.html",
    "templates/categories/single.html",
)
MOVED_ASSETS = (
    "static/site.css",
    "static/js/site.js",
    "highlighting/github-dark-accessible.json",
)


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.stack = []
        self.policy_links = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and (attributes.get("href") or "").endswith("/ai-policy/"):
            self.policy_links.append(tuple(self.stack))
        if tag not in {"meta", "link", "img", "input", "br", "hr", "source", "wbr"}:
            self.stack.append((tag, attributes.get("class", "")))

    def handle_startendtag(self, tag, attrs):
        if tag == "a":
            attributes = dict(attrs)
            if (attributes.get("href") or "").endswith("/ai-policy/"):
                self.policy_links.append(tuple(self.stack))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                return


class ParentPolicyTests(unittest.TestCase):
    def test_policy_source_is_empty_and_unchanged(self):
        policy = (ROOT / "content/ai-policy.md").read_bytes()
        expected = b'+++\ntitle = "AI Policy"\ntemplate = "policy.html"\n+++'
        self.assertEqual(policy.rstrip(b"\n"), expected)
        baseline = subprocess.run(
            ["git", "show", "HEAD:content/ai-policy.md"],
            cwd=ROOT,
            text=False,
            capture_output=True,
            check=True,
        ).stdout
        self.assertEqual(policy, baseline)

    def test_parent_selects_theme_contract_and_has_no_duplicate_overrides(self):
        config = (ROOT / "config.toml").read_text(encoding="utf-8")
        self.assertIsNotNone(re.search(r'^theme\s*=\s*"DeepThought"', config, re.MULTILINE))
        self.assertIn('featured_page = "blog/goto-statement/index.md"', config)
        self.assertIn('[extra.policy]', config)
        self.assertIn('url = "$BASE_URL/ai-policy/"', config)
        self.assertIn('extra_themes = ["themes/DeepThought/highlighting/github-dark-accessible.json"]', config)
        self.assertTrue((ROOT / "themes/DeepThought").is_dir())
        for relative in MOVED_TEMPLATES + MOVED_ASSETS:
            self.assertFalse((ROOT / relative).exists(), f"parent still overrides {relative}")

    def test_rendered_site_contains_policy_links_and_empty_policy_page(self):
        self.assertTrue(PUBLIC.is_dir(), f"build output is missing: {PUBLIC}")
        pages = [path for path in PUBLIC.rglob("*.html") if "<title>Redirect</title>" not in path.read_text(encoding="utf-8")]
        self.assertTrue(pages, f"no rendered pages found in {PUBLIC}")
        for path in pages:
            with self.subTest(page=str(path.relative_to(PUBLIC))):
                document = Document(path.read_text(encoding="utf-8"))
                self.assertTrue(
                    any(ancestor[0] == "nav" for link in document.policy_links for ancestor in link),
                    "AI Policy is present in the global navigation",
                )
                relative = path.relative_to(PUBLIC)
                if relative.parts[:1] == ("blog",) and len(relative.parts) == 3:
                    self.assertTrue(
                        any(ancestor[0] == "article" for link in document.policy_links for ancestor in link),
                        "AI Policy is present in article metadata",
                    )
                    self.assertFalse(
                        any(ancestor[0] == "aside" for link in document.policy_links for ancestor in link),
                        "AI Policy must not appear in the article aside",
                    )
        policy_page = PUBLIC / "ai-policy/index.html"
        self.assertTrue(policy_page.is_file())
        policy_html = policy_page.read_text(encoding="utf-8")
        self.assertRegex(policy_html, r'<article class="prose">\s*</article>')


if __name__ == "__main__":
    unittest.main()
