"""Operator-only preparation; its metadata never enters a model session."""
import argparse
import hashlib
import json
import random
import struct
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parent



def load(path):
    if path.suffix=='.npz':
        with np.load(path,allow_pickle=False) as z:
            return {k:np.array(z[k]) for k in z.files}
    raw=path.read_bytes()
    n=struct.unpack('<Q',raw[:8])[0]
    header=json.loads(raw[8:8+n])
    dtypes={'F32':'<f4','F16':'<f2','F64':'<f8','I64':'<i8','I32':'<i4'}
    out={}
    for k,v in header.items():
        if k=='__metadata__': continue
        start,end=v['data_offsets']
        out[k]=np.frombuffer(raw[8+n+start:8+n+end],dtype=dtypes[v['dtype']]).reshape(v['shape']).copy()
    return out


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",required=True,type=Path,help="DQN repository weights directory")
    args=parser.parse_args()
    source=args.source.expanduser().resolve()
    (ROOT/'operator').mkdir(exist_ok=True)
    (ROOT/'payloads').mkdir(exist_ok=True)
    rng=random.Random(20261103)
    paths=sorted(source.rglob('epoch_200.safetensors'))
    assert len(paths)==3, 'This pilot expects exactly the three epoch-200 game checkpoints.'
    rng.shuffle(paths)
    manifest=[]
    for i,path in enumerate(paths,1):
        label=f'sample_{i:02d}'
        weights=load(path)
        names=sorted(weights)
        anonymous={f't{j:03d}':weights[k] for j,k in enumerate(names)}
        target=ROOT/'payloads'/f'{label}.npz'
        np.savez(target,**anonymous)
        for original,exported in zip((weights[k] for k in names),anonymous.values()):
            assert original.dtype==exported.dtype and original.shape==exported.shape
            assert original.tobytes()==exported.tobytes()
        record=dict(id=label,source=str(path),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),payload_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),tensor_map=dict(zip(anonymous,names)),tensor_count=len(weights),total_elements=sum(v.size for v in weights.values()))
        record['game']=path.parent.name.removesuffix('NoFrameskip-v4')
        manifest.append(record)
        print(label,len(weights),record['total_elements'],path.parent.name,flush=True)
    (ROOT/'operator'/'manifest.json').write_text(json.dumps(manifest,indent=2))


if __name__=='__main__': main()
