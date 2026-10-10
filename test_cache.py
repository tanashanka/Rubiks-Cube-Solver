##### Tests for the tables cache helpers in build_tables.py #####
import os
import pickle
import subprocess
import sys
import tempfile

import build_tables
from build_tables import Tables, load_cache, save_cache, cache_path


def fake_tables(value=0):
    """Ten small stand-in tables, so these tests don't need the real (slow) ones."""
    return Tables(*[[[value + i, value + i + 1], [value + i]] for i in range(10)])


def new_path():
    return os.path.join(tempfile.mkdtemp(), 'tables_cache.pkl')


def test_missing_file_gives_none():
    return [] if load_cache(new_path()) is None else ["a missing file was not treated as no cache"]


def test_roundtrip():
    p = new_path()
    t = fake_tables()
    save_cache(p, t)
    loaded = load_cache(p)
    failures = []
    if loaded != t:
        failures.append("loaded tables differ from the saved ones")
    if not isinstance(loaded, Tables):
        failures.append(f"loaded object is a {type(loaded).__name__}, not Tables")
    if os.path.exists(p + '.tmp'):
        failures.append("temporary file was left behind")
    return failures


def test_cache_does_not_depend_on_the_tables_class():
    """The file must hold only plain data. If it recorded a reference to Tables
    (for example as __main__.Tables), it could not be loaded by a different program,
    such as the packaged .exe."""
    p = new_path()
    save_cache(p, fake_tables())
    raw = open(p, 'rb').read()
    failures = []
    if b'Tables' in raw or b'__main__' in raw:
        failures.append("the cache file refers to a class by name")
    here = os.path.dirname(os.path.abspath(build_tables.__file__))
    script = (f"import sys; sys.path.insert(0, {here!r}); import build_tables as b; "
              f"t = b.load_cache({p!r}); print(t is not None)")
    out = subprocess.run([sys.executable, '-c', script], capture_output=True, text=True).stdout.strip()
    if out != 'True':
        failures.append(f"a separate process could not load the cache (printed {out!r})")
    return failures


def test_unusable_files_are_ignored():
    """A damaged or out-of-date cache must mean 'rebuild', never a crash."""
    p = new_path()
    save_cache(p, fake_tables())
    good = open(p, 'rb').read()
    failures = []

    def write(content):
        with open(p, 'wb') as f:
            f.write(content)

    cases = {
        "garbage": b"not a pickle",
        "empty": b"",
        "truncated": good[:20],
        "wrong version": pickle.dumps({'version': build_tables.CACHE_VERSION + 1,
                                       'tables': tuple(fake_tables())}),
        "wrong table count": pickle.dumps({'version': build_tables.CACHE_VERSION, 'tables': (1, 2, 3)}),
        "old bare format": pickle.dumps(tuple(fake_tables())),
    }
    for label, content in cases.items():
        write(content)
        try:
            result = load_cache(p)
        except Exception as e:
            failures.append((label, f"raised {e!r}"))
            continue
        if result is not None:
            failures.append((label, "was accepted"))
    return failures


def test_saving_again_replaces_the_cache():
    p = new_path()
    save_cache(p, fake_tables(0))
    new = fake_tables(100)
    save_cache(p, new)
    return [] if load_cache(p) == new else ["the old cache was not replaced"]


def test_cache_path():
    failures = []
    old = os.environ.get('LOCALAPPDATA')
    folder = tempfile.mkdtemp()
    try:
        os.environ['LOCALAPPDATA'] = folder
        p = cache_path()
        if p != os.path.join(folder, 'CubeSolver', 'tables_cache.pkl'):
            failures.append(f"unexpected path {p}")
        if not os.path.isdir(os.path.dirname(p)):
            failures.append("the folder was not created")
    finally:
        if old is None:
            os.environ.pop('LOCALAPPDATA', None)
        else:
            os.environ['LOCALAPPDATA'] = old
    return failures


if __name__ == "__main__":
    tests = [
        ("missing file -> no cache", test_missing_file_gives_none),
        ("save then load gives the same tables", test_roundtrip),
        ("cache holds plain data and loads in another process", test_cache_does_not_depend_on_the_tables_class),
        ("damaged or old caches are ignored", test_unusable_files_are_ignored),
        ("saving again replaces the cache", test_saving_again_replaces_the_cache),
        ("cache_path uses LOCALAPPDATA/CubeSolver", test_cache_path),
    ]
    total_failures = 0
    for name, fn in tests:
        failures = fn()
        total_failures += len(failures)
        print(f"{name}: {'PASS' if not failures else f'FAIL ({len(failures)})'}")
        if failures:
            print(f"  details: {failures[:3]}")
    print()
    print("All tests passed!" if total_failures == 0 else f"{total_failures} total failures -- see above.")