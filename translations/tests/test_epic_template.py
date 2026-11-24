"""Synthetic templates exercise the Epic mapping, the update flags and the review gate.

Fixtures come from a synthetic matrix, or from the live platforms.json and en.md
addressed by field ID. No test depends on English wording or reads a live locale
catalog, source hash or review record.
"""
import contextlib
import copy
import csv
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import epic_template as epic

S = epic.storefront

PLATFORM = {
    'locales': {'en': 'en', 'fr': 'fr', 'de': 'de', 'el': 'el'},
    'switches': {'ai_coplay': False, 'online_play': False},
    'bullet_prefix': '- ',
    'fields': {
        'title': {'paragraphs': [['product_name']], 'limit': None},
        'short_description': {'paragraphs': [['short_pitch']], 'limit': None},
        'description': {'paragraphs': [
            ['headline', 'fair_deal_line'],
            ['listing_intro'],
            {'lines': ['features_heading'], 'bullets': ['feature_a', 'feature_b']},
            ['multiplayer_heading', [{'field': 'multiplayer_online_body', 'when': 'online_play'}, 'multiplayer_lan_body']],
            {'when': 'ai_coplay', 'lines': ['ai_heading', 'ai_body']},
            ['open_source_heading', 'open_source_body'],
            ['epic_tail']], 'limit': 10000},
        'legal': {'paragraphs': [['epic_legal']], 'limit': None}}}
SPECS = ['Store Configs', 'synthetic-config', 'Synthetic config', '',
         'technicalRequirements.windows.cpu.minimum', 'Technical Requirements', 'string', 'Existing specification']
LINK = ['Store Configs', 'synthetic-config', 'Synthetic config', '',
        'socialLinks.twitter', 'Social link', 'string', 'https://social.example/en']
FOOTER = ['#Note. Keep footer']


def catalog(code, platform=PLATFORM):
    """Every field the matrix references, with a value that names its locale and field."""
    names = set().union(*(S.referenced(spec['paragraphs']) for spec in platform['fields'].values()))
    return {name: 'Globulation 2' if name == 'product_name' else f'{code}:{name}' for name in sorted(names)}


def mapped_rows(platform, english, columns, saved=lambda key, column: ''):
    """One template row per canonical key: saved English plus saved(key, column) in each locale column."""
    values, names, count = epic.canonical_rows('en', english, platform)
    return [[entity, f'synthetic {entity}', 'Synthetic product', '', field, names[entity, field],
             'markdown' if field.endswith('.body') else 'string', text]
            + [saved((entity, field), column) for column in columns]
            for (entity, field), text in values.items()]


def csv_text(header, rows):
    output = io.StringIO(newline='')
    csv.writer(output).writerows([header, *rows])
    return output.getvalue()


def about(number, part, entity='Offer'):
    return (entity, f'aboutItem.{number}.textBlock.{part}')


