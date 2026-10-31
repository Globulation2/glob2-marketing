#!/usr/bin/env python3
"""Validate canonical Markdown and export review-gated storefront payloads.

No network, publishing, truncation, or application-language declarations.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CODES = 'ar pt-BR ca cs de da en es eo eu fa fr el hu it nl pl pt-PT ro ru sl sk sr-Cyrl fi sv tr zh-Hant zh-Hans uk id vi ja ko'.split()


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
    hashes = source_hashes(source)
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
            protected = {'screenshot_caption_battle': 'River', 'screenshot_caption_strategic': 'Four Squares', 'screenshot_caption_terrain': 'Lava Shield'}
            for key, term in protected.items():
                if key in fields and term in source.get(key, '') and term not in fields[key]:
                    errors.append(f'{code}/{key}: protected map name {term} changed')
            if require_review and code != 'en':
                errors.extend(check_review(root, code, fields, hashes))
        except (OSError, ValueError) as error:
            errors.append(str(error))
    return errors, catalogs


def compose(fields, spec):
    """A paragraph is a list of field IDs, joined with newline; paragraphs use blank line."""
    return '\n\n'.join('\n'.join(fields[key] for key in paragraph) for paragraph in spec)


def platform_payload(fields, platform):
    payload = {}
    errors = []
    for name, spec in platform['fields'].items():
        value = compose(fields, spec['paragraphs'])
        if spec.get('limit') is not None and len(value) > spec['limit']:
            errors.append(f'{name}: {len(value)} characters exceeds {spec["limit"]}; reviewed adaptation required')
        payload[name] = value
    return payload, errors


def export(root, destination, require_review=True):
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
            payload, failures = platform_payload(fields, platform)
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
    component = ET.Element('component')
    description = ET.SubElement(component, 'description')
    captions = ET.SubElement(component, 'screenshots')
    for code, fields in catalogs.items():
        lang = config['upstream_locales'][code]
        for tag, key in [('name', 'product_name'), ('summary', 'appstream_summary')]:
            item = ET.SubElement(component, tag)
            if code != 'en': item.set('{http://www.w3.org/XML/1998/namespace}lang', lang)
            item.text = fields[key]
        for paragraph in config['description_paragraphs']:
            item = ET.SubElement(description, 'p')
            if code != 'en': item.set('{http://www.w3.org/XML/1998/namespace}lang', lang)
            item.text = ' '.join(fields[key] for key in paragraph)
        for role in ('colony', 'battle', 'strategic', 'terrain'):
            # Merge captions into matching existing screenshot nodes; images are not changed.
            item = ET.SubElement(captions, 'caption', {'source_role': role})
            if code != 'en': item.set('{http://www.w3.org/XML/1998/namespace}lang', lang)
            item.text = fields[f'screenshot_caption_{role}']
    ET.indent(component)
    (destination / 'appstream-fragment.xml').write_text(ET.tostring(component, encoding='unicode') + '\n')
    desktop = ['[Desktop Entry]']
    for code, fields in catalogs.items():
        suffix = '' if code == 'en' else f'[{config["upstream_locales"][code]}]'
        desktop.append(f'Name{suffix}={fields["product_name"]}')
        desktop.append(f'Comment{suffix}={fields["headline"]}')
    (destination / 'desktop-fragment.ini').write_text('\n'.join(desktop) + '\n')
    (destination / 'export-manifest.json').write_text(json.dumps({'upload_eligible': False, 'source_hashes': source_hashes(catalogs['en']), 'translation_hashes': {code: source_hashes(fields) for code, fields in catalogs.items()}, 'notes': ['All artifacts are merge/preparation inputs, not replacement manifests or upload permission. Verify current platform constraints and review state. AppStream captions carry source_role annotations to merge into approved existing screenshot nodes; do not upload fragment as a complete component.']}, indent=2) + '\n')
    (destination / 'unsupported.json').write_text(json.dumps(pending, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check', 'hashes', 'export', 'review-record'])
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
