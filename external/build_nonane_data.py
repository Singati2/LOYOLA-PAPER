"""Rebuild nonane_data.csv / nonane_provenance.csv / nonane_identity.csv from the NIST WebBook
pages archived in nonane_raw_nist/ (fetched 2026-10-03 with curl). No values are typed by hand."""
import re,html,json,csv,os
D=os.path.dirname(os.path.abspath(__file__))+'/'
RAW=D+'nonane_raw_nist/'
from decimal import Decimal,ROUND_HALF_UP
def clean(s): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',s))).strip()
iso=[l.split('\t') for l in '''nonane	CCCCCCCCC
2-methyloctane	CC(C)CCCCCC
3-methyloctane	CCC(C)CCCCC
4-methyloctane	CCCC(C)CCCC
3-ethylheptane	CCC(CC)CCCC
4-ethylheptane	CCCC(CC)CCC
2,2-dimethylheptane	CC(C)(C)CCCCC
2,3-dimethylheptane	CC(C)C(C)CCCC
2,4-dimethylheptane	CC(C)CC(C)CCC
2,5-dimethylheptane	CC(C)CCC(C)CC
2,6-dimethylheptane	CC(C)CCCC(C)C
3,3-dimethylheptane	CCC(C)(C)CCCC
3,4-dimethylheptane	CCC(C)C(C)CCC
3,5-dimethylheptane	CCC(C)CC(C)CC
4,4-dimethylheptane	CCCC(C)(C)CCC
3-ethyl-2-methylhexane	CC(C)C(CC)CCC
3-ethyl-3-methylhexane	CCC(C)(CC)CCC
4-ethyl-2-methylhexane	CC(C)CC(CC)CC
3-ethyl-4-methylhexane	CCC(CC)C(C)CC
2,2,3-trimethylhexane	CC(C)(C)C(C)CCC
2,2,4-trimethylhexane	CC(C)(C)CC(C)CC
2,2,5-trimethylhexane	CC(C)(C)CCC(C)C
2,3,3-trimethylhexane	CC(C)C(C)(C)CCC
2,3,4-trimethylhexane	CC(C)C(C)C(C)CC
2,3,5-trimethylhexane	CC(C)C(C)CC(C)C
2,4,4-trimethylhexane	CC(C)CC(C)(C)CC
3,3,4-trimethylhexane	CCC(C)(C)C(C)CC
3,3-diethylpentane	CCC(CC)(CC)CC
3-ethyl-2,2-dimethylpentane	CC(C)(C)C(CC)CC
3-ethyl-2,3-dimethylpentane	CC(C)C(C)(CC)CC
3-ethyl-2,4-dimethylpentane	CC(C)C(CC)C(C)C
2,2,3,3-tetramethylpentane	CC(C)(C)C(C)(C)CC
2,2,3,4-tetramethylpentane	CC(C)(C)C(C)C(C)C
2,2,4,4-tetramethylpentane	CC(C)(C)CC(C)(C)C
2,3,3,4-tetramethylpentane	CC(C)C(C)(C)C(C)C'''.split('\n')]
RET='2026-10-03'
COMPILATIONS={'Weast and Grasselli, 1989','Majer and Svoboda, 1985','Reid, 1972','Ruzicka and Majer, 1994'}
def refs_of(t):
    d={}
    parts=re.split(r'<span id="(ref-\d+)"><strong>(.*?)</strong></span>',t)
    for i in range(1,len(parts)-2,3):
        body=parts[i+2]; body=body.split('<span id="ref-')[0].split('[<a')[0]
        d[clean(parts[i+1])]=clean(parts[i+1])+': '+clean(body)
    return d
def rows_of(t):
    m=re.search(r'<table class="data" aria-label="One dimensional data">(.*?)</table>',t,re.S); out=[]
    for r in re.findall(r'<tr[^>]*>(.*?)</tr>',m.group(1),re.S):
        tds=[clean(x) for x in re.findall(r'<td[^>]*>(.*?)</td>',r,re.S)]
        if len(tds)==6: out.append(tds)
    return out
def pts_of(f):
    try: t=open(f).read()
    except FileNotFoundError: return None
    rows=[]
    for tb in re.findall(r'<table.*?</table>',t,re.S):
        for r in re.findall(r'<tr[^>]*>(.*?)</tr>',tb,re.S):
            c=[clean(x) for x in re.findall(r'<td[^>]*>(.*?)</td>',r,re.S)]
            if c and re.match(r'^[0-9]',c[0]): rows.append(c)
    return rows
def year(ref):
    m=re.search(r'(\d{4})',ref); return int(m.group(1)) if m else 0
