#!/usr/bin/env python3
"""Prepare a Microsoft CSV from a fresh console export; never publish or upload.

Preserve all template rows/identifiers, existing locale values and asset URLs.
New locales copy the English media/unchanged optional fields, then override only
reviewed canonical listing text. No guessed asset paths or binary declarations.

Locale columns the export already has stop generation unless --update-existing
is given. Then only the mapped text rows are replaced with reviewed canonical
values; every other cell in those columns (media URLs, technical/legal fields)
is kept, missing locales are still appended, and the English column must
already equal canonical English (or be replaced explicitly with --update-english).

Extending the mapping: canonical values are the payload keys of platforms.json
-> platforms.microsoft.fields (composed from catalog field IDs, limits enforced
without truncation). FIELD_FAMILIES below binds each payload key to its template
Field row. '{n}' families take as many numbered rows as platforms.json defines,
so a fifth screenshot caption needs only a desktop_screenshot_caption_5 entry
there. A new kind of translated text row needs one more FIELD_FAMILIES line.
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

# (payload key, candidate template Field names, companion media Field or None).
# '{n}' is the same 1-based number in all three. Every payload key that
# platforms.json defines must land on exactly one candidate row of the current
# export, or generation stops. TrailerTitle{n} follows Microsoft's trailer
# title rows but has not been observed in a project export yet.
FIELD_FAMILIES = (
    ('title', ('Title',), None),
    ('description', ('Description',), None),
    ('short_description', ('ShortDescription',), None),
    ('feature_{n}', ('Feature{n}',), None),
    ('search_term_{n}', ('SearchTerm{n}', 'SearchTerms{n}', 'Keyword{n}', 'Keywords{n}'), None),
    ('desktop_screenshot_caption_{n}', ('DesktopScreenshotCaption{n}', 'DesktopScreenshot{n}AltText'), 'DesktopScreenshot{n}'),
    ('trailer_title_{n}', ('TrailerTitle{n}',), 'Trailer{n}'),
)
PAYLOAD_ALIASES = {'search_term': 'search_term_1'}  # Unnumbered storefront-v1 key.
# storefront-v1 fallback: catalog screenshot_caption_{role} fields in gallery order,
# used only while platforms.json defines no desktop_screenshot_caption_{n} and
# only for caption rows the export actually exposes.
LEGACY_CAPTION_ROLES = ('colony', 'battle', 'strategic', 'terrain')


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


def numbered(pattern):
    prefix, suffix = pattern.split('{n}')
    return re.compile(re.escape(prefix) + '([1-9][0-9]*)' + re.escape(suffix))


def canonical_payload(locale, fields, config):
    """Return one locale's reviewed values keyed as FIELD_FAMILIES expects, plus the legacy-sourced keys."""
    payload, failures = platform_payload(fields, config)
    if failures: raise ValueError(f'{locale}: {failures}')
    for old, new in PAYLOAD_ALIASES.items():
        if old in payload:
            if new in payload: raise ValueError(f'platforms.json microsoft defines both {old} and {new}')
            payload[new] = payload.pop(old)
    legacy = set()
    if not any(numbered('desktop_screenshot_caption_{n}').fullmatch(key) for key in payload):
        for index, role in enumerate(LEGACY_CAPTION_ROLES, 1):
            if f'screenshot_caption_{role}' in fields:
                payload[f'desktop_screenshot_caption_{index}'] = fields[f'screenshot_caption_{role}']
                legacy.add(f'desktop_screenshot_caption_{index}')
    return payload, legacy


def bind(keys, legacy, by_field):
    """Bind payload keys to template rows: ({Field: (payload key, companion Field or None)}, unsourced numbered Fields)."""
    mapping, missing, bound = {}, [], set()
    for pattern, candidates, companion in FIELD_FAMILIES:
        if '{n}' in pattern:
            matches = [numbered(pattern).fullmatch(key) for key in keys]
            indexes = [str(index) for index in sorted(int(match[1]) for match in matches if match)]
        else:
            indexes = [''] if pattern in keys else []
        for index in indexes:
            key = pattern.replace('{n}', index)
            bound.add(key)
            options = [name for name in (item.replace('{n}', index) for item in candidates) if name in by_field]
            if len(options) > 1: raise ValueError(f'Ambiguous template fields {options} for {key}; inspect actual template')
            if options: mapping[options[0]] = (key, companion.replace('{n}', index) if companion else None)
            elif key not in legacy: missing.append('/'.join(item.replace('{n}', index) for item in candidates))
    unbound = sorted(set(keys) - bound)
    if unbound: raise ValueError(f'platforms.json microsoft fields {unbound} have no template row mapping; extend FIELD_FAMILIES in microsoft_import.py')
    if missing: raise ValueError(f'Actual template lacks expected text fields {sorted(missing)}; reconcile observed fields first')
    unsourced = [field for pattern, candidates, companion in FIELD_FAMILIES if '{n}' in pattern
                 for name in candidates for field in by_field if field not in mapping and numbered(name).fullmatch(field)]
    return mapping, unsourced


