"""Synthetic templates exercise identity preservation and source-drift rejection."""
import csv
import io
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import epic_template as epic


class EpicTemplateTests(unittest.TestCase):
    def setUp(self):
        self.header = epic.METADATA_COLUMNS + ['en', 'fr', 'es', 'bg']
        self.catalogs = {'en': {'short_pitch': 'English pitch'},
                         'fr': {'short_pitch': 'Texte français'}}
        self.mapping = {'en': 'en', 'fr': 'fr', 'el': 'el'}
        self.row = ['Offer', 'synthetic-id', 'Synthetic product', '', 'description',
                    'Short description', 'string', 'English pitch', '', 'keep Spanish', 'keep Bulgarian']

    def template(self, *rows):
        output = io.StringIO(newline='')
        csv.writer(output).writerows([self.header, *rows])
        return output.getvalue()

    def test_preserves_identity_english_unsupported_and_known_specs(self):
        specs = ['Store Configs', 'synthetic-config', 'Synthetic config', '',
                 'technicalRequirements.windows.cpu.minimum', 'Technical Requirements',
                 'string', 'Existing specification', 'existing French', '', '']
        text, report = epic.adapt(self.template(self.row, specs, [], ['#Note. Keep footer']),
                                  self.catalogs, self.mapping)
        rows = list(csv.reader(io.StringIO(text)))
        self.assertEqual(rows[1][:8], self.row[:8])
        self.assertEqual(rows[1][8:], ['Texte français', 'keep Spanish', 'keep Bulgarian'])
        self.assertEqual(rows[2], specs)
        self.assertEqual(rows[3:], [[], ['#Note. Keep footer']])
        self.assertEqual(report['configured_locales_missing_from_template'], ['el'])
        self.assertEqual(report['mapped_rows'], 1)

    def test_rejects_source_drift_unknown_rows_and_duplicate_rows(self):
        drift = self.row[:]
        drift[7] = 'Changed English'
        unknown = self.row[:]
        unknown[4] = 'newUnreviewedField'
        for rows in [(drift,), (unknown,), (self.row, self.row)]:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                epic.adapt(self.template(*rows), self.catalogs, self.mapping)

    def test_rejects_conflicting_existing_translation_and_accepts_identical(self):
        existing = self.row[:]
        existing[8] = 'Existing independent translation'
        with self.assertRaisesRegex(ValueError, 'reconcile before import'):
            epic.adapt(self.template(existing), self.catalogs, self.mapping)
        existing[8] = self.catalogs['fr']['short_pitch']
        text, _ = epic.adapt(self.template(existing), self.catalogs, self.mapping)
        self.assertEqual(list(csv.reader(io.StringIO(text)))[1], existing)

    def test_roundtrips_commas_quotes_and_line_breaks_deterministically(self):
        self.catalogs['fr']['short_pitch'] = 'Texte, avec "guillemets"\net une ligne'
        template = self.template(self.row)
        first = epic.adapt(template, self.catalogs, self.mapping)
        self.assertEqual(first, epic.adapt(template, self.catalogs, self.mapping))
        self.assertEqual(list(csv.reader(io.StringIO(first[0])))[1][8],
                         self.catalogs['fr']['short_pitch'])


if __name__ == '__main__':
    unittest.main()
