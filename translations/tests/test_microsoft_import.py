import contextlib
import csv
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
from xml.etree import ElementTree as ET
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / 'tools'))
import microsoft_import as M


class MicrosoftImportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.template = self.root / 'original.csv'
        self.out = self.root / 'translated.csv'
        self.headers = ['Field','ID','Type','default','en-us']
        self.rows = [{'Field':f,'ID':str(i),'Type':'Text','default':'','en-us':'original '+f} for i,f in enumerate(['Title','Description','ShortDescription','Feature1','Feature2','Feature3','Feature4','SearchTerm1','DesktopScreenshot1','ReleaseNotes'])]
        self.rows[-2]['Type'] = 'Relative path (or URL to file in Partner Center)'
        self.rows[-2]['en-us'] = 'https://approved.example/image.png'
        self.write_template()
        spec = {'locales': {'en':'en-us','de':'de'}, 'fields': {'title':{'paragraphs':[['product_name']]},'description':{'paragraphs':[['description']]},'short_description':{'paragraphs':[['short']]},'search_term':{'paragraphs':[['search']]},**{f'feature_{i}':{'paragraphs':[[f'feature_{i}']]} for i in range(1,5)}}}
        (self.root / 'platforms.json').write_text(json.dumps({'platforms':{'microsoft':spec}}))
        self.fields = {'product_name':'Globulation 2','description':'Reviewed & translated','short':'Short','search':'Strategy', **{f'feature_{i}':str(i) for i in range(1,5)}, **{f'screenshot_caption_{r}':r for r in ('colony','battle','strategic','terrain')}}

    def write_template(self):
        with self.template.open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=self.headers);writer.writeheader();writer.writerows(self.rows)

    def test_preserves_identifiers_existing_values_and_media(self):
        with patch.object(M,'validate',return_value=([],{'de':self.fields})):
            result=M.build(self.template,self.out,self.root)
        with self.out.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
        self.assertEqual(1,result['new_locales'])
        self.assertEqual(self.rows,[{k:r[k] for k in self.headers} for r in rows])
        self.assertEqual('Reviewed & translated',rows[1]['de'])
        self.assertEqual('https://approved.example/image.png',rows[-2]['de'])

    def test_actual_console_header_and_caption_shape(self):
        self.headers[2] = 'Type (Type)'
        for row in self.rows: row['Type (Type)'] = row.pop('Type')
        self.rows.append({'Field':'DesktopScreenshotCaption1','ID':'150','Type (Type)':'Text','default':'','en-us':'English caption'})
        self.rows.extend([{key:'' for key in self.headers} for _ in range(2)])
        self.write_template()
        with patch.object(M,'validate',return_value=([],{'de':self.fields})):
            M.build(self.template,self.out,self.root)
        with self.out.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
        self.assertEqual('colony',rows[-3]['de'])
        self.assertEqual('Type (Type)',list(rows[0])[2])

    def write_xlsx_fixture(self, *, formula=False, second_sheet=False):
        path = self.root / 'export.xlsx'
        ns = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
        sheet = ET.Element('worksheet', xmlns=ns)
        data = ET.SubElement(sheet, 'sheetData')
        values = [self.headers] + [[row.get(header, '') for header in self.headers] for row in self.rows]
        for i, row in enumerate(values, 1):
            node = ET.SubElement(data, 'row', r=str(i))
            for j, value in enumerate(row, 1):
                if not value: continue  # Missing/empty cells must retain their positions.
                cell = ET.SubElement(node, 'c', r=f'{chr(64+j)}{i}')
                if i == 2 and j == 1:
                    cell.set('t', 's'); ET.SubElement(cell, 'v').text = '0'
                elif i > 1 and j == 2:
                    ET.SubElement(cell, 'v').text = value
                else:
                    cell.set('t', 'inlineStr')
                    ET.SubElement(ET.SubElement(cell, 'is'), 't').text = value
                if formula and i == 2 and j == 5: ET.SubElement(cell, 'f').text = 'A1'
        extra = '<sheet name="ambiguous" sheetId="2" r:id="rId2"/>' if second_sheet else ''
        with zipfile.ZipFile(path, 'w') as archive:
            archive.writestr('xl/workbook.xml', f'<workbook xmlns="{ns}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="exportedData" sheetId="1" r:id="rId1"/>{extra}</sheets></workbook>')
            archive.writestr('xl/_rels/workbook.xml.rels', '<Relationships><Relationship Id="rId1" Target="worksheets/sheet1.xml"/></Relationships>')
            archive.writestr('xl/sharedStrings.xml', f'<sst xmlns="{ns}"><si><r><t>Ti</t></r><r><t>tle</t></r></si></sst>')
            archive.writestr('xl/worksheets/sheet1.xml', ET.tostring(sheet))
        return path

    def test_xlsx_mixed_strings_ids_empty_cells_and_exact_csv_equivalence(self):
        fixture = self.write_xlsx_fixture()
        headers, rows = M.read_xlsx(fixture)
        self.assertEqual(self.headers, headers)
        self.assertEqual(self.rows, rows)
        with patch.object(M,'validate',return_value=([],{'de':self.fields})):
            M.build(self.template,self.out,self.root)
            other = self.root / 'from-xlsx.csv'
            M.build(fixture,other,self.root)
        self.assertEqual(self.out.read_bytes(),other.read_bytes())

    def test_xlsx_rejects_formulas_and_ambiguous_sheets(self):
        fixture = self.write_xlsx_fixture(formula=True)
        self.assertRaisesRegex(ValueError,'formulas',M.read_xlsx,fixture)
        fixture = self.write_xlsx_fixture(second_sheet=True)
        self.assertRaisesRegex(ValueError,'exactly one',M.read_xlsx,fixture)

    def test_refuses_existing_locale_overwrite(self):
        self.headers.append('de');self.write_template()
        with patch.object(M,'validate',return_value=([],{'de':self.fields})):
            self.assertRaisesRegex(ValueError,'Existing locale columns de .*--update-existing',M.build,self.template,self.out,self.root)
        self.assertFalse(self.out.exists())

    # --update-existing: a saved listing whose locale columns already hold earlier copy.

    def saved_listing(self):
        """Canonical English, a German column with older text and its own media reference, no French yet."""
        config = json.loads((self.root / 'platforms.json').read_text())
        config['platforms']['microsoft']['locales'] = {'en':'en-us','de':'de','fr':'fr'}
        (self.root / 'platforms.json').write_text(json.dumps(config))
        self.en = dict(self.fields, description='English description', short='English short', search='English term', screenshot_caption_colony='English caption', **{f'feature_{i}':f'English {i}' for i in range(1,5)})
        self.fr = dict(self.fields, description='Description française', short='Court')
        self.catalogs = {'en':self.en,'de':self.fields,'fr':self.fr}
        self.rows.append({'Field':'DesktopScreenshotCaption1','ID':'150','Type':'Text','default':'','en-us':''})
        self.mapped = {'Title':'product_name','Description':'description','ShortDescription':'short','SearchTerm1':'search','DesktopScreenshotCaption1':'screenshot_caption_colony', **{f'Feature{i}':f'feature_{i}' for i in range(1,5)}}
        self.headers.append('de')
        for row in self.rows:
            row['de'] = 'old de ' + row['Field']
            if row['Field'] in self.mapped: row['en-us'] = self.en[self.mapped[row['Field']]]
        self.row('Title')['de'] = 'Globulation 2'
        self.row('DesktopScreenshot1')['de'] = 'https://approved.example/image.png?parentId=de'
        self.write_template()

    def row(self, field, rows=None):
        return next(row for row in (self.rows if rows is None else rows) if row['Field'] == field)

    def update(self, **options):
        with patch.object(M,'validate',return_value=([],self.catalogs)):
            result = M.build(self.template,self.out,self.root,update_existing=True,**options)
        with self.out.open(encoding='utf-8-sig',newline='') as f: return result, list(csv.DictReader(f))

    def test_update_existing_replaces_only_mapped_fields_and_appends_missing_locales(self):
        self.saved_listing()
        result, rows = self.update()
        changed = [field for field in self.mapped if field != 'Title']
        self.assertEqual({'de':sorted(changed)},{'de':sorted(result['updated_locales']['de'])})
        self.assertEqual((1,['fr'],len(changed)),(result['new_locales'],result['added_locales'],result['changed_cells']))
        self.assertEqual({'column':'en-us','status':'matches canonical','changed':[]},result['english'])
        self.assertEqual(['Field','ID','Type','default','en-us','de','fr'],list(rows[0]))
        for before, after in zip(self.rows, rows):
            field = before['Field']
            self.assertEqual({k:before[k] for k in ('Field','ID','Type','default','en-us')},{k:after[k] for k in ('Field','ID','Type','default','en-us')})
            if field in self.mapped:
                self.assertEqual(self.fields[self.mapped[field]],after['de'])
                self.assertEqual(self.fr[self.mapped[field]],after['fr'])
            else:
                self.assertEqual(before['de'],after['de'])  # Media reference, release notes: untouched.
                self.assertEqual(before['en-us'],after['fr'])  # New locale still starts from English.
        self.assertEqual('https://approved.example/image.png?parentId=de',self.row('DesktopScreenshot1',rows)['de'])
        self.assertEqual('old de ReleaseNotes',self.row('ReleaseNotes',rows)['de'])

    def test_update_existing_is_idempotent_and_reports_no_changes(self):
        self.saved_listing()
        self.update()
        first = self.out.read_bytes()
        self.template = self.root / 'second-export.csv'
        self.template.write_bytes(first)
        result, rows = self.update()
        self.assertEqual(({'de':[],'fr':[]},0,0),(result['updated_locales'],result['changed_cells'],result['new_locales']))
        self.assertEqual(first,self.out.read_bytes())

    def test_update_existing_fails_on_stale_english_unless_explicitly_replaced(self):
        self.saved_listing()
        self.row('Description')['en-us'] = 'Earlier English description'
        self.write_template()
        with patch.object(M,'validate',return_value=([],self.catalogs)):
            self.assertRaisesRegex(ValueError,r"English column en-us differs from canonical English in \['Description'\]",M.build,self.template,self.out,self.root,update_existing=True)
            self.assertRaisesRegex(ValueError,'only applies together',M.build,self.template,self.out,self.root,update_english=True)
        self.assertFalse(self.out.exists())
        result, rows = self.update(update_english=True)
        self.assertEqual({'column':'en-us','status':'updated','changed':['Description']},result['english'])
        self.assertEqual('English description',self.row('Description',rows)['en-us'])
        for field in ('DesktopScreenshot1','ReleaseNotes','Title'):
            self.assertEqual(self.row(field)['en-us'],self.row(field,rows)['en-us'])

    def test_update_existing_keeps_review_and_limit_gates(self):
        self.saved_listing()
        with patch.object(M,'validate',return_value=(['de: review source hashes stale'],{})):
            self.assertRaisesRegex(ValueError,'review source hashes stale',M.build,self.template,self.out,self.root,update_existing=True)
        config = json.loads((self.root / 'platforms.json').read_text())
        config['platforms']['microsoft']['fields']['short_description']['limit'] = 6
        (self.root / 'platforms.json').write_text(json.dumps(config))
        with patch.object(M,'validate',return_value=([],self.catalogs)):
            self.assertRaisesRegex(ValueError,'exceeds 6',M.build,self.template,self.out,self.root,update_existing=True)
        self.assertFalse(self.out.exists())

    def add_numbered_captions(self, count):
        """Captions bound through platforms.json to arbitrary catalog field IDs, not the four legacy roles."""
        config = json.loads((self.root / 'platforms.json').read_text())
        for i in range(1,count+1):
            config['platforms']['microsoft']['fields'][f'desktop_screenshot_caption_{i}'] = {'paragraphs':[[f'gallery_text_{i}']],'limit':200}
            for code, catalog in self.catalogs.items(): catalog[f'gallery_text_{i}'] = f'{code} shot {i}'
            if i > 1:
                self.rows.append({'Field':f'DesktopScreenshot{i}','ID':str(200+i),'Type':'Relative path (or URL to file in Partner Center)','default':'','en-us':f'https://approved.example/{i}.png','de':f'https://approved.example/{i}.png?parentId=de' if i < 5 else ''})
                self.rows.append({'Field':f'DesktopScreenshotCaption{i}','ID':str(150+i),'Type':'Text','default':'','en-us':'','de':f'old de caption {i}' if i < 5 else ''})
            self.row(f'DesktopScreenshotCaption{i}')['en-us'] = f'en shot {i}'
        (self.root / 'platforms.json').write_text(json.dumps(config))
        self.write_template()

    def test_caption_rows_follow_platform_fields_beyond_four_screenshots(self):
        self.saved_listing()
        self.add_numbered_captions(6)
        result, rows = self.update()
        for i in range(1,7):
            self.assertEqual(f'de shot {i}',self.row(f'DesktopScreenshotCaption{i}',rows)['de'])
            self.assertEqual(f'fr shot {i}',self.row(f'DesktopScreenshotCaption{i}',rows)['fr'])
        self.assertEqual([f'DesktopScreenshotCaption{i}' for i in range(1,7)],result['mapped_text_fields'][-6:])
        self.assertEqual('',self.row('DesktopScreenshot5',rows)['de'])  # Media is never filled in for an existing column.
        self.assertEqual(['DesktopScreenshotCaption5: DesktopScreenshot5 is empty in 1 column(s): de; the text has no media to describe there','DesktopScreenshotCaption6: DesktopScreenshot6 is empty in 1 column(s): de; the text has no media to describe there'],result['warnings'])

    def test_canonical_field_without_template_row_or_mapping_stops_generation(self):
        self.saved_listing()
        self.add_numbered_captions(6)
        self.rows.remove(self.row('DesktopScreenshotCaption6'))
        self.write_template()
        with patch.object(M,'validate',return_value=([],self.catalogs)):
            self.assertRaisesRegex(ValueError,'lacks expected text fields.*DesktopScreenshotCaption6',M.build,self.template,self.out,self.root,update_existing=True)
        config = json.loads((self.root / 'platforms.json').read_text())
        config['platforms']['microsoft']['fields']['tagline'] = {'paragraphs':[['short']]}
        (self.root / 'platforms.json').write_text(json.dumps(config))
        with patch.object(M,'validate',return_value=([],self.catalogs)):
            self.assertRaisesRegex(ValueError,r"\['tagline'\] have no template row mapping; extend FIELD_FAMILIES",M.build,self.template,self.out,self.root,update_existing=True)
        self.assertFalse(self.out.exists())

    def test_update_existing_warns_about_numbered_rows_without_canonical_value(self):
        self.saved_listing()
        self.rows.append({'Field':'Feature5','ID':'77','Type':'Text','default':'','en-us':'','de':'old de fifth feature'})
        self.headers.append('xx-yy')
        for row in self.rows: row['xx-yy'] = 'unmapped locale ' + row['Field']
        self.write_template()
        result, rows = self.update()
        self.assertEqual('old de fifth feature',self.row('Feature5',rows)['de'])
        self.assertEqual('unmapped locale Description',self.row('Description',rows)['xx-yy'])
        self.assertEqual(['Feature5: no canonical value; existing text left unchanged in 1 column(s): de','Locale columns without a canonical mapping left unchanged: xx-yy'],result['warnings'])

    def test_command_line_requires_the_flag_and_prints_per_locale_changes(self):
        self.saved_listing()
        out, err = io.StringIO(), io.StringIO()
        with patch.object(M,'validate',return_value=([],self.catalogs)), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            with patch.object(sys,'argv',['microsoft_import.py',str(self.template),'--out',str(self.out),'--root',str(self.root)]):
                self.assertEqual(1,M.main())
            self.assertIn('--update-existing',err.getvalue())
            self.assertFalse(self.out.exists())
            with patch.object(sys,'argv',['microsoft_import.py',str(self.template),'--out',str(self.out),'--root',str(self.root),'--update-existing']):
                self.assertEqual(0,M.main())
        summary = json.loads(out.getvalue())
        self.assertEqual({'de':'Description, ShortDescription, Feature1, Feature2, Feature3, Feature4, SearchTerm1, DesktopScreenshotCaption1'},summary['updated_locales'])
        self.assertEqual('fr',summary['added_locales'])

    def test_indonesian_locale_does_not_collide_with_reserved_ID_header(self):
        config = json.loads((self.root / 'platforms.json').read_text())
        config['platforms']['microsoft']['locales'] = {'en':'en-us','id':'id'}
        (self.root / 'platforms.json').write_text(json.dumps(config))
        with patch.object(M,'validate',return_value=([],{'id':self.fields})):
            result=M.build(self.template,self.out,self.root)
        with self.out.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
        self.assertEqual(1,result['new_locales'])
        self.assertEqual('1',rows[1]['ID'])
        self.assertEqual('Reviewed & translated',rows[1]['id'])

    def test_stale_review_prevents_output(self):
        with patch.object(M,'validate',return_value=(['review stale'],{})):
            self.assertRaisesRegex(ValueError,'review stale',M.build,self.template,self.out,self.root)
        self.assertFalse(self.out.exists())


if __name__=='__main__': unittest.main()
