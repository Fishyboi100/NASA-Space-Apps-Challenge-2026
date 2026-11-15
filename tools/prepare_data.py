"""Build Ember's packed data file from NASA FIRMS archive downloads.

Usage:  python prepare_data.py <folder with FIRMS CSVs> ../data/california.b64.txt

The folder can hold the archive (fire_archive_*.csv) and near-real-time (fire_nrt_*.csv)
files for MODIS C6.1 and VIIRS S-NPP / NOAA-20 / NOAA-21 375 m. Every detection is kept;
values are stored compactly (location to ~8 m, fire power to 0.1%), gzipped, then base64
encoded so any web host can serve the file as plain text.
"""
import base64, glob, gzip, json, os, struct, sys
import numpy as np, pandas as pd

def load(folder):
    frames = []
    for f in sorted(glob.glob(os.path.join(folder, '**', '*.csv'), recursive=True)):
        d = pd.read_csv(f, dtype={'acq_time': str, 'confidence': str, 'satellite': str})
        if 'type' not in d: d['type'] = -1  # near-real-time files carry no source type
        frames.append(d[['latitude', 'longitude', 'acq_date', 'acq_time', 'satellite', 'confidence', 'frp', 'daynight', 'type']])
    d = pd.concat(frames, ignore_index=True)
    d['s'] = d['satellite'].map({'Terra': 0, 'T': 0, 'Aqua': 1, 'A': 1, 'SNPP': 2, 'N': 2, 'N20': 3, '1': 3, 'N21': 4, '2': 4})
    d = d[d['s'].notna()].copy(); d['s'] = d['s'].astype('int8')
    num = pd.to_numeric(d['confidence'], errors='coerce'); c = d['confidence'].astype(str)
    d['conf'] = np.where(num.notna(), np.where(num >= 80, 2, np.where(num >= 30, 1, 0)),
                         np.where(c.str.startswith('h'), 2, np.where(c.str.startswith('l'), 0, 1))).astype('int8')
    d['dn'] = (d['daynight'] == 'N').astype('int8')
    d['date'] = pd.to_datetime(d['acq_date'])
    return d.sort_values(['date', 's', 'acq_time']).reset_index(drop=True)

def pack(d, label):
    lat0, lat1 = d.latitude.min() - 0.01, d.latitude.max() + 0.01
    lon0, lon1 = d.longitude.min() - 0.01, d.longitude.max() + 0.01
    q = lambda v, a, b: np.clip(np.round((v - a) / (b - a) * 65535), 0, 65535).astype('<u2')
    typ = d['type'].values
    meta = (d.s.values.astype('u1') | (d.dn.values.astype('u1') << 3) | (d.conf.values.astype('u1') << 4)
            | (np.isin(typ, [1, 2, 3]).astype('u1') << 6) | ((typ == -1).astype('u1') << 7)).astype('u1')
    hdr = dict(v=1, n=len(d), lat=[float(lat0), float(lat1)], lon=[float(lon0), float(lon1)], frpScale=5000, label=label,
               requested=str(d['date'].max().date()), source='NASA FIRMS archive download (MODIS C6.1, VIIRS 375 m C2)')
    hb = json.dumps(hdr).encode()
    cols = [q(d.latitude.values, lat0, lat1), q(d.longitude.values, lon0, lon1),
            ((d['date'] - pd.Timestamp('2000-01-01')).dt.days).astype('<u2').values,
            pd.to_numeric(d['acq_time'], errors='coerce').fillna(0).astype('<u2').values,
            np.clip(np.round(np.log1p(np.clip(d.frp.values, 0, None)) * 5000), 0, 65535).astype('<u2'), meta]
    pad = b'\0' * ((4 - (4 + len(hb)) % 4) % 4)
    return struct.pack('<I', len(hb)) + hb + pad + b''.join(c.tobytes() for c in cols)

if __name__ == '__main__':
    d = load(sys.argv[1])
    blob = gzip.compress(pack(d, 'California (state boundary + 15 km buffer)'), 9)
    open(sys.argv[2], 'w').write(base64.b64encode(blob).decode())
    print(f'{len(d):,} detections -> {sys.argv[2]}')
