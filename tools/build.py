"""Build the player edition of the starmap, world-class wiki and chronology into the of-the-waters site.

python3 tools/build.py --starmap STARMAP.html --timeline TIMELINE.html --wiki WIKI.html \
    --map-data DIR --timeline-data DIR --repo REPO

The three HTML files are the GM's claude.ai artifacts (as saved by an Artifact read; the page skeleton is
tolerated). DIR holds the artifact databases as saved by ArtifactData list with out_dir: map-data has
systems/ bodies/ routes/ objects/, timeline-data has entries/.
GM-only notes are left out; the chronology shows only entries ticked "Show on the player site"."""
import json, os, sys, glob, datetime, re, argparse
S=os.path.dirname(os.path.abspath(__file__))
ap=argparse.ArgumentParser();[ap.add_argument('--'+k,required=True) for k in ('starmap','timeline','wiki','map-data','timeline-data','repo')]
A=ap.parse_args(); snap, tlsnap, repo = A.map_data, A.timeline_data, A.repo
def src(p):
    """the page content of a saved artifact, without the skeleton the artifact service wraps around it"""
    t=open(p,encoding='utf-8').read()
    if t.lstrip().lower().startswith('<!doctype'):
        i=t.find('<body>');j=t.rfind('</body>')
        if i>=0: t=t[i+6:j if j>i else None]
    return t.strip()
shim=open(os.path.join(S,'shim.js')).read()
stripped=[]
def load(d,col):
    out={}
    for f in sorted(glob.glob(os.path.join(d,col,'*.json'))):
        out[os.path.basename(f)[:-5]]=json.load(open(f))
    return out
def strip_doc(col,id,doc):
    if doc.get('gmNotes') and doc.get('notes'): stripped.append(f'{col}/{id}'); doc['notes']=''
    doc.pop('gmNotes',None)
    if col=='bodies':
        if doc.get('priGM') and doc.get('priNotes'): stripped.append(f'{col}/{id}/primary'); doc['priNotes']=''
        doc.pop('priGM',None)
        for k in ('bodies','regions'):
            for b in doc.get(k) or []:
                if b.get('gmNotes') and b.get('notes'): stripped.append(f"{col}/{id}/{b.get('name') or b.get('id')}"); b['notes']=''
                b.pop('gmNotes',None)
                if b.get('profileGM'): stripped.append(f"{col}/{id}/{b.get('name') or b.get('id')} profile"); b['profile']={'hidden':True}
                b.pop('profileGM',None)
    return doc
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d%H%M')
def page(title,body):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<style>:root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>'
            '</head><body>\n'+body+'\n</body></html>\n')
def inject(html,data):
    blob=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    head=f'<script type="application/json" id="otw-snapshot">{blob}</script>\n<script>{shim}</script>\n'
    return head+html

# ---- starmap
data={c:{i:strip_doc(c,i,d) for i,d in load(snap,c).items()} for c in ('systems','bodies','routes','objects')}
data['__key']='otw-starmap'
data['__made']=datetime.datetime.now(datetime.timezone.utc).isoformat()
H=src(A.starmap)
H=H.replace("const WIKI='https://claude.ai/artifact/RH9rUoRCF4UJL8RhX3HTx5';","const WIKI='../world-classes/';")
assert "../world-classes/" in H
H=H.replace('<button class="btn pri" id="bSync" hidden>Sync with Obsidian</button>',
  '<button class="btn pri" id="bSync" hidden>Sync with Obsidian</button><a class="btn" id="otwHome" href="../" style="text-decoration:none">← Of the Waters</a><button class="btn" id="otwSend" hidden title="Package what you changed so the GM can add it to the campaign map">Send my changes to the GM</button><button class="btn" id="otwReset" hidden title="Undo everything you changed on this map in this browser">Reset to the GM\'s map</button>')
assert 'otwReset' in H
H+='\n<style>#bSync,#bPublish{display:none!important}</style>'+open(os.path.join(S,'send.html')).read()
os.makedirs(os.path.join(repo,'starmap'),exist_ok=True)
open(os.path.join(repo,'starmap','index.html'),'w').write(page('Starmap',inject(H,data)))

# ---- world classes wiki (standalone already)
os.makedirs(os.path.join(repo,'world-classes'),exist_ok=True)
W=src(A.wiki)+'<style>#bPublish{display:none!important}</style>'
open(os.path.join(repo,'world-classes','index.html'),'w').write(page('World classes',W+'\n<p style="text-align:center;margin:24px 0"><a href="../" style="color:inherit">← Of the Waters</a></p>'))

# ---- chronology (read-only)
tl0=load(tlsnap,'entries')
# the chronology is GM-only by default: an entry reaches players only when ticked "Show on the player site";
# an era is kept (title and years) when it holds a shown entry, and its notes only when the era itself is ticked
shown={i:d for i,d in tl0.items() if d.get('player')}
for i,d in tl0.items():
    if d.get('kind')=='era' and i not in shown and any(e.get('era')==i for e in shown.values()):
        shown[i]={k:v for k,v in d.items() if k not in ('notes','links')}
tl={i:strip_doc('entries',i,d) for i,d in shown.items()}
for d in tl.values(): d.pop('player',None)
# links to the GM's own project documents mean nothing to players (and name GM files): keep only web links
for d in tl.values():
    if isinstance(d.get('links'),list): d['links']=[l for l in d['links'] if str(l.get('href','')).startswith(('http://','https://'))]
T=src(A.timeline)
T=T.replace('<div class="eyebrow">Mothership campaign · setting record</div>','<div class="eyebrow"><a href="../" style="color:inherit">Of the Waters</a> · setting record</div>')
T+='\n<style>#sync,#publish{display:none!important}</style><script>setTimeout(function(){var m=document.getElementById("mode");if(m)m.textContent="Read-only";},400);</script>'
os.makedirs(os.path.join(repo,'chronology'),exist_ok=True)
open(os.path.join(repo,'chronology','index.html'),'w').write(page('Chronology',inject(T,{'entries':tl,'__key':'otw-chronology','__readonly':True})))
print('stripped GM-only notes:',len(stripped)); [print('  ',s) for s in stripped]
print('systems',len(data['systems']),'bodies',len(data['bodies']),'routes',len(data['routes']),'objects',len(data['objects']),'entries',len(tl),'of',len(tl0))