def build(template, destination, root=ROOT, update_existing=False, update_english=False):
    if update_english and not update_existing: raise ValueError('--update-english only applies together with --update-existing')
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
    planned = []
    for locale, platform_code in config['locales'].items():
        if locale == 'en': continue  # English is never translated; update mode verifies it below.
        matches = [header for header in headers[4:] if header.lower() == platform_code.lower()]
        if len(matches) > 1: raise ValueError(f'Ambiguous existing locale columns {matches} for {locale}')
        payload, legacy = canonical_payload(locale, catalogs[locale], config)
        planned.append((matches[0] if matches else platform_code, payload, legacy, bool(matches)))
    existing = [column for column, payload, legacy, exists in planned if exists]
    if existing and not update_existing:
        raise ValueError(f'Existing locale columns {", ".join(existing)} require explicit current-value reconciliation, not blind overwrite; rerun with --update-existing to replace only the mapped canonical text fields')
    english = canonical_payload('en', catalogs['en'], config) if update_existing else None
    sources = [(payload, legacy) for column, payload, legacy, exists in planned] + ([english] if english else [])
    keys, legacy = (set(sources[0][0]), sources[0][1]) if sources else (set(), set())
    if any(set(payload) != keys for payload, other in sources):
        raise ValueError('Canonical catalogs expose different Microsoft fields; run storefront.py check first')
    mapping, unsourced = bind(keys, legacy, by_field)

    def current(field, column):  # A blank locale cell falls back to the default column in the Store.
        return by_field[field].get(column) or by_field[field].get('default') or ''

    report = {}
    changed_cells = 0
    if update_existing:
        # The default-language listing must already carry canonical English unless explicitly replaced here.
        stale = [field for field, (key, companion) in mapping.items() if current(field, source_column) != english[0][key]]
        if stale and not update_english:
            raise ValueError(f'English column {source_column} differs from canonical English in {stale}; save the approved English in the console and export again, or rerun with --update-english to replace exactly those fields')
        if stale and source_column == 'default':
            raise ValueError('Export has no en-us column; --update-english will not write English into the shared default column')
        for field in stale: by_field[field][source_column] = english[0][mapping[field][0]]
        changed_cells += len(stale)
        report = {'column': source_column, 'status': 'updated' if stale else 'matches canonical', 'changed': stale}
    added, updated = [], {}
    for column, payload, other, exists in planned:
        if exists:
            # Only mapped text cells are touched; media URLs and every other row keep their saved values.
            updated[column] = [field for field, (key, companion) in mapping.items() if (by_field[field].get(column) or '') != payload[key]]
            changed_cells += len(updated[column])
        else:
            headers.append(column)
            added.append(column)
            for row in rows:
                # Current English URLs preserve approved media without uploading files.
                row[column] = row.get(source_column, '') or row.get('default', '')
        for field, (key, companion) in mapping.items():
            by_field[field][column] = payload[key]
    targets = added + list(updated)
    warnings = []
    for field in unsourced:
        columns = [column for column in dict.fromkeys([source_column] + targets) if current(field, column)]
        if columns: warnings.append(f'{field}: no canonical value; existing text left unchanged in {len(columns)} column(s): {", ".join(columns)}')
    for field, (key, companion) in mapping.items():
        columns = [column for column in targets if companion in by_field and not current(companion, column)]
        if columns: warnings.append(f'{field}: {companion} is empty in {len(columns)} column(s): {", ".join(columns)}; the text has no media to describe there')
    unmapped = [header for header in headers[4:] if header != source_column and header not in targets]
    if unmapped: warnings.append(f'Locale columns without a canonical mapping left unchanged: {", ".join(unmapped)}')
    with destination.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    result = {'new_locales': len(added), 'added_locales': added, 'updated_locales': updated, 'changed_cells': changed_cells, 'rows_preserved': len(rows), 'source_column': source_column, 'mapped_text_fields': list(mapping), 'warnings': warnings, 'upload_eligible': False, 'note': 'Requires console validation, current submission preflight and saved readback. Template identifiers and unmapped cells preserved; changed_cells counts overwritten cells in columns the export already had.'}
    if update_existing: result['english'] = report
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('template', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--update-existing', action='store_true', help='Replace the mapped canonical text rows in locale columns the export already has; every other cell in those columns is kept')
    parser.add_argument('--update-english', action='store_true', help='With --update-existing: also replace mapped text rows of the English column instead of stopping when they differ from canonical English')
    args = parser.parse_args()
    try:
        if args.template.resolve() == args.out.resolve(): raise ValueError('Preserve original console export; output must be a different path')
        result = build(args.template, args.out, args.root, args.update_existing, args.update_english)
        # One line per locale: the template Fields whose saved value was replaced.
        result['updated_locales'] = {column: ', '.join(fields) or 'already current' for column, fields in result['updated_locales'].items()}
        result['added_locales'] = ', '.join(result['added_locales'])
        print(json.dumps(result, indent=2))
    except (ValueError, OSError, KeyError, ET.ParseError, zipfile.BadZipFile) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__': raise SystemExit(main())
