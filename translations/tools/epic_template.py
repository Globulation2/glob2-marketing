#!/usr/bin/env python3
"""Fill or update supported locales in an actual Epic CSV template using reviewed catalogs.

The downloaded template and generated upload file stay outside version control.
Unknown rows, changed English for mapped fields and differing saved translations
fail before output is written. --update-existing replaces differing saved
translations and --update-english replaces differing English, in mapped rows
only; every other cell keeps its saved value.

Extending the mapping: canonical values are the payload keys of platforms.json
-> platforms.epic.fields, composed with that entry's switches and bullet prefix
(limits enforced without truncation). FIELD_FAMILIES below binds each key to
its template rows. The composed description is entered as About items: a
paragraph whose first line is a heading field (HEADING_FIELDS) starts an item,
and the rest of that paragraph plus the paragraphs up to the next heading form
its body. A switched-off paragraph is no item, so the item count follows the
switches. A new payload key (trailer or caption text, say) needs one more
FIELD_FAMILIES line naming the row the current template actually exposes.
"""
import argparse
import csv
from fnmatch import fnmatchcase
import io
import json
from pathlib import Path
import re
import sys

import storefront

METADATA_COLUMNS = ['Entity Type', 'Entity Id', 'Entity Name', 'Entity Description',
                    'Localization Field', 'Field Description', 'Field Type']

# (payload key, template rows as (Entity Type, Localization Field)). Every payload
# key that platforms.json defines must be bound here or be ABOUT_KEY, or generation stops.
FIELD_FAMILIES = (
    ('title', (('Offer', 'title'), ('Store Configs', 'productDisplayName'))),
    ('short_description', (('Offer', 'description'), ('Store Configs', 'shortDescription'))),
    ('legal', (('Store Configs', 'legalText'),)),
)
# The payload key entered as heading/body About items, the entities that carry
# them and the row naming observed in the 2026-10-31 and 2026-11-17 templates.
ABOUT_KEY = 'description'
ABOUT_ENTITIES = ('Offer', 'Product Home')
ABOUT_PARTS = ('headline', 'body')
ABOUT_ROW = re.compile(r'aboutItem\.(0|[1-9][0-9]*)\.textBlock\.(headline|body)')
HEADING_FIELDS = ('headline', '*_heading')

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


def about_items(fields, platform):
    """Split the composed description into Epic About items: [(heading, body), ...]."""
    switches = platform.get('switches', {})
    prefix = platform.get('bullet_prefix', '• ')
    items = []
    for paragraph in platform['fields'][ABOUT_KEY]['paragraphs']:
        composed = storefront.blocks(fields, [paragraph], switches)
        if not composed:
            continue  # Switched off for this platform.
        text = composed[0]['lines'] + [prefix + bullet for bullet in composed[0]['bullets']]
        first = (paragraph.get('lines', []) if isinstance(paragraph, dict) else paragraph)[:1]
        name = first[0].get('field') if first and isinstance(first[0], dict) else first[0] if first else None
        if isinstance(name, str) and any(fnmatchcase(name, pattern) for pattern in HEADING_FIELDS):
            if not storefront.enabled(first[0], switches):
                raise ValueError(f'platforms.json epic {ABOUT_KEY}: heading {name} is switched off while its paragraph is on; switch the whole paragraph')
            items.append((text[0], ['\n'.join(text[1:])] if text[1:] else []))
        elif not items:
            raise ValueError(f'platforms.json epic {ABOUT_KEY} must open with a heading field ({", ".join(HEADING_FIELDS)})')
        else:
            items[-1][1].append('\n'.join(text))
    empty = [str(number) for number, (heading, body) in enumerate(items, 1) if not body]
    if empty:
        raise ValueError(f'platforms.json epic {ABOUT_KEY}: About item {", ".join(empty)} has a heading and no body')
    return [(heading, '\n\n'.join(body)) for heading, body in items]


def canonical_rows(code, fields, platform):
    """One locale's cell values and short field names keyed by (Entity Type, Localization Field), and the About item count."""
    try:
        payload, failures = storefront.platform_payload(fields, platform)
        if failures:
            raise ValueError(f'{code}: {failures}')
        items = about_items(fields, platform) if ABOUT_KEY in payload else []
    except KeyError as error:
        raise ValueError(f'{code}: catalog lacks field {error}; a stale catalog cannot fill the current Epic layout')
    unbound = sorted(set(payload) - {key for key, targets in FIELD_FAMILIES} - {ABOUT_KEY})
    if unbound:
        raise ValueError(f'platforms.json epic fields {unbound} have no template row mapping; extend FIELD_FAMILIES in epic_template.py')
    # The items must carry exactly the limit-checked description, whatever the line breaks between them.
    joined = '\n'.join(heading + '\n' + body for heading, body in items)
    if re.sub(r'\n+', '\n', joined) != re.sub(r'\n+', '\n', payload.get(ABOUT_KEY, '')):
        raise ValueError(f'{code}: About items do not reassemble into the composed {ABOUT_KEY}')
    values, names = {}, {}
    for key, targets in FIELD_FAMILIES:
        for target in targets if key in payload else ():
            values[target], names[target] = payload[key], key
    for number, item in enumerate(items):
        for entity in ABOUT_ENTITIES:
            for part, text in zip(ABOUT_PARTS, item):
                target = (entity, f'aboutItem.{number}.textBlock.{part}')
                values[target], names[target] = text, f'about_item_{number + 1}.{part}'
    return values, names, len(items)


