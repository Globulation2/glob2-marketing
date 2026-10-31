import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest
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

    def test_refuses_existing_locale_overwrite(self):
        self.headers.append('de');self.write_template()
        with patch.object(M,'validate',return_value=([],{'de':self.fields})):
            self.assertRaisesRegex(ValueError,'Existing locale',M.build,self.template,self.out,self.root)

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
