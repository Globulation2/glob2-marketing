#!/usr/bin/env python3
"""Validate canonical Markdown and export review-gated storefront payloads.

No network, publishing, truncation, or application-language declarations.

Composition (platforms.json): a destination field is a list of paragraphs joined
by a blank line. A paragraph is a list of lines, or an object with "lines",
"bullets" and an optional "when"/"unless" switch. A line or bullet is a field
ID, a {"field": ID, "when"/"unless": switch} reference, or a list of those
joined into one line. Switches are declared per platform; a reference whose
switch is off is left out, and a destination field left empty is not exported.
A destination field may set "locale_overrides": {locale: {"paragraphs", "limit",
"length_unit"}}; those keys replace the field's own for that locale only.
"""
import argparse
from fnmatch import fnmatchcase
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CODES = 'ar pt-BR ca cs de da en es eo eu fa fr el hu it nl pl pt-PT ro ru sl sk sr-Cyrl fi sv tr zh-Hant zh-Hans uk id vi ja ko hi ur sw bn nb ms mr ta te fil bg th'.split()


def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def read_fields(path):
    text = path.read_text(encoding='utf-8')
    fields = {}
    matches = list(re.finditer(r'^## ([a-z][a-z0-9_]*)\s*$', text, re.M))
    for i, match in enumerate(matches):
        key = match.group(1)
        if key in fields:
            raise ValueError(f'{path}: duplicate field {key}')
        value = text[match.end():matches[i+1].start() if i+1 < len(matches) else len(text)].strip()
        if not value:
            raise ValueError(f'{path}: empty field {key}')
        if re.search(r'^#{1,6}\s', value, re.M):
            raise ValueError(f'{path}: nested/unrecognized heading in {key}')
        fields[key] = value
    if not fields:
        raise ValueError(f'{path}: no fields')
    return fields


def urls(value):
    return {url.rstrip('.,;:!?。；，！）)') for url in re.findall(r'https?://[^\s<>]+', value)}


def source_hashes(fields):
    return {key: digest(value) for key, value in fields.items()}


def ascii_digits(value):
    """Map every Unicode decimal digit to ASCII so protected numbers survive local numerals."""
    return ''.join(char if unicodedata.decimal(char, None) is None else str(unicodedata.decimal(char)) for char in value)


def enabled(item, switches):
    """True unless the item carries a when/unless switch that is off; undeclared switches are errors."""
    if not isinstance(item, dict): return True
    for key, wanted in (('when', True), ('unless', False)):
        name = item.get(key)
        if name is None: continue
        if name not in switches: raise ValueError(f'undeclared switch {name!r}; declare it in the platform switches')
        if bool(switches[name]) != wanted: return False
    return True


def join_inline(parts):
    """Join sentences into one line: a space, except after CJK sentence punctuation."""
    result = ''
    for part in parts:
        result += part if not result or result[-1] in '。！？' else ' ' + part
    return result


def resolve(fields, reference, switches):
    """Text of one line or bullet reference; an empty string when switched off."""
    if isinstance(reference, list):
        return join_inline([text for text in (resolve(fields, item, switches) for item in reference) if text])
    if isinstance(reference, dict):
        if set(reference) - {'field', 'when', 'unless'} or 'field' not in reference:
            raise ValueError(f'unsupported field reference {reference!r}')
        if not enabled(reference, switches): return ''
        reference = reference['field']
    return fields[reference]


def blocks(fields, spec, switches=None):
    """Resolve a paragraph list into [{'lines': [...], 'bullets': [...]}], dropping switched-off or empty paragraphs."""
    switches = switches or {}
    result = []
    for paragraph in spec:
        lines, bullets = paragraph, []
        if isinstance(paragraph, dict):
            if set(paragraph) - {'lines', 'bullets', 'when', 'unless'}:
                raise ValueError(f'unsupported paragraph keys {sorted(paragraph)}')
            if not enabled(paragraph, switches): continue
            lines, bullets = paragraph.get('lines', []), paragraph.get('bullets', [])
        block = {'lines': [text for text in (resolve(fields, item, switches) for item in lines) if text],
                 'bullets': [text for text in (resolve(fields, item, switches) for item in bullets) if text]}
        if block['lines'] or block['bullets']: result.append(block)
    return result


