# -*- coding: utf-8 -*-
"""URL lookup for the Canada plan: pulls the exact URL from the research notes A-E so that no link is retyped.
U('key') returns the first URL in the notes that contains 'key' (raises if none)."""
import io, os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
_URLS = []
for fn in sorted(glob.glob(os.path.join(HERE, '[A-E]_*.md'))):
    txt = io.open(fn, encoding='utf-8').read()
    for u in re.findall(r'https?://[^\s|;<>"]+', txt):
        u = u.rstrip('.,)')
        if u not in _URLS:
            _URLS.append(u)


def U(key):
    for u in _URLS:
        if key in u:
            return u
    raise KeyError(f'no URL containing {key!r} in the research notes')
