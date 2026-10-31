#!/usr/bin/env python3
"""Prepare a Microsoft CSV from a fresh console export; never publish or upload.

Preserve all template rows/identifiers, existing locale values and asset URLs.
New locales copy the English media/unchanged optional fields, then override only
reviewed canonical listing text. No guessed asset paths or binary declarations.
"""
import argparse
import csv
import json
from pathlib import Path
import posixpath
import re
import sys
import zipfile
from xml.etree import ElementTree as ET
from storefront import ROOT, platform_payload, validate


XML = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def rich_text(element):
    if element is None: return ''
    parts = []
    for child in element:
        if child.tag == '{' + XML['m'] + '}t': parts.append(child.text or '')
        elif child.tag == '{' + XML['m'] + '}r':
            parts.extend(item.text or '' for item in child.findall('m:t', XML))
    return ''.join(parts)


def read_xlsx(path):
    """Read a single-sheet text/ID console export without editing its workbook."""
    with zipfile.ZipFile(path) as archive:
        workbook = ET.fromstring(archive.read('xl/workbook.xml'))
        sheets = workbook.findall('m:sheets/m:sheet', XML)
        if len(sheets) != 1: raise ValueError('XLSX template must have exactly one unambiguous worksheet')
        sheet_id = sheets[0].get('{' + REL + '}id')
        relationships = ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))
        matching = [item for item in relationships if item.get('Id') == sheet_id]
        if len(matching) != 1 or matching[0].get('TargetMode') == 'External':
            raise ValueError('XLSX worksheet relationship is missing, ambiguous or external')
        target = matching[0].get('Target', '')
        target = posixpath.normpath(target.lstrip('/') if target.startswith('/') else 'xl/' + target)
        if not target.startswith('xl/worksheets/'):
            raise ValueError('Unsupported XLSX worksheet relationship target')
        strings = []
        if 'xl/sharedStrings.xml' in archive.namelist():
            strings = [rich_text(item) for item in ET.fromstring(archive.read('xl/sharedStrings.xml'))]
        sheet = ET.fromstring(archive.read(target))
        if sheet.find('.//m:f', XML) is not None:
            raise ValueError('XLSX formulas are not accepted; use an unmodified console export')
        cells = {}
        last_row = 0
        for row in sheet.findall('m:sheetData/m:row', XML):
            try: row_id = int(row.get('r', ''))
            except ValueError: raise ValueError('XLSX row has no valid index')
            if not 1 <= row_id <= 10000: raise ValueError('XLSX row index outside supported template size')
            last_row = max(last_row, row_id)
            for cell in row.findall('m:c', XML):
                match = re.fullmatch(r'([A-Z]+)([1-9][0-9]*)', cell.get('r', ''))
                if not match or int(match[2]) != row_id: raise ValueError('Invalid XLSX cell reference')
                column = 0
                for letter in match[1]: column = column * 26 + ord(letter) - ord('A') + 1
                if column > 1000: raise ValueError('XLSX column index outside supported template size')
                coordinate = (row_id, column)
                if coordinate in cells: raise ValueError('Duplicate XLSX cell reference')
                kind = cell.get('t')
                value = cell.findtext('m:v', '', XML)
                if kind == 's':
                    try:
                        string_id = int(value)
                        if string_id < 0: raise ValueError()
                        value = strings[string_id]
                    except (ValueError, IndexError): raise ValueError('Invalid XLSX shared string index')
                elif kind == 'inlineStr': value = rich_text(cell.find('m:is', XML))
                elif kind not in (None, 'n', 'str', 'b'):
                    raise ValueError(f'Unsupported XLSX cell type {kind}')
                cells[coordinate] = value
        width = max((column for (row, column), value in cells.items() if row == 1 and value), default=0)
        if not width: raise ValueError('XLSX has no header row')
        if any(column > width and value for (row, column), value in cells.items()):
            raise ValueError('XLSX contains populated cells beyond its header columns')
        headers = [cells.get((1, column), '') for column in range(1, width + 1)]
        if any(not value for value in headers) or len(set(headers)) != len(headers):
            raise ValueError('XLSX header columns must be nonempty and unique')
        return headers, [{headers[column - 1]: cells.get((row, column), '') for column in range(1, width + 1)} for row in range(2, last_row + 1)]