def referenced(spec):
    """Every catalog field ID a paragraph list can use, whatever its switches."""
    found = set()
    def walk(item):
        if isinstance(item, str): found.add(item)
        elif isinstance(item, list):
            for child in item: walk(child)
        elif isinstance(item, dict):
            for key in ('field', 'lines', 'bullets'):
                if key in item: walk(item[key])
    walk(spec)
    return found


def config_fields(config):
    """Catalog field IDs used by any destination, the AppStream fragments or image/video text."""
    found = set()
    for platform in config.get('platforms', {}).values():
        for spec in platform['fields'].values():
            found |= referenced(spec['paragraphs'])
            for override in spec.get('locale_overrides', {}).values(): found |= referenced(override.get('paragraphs', []))
    appstream = config.get('appstream')
    if appstream:
        found |= {'product_name', appstream['summary_field'], appstream.get('comment_field', 'headline')}
        found |= referenced(appstream['description_paragraphs']) | set(appstream.get('screenshot_captions', {}).values())
    assets = config.get('asset_text')
    if assets:
        for role in assets.get('screenshot_roles', []):
            found |= {assets[key].format(role=role) for key in ('overlay_fields', 'caption_fields') if key in assets}
        found |= set(assets.get('trailer_lines', [])) | set(assets.get('trailer_desktop_only_lines', []))
        if 'trailer_title' in assets: found.add(assets['trailer_title'])
    return found


def field_limit(rule, code):
    """The limit one field_limits rule sets for a locale: its script group's, else the rule's default."""
    groups = [name for name, group in rule.get('script_groups', {}).items() if code in group['locales']]
    if len(groups) > 1: raise ValueError(f'field_limits {rule["fields"]}: locale {code} is in more than one script group: {groups}')
    return rule['script_groups'][groups[0]]['limit'] if groups else rule['limit']


def field_limit_errors(config, code, fields):
    """Limits that bind in every locale (image overlays, captions, trailer text).

    A rule's "limit" is the default; "script_groups" may give listed locales their own limit.
    """
    errors = []
    for rule in config.get('field_limits', []):
        unit = rule.get('length_unit', 'character')
        if unit not in ('byte', 'character'): raise ValueError(f'field_limits: unsupported length_unit {unit!r}')
        limit = field_limit(rule, code)
        for key, value in fields.items():
            if not fnmatchcase(key, rule['fields']): continue
            measured = len(value.encode('utf-8')) if unit == 'byte' else len(value)
            if measured > limit:
                errors.append(f'{code}/{key}: {measured} {"UTF-8 bytes" if unit == "byte" else "characters"} exceeds {limit}; reviewed adaptation required')
    return errors


def validate_source(root=ROOT):
    """English-only check: the source parses, every destination composes within its limit, and no field is orphaned.

    Does not read locale catalogs, source hashes or reviews, so it can run while translations are stale.
    """
    source = read_fields(root / 'en.md')
    config = json.loads((root / 'platforms.json').read_text())
    errors = []
    if source.get('product_name') != 'Globulation 2': errors.append('en/product_name: protected product name changed')
    for key, value in source.items():
        if '\x00' in value or re.search(r'<[^>]+>', value): errors.append(f'en/{key}: NUL or raw HTML is not canonical plain text')
    errors.extend(field_limit_errors(config, 'en', source))
    used = config_fields(config)
    if used - source.keys(): errors.append(f'platforms.json references fields missing from en.md: {sorted(used - source.keys())}')
    if source.keys() - used: errors.append(f'en.md fields no destination uses: {sorted(source.keys() - used)}')
    if not used - source.keys():
        for platform_id, platform in config['platforms'].items():
            if 'en' not in platform['locales']: continue
            _, failures = platform_payload(source, platform, 'en')
            errors.extend(f'{platform_id}/en: {failure}' for failure in failures)
        if 'appstream' in config: blocks(source, config['appstream']['description_paragraphs'], config['appstream'].get('switches', {}))
    return errors, source