def adapt(template_text, catalogs, platform, update_existing=False, update_english=False):
    rows = list(csv.reader(io.StringIO(template_text.lstrip('\ufeff'), newline='')))
    if not rows or rows[0][:7] != METADATA_COLUMNS or 'en' not in rows[0]:
        raise ValueError('Unexpected Epic template columns; download and inspect the current template')
    header = rows[0]
    if len(header) != len(set(header)):
        raise ValueError('Duplicate template columns')
    index = {name: i for i, name in enumerate(header)}
    locale_map = platform['locales']
    supported = {code: column for code, column in locale_map.items()
                 if code != 'en' and column in index}
    if len(set(supported.values())) != len(supported):
        raise ValueError('Canonical locales map to duplicate destination columns')
    canonical = {}
    for code in ['en', *supported]:
        if code not in catalogs:
            raise ValueError(f'{code}: no canonical catalog')
        canonical[code], names, about_count = canonical_rows(code, catalogs[code], platform)
    mapped = canonical['en']
    if any(values.keys() != mapped.keys() for values in canonical.values()):
        raise ValueError('Canonical catalogs expose different Epic fields; run storefront.py check first')
    prefix = platform.get('bullet_prefix', '• ')
    removed_columns = [column for column in header[7:]
                       if column != 'en' and column not in supported.values()]
    keep_indexes = [i for i, column in enumerate(header) if column not in removed_columns]
    result = [[header[i] for i in keep_indexes]]
    mapped_rows = 0
    invariant_rows = 0
    invariant_cells = 0
    invariant_filled = 0
    seen = set()
    matched = set()
    about_seen = {}
    english_stale, english_changed, conflicts, warnings = [], [], {}, []
    changed = {column: {'replaced': [], 'filled': [], 'fields': []} for column in sorted(supported.values())}
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
        key = (entity, field)
        label = f'{entity}/{field}'
        about = ABOUT_ROW.fullmatch(field) if entity in ABOUT_ENTITIES else None
        if key in mapped:
            if row[index['Field Type']] not in ('string', 'markdown'):
                raise ValueError(f'Row {number}: unexpected mapped field type')
            matched.add(key)
            if about:
                about_seen.setdefault(identity[:2], set()).add(field)
            if row[index['en']] != mapped[key]:
                if update_english:
                    row[index['en']] = mapped[key]
                    english_changed.append(label)
                else:
                    english_stale.append(f'row {number} {label} ({names[key]})')
            if row[index['Field Type']] != 'markdown' and any(line.startswith(prefix) for line in mapped[key].split('\n')):
                warnings.append(f'{label}: the canonical value holds a list but the row type is {row[index["Field Type"]]}; check how the list renders after import')
            for code, column in supported.items():
                existing, translated = row[index[column]], canonical[code][key]
                if existing == translated:
                    continue  # Identical saved translations are preserved.
                if existing and not update_existing:
                    conflicts.setdefault(column, []).append(f'row {number} {label}')
                    continue
                # Only mapped cells are written; every other cell of the column keeps its saved value.
                changed[column]['replaced' if existing else 'filled'].append(label)
                if names[key] not in changed[column]['fields']:
                    changed[column]['fields'].append(names[key])
                row[index[column]] = translated
            mapped_rows += 1
        elif about:
            raise ValueError(f'Row {number} {label}: the canonical layout has {about_count} About items; remove or reconcile the extra item in the console, then download a fresh template')
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
                invariant_filled += not existing
            invariant_rows += 1
        elif entity == 'Store Configs' and field in PRESERVED_CONFIGS:
            pass
        else:
            raise ValueError(f'Row {number}: unknown source row {entity}/{field}; explicit source review required')
        # IDs and field definitions retain exact values; unused blank locales are omitted.
        result.append([row[i] for i in keep_indexes])
    # A partly present About section would leave a listing that mixes this layout with an earlier one.
    for (entity, entity_id), fields in about_seen.items():
        missing = [field for other, field in mapped if other == entity and ABOUT_ROW.fullmatch(field) and field not in fields]
        if missing:
            raise ValueError(f'{entity}: template lacks About rows {missing} of the {about_count}-item canonical layout; create the missing items in the console, then download a fresh template')
    problems = []
    if english_stale:
        problems.append(f'English differs from canonical in {len(english_stale)} mapped row(s): {"; ".join(english_stale)}. Save the approved English in the console and download a fresh template, or rerun with --update-english to replace exactly those cells')
    if conflicts:
        cells = sum(len(found) for found in conflicts.values())
        columns = [column for column in header if column in conflicts]
        problems.append(f'{cells} existing translation(s) in {len(columns)} locale column(s) ({", ".join(columns)}) differ from the reviewed catalogs, first {columns[0]} {conflicts[columns[0]][0]}; reconcile before import, or rerun with --update-existing to replace exactly those mapped cells')
    if problems:
        raise ValueError('\n'.join(problems))
    present = {names[key] for key in matched}
    absent = list(dict.fromkeys(names[key] for key in mapped if names[key] not in present))
    if absent:
        warnings.append(f'Template has no row for canonical {", ".join(absent)}; not part of this import')
    stream = io.StringIO(newline='')
    csv.writer(stream, lineterminator='\r\n').writerows(result)
    report = {'mapped_rows': mapped_rows, 'about_items': about_count,
              'switches': platform.get('switches', {}),
              'translated_locale_count': len(supported),
              'translated_columns': sorted(supported.values()),
              'configured_locales_missing_from_template': sorted(
                  code for code, column in locale_map.items() if column not in index),
              'removed_unused_locale_columns': removed_columns,
              'translated_cells': mapped_rows * len(supported),
              'changed_cells': sum(len(found['replaced']) + len(found['filled']) for found in changed.values()),
              'changed_fields': changed,
              'english': {'status': 'updated' if english_changed else 'matches canonical', 'changed': english_changed},
              'warnings': warnings,
              'english_fallback_rows': invariant_rows,
              'english_fallback_cells': invariant_cells,
              'english_fallback_cells_filled': invariant_filled,
              'english_fallback_note': 'Existing identity, URLs and system requirements copied exactly; not localized technical prose.',
              'metadata_and_unmapped_cells_preserved': True,
              'publication_status': 'prepared only; import/save/server readback required'}
    return stream.getvalue(), report


