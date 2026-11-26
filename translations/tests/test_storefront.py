import importlib.util
import json
from pathlib import Path
import re
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
        self.fields = {'product_name': 'Globulation 2', 'headline': 'Build & grow', 'appstream_summary': 'Grow a colony', 'shot_caption_hero': 'Colony & food', 'shot_caption_battle': 'Battle'}
        for code in S.CODES: self.write(code, self.fields)
        (self.root / 'source-hashes.json').write_text(json.dumps(S.source_hashes(self.fields)))
        (self.root / 'reviews').mkdir()
        for code in S.CODES:
            if code != 'en': self.review(code)
        self.config = {'platforms': {'example': {'locales': {'en': 'en-US', 'zh-Hant': 'zh-TW'}, 'fields': {'summary': {'paragraphs': [['headline']], 'limit': 80}}}},
                       'appstream': {'summary_field': 'appstream_summary', 'comment_field': 'appstream_summary', 'description_paragraphs': [['headline']],
                                     'screenshot_captions': {'hero': 'shot_caption_hero', 'battle': 'shot_caption_battle'}},
                       'upstream_locales': {c: c for c in S.CODES}}
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

    def test_multibyte_byte_limit_and_character_default(self):
        fields = dict(self.fields, headline='戦略')  # Two characters, six UTF-8 bytes.
        spec = {'paragraphs': [['headline']], 'limit': 2}
        self.assertEqual([], S.platform_payload(fields, {'fields': {'keywords': spec}})[1])
        spec['length_unit'] = 'byte'
        payload, errors = S.platform_payload(fields, {'fields': {'keywords': spec}})
        self.assertEqual('戦略', payload['keywords'])
        self.assertIn('6 UTF-8 bytes exceeds 2', errors[0])
        spec['limit'] = 6
        self.assertEqual([], S.platform_payload(fields, {'fields': {'keywords': spec}})[1])
        spec['length_unit'] = 'character'
        spec['limit'] = 2
        self.assertEqual([], S.platform_payload(fields, {'fields': {'keywords': spec}})[1])

    def test_unknown_length_unit_rejected(self):
        platform = {'fields': {'summary': {'paragraphs': [['headline']], 'length_unit': 'bytes'}}}
        self.assertRaisesRegex(ValueError, 'unsupported length_unit', S.platform_payload, self.fields, platform)

    def test_check_and_export_both_reject_oversize_destination_bytes(self):
        spec = self.config['platforms']['example']['fields']['summary']
        spec.update(limit=1, length_unit='byte')
        (self.root / 'platforms.json').write_text(json.dumps(self.config))
        errors, _ = S.validate(self.root, True)
        self.assertTrue(any('example/zh-Hant' in e and 'UTF-8 bytes' in e for e in errors))
        out = self.root / 'blocked'
        self.assertRaisesRegex(ValueError, 'UTF-8 bytes', S.export, self.root, out)
        self.assertFalse(out.exists())

    def test_refuses_nonempty_export_to_prevent_stale_locales(self):
        out = self.root / 'out'
        out.mkdir()
        (out / 'stale.json').write_text('preserve')
        self.assertRaisesRegex(ValueError, 'must be empty', S.export, self.root, out)
        self.assertEqual('preserve', (out / 'stale.json').read_text())

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
        self.assertEqual(['hero', 'battle'], [item.get('source_role') for item in xml.findall('screenshots/caption')[:2]])
        self.assertEqual('Colony & food', xml.find('screenshots/caption').text)
        self.assertIn('Comment[zh_TW]=Grow a colony', (out / 'desktop-fragment.ini').read_text())
        self.assertTrue(any(i['locale'] == 'eo' for i in json.loads((out / 'unsupported.json').read_text())))

    def save_config(self):
        (self.root / 'platforms.json').write_text(json.dumps(self.config))

    def test_bullets_inline_lines_and_switches(self):
        fields = {'h': 'Heading.', 'a': 'One.', 'b': 'Two.', 'x': 'First item', 'y': 'Second item', 'agent': 'Agent section.'}
        spec = [['h', ['a', {'field': 'b', 'when': 'online'}]],
                {'lines': ['h'], 'bullets': ['x', {'field': 'y', 'unless': 'online'}]},
                {'when': 'agent', 'lines': ['agent']}]
        on = S.compose(fields, spec, {'online': True, 'agent': True})
        self.assertEqual('Heading.\nOne. Two.\n\nHeading.\n• First item\n\nAgent section.', on)
        off = S.compose(fields, spec, {'online': False, 'agent': False}, bullet_prefix='- ')
        self.assertEqual('Heading.\nOne.\n\nHeading.\n- First item\n- Second item', off)
        self.assertEqual({'h', 'a', 'b', 'x', 'y', 'agent'}, S.referenced(spec))
        self.assertEqual('句子。下一句。', S.join_inline(['句子。', '下一句。']))

    def test_switch_must_be_declared_and_shapes_are_checked(self):
        fields = {'a': 'One.'}
        self.assertRaisesRegex(ValueError, 'undeclared switch', S.compose, fields, [[{'field': 'a', 'when': 'typo'}]], {})
        self.assertRaisesRegex(ValueError, 'unsupported paragraph keys', S.compose, fields, [{'line': ['a']}], {})
        self.assertRaisesRegex(ValueError, 'unsupported field reference', S.compose, fields, [[{'fields': 'a'}]], {})
        self.assertRaises(KeyError, S.compose, fields, [['missing']], {})

    def test_platform_switches_prefix_and_fully_disabled_field(self):
        fields = dict(self.fields, agent='Agent caption', item='Item')
        platform = {'switches': {'agent': False}, 'bullet_prefix': '- ', 'fields': {
            'caption_8': {'paragraphs': [[{'field': 'agent', 'when': 'agent'}]], 'limit': 5},
            'short': {'paragraphs': [[{'field': 'agent', 'when': 'agent'}, {'field': 'headline', 'unless': 'agent'}]], 'limit': 80},
            'description': {'paragraphs': [{'bullets': ['item']}], 'limit': None}}}
        payload, errors = S.platform_payload(fields, platform)
        self.assertEqual({'short': 'Build & grow', 'description': '- Item'}, payload)
        self.assertEqual([], errors)
        platform['switches']['agent'] = True
        payload, errors = S.platform_payload(fields, platform)
        self.assertEqual('Agent caption', payload['short'])
        self.assertTrue(any('caption_8' in error for error in errors))

    def test_protected_terms_come_from_config_and_accept_local_numerals(self):
        self.fields['maps'] = '23 maps for Globulation 2 with MCP'
        for code in S.CODES: self.write(code, self.fields)
        self.config['protected_terms'] = ['Globulation 2', 'MCP', '23']
        self.config['platforms']['example']['fields']['maps'] = {'paragraphs': [['maps']], 'limit': None}
        self.save_config()
        self.write('fa', dict(self.fields, maps='۲۳ نقشه برای Globulation ۲ با MCP'))
        self.write('fr', dict(self.fields, maps='24 cartes pour Globulation 2 avec MCP'))
        self.write('de', dict(self.fields, maps='23 Karten für Globulation 2 mit dem Protokoll'))
        errors = S.validate(self.root)[0]
        self.assertIn('fr/maps: protected term 23 changed', errors)
        self.assertIn('de/maps: protected term MCP changed', errors)
        self.assertFalse(any(error.startswith('fa/') for error in errors))

    def test_field_limits_apply_to_every_locale(self):
        self.fields['shot_overlay_hero'] = 'Short'
        for code in S.CODES: self.write(code, self.fields)
        self.config['field_limits'] = [{'fields': 'shot_overlay_*', 'limit': 8}]
        self.config['asset_text'] = {'screenshot_roles': ['hero'], 'overlay_fields': 'shot_overlay_{role}'}
        self.save_config()
        self.write('eo', dict(self.fields, shot_overlay_hero='Multe tro longa'))
        errors = S.validate(self.root)[0]
        self.assertIn('eo/shot_overlay_hero: 15 characters exceeds 8; reviewed adaptation required', errors)
        self.assertFalse(any(error.startswith('en/') for error in errors))

    def test_field_limits_follow_script_groups_with_a_default(self):
        self.fields.update(shot_overlay_hero='Short', trailer_line_1='Short')
        for code in S.CODES: self.write(code, self.fields)
        self.config['field_limits'] = [
            {'fields': 'shot_overlay_*', 'limit': 28, 'script_groups': {
                'japanese': {'limit': 20, 'target': 18, 'locales': ['ja']},
                'devanagari': {'limit': 48, 'target': 40, 'locales': ['hi', 'mr']}}},
            {'fields': 'trailer_line_*', 'limit': 44}]
        self.config['asset_text'] = {'screenshot_roles': ['hero'], 'overlay_fields': 'shot_overlay_{role}', 'trailer_lines': ['trailer_line_1']}
        self.save_config()
        self.write('ja', dict(self.fields, shot_overlay_hero='あ' * 21))  # Over the Japanese ceiling, under the default.
        self.write('hi', dict(self.fields, shot_overlay_hero='क' * 45))  # Over the default, under the Devanagari ceiling.
        self.write('mr', dict(self.fields, shot_overlay_hero='क' * 49))
        self.write('fr', dict(self.fields, shot_overlay_hero='a' * 29))  # In no group: the default binds.
        self.write('de', dict(self.fields, shot_overlay_hero='a' * 28, trailer_line_1='a' * 44))
        self.write('ko', dict(self.fields, trailer_line_1='가' * 45))  # A rule without groups binds every locale alike.
        errors = [error for error in S.validate(self.root)[0] if 'exceeds' in error]
        self.assertEqual(['fr/shot_overlay_hero: 29 characters exceeds 28; reviewed adaptation required',
                          'ja/shot_overlay_hero: 21 characters exceeds 20; reviewed adaptation required',
                          'ko/trailer_line_1: 45 characters exceeds 44; reviewed adaptation required',
                          'mr/shot_overlay_hero: 49 characters exceeds 48; reviewed adaptation required'], sorted(errors))
        rule = self.config['field_limits'][0]
        self.assertEqual([20, 48, 28], [S.field_limit(rule, code) for code in ('ja', 'hi', 'xx')])
        # A code outside the roster (the renderer's test strings, a locale not yet assigned) gets the default.
        self.assertEqual([], S.field_limit_errors(self.config, 'xx', {'shot_overlay_hero': 'a' * 28}))
        self.assertEqual(['xx/shot_overlay_hero: 29 characters exceeds 28; reviewed adaptation required'],
                         S.field_limit_errors(self.config, 'xx', {'shot_overlay_hero': 'a' * 29}))
        rule['script_groups']['kana'] = {'limit': 18, 'locales': ['ja']}
        self.assertRaisesRegex(ValueError, 'more than one script group', S.field_limit, rule, 'ja')

    def test_locale_override_replaces_paragraphs_and_limit_for_that_locale_only(self):
        fields = dict(self.fields, extra='Extra paragraph')
        platform = {'locales': {'en': 'en-US', 'ja': 'Japanese'}, 'fields': {'description': {
            'paragraphs': [['headline'], ['extra']], 'limit': 100,
            'locale_overrides': {'ja': {'paragraphs': [['headline']], 'limit': 12}}}}}
        self.assertEqual('Build & grow\n\nExtra paragraph', S.platform_payload(fields, platform, 'en')[0]['description'])
        self.assertEqual('Build & grow\n\nExtra paragraph', S.platform_payload(fields, platform)[0]['description'])
        self.assertEqual(({'description': 'Build & grow'}, []), S.platform_payload(fields, platform, 'ja'))
        platform['fields']['description']['locale_overrides']['ja']['limit'] = 11
        self.assertEqual(['description: 12 characters exceeds 11; reviewed adaptation required'], S.platform_payload(fields, platform, 'ja')[1])
        self.assertEqual([], S.platform_payload(fields, platform, 'en')[1])  # The override's limit does not bind other locales.
        platform['fields']['description']['locale_overrides'] = {'ja': {'limit': 5}}  # A limit alone keeps the paragraphs.
        self.assertEqual(['description: 29 characters exceeds 5; reviewed adaptation required'], S.platform_payload(fields, platform, 'ja')[1])
        platform['fields']['description']['locale_overrides'] = {'ja': {'lines': [['headline']]}}
        self.assertRaisesRegex(ValueError, 'may set only', S.platform_payload, fields, platform, 'en')
        platform['fields']['description']['locale_overrides'] = {'ko': {'limit': 5}}
        self.assertRaisesRegex(ValueError, "'ko', which the platform does not map", S.platform_payload, fields, platform, 'en')

    def test_check_and_export_apply_locale_overrides(self):
        spec = self.config['platforms']['example']['fields']['summary']
        spec['locale_overrides'] = {'zh-Hant': {'limit': 5}}
        self.save_config()
        errors = S.validate(self.root, True)[0]
        self.assertEqual(['example/zh-Hant: summary: 12 characters exceeds 5; reviewed adaptation required'], errors)
        self.assertRaisesRegex(ValueError, 'exceeds 5', S.export, self.root, self.root / 'blocked')
        spec['locale_overrides'] = {'zh-Hant': {'paragraphs': [['product_name']]}}
        self.save_config()
        out = self.root / 'out'
        S.export(self.root, out)
        self.assertEqual('Globulation 2', json.loads((out / 'example' / 'zh-TW' / 'listing.json').read_text())['fields']['summary'])
        self.assertEqual('Build & grow', json.loads((out / 'example' / 'en-US' / 'listing.json').read_text())['fields']['summary'])

    def test_override_fields_count_as_used_and_must_exist(self):
        self.config['platforms']['example']['fields']['summary']['locale_overrides'] = {'zh-Hant': {'paragraphs': [['not_in_catalog']]}}
        self.save_config()
        self.assertIn('not_in_catalog', S.config_fields(self.config))
        self.assertTrue(any('missing from en.md' in e and 'not_in_catalog' in e for e in S.validate_source(self.root)[0]))

    def test_missing_destination_field_is_reported_not_raised(self):
        self.config['platforms']['example']['fields']['summary']['paragraphs'] = [['headline', 'not_in_catalog']]
        self.save_config()
        self.assertTrue(any('missing from en.md' in e and 'not_in_catalog' in e for e in S.validate(self.root)[0]))
        self.assertTrue(any('missing from en.md' in e for e in S.validate_source(self.root)[0]))

    def test_source_check_ignores_stale_locales_but_review_gate_does_not(self):
        """An English edit can be checked alone; the strict gate still rejects every stale locale."""
        changed = dict(self.fields, headline='A new English line', new_field='New')
        self.write('en', changed)
        self.config['platforms']['example']['fields']['extra'] = {'paragraphs': [['new_field']], 'limit': 3}
        self.save_config()
        self.assertEqual([], S.validate_source(self.root)[0])
        errors = S.validate(self.root, True)[0]
        self.assertTrue(any('source-hashes.json missing or stale' in e for e in errors))
        self.assertTrue(any(e.startswith('fr: missing') for e in errors))
        self.assertRaises(ValueError, S.export, self.root, self.root / 'blocked')
        self.write('en', dict(changed, new_field='Too long'))
        self.assertTrue(any('example/en: extra' in e for e in S.validate_source(self.root)[0]))
        self.write('en', dict(changed, orphan='Unused'))
        self.assertTrue(any('no destination uses' in e and 'orphan' in e for e in S.validate_source(self.root)[0]))

    def test_appstream_lists_and_switches(self):
        self.fields.update(features='Included.', one='A map editor', two='Replays', agent='Agent.')
        for code in S.CODES: self.write(code, self.fields)
        (self.root / 'source-hashes.json').write_text(json.dumps(S.source_hashes(self.fields)))
        for code in S.CODES:
            if code != 'en': self.review(code)
        self.config['appstream'].update(switches={'agent': False}, description_paragraphs=[
            ['headline'], {'lines': ['features'], 'bullets': ['one', 'two']}, {'when': 'agent', 'lines': ['agent']}])
        self.save_config()
        out = self.root / 'out'
        S.export(self.root, out)
        description = ET.parse(out / 'appstream-fragment.xml').find('description')
        self.assertEqual(1, len(description.findall('ul')))
        self.assertEqual(2 * len(S.CODES), len(description.findall('ul/li')))
        self.assertNotIn('Agent.', [item.text for item in description.findall('p')])
        english = [item.text for item in description.findall('p') if not item.attrib]
        self.assertEqual(['Build & grow', 'Included.'], english)