def check_review(root, code, fields, hashes):
    path = root / 'reviews' / f'{code}.json'
    if not path.exists():
        return [f'{code}: independent review missing']
    review = json.loads(path.read_text())
    errors = []
    if review.get('status') != 'reviewed' or review.get('issues') != []:
        errors.append(f'{code}: review incomplete or unresolved issues')
    if not review.get('reviewer') or review.get('reviewer') == review.get('translator'):
        errors.append(f'{code}: distinct translator/reviewer identities required')
    stale = [key for key, value in hashes.items() if review.get('source_hashes', {}).get(key) != value]
    if stale:
        errors.append(f'{code}: review source hashes stale: {stale}')
    changed = [key for key, value in source_hashes(fields).items() if review.get('translation_hashes', {}).get(key) != value]
    if changed:
        errors.append(f'{code}: reviewed translation hashes stale: {changed}')
    return errors


def validate(root=ROOT, require_review=False):
    errors = []
    source = read_fields(root / 'en.md')
    config = json.loads((root / 'platforms.json').read_text())
    hashes = source_hashes(source)
    missing = config_fields(config) - source.keys()
    if missing: errors.append(f'platforms.json references fields missing from en.md: {sorted(missing)}')
    hash_path = root / 'source-hashes.json'
    if not hash_path.exists() or json.loads(hash_path.read_text()) != hashes:
        errors.append('source-hashes.json missing or stale; run hashes after reviewing English source')
    catalogs = {}
    for code in CODES:
        try:
            fields = read_fields(root / f'{code}.md')
            catalogs[code] = fields
            if fields.keys() != source.keys():
                errors.append(f'{code}: missing {sorted(source.keys()-fields.keys())}; extra {sorted(fields.keys()-source.keys())}')
            for key, value in fields.items():
                if '\x00' in value or urls(value) != urls(source.get(key, '')):
                    errors.append(f'{code}/{key}: invalid NUL or changed URL')
                if key == 'product_name' and value != 'Globulation 2':
                    errors.append(f'{code}/{key}: protected product name changed')
                if re.search(r'<[^>]+>', value):
                    errors.append(f'{code}/{key}: raw HTML is not canonical plain text')
            # Terms that stay as written wherever the English field has them: names, protocol and licence
            # abbreviations, and verified counts and years (compared after mapping local numerals to ASCII).
            for term in config.get('protected_terms', []):
                for key, value in fields.items():
                    if term in source.get(key, '') and term not in ascii_digits(value):
                        errors.append(f'{code}/{key}: protected term {term} changed')
            errors.extend(field_limit_errors(config, code, fields))
            if require_review and code != 'en':
                errors.extend(check_review(root, code, fields, hashes))
        except (OSError, ValueError) as error:
            errors.append(str(error))
    if not errors:
        for platform_id, platform in config['platforms'].items():
            for code in platform['locales']:
                _, failures = platform_payload(catalogs[code], platform, code)
                errors.extend(f'{platform_id}/{code}: {failure}' for failure in failures)
    return errors, catalogs


def compose(fields, spec, switches=None, bullet_prefix='• '):
    """Plain text: lines and prefixed bullets joined with newline; paragraphs with a blank line."""
    return '\n\n'.join('\n'.join(block['lines'] + [bullet_prefix + item for item in block['bullets']])
                       for block in blocks(fields, spec, switches))


OVERRIDE_KEYS = {'paragraphs', 'limit', 'length_unit'}


def locale_spec(name, spec, code, locales=None):
    """A destination field's spec for one locale: a locale_overrides entry replaces paragraphs, limit or length_unit."""
    overrides = spec.get('locale_overrides', {})
    for locale, override in overrides.items():
        if not isinstance(override, dict) or not override or set(override) - OVERRIDE_KEYS:
            raise ValueError(f'{name}: locale_overrides[{locale!r}] may set only {sorted(OVERRIDE_KEYS)}')
        if locales is not None and locale not in locales:
            raise ValueError(f'{name}: locale_overrides names {locale!r}, which the platform does not map')
    return {**spec, **overrides[code]} if code in overrides else spec


