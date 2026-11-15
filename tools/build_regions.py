# Build the packed data files for Texas, Chile, Portugal and Greece from FIRMS downloads.
# Usage: python build_regions.py <folder with the unzipped DL_FIRE_* folders> <output data folder> [region ...]
# (the request numbers 85041x-85043x and 85102x are this team's FIRMS orders; change them for your own)
import sys, gzip, base64, glob, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prepare_data import load, pack
R = {
 'chile':    ('41', 'Chile, mainland (FIRMS country file; Easter Island and Juan Fernández left out)', lambda d: d[d.longitude >= -76]),
 'portugal': ('42', 'Portugal, mainland (FIRMS country file; Azores and Madeira left out)', lambda d: d[(d.longitude >= -9.8) & (d.latitude >= 36.8)]),
 'greece':   ('43', 'Greece (FIRMS country file, including the islands)', lambda d: d),
 'texas':    ('102', 'Texas (FIRMS US state download)', lambda d: d),
}
ONLY = sys.argv[3:] or list(R)
for rid, (g, label, clip) in [(k, R[k]) for k in ONLY]:
    tmp = os.path.join(sys.argv[1], 'work', rid)
    os.makedirs(tmp, exist_ok=True)
    for f in glob.glob(os.path.join(sys.argv[1], f'*_85{g}?' if len(g) == 3 else f'*_850{g}?', '*.csv')):
        dst = os.path.join(tmp, os.path.basename(f))
        if not os.path.exists(dst): os.symlink(f, dst)
    d = load(tmp); n0 = len(d); d = clip(d).reset_index(drop=True)
    blob = gzip.compress(pack(d, label), 9)
    out = os.path.join(sys.argv[2], f'{rid}.b64.txt')
    open(out, 'w').write(base64.b64encode(blob).decode())
    print(rid, f'{n0:,} -> {len(d):,}', d.groupby('s').size().to_dict(), d.date.min().date(), d.date.max().date(), os.path.getsize(out)//1024, 'KB')