def num(v): return Decimal(v.split('±')[0].strip().rstrip('.') or '0')
def r1(x): return str(x.quantize(Decimal('0.1'),ROUND_HALF_UP))
def r2(x): return str(x.quantize(Decimal('0.01'),ROUND_HALF_UP))
data=[];prov=[];ident=[]
for name,smi in iso:
    nt=open(RAW+f'name_{name}.html').read()
    cas=re.search(r'CAS Registry Number:</strong> ([0-9-]+)',nt).group(1); cid='C'+cas.replace('-','')
    t=open(RAW+f'cas_{cid}.html').read()
    assert cas==re.search(r'CAS Registry Number:</strong> ([0-9-]+)',t).group(1)
    nist_name=re.search(r'"@type" : "MolecularEntity",\s*"name" : "([^"]*)"',t).group(1)
    inchi=re.search(r'"inChI" : "([^"]*)"',t).group(1)
    url=f'https://webbook.nist.gov/cgi/cbook.cgi?ID={cid}&Mask=4'
    nurl=f'https://webbook.nist.gov/cgi/cbook.cgi?Name={name.replace(",","%2C")}&Units=SI&Mask=4'
    ident.append(dict(name=name,cas=cas,smiles=smi,nist_name=nist_name,nist_inchi=inchi,url=url,name_search_url=nurl,retrieved=RET,verbatim_snippet=f'{nist_name} ... IUPAC Standard InChI: {inchi} ... CAS Registry Number: {cas}'))
    refs=refs_of(t); rows=rows_of(t)
    rec=dict(name=name,cas=cas,smiles=smi,T_B_C='',dHvap_kcal='')
    # ---- Tboil
    tb=[r for r in rows if r[0]=='Tboil']
    avg=[r for r in tb if r[3]=='AVG']
    if avg:
        r=avg[0]; K=num(r[1]); pts=pts_of(RAW+f'pts_{cid}_TBOIL.html')
        alld='; '.join(f'{p[0]} K ({p[1]}; {p[2]})' for p in pts) if pts else ''
        rule='NIST average (AVG) value — prereg primary rule'
        snip=' | '.join(r); src_url=url+' ; points: '+f'https://webbook.nist.gov/cgi/cbook.cgi?ID={cid}&Type=TBOIL'
    elif tb:
        prim=[r for r in tb if r[4] not in COMPILATIONS]
        if len(tb)==1: r=tb[0]; rule='single NIST Tboil determination (no AVG given)'
        else:
            r=max(prim,key=lambda r:year(r[4])); rule='no NIST AVG; most recent primary experimental determination (compilations e.g. Weast & Grasselli 1989 CRC excluded) — PREREG GAP: calorimetric fallback inapplicable to Tboil; interpretation needs author ratification'
        K=num(r[1]); alld='; '.join(f'{x[1]} K ({refs.get(x[4],x[4])}; {x[5]})' for x in tb); snip=' | '.join(r); src_url=url
    else: K=None
    if K is not None:
        C=K-Decimal('273.15'); rec['T_B_C']=r1(C)
        prov.append(dict(name=name,cas=cas,property='T_B',value_used=r1(C),original_value=r[1],original_units='K',conditions='normal boiling point (1 atm); converted degC = K - 273.15, rounded half-up to 0.1',all_determinations=alld,selection_rule=rule,url=src_url,retrieved=RET,verbatim_snippet=snip))
    # ---- dHvap standard
    hv=[r for r in rows if r[0]=='ΔvapH°']
    avg=[r for r in hv if r[3]=='AVG']; cal=[r for r in hv if r[3]=='C']
    if avg:
        r=avg[0]; pts=pts_of(RAW+f'pts_{cid}_HVAP.html')
        alld='; '.join(f'{p[0]} kJ/mol ({p[1]}; {p[2]}; {p[3] if len(p)>3 else ""})' for p in pts)
        rule='NIST average (AVG) value — prereg primary rule'; src_url=url+' ; points: '+f'https://webbook.nist.gov/cgi/cbook.cgi?ID={cid}&Type=HVAP'
    elif cal:
        y=max(year(x[4]) for x in cal); cands=[x for x in cal if year(x[4])==y]
        r=max(cands,key=lambda x:len(x[1].split('±')[0].strip()))  # most precise listing of same study
        rule='no NIST AVG; most recent calorimetric (method C) determination — prereg fallback rule'+(f' (same study listed {len(cands)}x; most precisely reported entry used)' if len(cands)>1 else ''); src_url=url
        alld='; '.join(f'{x[1]} kJ/mol (method {x[3]}; {refs.get(x[4],x[4])}; {x[5]})' for x in hv)
    elif hv:
        r=hv[0] if len(hv)==1 else None
        assert r is not None, name
        rule='only one NIST ΔvapH° entry, non-calorimetric (method N/A); prereg rules (AVG / calorimetric) not met — used as sole available NIST value; FLAG' ; src_url=url
        alld='; '.join(f'{x[1]} kJ/mol (method {x[3]}; {refs.get(x[4],x[4])}; {x[5]})' for x in hv)
    else: r=None
    if r is not None:
        kj=num(r[1]); kc=kj/Decimal('4.184')
        rec['dHvap_kcal']=r2(kc)
        prov.append(dict(name=name,cas=cas,property='dHvap',value_used=r2(kc),original_value=r[1],original_units='kJ/mol',conditions='standard enthalpy of vaporization (NIST "ΔvapH°: Enthalpy of vaporization at standard conditions"); kcal/mol = kJ/4.184, rounded half-up to 0.01',all_determinations=alld,selection_rule=rule,url=src_url,retrieved=RET,verbatim_snippet=' | '.join(r)))
    data.append(rec)
for fn,rows_ in [('nonane_data.csv',data),('nonane_provenance.csv',prov),('nonane_identity.csv',ident)]:
    with open(D+fn,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows_[0].keys())); w.writeheader(); w.writerows(rows_)
print(sum(1 for d in data if d['T_B_C']),sum(1 for d in data if d['dHvap_kcal']))
for p in prov: print(p['name'],p['property'],p['value_used'],p['original_value'],p['selection_rule'][:60])
