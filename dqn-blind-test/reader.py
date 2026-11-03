"""Minimal read-only MCP tensor reader. No model-supplied code or paths execute."""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np


def build_tools(shapes_only=False):
    annotations=dict(readOnlyHint=True,destructiveHint=False,idempotentHint=True,openWorldHint=False)
    tools = [dict(name="catalog", description="List anonymous tensor IDs, shapes, and dtypes. No connectivity or labels are supplied.", inputSchema={"type":"object","properties":{},"additionalProperties":False},annotations=annotations)]
    if shapes_only:
        return tools
    definitions = [
        ("statistics", "Exact descriptive statistics and quantiles of selected weight tensors; at most 16 per request.", {"ids":{"type":"array","items":{"type":"string"},"maxItems":16}}, ["ids"]),
        ("values", "Read raw numerical entries. Supply index with one integer or null per axis to slice (null keeps axis), or flat offset/count. At most 4096 values.", {"id":{"type":"string"},"index":{"type":"array","items":{"type":["integer","null"]}},"offset":{"type":"integer","minimum":0},"count":{"type":"integer","minimum":1,"maximum":4096}}, ["id"]),
        ("axis_statistics", "Summarize variation along an axis, plus pairwise slice cosine similarity when the axis has at most 8 entries. Useful for examining channel relationships.", {"id":{"type":"string"},"axis":{"type":"integer"}}, ["id","axis"]),
        ("singular_values", "SVD of the tensor reshaped to (shape[0], -1). Limited to 262144 elements and minimum matrix dimension <=512. Returns singular values, not a forward pass.", {"id":{"type":"string"}}, ["id"]),
    ]
    for name, desc, props, required in definitions:
        tools.append(dict(name=name,description=desc,inputSchema=dict(type="object",properties=props,required=required,additionalProperties=False),annotations=annotations))
    return tools


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--payload",required=True)
    p.add_argument("--audit",required=True)
    p.add_argument("--shapes-only",action="store_true")
    args=p.parse_args()
    # Payload is always an explicit operator-selected NPZ, never a model path.
    with np.load(args.payload,allow_pickle=False) as z:
        weights={k:np.array(z[k]) for k in z.files}
    catalog=[dict(id=k,shape=list(v.shape),dtype=str(v.dtype),elements=int(v.size)) for k,v in weights.items()]
    tool_specs=build_tools(args.shapes_only)
    allowed={t['name'] for t in tool_specs}
    calls=0

    def call(name,a):
        nonlocal calls
        calls+=1
        if calls>24:
            raise ValueError("The 24-call inspection budget is exhausted. Submit your final answer.")
        if name not in allowed:
            raise ValueError("Operation unavailable.")
        if name=="catalog":
            return dict(tensors=catalog,total_elements=sum(x['elements'] for x in catalog))
        if name=="statistics":
            if not 1<=len(a['ids'])<=16: raise ValueError("Choose 1 to 16 IDs.")
            out=[]
            for k in a['ids']:
                v=weights[k].astype(np.float64).ravel()
                out.append(dict(id=k,mean=float(v.mean()),std=float(v.std()),min=float(v.min()),max=float(v.max()),l2=float(np.linalg.norm(v)),zero_fraction=float(np.mean(v==0)),positive_fraction=float(np.mean(v>0)),quantiles=dict(zip(['p01','p10','p50','p90','p99'],np.quantile(v,[.01,.1,.5,.9,.99]).tolist()))))
            return out
        v=weights[a['id']]
        if name=="values":
            if 'index' in a:
                if len(a['index'])!=v.ndim: raise ValueError("Index rank must match tensor rank.")
                selected=v[tuple(slice(None) if i is None else int(i) for i in a['index'])]
            else:
                offset=int(a.get('offset',0)); count=int(a.get('count',64))
                if offset<0 or not 1<=count<=4096: raise ValueError("Invalid slice bounds.")
                selected=v.ravel()[offset:offset+count]
            if selected.size>4096: raise ValueError("Select at most 4096 entries.")
            return dict(id=a['id'],shape=list(selected.shape),values=selected.tolist())
        if name=="axis_statistics":
            axis=int(a['axis'])
            if not -v.ndim<=axis<v.ndim: raise ValueError("Invalid axis.")
            slices=np.moveaxis(v,axis,0).reshape(v.shape[axis],-1).astype(np.float64)
            if len(slices)>4096: raise ValueError("Axis too large.")
            norms=np.linalg.norm(slices,axis=1)
            out=dict(id=a['id'],axis=axis,means=slices.mean(axis=1).tolist(),stds=slices.std(axis=1).tolist(),l2=norms.tolist())
            if len(slices)<=8:
                unit=slices/np.maximum(norms[:,None],1e-100)
                out['cosine']= (unit@unit.T).tolist()
                out['relative_distance_to_slice0']=(np.linalg.norm(slices-slices[:1],axis=1)/max(norms[0],1e-100)).tolist()
            return out
        if name=="singular_values":
            if v.ndim<2: raise ValueError("Choose a matrix or higher-rank tensor.")
            m=v.reshape(v.shape[0],-1)
            if m.size>262144 or min(m.shape)>512: raise ValueError("Matrix exceeds SVD resource limit.")
            return dict(id=a['id'],matrix_shape=list(m.shape),singular_values=np.linalg.svd(m.astype(np.float64),compute_uv=False).tolist())
        raise ValueError("Unknown operation.")

    for line in sys.stdin:
        try:
            request=json.loads(line)
            method=request.get('method')
            if 'id' not in request: continue
            if method=='initialize':
                result=dict(protocolVersion=request.get('params',{}).get('protocolVersion','2024-11-05'),capabilities=dict(tools=dict(listChanged=False)),serverInfo=dict(name='tensors',version='1.0'))
            elif method=='tools/list': result=dict(tools=tool_specs)
            elif method=='tools/call':
                params=request['params']; started=time.time()
                try:
                    value=call(params['name'],params.get('arguments',{}))
                    text=json.dumps(value,allow_nan=False)
                    result=dict(content=[dict(type='text',text=text)],isError=False)
                except Exception as e:
                    # No tracebacks, file names, or host paths are exposed.
                    result=dict(content=[dict(type='text',text=f"Request rejected: {type(e).__name__}: {str(e) if isinstance(e,(ValueError,KeyError,IndexError)) else 'invalid tensor operation'}")],isError=True)
                record=dict(time=time.time(),request=params,result=result,seconds=time.time()-started)
                with open(args.audit,'a') as f: f.write(json.dumps(record)+'\n')
            elif method=='ping': result={}
            else:
                print(json.dumps(dict(jsonrpc='2.0',id=request['id'],error=dict(code=-32601,message='Method unavailable'))),flush=True)
                continue
            print(json.dumps(dict(jsonrpc='2.0',id=request['id'],result=result)),flush=True)
        except (json.JSONDecodeError,KeyError):
            continue


if __name__=='__main__': main()
