"""Independent exhaustive count-probe optimizer over supplied small posets.

It evaluates counter values on every ideal; it does not use the coloring
criterion to decide whether a probe family is sufficient.
"""
from __future__ import annotations
import itertools
import json
import time
from pathlib import Path


def verify(record:dict)->dict:
    started=time.monotonic()
    n=record['points'];assert type(n)is int and 1<=n<=4
    rows=record['upper_sets'];assert len(rows)==n
    relation={(i,j) for i in range(n) for j in range(n) if rows[i]>>j&1}
    assert all((i,i)in relation for i in range(n))
    assert all(i==j or (j,i)not in relation for i,j in relation)
    assert all((a,d)in relation for a,b in relation for c,d in relation if b==c)
    ideals=[s for s in range(1<<n) if all(not(s>>b&1) or s>>a&1 for a,b in relation)]
    perm=[]
    for p in itertools.permutations(range(n)):
        if {(p[a],p[b]) for a,b in relation}==relation:perm.append(p)
    assert len(perm)==record['automorphism_count']
    induced=[]
    for p in perm:
        images=[sum(1<<p[i] for i in range(n) if s>>i&1) for s in ideals]
        induced.append(images)
    tables={s:[(s&i).bit_count() for i in ideals] for s in range(1<<n)}
    index={s:i for i,s in enumerate(ideals)}
    # This table is calculated from counter values on complete ideals, not colors.
    survives={s:[all(tables[s][index[t]]==tables[s][i] for i,t in enumerate(image)) for image in induced] for s in tables}
    by_k=[];least=None;winning=[]
    for k in range(0,3):
        accepted=0;first=None
        for supports in itertools.product(range(1<<n),repeat=k):
            stabilizer=[pi for pi in range(len(perm)) if all(survives[s][pi] for s in supports)]
            if len(stabilizer)==1:
                accepted+=1
                if first is None:first=list(supports)
        by_k.append({'probes':k,'families':(1<<n)**k,'rigid_families':accepted})
        if accepted and least is None:least=k;winning=first
        if time.monotonic()-started>100:raise TimeoutError('probe search deadline')
    assert least==record['minimum_count_probes']
    assert least==(record['distinguishing_number']-1).bit_length()
    chosen=record['supports'];assert len(chosen)==least
    stable=[pi for pi in range(len(perm)) if all(survives[s][pi] for s in chosen)]
    assert len(stable)==1
    # Check the producer coloring, without using it for the probe minimization.
    color=record['coloring'];assert len(color)==n
    assert len(set(color))==record['distinguishing_number']
    assert all(p==tuple(range(n)) or any(color[p[i]]!=color[i] for i in range(n)) for p in perm)
    signatures=[tuple(tables[s][i] for s in chosen) for i in range(len(ideals))]
    return {'points':n,'upper_sets':rows,'lattice_size':len(ideals),'automorphism_count':len(perm),
            'minimum_count_probes':least,'producer_supports':chosen,'first_optimal_supports':winning,
            'jointly_injective':len(set(signatures))==len(ideals),'family_counts':by_k}


def main():
    import argparse
    p=argparse.ArgumentParser();p.add_argument('input',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    data=json.loads(a.input.read_text());assert len(data)<=50
    verified=[verify(r) for r in data]
    a.output.write_text(json.dumps(verified,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'verified_posets':len(verified),'tested_families':sum(s['families'] for r in verified for s in r['family_counts'])}))
if __name__=='__main__':main()