class EnglishSourceTests(unittest.TestCase):
    """Guards on the real English source and platform matrix; locale catalogs, hashes and reviews are not read."""

    MOBILE = ('google-play', 'ios', 'amazon', 'fastlane')
    ACRONYMS = {'RTS', 'MCP', 'AI', 'LAN', 'GPL'}

    @classmethod
    def setUpClass(cls):
        cls.fields = S.read_fields(S.ROOT / 'en.md')
        cls.config = json.loads((S.ROOT / 'platforms.json').read_text())
        cls.payloads = {name: S.platform_payload(cls.fields, platform)[0] for name, platform in cls.config['platforms'].items()}

    def text(self, platform):
        return '\n'.join(self.payloads[platform].values())

    def test_source_composes_within_every_limit(self):
        self.assertEqual([], S.validate_source(S.ROOT)[0])

    def test_fair_deal_is_the_second_line_of_every_description(self):
        for name, payload in self.payloads.items():
            description = payload.get('description') or payload['full_description']
            self.assertEqual([self.fields['headline'], self.fields['fair_deal_line']], description.split('\n')[:2], name)

    def test_no_banned_claims_anywhere(self):
        banned = r'\b(campaigns?|first|forever|never|nothing is sold|hive mind|skins?|credits?|studios?|best|#1|top-rated|award|download now|play now)\b'
        for key, value in self.fields.items():
            self.assertIsNone(re.search(banned, value, re.I), f'{key}: {value}')
            words = set(re.findall(r'\b[A-Z]{2,}\b', re.sub(r'https?://\S+', '', value)))
            self.assertFalse(words - self.ACRONYMS, f'{key}: all-caps words {words - self.ACRONYMS}')
            self.assertTrue(value.isascii() or key == 'product_name', f'{key}: non-ASCII character (emoji or symbol)')

    def test_image_and_trailer_text_is_short_and_carries_no_price_words(self):
        assets = self.config['asset_text']
        overlays = [assets['overlay_fields'].format(role=role) for role in assets['screenshot_roles']]
        for key in overlays + assets['trailer_lines'] + assets['trailer_desktop_only_lines'] + [assets['trailer_title']]:
            self.assertIsNone(re.search(r'\b(free|price|sale|discount|paid|buy)\b|[$€£]', self.fields[key], re.I), key)
        for key in overlays:
            self.assertTrue(2 <= len(self.fields[key].split()) <= 5, key)
        # Length is whatever field_limits says for English (the Latin ceiling), the same rule the renderer applies.
        self.assertEqual([], S.field_limit_errors(self.config, 'en', self.fields))
        self.assertLessEqual(len(assets['trailer_lines']) + len(assets['trailer_desktop_only_lines']), 5)

    def rule(self, pattern):
        return next(rule for rule in self.config['field_limits'] if rule['fields'] == pattern)

    def test_overlay_limits_follow_the_measured_script_ceilings(self):
        """Ceilings from assets/storefront/tools/README.md, "How long a caption can be" (measured 2026-11-24)."""
        rule = self.rule('shot_overlay_*')
        groups = rule['script_groups']
        assigned = [code for group in groups.values() for code in group['locales']]
        self.assertEqual(sorted(self.config['locales']), sorted(assigned), 'every locale is in exactly one script group')
        self.assertEqual(sorted(S.CODES), sorted(assigned))
        self.assertEqual({'latin': (40, 32), 'cyrillic_greek': (36, 28), 'chinese': (24, 20), 'japanese': (20, 18), 'korean': (32, 22),
                          'devanagari': (48, 40), 'bengali': (46, 36), 'telugu': (50, 32), 'tamil': (32, 24), 'arabic_persian': (48, 40),
                          'urdu': (28, 28), 'thai': (28, 28)},
                         {name: (group['limit'], group['target']) for name, group in groups.items()})
        self.assertEqual(20, groups['thai']['target_without_break'])
        expected = {'en': 40, 'de': 40, 'vi': 40, 'sw': 40, 'ru': 36, 'sr-Cyrl': 36, 'el': 36, 'zh-Hans': 24, 'zh-Hant': 24, 'ja': 20, 'ko': 32,
                    'hi': 48, 'mr': 48, 'bn': 46, 'te': 50, 'ta': 32, 'ar': 48, 'fa': 48, 'ur': 28, 'th': 28, 'not-a-locale': 28}
        self.assertEqual(expected, {code: S.field_limit(rule, code) for code in expected})
        for code, limit in expected.items():
            self.assertEqual([], S.field_limit_errors(self.config, code, {'shot_overlay_hero': '字' * limit}), code)
            self.assertEqual([f'{code}/shot_overlay_hero: {limit + 1} characters exceeds {limit}; reviewed adaptation required'],
                             S.field_limit_errors(self.config, code, {'shot_overlay_hero': '字' * (limit + 1)}))
        self.assertTrue(S.field_limit_errors(self.config, 'zh-Hans', {'shot_overlay_maps': '图' * 25}))
        self.assertEqual([], S.field_limit_errors(self.config, 'hi', {'shot_overlay_maps': 'क' * 45}))

    def test_trailer_and_caption_limits_are_the_same_in_every_locale(self):
        for pattern, limit in (('trailer_line_*', 44), ('trailer_title', 50), ('shot_caption_*', 100)):
            rule = self.rule(pattern)
            self.assertNotIn('script_groups', rule, pattern)
            self.assertEqual({limit}, {S.field_limit(rule, code) for code in S.CODES + ['not-a-locale']}, pattern)

    def test_gallery_orders_cover_the_roles_and_match_the_desktop_caption_numbering(self):
        assets = self.config['asset_text']
        mobile, desktop = assets['mobile_gallery_order'], assets['desktop_gallery_order']
        # App Store search results show the first three portrait screenshots, so the fair deal is third.
        self.assertEqual(['hero', 'battle', 'fair_deal', 'build', 'economy', 'territory', 'maps'], mobile)
        self.assertEqual(['hero', 'battle', 'build', 'ai_coplay', 'maps', 'territory', 'economy'], desktop)
        # 'opponents' keeps its translated caption fields but is no longer shown in any gallery (round-2 review, 2026-11-24).
        self.assertEqual(set(assets['screenshot_roles']) - {'opponents'}, set(mobile) | set(desktop))
        self.assertFalse(set(mobile) & set(assets['desktop_only_roles']))
        self.assertNotIn('fair_deal', desktop)
        # Microsoft's DesktopScreenshotCaptionN rows and the AppStream caption list are numbered in the desktop order.
        captions = [assets['caption_fields'].format(role=role) for role in desktop]
        microsoft = self.config['platforms']['microsoft']['fields']
        numbered = sorted((int(key.rsplit('_', 1)[1]), spec) for key, spec in microsoft.items() if key.startswith('desktop_screenshot_caption_'))
        self.assertEqual(captions, [next(iter(S.referenced(spec['paragraphs']))) for _, spec in numbered])
        self.assertEqual(desktop, list(self.config['appstream']['screenshot_captions']))
        self.assertEqual(captions, list(self.config['appstream']['screenshot_captions'].values()))

    def test_android_title_is_the_title_on_google_play_and_amazon_only(self):
        """User request of 2026-11-26: Play and Amazon titles become "Globulation 2 - Offline RTS"; every other store keeps the name."""
        self.assertEqual('Globulation 2 - Offline RTS', self.fields['android_title'])
        android = {('google-play', 'title'), ('amazon', 'title')}
        for name, platform in self.config['platforms'].items():
            for field, spec in platform['fields'].items():
                self.assertEqual((name, field) in android, 'android_title' in S.referenced(spec['paragraphs']), f'{name}/{field}')
        for name, field in android: self.assertEqual(self.fields['android_title'], self.payloads[name][field], name)
        for name, field in (('ios', 'name'), ('mac', 'name'), ('microsoft', 'title'), ('epic', 'title'), ('fastlane', 'title'),
                            ('itch', 'title'), ('steam', 'title'), ('gog', 'title')):
            self.assertEqual(self.fields['product_name'], self.payloads[name][field], name)
        self.assertEqual({30}, {S.field_limit(self.rule('android_title'), code) for code in S.CODES + ['not-a-locale']})

    def test_short_store_fields_carry_no_price_words(self):
        for platform, names in {'google-play': ('title', 'short_description'), 'fastlane': ('title', 'short_description'),
                                'ios': ('name', 'subtitle', 'keywords'), 'mac': ('name', 'subtitle', 'keywords')}.items():
            for name in names:
                self.assertIsNone(re.search(r'\bfree\b', self.payloads[platform][name], re.I), f'{platform}/{name}')

    def test_mobile_listings_never_mention_agents_or_mcp(self):
        for platform in self.MOBILE:
            self.assertIsNone(re.search(r'MCP|AI agent|JavaScript', self.text(platform)), platform)
            self.assertNotIn('ai_coplay', self.config['platforms'][platform].get('switches', {}), platform)

    def test_apple_copy_names_no_other_platform_and_omits_held_claims(self):
        for platform in ('ios', 'mac'):
            text = self.text(platform)
            self.assertIsNone(re.search(r'Android|Windows|Linux|Google|Steam|Amazon|Epic|itch|Microsoft|browser|desktop', text, re.I), platform)
            self.assertIsNone(re.search(r'45 languages|JavaScript|tracking|analytics', text, re.I), platform)

    def test_amazon_edition_claims_no_online_play_and_at_most_five_bullets(self):
        text = self.text('amazon')
        self.assertIsNone(re.search(r'ranked|quick match|invite|guest|sign in|same online games', text, re.I))
        self.assertLessEqual(sum(1 for name in self.payloads['amazon'] if name.startswith('feature_')), 5)

    def test_held_switches_follow_the_claims_record(self):
        platforms = self.config['platforms']
        self.assertFalse(platforms['mac']['switches']['ai_coplay'])
        self.assertFalse(platforms['epic']['switches']['ai_coplay'])
        self.assertFalse(platforms['epic']['switches']['online_play'])
        self.assertFalse(platforms['microsoft']['switches']['online_play'])
        for platform in ('mac', 'epic'):
            self.assertNotIn('MCP', self.text(platform))
            enabled = dict(platforms[platform], switches=dict(platforms[platform]['switches'], ai_coplay=True))
            payload, errors = S.platform_payload(self.fields, enabled)
            self.assertIn(self.fields['ai_heading'], payload['description'])
            self.assertEqual([], errors)
        for platform in ('epic', 'microsoft'):
            self.assertNotIn(self.fields['multiplayer_online_body'], self.text(platform))
        self.assertIsNone(re.search(r'Steam|GOG|Microsoft Store|itch\.io|Snap|Google Play|App Store|Amazon', self.text('epic')))

    def test_microsoft_keys_are_contiguous_and_within_store_counts(self):
        keys = self.payloads['microsoft']
        for family, most in (('feature', 20), ('search_term', 7), ('desktop_screenshot_caption', 10), ('trailer_title', 15)):
            numbers = sorted(int(key.rsplit('_', 1)[1]) for key in keys if re.fullmatch(family + r'_\d+', key))
            self.assertEqual(list(range(1, len(numbers) + 1)), numbers, family)
            self.assertLessEqual(len(numbers), most, family)
        terms = [keys[key] for key in keys if key.startswith('search_term_')]
        self.assertLessEqual(len({word.lower() for term in terms for word in term.split()}), 21)