class EpicTemplateTests(unittest.TestCase):
    def setUp(self):
        self.platform = copy.deepcopy(PLATFORM)
        self.catalogs = {code: catalog(code) for code in ('en', 'fr', 'de')}
        self.columns = ['fr', 'de', 'es', 'bg']  # No canonical locale maps to es or bg here.
        self.header = epic.METADATA_COLUMNS + ['en'] + self.columns

    def rows(self, saved=lambda key, column: ''):
        return mapped_rows(self.platform, self.catalogs['en'], self.columns, saved)

    def config(self, row, *cells):
        return row + list(cells) + [''] * (len(self.columns) - len(cells))

    def adapt(self, rows, **options):
        text, report = epic.adapt(csv_text(self.header, rows), self.catalogs, self.platform, **options)
        return list(csv.reader(io.StringIO(text))), report

    def saved_listing(self):
        """Canonical English; French and German hold earlier translations except a current French title
        and a German About item created after the last import; config rows hold their own saved values."""
        def saved(key, column):
            if column not in ('fr', 'de'): return ''
            if column == 'fr' and key[1] in ('title', 'productDisplayName'): return 'Globulation 2'
            if column == 'de' and key[1].startswith('aboutItem.3.'): return ''
            return f'earlier {column} {key[1]}'
        return self.rows(saved) + [self.config(SPECS, 'Existing specification', 'Existing specification'),
                                   self.config(LINK, 'https://social.example/fr'), [], FOOTER]

    # Mapping read from the matrix.

    def test_rows_follow_the_matrix_composition(self):
        values, names, count = epic.canonical_rows('en', self.catalogs['en'], self.platform)
        self.assertEqual(4, count)
        self.assertEqual(5 + 2 * 2 * 4, len(values))
        for entity in epic.ABOUT_ENTITIES:
            self.assertEqual(['en:headline', 'en:features_heading', 'en:multiplayer_heading', 'en:open_source_heading'],
                             [values[about(number, 'headline', entity)] for number in range(4)])
            self.assertEqual(['en:fair_deal_line\n\nen:listing_intro', '- en:feature_a\n- en:feature_b',
                              'en:multiplayer_lan_body', 'en:open_source_body\n\nen:epic_tail'],
                             [values[about(number, 'body', entity)] for number in range(4)])
        self.assertEqual('Globulation 2', values['Offer', 'title'])
        self.assertEqual('Globulation 2', values['Store Configs', 'productDisplayName'])
        self.assertEqual('en:short_pitch', values['Offer', 'description'])
        self.assertEqual('en:short_pitch', values['Store Configs', 'shortDescription'])
        self.assertEqual('en:epic_legal', values['Store Configs', 'legalText'])
        self.assertEqual('about_item_2.body', names[about(1, 'body', 'Product Home')])

    def test_switches_decide_items_and_sentences(self):
        values = epic.canonical_rows('en', self.catalogs['en'], self.platform)[0]
        self.assertFalse([text for text in values.values() if 'ai_' in text or 'online' in text])
        self.platform['switches'] = {'ai_coplay': True, 'online_play': True}
        values, names, count = epic.canonical_rows('en', self.catalogs['en'], self.platform)
        self.assertEqual(5, count)
        self.assertEqual('en:multiplayer_online_body en:multiplayer_lan_body', values[about(2, 'body')])
        self.assertEqual(('en:ai_heading', 'en:ai_body'), (values[about(3, 'headline')], values[about(3, 'body')]))
        self.assertEqual('en:open_source_heading', values[about(4, 'headline', 'Product Home')])

    def test_item_saved_while_a_switch_was_on_stops_once_it_is_off(self):
        on = copy.deepcopy(self.platform)
        on['switches']['ai_coplay'] = True
        rows = mapped_rows(on, self.catalogs['en'], self.columns)
        with self.assertRaisesRegex(ValueError, 'canonical layout has 4 About items'):
            self.adapt(rows, update_existing=True, update_english=True)

    def test_matrix_shapes_the_adapter_cannot_place_stop(self):
        paragraphs = self.platform['fields']['description']['paragraphs']
        for change, message in [
                (lambda: paragraphs.insert(0, ['listing_intro']), 'must open with a heading field'),
                (lambda: paragraphs.append(['ai_heading']), 'About item 5 has a heading and no body'),
                (lambda: paragraphs.append([{'field': 'ai_heading', 'when': 'ai_coplay'}, 'ai_body']), 'heading ai_heading is switched off'),
                (lambda: self.platform['fields'].update(trailer_title={'paragraphs': [['short_pitch']]}), 'trailer_title.*extend FIELD_FAMILIES')]:
            self.platform = copy.deepcopy(PLATFORM)
            paragraphs = self.platform['fields']['description']['paragraphs']
            change()
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                epic.canonical_rows('en', self.catalogs['en'], self.platform)

    # Filling a template with empty locale columns.

    def test_fills_empty_locales_and_preserves_identity_english_and_specs(self):
        mapped = self.rows()
        rows, report = self.adapt(mapped + [self.config(SPECS), self.config(LINK), [], FOOTER])
        self.assertEqual(self.header[:10], rows[0])
        values = {code: epic.canonical_rows(code, self.catalogs[code], self.platform)[0] for code in ('fr', 'de')}
        for original, row in zip(mapped, rows[1:]):
            key = (original[0], original[4])
            self.assertEqual(original[:8] + [values['fr'][key], values['de'][key]], row)
        self.assertEqual(SPECS + ['Existing specification'] * 2, rows[22])
        self.assertEqual(LINK + ['', ''], rows[23])
        self.assertEqual([[], FOOTER], rows[24:])
        self.assertEqual(['es', 'bg'], report['removed_unused_locale_columns'])
        self.assertEqual(['el'], report['configured_locales_missing_from_template'])
        self.assertEqual((21, 4, 2, 42, 42), (report['mapped_rows'], report['about_items'], report['translated_locale_count'],
                                              report['translated_cells'], report['changed_cells']))
        self.assertEqual((2, 2), (report['english_fallback_cells'], report['english_fallback_cells_filled']))
        self.assertEqual((21, 0), (len(report['changed_fields']['de']['filled']), len(report['changed_fields']['de']['replaced'])))
        self.assertEqual({'status': 'matches canonical', 'changed': []}, report['english'])
        self.assertEqual([], report['warnings'])

    def test_roundtrips_commas_quotes_and_line_breaks_deterministically(self):
        self.catalogs['fr']['short_pitch'] = 'Texte, avec "guillemets"\net une ligne'
        template = csv_text(self.header, self.rows())
        first = epic.adapt(template, self.catalogs, self.platform)
        self.assertEqual(first, epic.adapt(template, self.catalogs, self.platform))
        row = next(row for row in csv.reader(io.StringIO(first[0])) if row[4] == 'shortDescription')
        self.assertEqual(self.catalogs['fr']['short_pitch'], row[8])

    # Updating a template whose locale columns already hold earlier translations.

    def test_refuses_differing_saved_translations_without_the_update_flag(self):
        with self.assertRaisesRegex(ValueError, r'36 existing translation\(s\) in 2 locale column\(s\) \(fr, de\).*reconcile before import, or rerun with --update-existing'):
            self.adapt(self.saved_listing())

    def test_update_replaces_only_mapped_cells(self):
        listing = self.saved_listing()
        rows, report = self.adapt(listing, update_existing=True)
        values = {code: epic.canonical_rows(code, self.catalogs[code], self.platform)[0] for code in ('fr', 'de')}
        for original, row in zip(listing[:21], rows[1:]):
            key = (original[0], original[4])
            self.assertEqual(original[:8] + [values['fr'][key], values['de'][key]], row)
        # Unmapped rows, separators and the footer keep every saved value.
        self.assertEqual([listing[21][:10], listing[22][:10], [], FOOTER], rows[22:])
        self.assertEqual('https://social.example/fr', rows[23][8])
        french, german = report['changed_fields']['fr'], report['changed_fields']['de']
        self.assertEqual((19, 0), (len(french['replaced']), len(french['filled'])))
        self.assertNotIn('Offer/title', french['replaced'])
        self.assertNotIn('title', french['fields'])
        self.assertEqual((17, 4), (len(german['replaced']), len(german['filled'])))
        self.assertEqual(['Offer/aboutItem.3.textBlock.headline', 'Offer/aboutItem.3.textBlock.body',
                          'Product Home/aboutItem.3.textBlock.headline', 'Product Home/aboutItem.3.textBlock.body'], german['filled'])
        self.assertEqual(['title', 'short_description', 'legal'] + [f'about_item_{number}.{part}' for number in range(1, 5) for part in epic.ABOUT_PARTS],
                         german['fields'])
        self.assertEqual(40, report['changed_cells'])
        self.assertEqual(0, report['english_fallback_cells_filled'])

    def test_summary_names_changed_fields_per_locale(self):
        text, report = epic.adapt(csv_text(self.header, self.saved_listing()), self.catalogs, self.platform, update_existing=True)
        lines = epic.summary(report)['changed_fields']
        self.assertEqual(['de', 'fr'], list(lines))
        self.assertEqual('19 replaced, 0 filled: short_description, legal, about_item_1-4', lines['fr'])
        self.assertEqual('17 replaced, 4 filled: title, short_description, legal, about_item_1-4', lines['de'])
        # The generated file is itself current: a second run changes nothing and needs no flag.
        again, report = epic.adapt(text, self.catalogs, self.platform)
        self.assertEqual(text, again)
        self.assertEqual(0, report['changed_cells'])
        self.assertEqual({'de': 'already current', 'fr': 'already current'}, epic.summary(report)['changed_fields'])
        self.assertEqual(['title', 'about_item_1', 'about_item_2.body', 'about_item_3-4', 'about_item_6.headline', 'legal'],
                         epic.compact(['title', 'about_item_1.headline', 'about_item_1.body', 'about_item_2.body', 'about_item_3.headline',
                                       'about_item_3.body', 'about_item_4.headline', 'about_item_4.body', 'about_item_6.headline', 'legal']))

    def test_english_drift_stops_unless_update_english(self):
        listing = self.rows()
        drifted = [row for row in listing if row[4] in ('shortDescription', 'aboutItem.0.textBlock.body')]
        for row in drifted: row[7] = 'Earlier English'
        with self.assertRaisesRegex(ValueError, r'English differs from canonical in 3 mapped row\(s\).*Offer/aboutItem.0.textBlock.body \(about_item_1.body\).*--update-english'):
            self.adapt(listing, update_existing=True)
        rows, report = self.adapt(listing + [self.config(LINK)], update_english=True)
        values = epic.canonical_rows('en', self.catalogs['en'], self.platform)[0]
        self.assertEqual([values[row[0], row[4]] for row in rows[1:22]], [row[7] for row in rows[1:22]])
        self.assertEqual('https://social.example/en', rows[22][7])
        self.assertEqual({'status': 'updated', 'changed': ['Offer/aboutItem.0.textBlock.body', 'Product Home/aboutItem.0.textBlock.body',
                                                           'Store Configs/shortDescription']}, dict(report['english'], changed=sorted(report['english']['changed'])))

    def test_each_flag_covers_only_its_own_difference(self):
        listing = self.saved_listing()
        listing[0][7] = 'Earlier English'
        with self.assertRaisesRegex(ValueError, '--update-english(.|\n)*--update-existing'):
            self.adapt(listing)
        with self.assertRaisesRegex(ValueError, '--update-existing'):
            self.adapt(listing, update_english=True)
        with self.assertRaisesRegex(ValueError, '--update-english'):
            self.adapt(listing, update_existing=True)
        self.adapt(listing, update_existing=True, update_english=True)

    def test_earlier_layout_with_fewer_about_items_stops_even_with_both_flags(self):
        listing = [row for row in self.saved_listing() if not (row and row[0] == 'Offer' and row[4].startswith(('aboutItem.2.', 'aboutItem.3.')))]
        with self.assertRaisesRegex(ValueError, r"Offer: template lacks About rows \['aboutItem.2.textBlock.headline'.*4-item canonical layout"):
            self.adapt(listing, update_existing=True, update_english=True)

    def test_template_without_an_entity_is_reported_not_guessed(self):
        listing = [row for row in self.rows() if row[0] == 'Store Configs']
        rows, report = self.adapt(listing)
        self.assertEqual(3, report['mapped_rows'])
        self.assertEqual(['Template has no row for canonical ' + ', '.join(f'about_item_{number}.{part}' for number in range(1, 5) for part in epic.ABOUT_PARTS)
                          + '; not part of this import'], report['warnings'])

    def test_list_in_a_plain_string_row_is_a_warning(self):
        listing = self.rows()
        for row in listing: row[6] = 'string'
        report = self.adapt(listing)[1]
        self.assertEqual(2, len(report['warnings']))
        self.assertIn('Offer/aboutItem.1.textBlock.body: the canonical value holds a list', report['warnings'][0])

    # Safety behaviour kept from the first adapter.

    def test_rejects_unknown_rows_duplicate_rows_and_unexpected_types(self):
        unknown = self.rows()[0]
        unknown[4] = 'newUnreviewedField'
        carousel = self.rows()[0]
        carousel[0], carousel[4] = 'Product Home', 'carousel.0.caption'
        typed = self.rows()
        typed[0][6] = 'image'
        for rows, message in [(self.rows() + [unknown], 'unknown source row Offer/newUnreviewedField'),
                              (self.rows() + [carousel], 'unknown source row Product Home/carousel.0.caption'),
                              (self.rows() + self.rows()[:1], 'duplicate entity/field row'),
                              (typed, 'unexpected mapped field type')]:
            for update in (False, True):
                with self.subTest(message=message, update=update), self.assertRaisesRegex(ValueError, message):
                    self.adapt(rows, update_existing=update, update_english=update)

    def test_rejects_removing_existing_unused_translation(self):
        listing = self.rows()
        listing[0][10] = 'Saved Spanish text'
        with self.assertRaisesRegex(ValueError, 'unused locale es has existing content'):
            self.adapt(listing, update_existing=True)

    def test_rejects_missing_invariant_source_and_conflicting_fallback(self):
        row = self.config(['Store Configs', 'synthetic-config', 'Synthetic config', '', 'developerDisplayName', 'Developer', 'string', ''])
        with self.assertRaisesRegex(ValueError, 'invariant English source is empty'):
            self.adapt([row])
        row[7], row[8] = 'Existing developer', 'Different developer'
        for update in (False, True):
            with self.subTest(update=update), self.assertRaisesRegex(ValueError, 'invariant differs'):
                self.adapt([row], update_existing=update)

    def test_stale_or_missing_catalog_is_refused(self):
        earlier = {key: value for key, value in self.catalogs['fr'].items() if key not in ('fair_deal_line', 'features_heading')}
        with self.assertRaisesRegex(ValueError, "fr: catalog lacks field '(fair_deal_line|features_heading)'"):
            epic.adapt(csv_text(self.header, self.rows()), dict(self.catalogs, fr=earlier), self.platform, update_existing=True)
        del self.catalogs['de']
        with self.assertRaisesRegex(ValueError, 'de: no canonical catalog'):
            self.adapt(self.rows())