def read_template(path):
    if path.suffix.lower() == '.xlsx': return read_xlsx(path)
    if path.suffix.lower() != '.csv': raise ValueError('Template must be a current .xlsx or .csv console export')
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        headers = reader.fieldnames or []
        rows = list(reader)
    if len(set(headers)) != len(headers) or any(None in row for row in rows):
        raise ValueError('CSV template has duplicate headers or unexpected extra cells')
    return headers, rows


def build(template, destination, root=ROOT):
    errors, catalogs = validate(root, require_review=True)
    if errors: raise ValueError('\n'.join(errors))
    config = json.loads((root / 'platforms.json').read_text())['platforms']['microsoft']
    headers, rows = read_template(template)
    if len(headers) < 4 or headers[:2] != ['Field', 'ID'] or headers[2] not in ('Type', 'Type (Type)') or 'default' not in headers:
        raise ValueError('Expected actual Microsoft export columns Field, ID, Type (or Type (Type)), default; inspect current template instead of guessing')
    source_column = next((header for header in headers if header.lower() == 'en-us'), 'default')
    by_field = {}
    for row in rows:
        field = row['Field']
        if not field:
            if any(row.values()): raise ValueError('Template row has values without a Field identifier')
            continue  # Preserve all-empty trailing/separator rows from current XLSX export.
        if field in by_field: raise ValueError(f'Duplicate template Field: {field}')
        by_field[field] = row
    mapping = {'Title': 'title', 'Description': 'description', 'ShortDescription': 'short_description', 'Feature1': 'feature_1', 'Feature2': 'feature_2', 'Feature3': 'feature_3', 'Feature4': 'feature_4'}
    missing = mapping.keys() - by_field.keys()
    if missing: raise ValueError(f'Actual template lacks expected text fields {sorted(missing)}; reconcile observed fields first')
    keyword_fields = [key for key in ('SearchTerm1', 'SearchTerms1', 'Keyword1', 'Keywords1') if key in by_field]
    if len(keyword_fields) == 1: mapping[keyword_fields[0]] = 'search_term'
    # Text caption field names are only added when the current export explicitly exposes them.
    for index, role in enumerate(('colony','battle','strategic','terrain'), 1):
        options = [key for key in (f'DesktopScreenshot{index}AltText', f'DesktopScreenshotCaption{index}') if key in by_field]
        if len(options) > 1: raise ValueError(f'Ambiguous desktop caption fields for screenshot {index}; inspect actual template')
        if options: mapping[options[0]] = f'caption_{role}'
    planned = []
    for locale, platform_code in config['locales'].items():
        if locale == 'en': continue  # Keep approved English exactly as exported.
        match = next((header for header in headers[4:] if header.lower() == platform_code.lower()), None)
        if match is not None:
            raise ValueError(f'Existing locale {match} requires explicit current-value reconciliation, not blind overwrite')
        payload, failures = platform_payload(catalogs[locale], config)
        if failures: raise ValueError(f'{locale}: {failures}')
        for role in ('colony','battle','strategic','terrain'):
            payload[f'caption_{role}'] = catalogs[locale][f'screenshot_caption_{role}']
        planned.append((platform_code, payload))
    for platform_code, payload in planned:
        headers.append(platform_code)
        for row in rows:
            # Current English URLs preserve approved media without uploading files.
            row[platform_code] = row.get(source_column, '') or row.get('default', '')
        for field, payload_key in mapping.items():
            by_field[field][platform_code] = payload[payload_key]
    with destination.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    return {'new_locales': len(planned), 'rows_preserved': len(rows), 'source_column': source_column, 'mapped_text_fields': list(mapping), 'upload_eligible': False, 'note': 'Requires console validation, current submission preflight and saved readback. Existing English and template identifiers preserved.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('template', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        if args.template.resolve() == args.out.resolve(): raise ValueError('Preserve original console export; output must be a different path')
        print(json.dumps(build(args.template, args.out, args.root), indent=2))
    except (ValueError, OSError, KeyError, ET.ParseError, zipfile.BadZipFile) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__': raise SystemExit(main())
