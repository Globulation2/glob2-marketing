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
import sys
from storefront import ROOT, platform_payload, validate


def build(template, destination, root=ROOT):
    errors, catalogs = validate(root, require_review=True)
    if errors: raise ValueError('\n'.join(errors))
    config = json.loads((root / 'platforms.json').read_text())['platforms']['microsoft']
    with template.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        headers = reader.fieldnames or []
        rows = list(reader)
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
    except (ValueError, OSError, KeyError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__': raise SystemExit(main())
