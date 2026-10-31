#!/usr/bin/env python3
"""Fill supported locales in an actual Epic CSV template using reviewed catalogs.

The downloaded template and generated upload file stay outside version control.
Unknown rows or changed English for mapped fields fail before output is written.
"""
import argparse
import csv
import io
import json
from pathlib import Path
import sys

import storefront

METADATA_COLUMNS = ['Entity Type', 'Entity Id', 'Entity Name', 'Entity Description',
                    'Localization Field', 'Field Description', 'Field Type']
ABOUT_FIELDS = [
    ('headline', 'listing_intro'),
    ('economy_heading', 'economy_body'),
    ('map_heading', 'map_body'),
    ('defense_heading', 'defense_body'),
    ('listing_open_source', 'epic_tail'),
]
MAPPED = {('Offer', 'title'): 'product_name', ('Offer', 'description'): 'short_pitch',
          ('Store Configs', 'productDisplayName'): 'product_name',
          ('Store Configs', 'shortDescription'): 'short_pitch',
          ('Store Configs', 'legalText'): 'epic_legal'}
for entity in ('Offer', 'Product Home'):
    for index, (headline, body) in enumerate(ABOUT_FIELDS):
        MAPPED[(entity, f'aboutItem.{index}.textBlock.headline')] = headline
        MAPPED[(entity, f'aboutItem.{index}.textBlock.body')] = body

PRESERVED_CONFIGS = {'developerDisplayName', 'publisherDisplayName', 'privacyLink'}
PRESERVED_CONFIGS.update('socialLinks.' + name for name in (
    'homepage', 'twitter', 'facebook', 'instagram', 'twitch', 'discord', 'vk',
    'youtube', 'reddit', 'naver', 'youku', 'weibo'))
PRESERVED_CONFIGS.update(f'technicalRequirements.windows.{name}.{level}'
                         for name in ('osVersion', 'cpu', 'memory', 'gpu', 'storage', 'soundCard')
                         for level in ('minimum', 'recommended'))
PRESERVED_CONFIGS.add('technicalRequirements.windows.additionalNotes.minimum')

# Required per-locale identity/requirements need explicit values in Epic imports.
# Preserve existing qualification wording as English fallback; these are not translations.
INVARIANT_CONFIGS = {'developerDisplayName', 'publisherDisplayName', 'privacyLink',
                     'socialLinks.homepage'}
INVARIANT_CONFIGS.update(field for field in PRESERVED_CONFIGS
                         if field.startswith('technicalRequirements.'))


def adapt(template_text, catalogs, locale_map):
    rows = list(csv.reader(io.StringIO(template_text.lstrip('\ufeff'), newline='')))
    if not rows or rows[0][:7] != METADATA_COLUMNS or 'en' not in rows[0]:
        raise ValueError('Unexpected Epic template columns; download and inspect the current template')
    header = rows[0]
    if len(header) != len(set(header)):
        raise ValueError('Duplicate template columns')
    index = {name: i for i, name in enumerate(header)}
    supported = {code: column for code, column in locale_map.items()
                 if code != 'en' and column in index}
    if len(set(supported.values())) != len(supported):
        raise ValueError('Canonical locales map to duplicate destination columns')
    removed_columns = [column for column in header[7:]
                       if column != 'en' and column not in supported.values()]
    keep_indexes = [i for i, column in enumerate(header) if column not in removed_columns]
    result = [[header[i] for i in keep_indexes]]
    mapped_rows = 0
    invariant_rows = 0
    invariant_cells = 0
    seen = set()
    for number, original in enumerate(rows[1:], start=2):
        # Empty separators and the official informational footer remain untouched.
        if not original or not any(original) or original[0].startswith('#Note.'):
            result.append([original[i] for i in keep_indexes] if len(original) == len(header) else original[:])
            continue
        if len(original) != len(header):
            raise ValueError(f'Row {number}: unexpected column count')
        for column in removed_columns:
            if original[index[column]]:
                raise ValueError(f'Row {number}: unused locale {column} has existing content; reconcile before removing column')
        row = original[:]
        entity, field = row[index['Entity Type']], row[index['Localization Field']]
        identity = (entity, row[index['Entity Id']], field)
        if identity in seen:
            raise ValueError(f'Row {number}: duplicate entity/field row')
        seen.add(identity)
        key = MAPPED.get((entity, field))
        if key is not None:
            if row[index['en']] != catalogs['en'][key]:
                raise ValueError(f'Row {number} {entity}/{field}: English differs from canonical {key}')
            if row[index['Field Type']] not in ('string', 'markdown'):
                raise ValueError(f'Row {number}: unexpected mapped field type')
            for code, column in supported.items():
                existing = row[index[column]]
                translated = catalogs[code][key]
                if existing and existing != translated:
                    raise ValueError(f'Row {number} {entity}/{field}: existing {column} translation differs; reconcile before import')
                row[index[column]] = translated
            mapped_rows += 1
        elif entity == 'Store Configs' and field in INVARIANT_CONFIGS:
            english = row[index['en']]
            if not english:
                raise ValueError(f'Row {number} {field}: invariant English source is empty; factual review required')
            for column in supported.values():
                existing = row[index[column]]
                if existing and existing != english:
                    raise ValueError(f'Row {number} {field}: existing {column} invariant differs; reconcile before import')
                row[index[column]] = english
                invariant_cells += 1
            invariant_rows += 1
        elif entity == 'Store Configs' and field in PRESERVED_CONFIGS:
            pass
        else:
            raise ValueError(f'Row {number}: unknown source row {entity}/{field}; explicit source review required')
        # IDs, English and field definitions retain exact values; unused blank locales are omitted.
        result.append([row[i] for i in keep_indexes])
    stream = io.StringIO(newline='')
    csv.writer(stream, lineterminator='\r\n').writerows(result)
    report = {'mapped_rows': mapped_rows, 'translated_locale_count': len(supported),
              'translated_columns': sorted(supported.values()),
              'configured_locales_missing_from_template': sorted(
                  code for code, column in locale_map.items() if column not in index),
              'removed_unused_locale_columns': removed_columns,
              'translated_cells': mapped_rows * len(supported),
              'english_fallback_rows': invariant_rows,
              'english_fallback_cells': invariant_cells,
              'english_fallback_note': 'Existing identity, URLs and system requirements copied exactly; not localized technical prose.',
              'english_and_metadata_preserved': True,
              'publication_status': 'prepared only; import/save/server readback required'}
    return stream.getvalue(), report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--template', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--root', type=Path, default=storefront.ROOT)
    args = parser.parse_args()
    try:
        if args.template.resolve() == args.out.resolve():
            raise ValueError('Output must differ from original downloaded template')
        errors, catalogs = storefront.validate(args.root, require_review=True)
        if errors:
            raise ValueError('\n'.join(errors))
        config = json.loads((args.root / 'platforms.json').read_text())
        text, report = adapt(args.template.read_text(encoding='utf-8-sig'), catalogs,
                             config['platforms']['epic']['locales'])
        args.out.write_text(text, encoding='utf-8-sig', newline='')
        args.out.with_suffix(args.out.suffix + '.report.json').write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps(report, ensure_ascii=False))
    except (OSError, ValueError, KeyError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
