#!/usr/bin/env python3
"""Download the caption fonts listed in fonts.json into .cache/fonts/ (not committed).

Standard library only. Every file is pinned to a commit or release in fonts.json and
checked against its recorded sha256; a mismatch is an error and the file is not kept.
Run `fetch_fonts.py --record` only when deliberately changing a pinned source: it
downloads without checking and writes the new hashes into fonts.json for review.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import sys
import urllib.parse
import urllib.request
import zipfile

HERE = Path(__file__).resolve().parent
CONFIG = HERE / 'fonts.json'
CACHE = HERE / '.cache' / 'fonts'


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def download(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'font-fetch'})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def url_for(config, font, path):
    return config['sources'][font['source']] + urllib.parse.quote(path)


def fetch(config, name, font, record):
    """Return {key: sha256} changes to record; raise ValueError on a hash mismatch."""
    target = CACHE / font['file']
    licence_target = CACHE / font['licence_file']
    changes = {}
    if not record and target.exists() and licence_target.exists() and sha256(target.read_bytes()) == font['sha256']:
        return changes
    raw = download(url_for(config, font, font['path']))
    licence = None
    if 'member' in font:
        # An archive: check the archive itself, then read the two members without extracting anything else.
        if record: changes['archive_sha256'] = sha256(raw)
        elif sha256(raw) != font['archive_sha256']:
            raise ValueError(f'{name}: archive sha256 {sha256(raw)} does not match fonts.json')
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            data = archive.read(font['member'])
            licence = archive.read(font['licence_member'])
    else:
        data = raw
        licence = download(url_for(config, font, font['licence_path']))
    if record: changes['sha256'] = sha256(data)
    elif sha256(data) != font['sha256']:
        raise ValueError(f'{name}: sha256 {sha256(data)} does not match fonts.json')
    CACHE.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    licence_target.write_bytes(licence)
    print(f'fetched {name}: {font["file"]} ({len(data):,} bytes)')
    return changes


def missing(config=None):
    """Names of fonts whose cached file is absent or does not match its pinned sha256."""
    config = config or json.loads(CONFIG.read_text())
    return [name for name, font in config['fonts'].items()
            if not (CACHE / font['file']).exists() or sha256((CACHE / font['file']).read_bytes()) != font['sha256']]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', action='store_true', help='write downloaded hashes into fonts.json instead of checking them')
    args = parser.parse_args()
    config = json.loads(CONFIG.read_text())
    failed = False
    for name, font in config['fonts'].items():
        try:
            font.update(fetch(config, name, font, args.record))
        except (OSError, ValueError, KeyError) as error:
            print(f'error: {error}', file=sys.stderr)
            failed = True
    if args.record and not failed:
        text = CONFIG.read_text()
        for name, font in json.loads(text)['fonts'].items():
            for key in ('sha256', 'archive_sha256'):
                if key in font and config['fonts'][name][key] != font[key]:
                    # Replace only this font's value so the hand-formatted file keeps its layout.
                    start = text.index(json.dumps(name) + ': {')
                    at = text.index(f'"{key}": "{font[key]}"', start)
                    text = text[:at] + f'"{key}": "{config["fonts"][name][key]}"' + text[at + len(f'"{key}": "{font[key]}"'):]
        CONFIG.write_text(text)
        print('recorded hashes in fonts.json; review the diff')
    if failed: return 1
    print(f'{len(config["fonts"])} fonts ready in {CACHE}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