class LiveMatrixTests(unittest.TestCase):
    """The live Epic entry and English master, addressed by field ID; locale catalogs are derived, never read."""

    def setUp(self):
        self.platform = json.loads((S.ROOT / 'platforms.json').read_text())['platforms']['epic']
        self.source = S.read_fields(S.ROOT / 'en.md')

    def layout(self, **switches):
        platform = dict(self.platform, switches=dict(self.platform.get('switches', {}), **switches))
        values, names, count = epic.canonical_rows('en', self.source, platform)
        return values, [(values[about(number, 'headline', 'Product Home')], values[about(number, 'body', 'Product Home')]) for number in range(count)]

    def test_switched_off_layout_matches_the_field_map(self):
        values, items = self.layout(ai_coplay=False, online_play=False)
        self.assertEqual([self.source[name] for name in ('headline', 'control_heading', 'economy_heading', 'map_heading', 'defense_heading',
                                                         'features_heading', 'multiplayer_heading', 'open_source_heading')],
                         [heading for heading, body in items])
        self.assertEqual(self.source['fair_deal_line'] + '\n\n' + self.source['listing_intro'], items[0][1])
        self.assertEqual(self.source['control_body'], items[1][1])
        self.assertTrue(all(line.startswith(self.platform['bullet_prefix']) for line in items[5][1].split('\n')))
        self.assertEqual(self.source['multiplayer_lan_body'], items[6][1])
        self.assertEqual(self.source['open_source_body'] + '\n\n' + self.source['epic_tail'], items[7][1])
        for held in ('ai_heading', 'ai_body', 'multiplayer_online_body', 'multiplayer_crossplay'):
            self.assertNotIn(self.source[held], '\n'.join(values.values()))
        self.assertEqual(self.source['product_name'], values['Offer', 'title'])
        self.assertEqual(self.source['short_pitch'], values['Store Configs', 'shortDescription'])
        self.assertEqual(self.source['epic_legal'], values['Store Configs', 'legalText'])
        self.assertEqual(values[about(5, 'body')], values[about(5, 'body', 'Product Home')])

    def test_switched_on_layout_adds_the_agent_item_and_online_sentences(self):
        values, items = self.layout(ai_coplay=True, online_play=True)
        self.assertEqual(9, len(items))
        self.assertEqual((self.source['ai_heading'], self.source['ai_body']), items[7])
        self.assertEqual(self.source['open_source_heading'], items[8][0])
        self.assertIn(self.source['multiplayer_online_body'], items[6][1])
        self.assertTrue(items[6][1].endswith(self.source['multiplayer_lan_body']))

    def test_live_switch_values_are_the_ones_applied(self):
        switches = self.platform['switches']
        values, items = self.layout()
        self.assertEqual(8 + bool(switches['ai_coplay']), len(items))
        text = '\n'.join(values.values())
        self.assertEqual(bool(switches['ai_coplay']), self.source['ai_body'] in text)
        self.assertEqual(bool(switches['online_play']), self.source['multiplayer_online_body'] in text)

    def test_updates_every_mapped_locale_of_a_saved_listing(self):
        columns = [column for code, column in self.platform['locales'].items() if code != 'en']
        catalogs = {code: {key: value if key == 'product_name' else f'{value} [{code}]' for key, value in self.source.items()}
                    for code in self.platform['locales']}
        catalogs['en'] = self.source
        listing = mapped_rows(self.platform, self.source, columns + ['es'],
                              lambda key, column: '' if column == 'es' else f'earlier {column} {key[1]}')
        header = epic.METADATA_COLUMNS + ['en'] + columns + ['es']
        text, report = epic.adapt(csv_text(header, listing), catalogs, self.platform, update_existing=True)
        rows = list(csv.reader(io.StringIO(text)))
        self.assertEqual(header[:-1], rows[0])
        self.assertEqual([row[:8] for row in listing], [row[:8] for row in rows[1:]])
        self.assertEqual((len(columns), len(listing) * len(columns), ['es'], []),
                         (report['translated_locale_count'], report['changed_cells'], report['removed_unused_locale_columns'], report['warnings']))
        self.assertFalse([cell for row in rows[1:] for cell in row[8:] if cell.startswith('earlier ')])