def reviewed_catalogs(root, platform):
    """Every catalog once all are current and independently reviewed; otherwise a refusal naming the Epic locales that are not."""
    errors, catalogs = storefront.validate(root, require_review=True)
    if not errors:
        return catalogs
    source = storefront.read_fields(root / 'en.md')
    hashes = storefront.source_hashes(source)
    targets = [code for code in platform['locales'] if code != 'en']
    blocked = []
    for code in targets:
        try:
            fields = storefront.read_fields(root / f'{code}.md')
            if fields.keys() != source.keys() or storefront.check_review(root, code, fields, hashes):
                blocked.append(code)
        except (OSError, ValueError):
            blocked.append(code)
    scope = (f'{len(blocked)} of {len(targets)} Epic locales lack the current fields or a current independent review: {", ".join(blocked)}'
             if blocked else 'every Epic locale is current, but another catalog, the source hashes or a destination limit is not')
    raise ValueError(f'Review gate: nothing written; {scope}. {len(errors)} validation error(s), first: {errors[0]}\n'
                     'Full list: python3 translations/tools/storefront.py check --require-review')


def compact(fields):
    """Field names with whole About items collapsed into runs: about_item_1-8; a lone part stays about_item_3.body."""
    result = []
    for name in fields:
        item, dot, part = name.partition('.')
        if not dot or any(f'{item}.{other}' not in fields for other in ABOUT_PARTS):
            result.append(name)
        elif part == ABOUT_PARTS[0]:
            number = int(item.rsplit('_', 1)[1])
            run = re.fullmatch(r'about_item_(\d+)(?:-(\d+))?', result[-1]) if result else None
            if run and int(run[2] or run[1]) == number - 1:
                result[-1] = f'about_item_{run[1]}-{number}'
            else:
                result.append(item)
    return result


def summary(report):
    """The report with one line per locale column: cells changed and the canonical fields they belong to."""
    lines = {}
    for column, found in report['changed_fields'].items():
        lines[column] = (f'{len(found["replaced"])} replaced, {len(found["filled"])} filled: {", ".join(compact(found["fields"]))}'
                         if found['fields'] else 'already current')
    return dict(report, changed_fields=lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--template', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--root', type=Path, default=storefront.ROOT)
    parser.add_argument('--update-existing', action='store_true', help='Replace saved translations that differ from the reviewed catalogs, in mapped rows only; every other cell is kept')
    parser.add_argument('--update-english', action='store_true', help='Replace English that differs from canonical English, in mapped rows only, instead of stopping')
    args = parser.parse_args()
    try:
        if args.template.resolve() == args.out.resolve():
            raise ValueError('Output must differ from original downloaded template')
        platform = json.loads((args.root / 'platforms.json').read_text())['platforms']['epic']
        catalogs = reviewed_catalogs(args.root, platform)
        text, report = adapt(args.template.read_text(encoding='utf-8-sig'), catalogs, platform,
                             args.update_existing, args.update_english)
        with args.out.open('w', encoding='utf-8-sig', newline='') as stream:
            stream.write(text)  # Exact CRLF rows; Path.write_text takes newline only from Python 3.10.
        args.out.with_suffix(args.out.suffix + '.report.json').write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        # The adjacent report lists every changed row; the printed summary names fields per locale.
        print(json.dumps(summary(report), ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
