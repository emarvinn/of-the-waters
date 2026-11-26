"""Build the player edition of the starmap, wiki and chronology into the of-the-waters site.
Usage: python3 build.py SNAPDIR TLSNAPDIR REPO"""
import json, os, sys, glob, datetime, re
S=os.path.dirname(os.path.abspath(__file__)); SP=os.path.dirname(S)
snap, tlsnap, repo = sys.argv[1], sys.argv[2], sys.argv[3]
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
H=open(os.path.join(SP,'out','jump-era-starmap.html')).read()
H=H.replace("const WIKI='https://claude.ai/artifact/RH9rUoRCF4UJL8RhX3HTx5';","const WIKI='../world-classes/';")
assert "../world-classes/" in H
H=H.replace('<button class="btn pri" id="bSync" hidden>Sync with Obsidian</button>',
  '<button class="btn pri" id="bSync" hidden>Sync with Obsidian</button><a class="btn" id="otwHome" href="../" style="text-decoration:none">← Of the Waters</a><button class="btn" id="otwReset" hidden title="Undo everything you changed on this map in this browser">Reset to the GM\'s map</button>')
assert 'otwReset' in H
H+=('\n<style>#bSync{display:none!important}</style><script>(function(){var b=document.getElementById("otwReset");function s(){b.hidden=!OTW.changed();}s();setInterval(s,1500);'
    'b.onclick=function(){if(confirm("Reset the map to the GM\'s version? Everything you changed in this browser will be lost."))OTW.reset();};})();</script>')
os.makedirs(os.path.join(repo,'starmap'),exist_ok=True)
open(os.path.join(repo,'starmap','index.html'),'w').write(page('Starmap',inject(H,data)))

# ---- world classes wiki (standalone already)
os.makedirs(os.path.join(repo,'world-classes'),exist_ok=True)
W=open(os.path.join(SP,'wiki','world-classes.html')).read()
W=W.replace('</body>','') # tolerate either form
open(os.path.join(repo,'world-classes','index.html'),'w').write(page('World classes',W+'\n<p style="text-align:center;margin:24px 0"><a href="../" style="color:inherit">← Of the Waters</a></p>'))

# ---- chronology (read-only)
tl={i:strip_doc('entries',i,d) for i,d in load(tlsnap,'entries').items()}
T=open(os.path.join(SP,'timeline','jump-era-chronology.html')).read()
T=T.replace('<div class="eyebrow">Mothership campaign · setting record</div>','<div class="eyebrow"><a href="../" style="color:inherit">Of the Waters</a> · setting record</div>')
T+='\n<style>#sync{display:none!important}</style><script>setTimeout(function(){var m=document.getElementById("mode");if(m)m.textContent="Read-only";},400);</script>'
os.makedirs(os.path.join(repo,'chronology'),exist_ok=True)
open(os.path.join(repo,'chronology','index.html'),'w').write(page('Chronology',inject(T,{'entries':tl,'__key':'otw-chronology','__readonly':True})))
print('stripped GM-only notes:',len(stripped)); [print('  ',s) for s in stripped]
print('systems',len(data['systems']),'bodies',len(data['bodies']),'routes',len(data['routes']),'objects',len(data['objects']),'entries',len(tl))