class ReviewGateTests(unittest.TestCase):
    """main() against a synthetic root: 45 catalogs, source hashes and review records written here."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = catalog('en')
        (self.root / 'reviews').mkdir()
        (self.root / 'platforms.json').write_text(json.dumps({'platforms': {'epic': PLATFORM}}))
        (self.root / 'source-hashes.json').write_text(json.dumps(S.source_hashes(self.source)))
        for code in S.CODES:
            self.write(code, catalog(code))
            if code != 'en': self.review(code)
        self.template = self.root / 'downloaded.csv'
        self.out = self.root / 'upload.csv'
        columns = ['fr', 'de']
        rows = mapped_rows(PLATFORM, self.source, columns, lambda key, column: f'earlier {column} {key[1]}')
        with self.template.open('w', encoding='utf-8-sig', newline='') as stream:
            stream.write(csv_text(epic.METADATA_COLUMNS + ['en'] + columns, rows))

    def write(self, code, fields):
        (self.root / f'{code}.md').write_text('# Translation\n' + ''.join(f'\n## {key}\n\n{value}\n' for key, value in fields.items()), encoding='utf-8')

    def review(self, code):
        fields = S.read_fields(self.root / f'{code}.md')
        (self.root / 'reviews' / f'{code}.json').write_text(json.dumps({
            'status': 'reviewed', 'issues': [], 'translator': 'translator', 'reviewer': 'reviewer',
            'source_hashes': S.source_hashes(self.source), 'translation_hashes': S.source_hashes(fields)}))

    def run_main(self, *flags):
        out, err = io.StringIO(), io.StringIO()
        argv = ['epic_template.py', '--template', str(self.template), '--out', str(self.out), '--root', str(self.root), *flags]
        with patch.object(sys, 'argv', argv), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = epic.main()
        return code, out.getvalue(), err.getvalue()

    def assert_refused(self, message):
        for flags in ((), ('--update-existing', '--update-english')):
            code, out, err = self.run_main(*flags)
            self.assertEqual((1, ''), (code, out))
            self.assertRegex(err, message)
            self.assertEqual(['downloaded.csv'], sorted(path.name for path in self.root.glob('*.csv*')))

    def test_refuses_a_locale_without_a_review_record(self):
        (self.root / 'reviews' / 'fr.json').unlink()
        self.assert_refused(r'Review gate: nothing written; 1 of 3 Epic locales lack .*: fr\. ')

    def test_refuses_a_translation_changed_after_its_review(self):
        self.write('de', dict(catalog('de'), headline='Edited after review'))
        self.assert_refused(r'Review gate: nothing written; 1 of 3 Epic locales lack .*: de\. ')

    def test_refuses_catalogs_that_predate_the_english_source(self):
        """The state after an English rewrite: locale files and reviews still hold the earlier field set."""
        earlier = lambda code: {key: value for key, value in catalog(code).items() if key not in ('fair_deal_line', 'features_heading')}
        for code in S.CODES:
            if code != 'en':
                self.write(code, dict(earlier(code), removed_field=f'{code}:removed'))
        self.assert_refused(r'Review gate: nothing written; 3 of 3 Epic locales lack .*: fr, de, el\. ')

    def test_refuses_english_changed_after_the_reviews(self):
        self.write('en', dict(self.source, headline='en:headline rewritten'))
        self.assert_refused(r'3 of 3 Epic locales lack .*: fr, de, el\. ')

    def test_refuses_while_any_other_catalog_is_stale(self):
        (self.root / 'reviews' / 'ca.json').unlink()
        self.assert_refused('every Epic locale is current, but another catalog.*first: ca: independent review missing')

    def test_reviewed_catalogs_update_the_template_and_print_a_summary(self):
        code, out, err = self.run_main()
        self.assertEqual(1, code)
        self.assertIn('--update-existing', err)
        self.assertFalse(self.out.exists())
        code, out, err = self.run_main('--update-existing')
        self.assertEqual((0, ''), (code, err))
        printed = json.loads(out)
        self.assertEqual('21 replaced, 0 filled: title, short_description, legal, about_item_1-4', printed['changed_fields']['fr'])
        self.assertEqual(printed['changed_fields']['fr'], printed['changed_fields']['de'])
        self.assertEqual((42, {'ai_coplay': False, 'online_play': False}), (printed['changed_cells'], printed['switches']))
        report = json.loads((self.root / 'upload.csv.report.json').read_text())
        self.assertEqual(21, len(report['changed_fields']['fr']['replaced']))
        with self.out.open(encoding='utf-8-sig', newline='') as stream:
            rows = list(csv.reader(stream))
        self.assertEqual('fr:short_pitch', next(row for row in rows if row[4] == 'shortDescription')[8])
        self.assertTrue(self.template.read_text(encoding='utf-8-sig').count('earlier fr'))

    def test_output_must_not_replace_the_downloaded_template(self):
        self.out = self.template
        code, out, err = self.run_main('--update-existing')
        self.assertEqual(1, code)
        self.assertIn('Output must differ', err)


if __name__ == '__main__':
    unittest.main()
