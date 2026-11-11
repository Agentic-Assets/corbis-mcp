import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'check_skills_sh_collection.py'
spec = importlib.util.spec_from_file_location('collection', SCRIPT)
collection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collection)
SOURCE = 'Agentic-Assets/corbis-mcp'
EXPECTED = {'citations', 'paper-review'}


def page(*slugs):
    links = ''.join(f'<a href="/agentic-assets/corbis-mcp/{s}">{s}</a>' for s in slugs)
    return f'<h1>agentic-assets<!-- -->/<!-- -->corbis-mcp</h1>{links}'


class CollectionTests(unittest.TestCase):
    def test_complete_and_partial_collection(self):
        state, visible, remaining = collection.classify(page('citations', 'paper-review'), SOURCE, EXPECTED)
        self.assertEqual((state, visible, remaining), ('visible', EXPECTED, set()))
        state, visible, remaining = collection.classify(page('citations'), SOURCE, EXPECTED)
        self.assertEqual((state, visible, remaining), ('pending', {'citations'}, {'paper-review'}))

    def test_soft_404_or_changed_page_is_unknown(self):
        for html in ('<h1>not found</h1>', page(), '<h1>agentic-assets/corbis-mcp</h1><a href="/other/repo/citations">citations</a>'):
            with self.subTest(html=html):
                self.assertEqual(collection.classify(html, SOURCE, EXPECTED)[0], 'unknown')

    def test_only_exact_source_skill_links_count(self):
        html = page('citations') + '<a href="/other/repo/paper-review">paper-review</a>'
        self.assertEqual(collection.classify(html, SOURCE, EXPECTED)[2], {'paper-review'})

    def test_http_error_or_redirect_is_unknown(self):
        class Opener:
            def open(self, req, timeout):
                raise HTTPError(req.full_url, 302, 'redirect', {}, None)
        self.assertEqual(collection.observe(SOURCE, EXPECTED, Opener())[0], 'unknown')

    def test_rate_limit_is_unknown(self):
        class Opener:
            def open(self, req, timeout):
                raise HTTPError(req.full_url, 429, 'limited', {}, None)
        self.assertEqual(collection.observe(SOURCE, EXPECTED, Opener())[0], 'unknown')

    def test_inventory_is_derived_and_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'skills' / 'citations').mkdir(parents=True)
            (root / 'skills' / 'citations' / 'SKILL.md').write_text('---\n')
            self.assertEqual(collection.inventory(root), {'citations'})
            (root / 'skills' / 'other').symlink_to(root / 'skills' / 'citations')
            with self.assertRaises(ValueError):
                collection.inventory(root)

    def test_source_validation(self):
        for source in ('../other', 'x/../y', 'x/y?secret=1', 'https://example.com/x'):
            with self.subTest(source=source), self.assertRaises(ValueError):
                collection.observe(source, EXPECTED)

    def test_retries_are_bounded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'skills' / 'citations').mkdir(parents=True)
            (root / 'skills' / 'citations' / 'SKILL.md').write_text('---\n')
            with patch.object(collection, 'observe', return_value=('unknown', set(), {'citations'})) as call, \
                    patch.object(collection.time, 'sleep') as sleep, \
                    patch('sys.argv', ['observer', '--source', SOURCE, '--root', str(root)]):
                self.assertEqual(collection.main(), 2)
                self.assertEqual(call.call_count, collection.ATTEMPTS)
                self.assertEqual(sleep.call_count, collection.ATTEMPTS - 1)

    def test_pending_is_not_reported_as_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'skills' / 'citations').mkdir(parents=True)
            (root / 'skills' / 'citations' / 'SKILL.md').write_text('---\n')
            with patch.object(collection, 'observe', return_value=('pending', set(), {'citations'})), \
                    patch.object(collection.time, 'sleep'), \
                    patch('sys.argv', ['observer', '--source', SOURCE, '--root', str(root)]):
                self.assertEqual(collection.main(), 1)


if __name__ == '__main__':
    unittest.main()
