#!/usr/bin/env python3
"""Writes catalogue/manifest.json: a version stamp plus the SHA-256 and entry count of every file in index.json.
Apps compare `version` (or a file's sha256) with their cached copy and download only what changed.
Run after any generator: python3 tools/manifest.py"""
import hashlib, json, os, datetime
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
idx = json.load(open(os.path.join(CAT, 'index.json')))
files, total = {}, 0
for f in idx:
    raw = open(os.path.join(CAT, f), 'rb').read()
    n = len(json.loads(raw)); total += n
    files[f] = {'sha256': hashlib.sha256(raw).hexdigest(), 'entries': n, 'bytes': len(raw)}
digest = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()[:12]
m = {'schema': 1, 'version': digest,
     'updated': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
     'entries': total, 'files': files}
json.dump(m, open(os.path.join(CAT, 'manifest.json'), 'w'), indent=1)
print('manifest', digest, total, 'entries in', len(files), 'files')
