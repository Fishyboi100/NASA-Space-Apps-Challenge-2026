# Usage: python verify_regions.py <folder with the FIRMS zips> <app data folder>
# Independent check: every detection in the user's original FIRMS zip files is in the app's packed data file,
# with the same date, time, satellite, day/night, confidence class and static-source flag, and with position and
# fire power equal within the packing precision. Reads the zips directly with the csv module (no pandas, no shared code).
import base64, csv, glob, gzip, io, json, math, os, struct, sys, zipfile
from collections import Counter
from datetime import date, timedelta

UP = sys.argv[1] + '/' if len(sys.argv) > 1 else './'  # folder with the FIRMS zip files
DATA = sys.argv[2] if len(sys.argv) > 2 else '../data'
REG = {
    'california': ('85006[4-7]', None, 'California'),
    'chile': ('85041[2-5]', lambda la, lo: lo >= -76, 'Chile'),
    'portugal': ('85042[4-7]', lambda la, lo: lo >= -9.8 and la >= 36.8, 'Portugal'),
    'greece': ('85043[3-6]', None, 'Greece'),
    'texas': ('85102[0-3]', None, 'Texas'),
}
SAT = {'Terra': 0, 'T': 0, 'Aqua': 1, 'A': 1, 'SNPP': 2, 'N': 2, 'N20': 3, '1': 3, 'N21': 4, '2': 4}
D0 = date(2000, 1, 1)

def conf_class(c):
    try:
        v = float(c); return 2 if v >= 80 else 1 if v >= 30 else 0
    except ValueError:
        return 2 if c.startswith('h') else 0 if c.startswith('l') else 1

def original(pattern, keep):
    rows, files = [], []
    for z in sorted(glob.glob(UP + '*DL_FIRE_*_' + pattern + '.zip')):
        with zipfile.ZipFile(z) as zf:
            for name in zf.namelist():
                if not name.endswith('.csv'): continue
                files.append(name)
                for r in csv.DictReader(io.TextIOWrapper(zf.open(name), encoding='utf-8')):
                    la, lo = float(r['latitude']), float(r['longitude'])
                    if keep and not keep(la, lo): continue
                    typ = int(r['type']) if r.get('type') not in (None, '') else -1
                    d = (date.fromisoformat(r['acq_date']) - D0).days
                    rows.append((d, SAT[r['satellite']], int(r['acq_time']), la, lo, float(r['frp']),
                                 conf_class(r['confidence']), 1 if r['daynight'] == 'N' else 0, 1 if typ in (1, 2, 3) else 0, 1 if typ == -1 else 0))
    return rows, files

def packed(path):
    raw = gzip.decompress(base64.b64decode(open(path).read()))
    hl = struct.unpack('<I', raw[:4])[0]; h = json.loads(raw[4:4 + hl]); off = 4 + hl; off += (4 - off % 4) % 4
    n = h['n']; col = lambda k, fmt, size: struct.unpack_from('<%d%s' % (n, fmt), raw, off + k)
    lat = col(0, 'H', 2); lon = col(2 * n, 'H', 2); day = col(4 * n, 'H', 2); tm = col(6 * n, 'H', 2); frp = col(8 * n, 'H', 2); meta = col(10 * n, 'B', 1)
    (a0, a1), (b0, b1) = h['lat'], h['lon']
    out = [(day[i], meta[i] & 7, tm[i], a0 + lat[i] / 65535 * (a1 - a0), b0 + lon[i] / 65535 * (b1 - b0), math.expm1(frp[i] / h['frpScale']),
            (meta[i] >> 4) & 3, (meta[i] >> 3) & 1, (meta[i] >> 6) & 1, (meta[i] >> 7) & 1) for i in range(n)]
    return out, h

report = {}
for rid, (pat, keep, name) in REG.items():
    orig, files = original(pat, keep)
    pk, h = packed(os.path.join(DATA, f'{rid}.b64.txt'))
    (a0, a1), (b0, b1) = h['lat'], h['lon']
    q = lambda v, x0, x1: min(65535, max(0, round((v - x0) / (x1 - x0) * 65535)))
    fq = lambda f: min(65535, max(0, round(math.log1p(max(f, 0)) * h['frpScale'])))
    # the original rows put through the documented packing, compared as whole records (a multiset, so order is irrelevant)
    O = Counter((r[0], r[1], r[2], q(r[3], a0, a1), q(r[4], b0, b1), fq(r[5]), r[6], r[7], r[8], r[9]) for r in orig)
    P = Counter((r[0], r[1], r[2], round((r[3] - a0) / (a1 - a0) * 65535), round((r[4] - b0) / (b1 - b0) * 65535), round(math.log1p(r[5]) * h['frpScale']), r[6], r[7], r[8], r[9]) for r in pk)
    bad = Counter()
    if len(orig) != len(pk): bad['row count'] = abs(len(orig) - len(pk))
    diff = (O - P) + (P - O)
    if diff: bad['records not matching exactly'] = sum(diff.values())
    maxla = (a1 - a0) / 65535 / 2; maxlo = (b1 - b0) / 65535 / 2
    o = orig
    sats = Counter(r[1] for r in o)
    report[rid] = dict(files=len(files), original_rows=len(o), app_rows=len(pk),
                       per_satellite={['Terra', 'Aqua', 'S-NPP', 'NOAA-20', 'NOAA-21'][k]: v for k, v in sorted(sats.items())},
                       first=str(D0 + timedelta(min(r[0] for r in o))), last=str(D0 + timedelta(max(r[0] for r in o))),
                       position_precision_deg=(round(maxla, 6), round(maxlo, 6)), position_precision_m=round(max(maxla, maxlo) * 111320, 1), fire_power_precision='0.01%', problems=dict(bad) or 'none')
    print(rid, json.dumps(report[rid]), flush=True)
json.dump(report, open('verify_report.json', 'w'), indent=1)