class AmazonJapaneseTests(unittest.TestCase):
    """The Amazon console caps the Japanese long description at 1,200 characters; Amazon-ja drops a body paragraph to fit."""

    @classmethod
    def setUpClass(cls):
        cls.config = json.loads((S.ROOT / 'platforms.json').read_text())
        cls.amazon = cls.config['platforms']['amazon']
        cls.spec = cls.amazon['fields']['description']

    def test_only_japanese_is_overridden_and_only_on_amazon(self):
        self.assertEqual({'ja'}, set(self.spec['locale_overrides']))
        self.assertEqual(4000, self.spec['limit'])
        self.assertEqual(1200, self.spec['locale_overrides']['ja']['limit'])
        for name, platform in self.config['platforms'].items():
            for field, spec in platform['fields'].items():
                if (name, field) != ('amazon', 'description'): self.assertNotIn('locale_overrides', spec, f'{name}/{field}')

    def test_japanese_keeps_the_essential_paragraphs_in_order(self):
        base, ja = self.spec['paragraphs'], self.spec['locale_overrides']['ja']['paragraphs']
        self.assertEqual([paragraph for paragraph in base if paragraph in ja], ja, 'a subset of the reviewed paragraphs, in the same order')
        for kept in (['headline', 'fair_deal_line'], ['control_heading', 'control_body'], ['open_source_heading', 'open_source_body'], ['amazon_tail']):
            self.assertIn(kept, ja)
        self.assertEqual([paragraph for paragraph in base if isinstance(paragraph, dict)], [paragraph for paragraph in ja if isinstance(paragraph, dict)])
        self.assertEqual([['map_heading', 'map_body']], [paragraph for paragraph in base if paragraph not in ja])

    def test_japanese_composes_within_1200_and_other_locales_are_unchanged(self):
        ja = S.read_fields(S.ROOT / 'ja.md')
        payload, errors = S.platform_payload(ja, self.amazon, 'ja')
        self.assertEqual([], errors)
        self.assertLessEqual(len(payload['description']), 1200)
        self.assertEqual([ja['headline'], ja['fair_deal_line']], payload['description'].split('\n')[:2])
        self.assertNotIn(ja['map_body'], payload['description'])
        full = S.compose(ja, self.spec['paragraphs'])
        self.assertGreater(len(full), 1200, 'the full composition is what the console rejects')
        self.assertEqual(['description: %d characters exceeds 1200; reviewed adaptation required' % len(full)],
                         S.platform_payload(ja, dict(self.amazon, fields={'description': dict(self.spec, locale_overrides={'ja': {'limit': 1200}})}), 'ja')[1])
        for code in self.amazon['locales']:
            if code == 'ja': continue
            fields = S.read_fields(S.ROOT / f'{code}.md')
            self.assertEqual(S.compose(fields, self.spec['paragraphs']), S.platform_payload(fields, self.amazon, code)[0]['description'], code)


if __name__ == '__main__': unittest.main()