def platform_payload(fields, platform, code=None):
    """Compose every destination field for one locale; code selects any locale_overrides (None: none apply)."""
    payload = {}
    errors = []
    switches = platform.get('switches', {})
    for name, spec in platform['fields'].items():
        spec = locale_spec(name, spec, code, platform.get('locales'))
        value = compose(fields, spec['paragraphs'], switches, platform.get('bullet_prefix', '• '))
        if not value: continue  # Every reference is switched off for this platform.
        unit = spec.get('length_unit', 'character')
        if unit not in ('byte', 'character'):
            raise ValueError(f'{name}: unsupported length_unit {unit!r}')
        measured = len(value.encode('utf-8')) if unit == 'byte' else len(value)
        label = 'UTF-8 bytes' if unit == 'byte' else 'characters'
        if spec.get('limit') is not None and measured > spec['limit']:
            errors.append(f'{name}: {measured} {label} exceeds {spec["limit"]}; reviewed adaptation required')
        payload[name] = value
    return payload, errors


def export(root, destination, require_review=True):
    if destination.exists() and any(destination.iterdir()):
        raise ValueError('Export destination must be empty; use a fresh directory to prevent stale locale payloads surviving configuration changes')
    errors, catalogs = validate(root, require_review)
    if errors:
        raise ValueError('\n'.join(errors))
    config = json.loads((root / 'platforms.json').read_text())
    pending = []
    prepared = []
    for platform_id, platform in config['platforms'].items():
        for code, fields in catalogs.items():
            mapping = platform['locales'].get(code)
            if mapping is None:
                pending.append({'platform': platform_id, 'locale': code, 'status': 'unsupported_or_unverified', 'action': 'retain existing English fallback'})
                continue
            payload, failures = platform_payload(fields, platform, code)
            if failures:
                errors.extend(f'{platform_id}/{code}: {failure}' for failure in failures)
            prepared.append((platform_id, mapping, code, payload, platform.get('mapping_status', 'requires_console_verification')))
    if errors:
        raise ValueError('\n'.join(errors))
    destination.mkdir(parents=True, exist_ok=True)
    for platform_id, mapping, code, payload, status in prepared:
        folder = destination / platform_id / mapping
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'listing.json').write_text(json.dumps({'canonical_locale': code, 'platform_locale': mapping, 'mapping_status': status, 'upload_eligible': False, 'eligibility_note': 'Preparation only: verify current console locale, editable state, exact destination fields, all scoped pending changes and saved value readback before applying.', 'source_hashes': source_hashes(catalogs['en']), 'translation_hashes': source_hashes(catalogs[code]), 'fields': payload}, ensure_ascii=False, indent=2) + '\n')
        if platform_id == 'fastlane':
            for field in ('title', 'short_description', 'full_description'):
                (folder / f'{field}.txt').write_text(payload[field] + '\n', encoding='utf-8')
    # AppStream elements are fragments to merge into maintained metadata, not a replacement component.
    appstream = config['appstream']
    component = ET.Element('component')
    description = ET.SubElement(component, 'description')
    captions = ET.SubElement(component, 'screenshots')
    def localized(parent, tag, code, text, **attributes):
        item = ET.SubElement(parent, tag, attributes)
        if code != 'en': item.set('{http://www.w3.org/XML/1998/namespace}lang', config['upstream_locales'][code])
        item.text = text
    # Paragraph by paragraph, English first: a heading and its body share one <p> per locale;
    # a bullet list is one <ul> with an <li> per bullet per locale.
    order = sorted(catalogs, key=lambda code: code != 'en')
    composed = {code: blocks(catalogs[code], appstream['description_paragraphs'], appstream.get('switches', {})) for code in order}
    for index in range(len(composed['en'])):
        for code in order:
            if composed[code][index]['lines']: localized(description, 'p', code, join_inline(composed[code][index]['lines']))
        if composed['en'][index]['bullets']:
            items = ET.SubElement(description, 'ul')
            for code in order:
                for bullet in composed[code][index]['bullets']: localized(items, 'li', code, bullet)
    for code, fields in catalogs.items():
        for tag, key in [('name', 'product_name'), ('summary', appstream['summary_field'])]:
            localized(component, tag, code, fields[key])
        for role, key in appstream.get('screenshot_captions', {}).items():
            # Merge captions into the matching screenshot nodes by role; images are not changed.
            localized(captions, 'caption', code, fields[key], source_role=role)
    ET.indent(component)
    (destination / 'appstream-fragment.xml').write_text(ET.tostring(component, encoding='unicode') + '\n')
    desktop = ['[Desktop Entry]']
    for code, fields in catalogs.items():
        suffix = '' if code == 'en' else f'[{config["upstream_locales"][code]}]'
        desktop.append(f'Name{suffix}={fields["product_name"]}')
        desktop.append(f'Comment{suffix}={fields[appstream.get("comment_field", "headline")]}')
    (destination / 'desktop-fragment.ini').write_text('\n'.join(desktop) + '\n')
    (destination / 'export-manifest.json').write_text(json.dumps({'upload_eligible': False, 'source_hashes': source_hashes(catalogs['en']), 'translation_hashes': {code: source_hashes(fields) for code, fields in catalogs.items()}, 'notes': ['All artifacts are merge/preparation inputs, not replacement manifests or upload permission. Verify current platform constraints and review state. AppStream captions carry source_role annotations to merge into approved existing screenshot nodes; do not upload fragment as a complete component.']}, indent=2) + '\n')
    (destination / 'unsupported.json').write_text(json.dumps(pending, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check', 'check-source', 'hashes', 'export', 'review-record'])
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--require-review', action='store_true')
    parser.add_argument('--allow-unreviewed', action='store_true', help='Internal QA export only; not eligible for upload')
    parser.add_argument('--locale', choices=CODES)
    parser.add_argument('--translator')
    parser.add_argument('--reviewer')
    args = parser.parse_args()
    try:
        if args.command == 'hashes':
            (args.root / 'source-hashes.json').write_text(json.dumps(source_hashes(read_fields(args.root / 'en.md')), indent=2) + '\n')
        elif args.command == 'review-record':
            if not args.locale or not args.translator or not args.reviewer or args.translator == args.reviewer:
                raise ValueError('Provide locale and distinct translator/reviewer identities; use only after actual independent review')
            record = {'status': 'reviewed', 'translator': args.translator, 'reviewer': args.reviewer, 'method': 'AI translation with independent AI linguistic review; not human/native-speaker validation', 'issues': [], 'source_hashes': source_hashes(read_fields(args.root / 'en.md')), 'translation_hashes': source_hashes(read_fields(args.root / f'{args.locale}.md'))}
            (args.root / 'reviews').mkdir(exist_ok=True)
            (args.root / 'reviews' / f'{args.locale}.json').write_text(json.dumps(record, indent=2) + '\n')
        elif args.command == 'check-source':
            errors, source = validate_source(args.root)
            if errors: raise ValueError('\n'.join(errors))
            print(f'English source: {len(source)} fields compose within every mapped destination limit (locale catalogs, hashes and reviews not checked)')
        elif args.command == 'check':
            errors, catalogs = validate(args.root, args.require_review)
            if errors: raise ValueError('\n'.join(errors))
            print(f'Validated {len(catalogs)} canonical locales' + (' with independent reviews' if args.require_review else ' (review gate not requested)'))
        else:
            if args.out is None: raise ValueError('--out is required; use an ignored/local temporary directory')
            export(args.root, args.out, not args.allow_unreviewed)
            print(f'Exported to {args.out}; generated payloads are not publication evidence')
    except (OSError, ValueError, KeyError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
