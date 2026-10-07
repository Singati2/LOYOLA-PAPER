"""Assemble the strict calorimetric (NIST method 'C') standard dHvap(298.15 K) set for acyclic alkanes
C4-C16 from archived NIST pages (nist_alkanes_skeletons_audit.csv, built from the archived pages) and AVG individual-point pages (nist_hvap_pts/). Octanes flagged as dev set."""
import csv,re,html,os
HERE = os.path.dirname(os.path.abspath(__file__))
def clean(s): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',s))).strip()
sk=list(csv.DictReader(open(os.path.join(HERE, 'nist_alkanes_skeletons_audit.csv'))))
rows=[]
for a in sk:
    cal=[]
    for part in a['hv_std_refs'].split(' || '):
        for e in part.split(' | '):
            m=re.match(r'(.+?) \(C; (.+)\)$',e)
            if m: cal.append(f'{m.group(1)} kJ/mol ({m.group(2)})')
    if a['hvAVG']=='True':
        for cid in a['ids'].split():
            f=os.path.join(HERE, f'nist_hvap_pts/{cid}.html')
            if not os.path.exists(f): raise FileNotFoundError(f'missing archived NIST points page {f} (v40.13: every skeleton with a NIST average must be resolved against its points page)')
            if True:
                t=open(f,errors='replace').read()
                for r in re.findall(r'<tr[^>]*>(.*?)</tr>',t,re.S):
                    c=[clean(x) for x in re.findall(r'<td[^>]*>(.*?)</td>',r,re.S)]
                    if c and re.match(r'^[0-9]',c[0]) and c[1]=='C': cal.append(f'{c[0]} kJ/mol ({c[2]})')
    if cal:
        n=int(a['n']); first=a['names'].split(' / ')[0]
        rows.append(dict(n=n,name=first,dev_set_octane=(n==8),already_used_nonane_test=(n==9),
            linear=first.lower().lstrip('n-') in ('butane','pentane','hexane','heptane','octane','nonane','decane','undecane','dodecane','tridecane','tetradecane','pentadecane','hexadecane'),
            calorimetric_determinations=' ; '.join(dict.fromkeys(cal)),urls=a['urls']))
w=csv.DictWriter(open(os.path.join(HERE, 'calorimetric_dHvap298_alkanes.csv'),'w',newline=''),list(rows[0].keys())); w.writeheader(); w.writerows(rows)
tot=len(rows); new=[r for r in rows if not r['dev_set_octane'] and not r['already_used_nonane_test']]
print('skeletons with >=1 calorimetric dHvap(298):',tot,'| octanes',sum(r['dev_set_octane'] for r in rows),'| nonanes',sum(r['already_used_nonane_test'] for r in rows),'| new (not C8/C9)',len(new),'of which linear',sum(r['linear'] for r in new),'branched',sum(not r['linear'] for r in new))
for r in new: print(r['n'],r['name'],'| linear' if r['linear'] else '')
