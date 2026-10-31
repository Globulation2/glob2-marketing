import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree as ET

SPEC = importlib.util.spec_from_file_location('storefront', Path(__file__).parents[1] / 'tools' / 'storefront.py')
S = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(S)


class StorefrontTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.fields = {'product_name': 'Globulation 2', 'headline': 'Build & grow <safely>', 'appstream_summary': 'Grow a colony', 'screenshot_caption_colony': 'Colony & food', 'screenshot_caption_battle': 'Battle', 'screenshot_caption_strategic': 'Map', 'screenshot_caption_terrain': 'Terrain'}
        self.fields['headline'] = 'Build & grow'
        for code in S.CODES: self.write(code, self.fields)
        (self.root / 'source-hashes.json').write_text(json.dumps(S.source_hashes(self.fields)))
        (self.root / 'reviews').mkdir()
        for code in S.CODES:
            if code != 'en': self.review(code)
        self.config = {'platforms': {'example': {'locales': {'en': 'en-US', 'zh-Hant': 'zh-TW'}, 'fields': {'summary': {'paragraphs': [['headline']], 'limit': 80}}}}, 'description_paragraphs': [['headline']], 'upstream_locales': {c: c for c in S.CODES}}
        self.config['upstream_locales'].update({'zh-Hant': 'zh_TW', 'zh-Hans': 'zh_CN', 'sr-Cyrl': 'sr'})
        (self.root / 'platforms.json').write_text(json.dumps(self.config))

    def write(self, code, fields):
        (self.root / f'{code}.md').write_text('# Translation\n' + ''.join(f'\n## {k}\n\n{v}\n' for k,v in fields.items()))

    def review(self, code):
        fields = S.read_fields(self.root / f'{code}.md')
        (self.root / 'reviews' / f'{code}.json').write_text(json.dumps({'status': 'reviewed', 'issues': [], 'translator': 'translator', 'reviewer': 'reviewer', 'source_hashes': S.source_hashes(self.fields), 'translation_hashes': S.source_hashes(fields)}))

    def test_complete_and_independent_review(self):
        self.assertEqual([], S.validate(self.root, True)[0])
        (self.root / 'reviews' / 'fr.json').unlink()
        self.assertIn('fr: independent review missing', S.validate(self.root, True)[0])

    def test_source_and_translation_staleness_name_fields(self):
        hashes = S.source_hashes(self.fields); hashes['headline'] = 'changed'
        errors = S.check_review(self.root, 'fr', self.fields, hashes)
        self.assertTrue(any('source hashes stale' in e and 'headline' in e for e in errors))
        changed = dict(self.fields, headline='Change')
        self.assertTrue(any('translation hashes stale' in e and 'headline' in e for e in S.check_review(self.root, 'fr', changed, S.source_hashes(self.fields))))

    def test_incomplete_and_duplicate_rejected(self):
        self.write('fr', {'product_name': 'Globulation 2'})
        self.assertTrue(any('fr: missing' in e for e in S.validate(self.root)[0]))
        with (self.root / 'fr.md').open('a') as f: f.write('\n## product_name\n\nDuplicate\n')
        self.assertRaises(ValueError, S.read_fields, self.root / 'fr.md')

    def test_missing_all_urls_detected(self):
        self.fields['legal'] = 'Policy: https://glob2.online/privacy/ .'
        for code in S.CODES: self.write(code, self.fields)
        changed = dict(self.fields, legal='Policy omitted')
        self.write('fr', changed)
        self.assertTrue(any('fr/legal: invalid NUL or changed URL' in e for e in S.validate(self.root)[0]))
        self.assertEqual(S.urls('https://glob2.online/privacy/。'), {'https://glob2.online/privacy/'})

    def test_limit_no_truncation(self):
        platform = {'fields': {'summary': {'paragraphs': [['headline']], 'limit': 2}}}
        payload, errors = S.platform_payload(self.fields, platform)
        self.assertEqual('Build & grow', payload['summary'])
        self.assertTrue(errors)

    def test_export_mapping_xml_safety_and_preparation_status(self):
        out = self.root / 'out'
        S.export(self.root, out)
        payload = json.loads((out / 'example' / 'zh-TW' / 'listing.json').read_text())
        self.assertEqual('zh-Hant', payload['canonical_locale'])
        self.assertFalse(payload['upload_eligible'])
        self.assertEqual(S.source_hashes(self.fields), payload['source_hashes'])
        xml = ET.parse(out / 'appstream-fragment.xml')
        self.assertEqual('Grow a colony', xml.find('summary').text)
        self.assertEqual('Build & grow', xml.find('description/p').text)
        self.assertIn('Comment[zh_TW]=', (out / 'desktop-fragment.ini').read_text())
        self.assertTrue(any(i['locale'] == 'eo' for i in json.loads((out / 'unsupported.json').read_text())))


if __name__ == '__main__': unittest.main()
