// Player edition: stands in for claude.ai's page database. The GM's snapshot is the base;
// whatever this visitor changes is kept in their own browser (localStorage) on top of it.
window.PLAYER_EDITION=true;
(function(){
  var SNAP=JSON.parse(document.getElementById('otw-snapshot').textContent), KEY=SNAP.__key||'otw', RO=!!SNAP.__readonly;
  var over={}; try{over=JSON.parse(localStorage.getItem(KEY)||'{}')||{};}catch(e){}
  var subs={};
  function clone(x){return x==null?x:JSON.parse(JSON.stringify(x));}
  function docs(col){var m=new Map(Object.entries(SNAP[col]||{})),o=over[col]||{};Object.keys(o).forEach(function(id){if(o[id]===null)m.delete(id);else m.set(id,o[id]);});return m;}
  function snapOf(col){var m=docs(col),list=[];m.forEach(function(d,id){list.push({id:id,exists:true,data:function(){return clone(d);}});});return {docs:list,size:list.length,empty:!list.length,forEach:function(f){list.forEach(f);}};}
  function persist(){try{localStorage.setItem(KEY,JSON.stringify(over));}catch(e){}}
  function emit(col){var s=snapOf(col);(subs[col]||[]).forEach(function(f){try{f(s);}catch(e){console.error(e);}});}
  function write(col,id,d){if(RO)return Promise.reject({code:'not_granted'});(over[col]||(over[col]={}))[id]=d;persist();setTimeout(function(){emit(col);},0);return Promise.resolve();}
  function collection(col){return {
    doc:function(id){id=String(id);return {
      get:function(){var d=docs(col).get(id);return Promise.resolve({id:id,exists:!!d,data:function(){return clone(d);}});},
      set:function(x){return write(col,id,clone(x));},
      update:function(x){var d=docs(col).get(id);return d?write(col,id,Object.assign({},d,clone(x))):Promise.reject({code:'not_found'});},
      delete:function(){return write(col,id,null);},
      onSnapshot:function(f){var w=function(s){var d=docs(col).get(id);f({id:id,exists:!!d,data:function(){return clone(d);}});};(subs[col]||(subs[col]=[])).push(w);setTimeout(w,0);return function(){subs[col]=subs[col].filter(function(g){return g!==w;});};}};},
    add:function(x){var id='p'+Date.now().toString(36)+Math.random().toString(36).slice(2,6);return write(col,id,clone(x)).then(function(){return {id:id};});},
    onSnapshot:function(f){(subs[col]||(subs[col]=[])).push(f);setTimeout(function(){f(snapOf(col));},0);return function(){subs[col]=subs[col].filter(function(g){return g!==f;});};},
    get:function(){return Promise.resolve(snapOf(col));}};}
  var db={collection:collection};
  var user={can:function(){return Promise.resolve(!RO);},isOwner:function(){return Promise.resolve(false);},canEdit:function(){return Promise.resolve(false);},
    id:function(){return Promise.resolve('local');},me:function(){return Promise.resolve({id:'local',name:''});},profiles:function(){return Promise.resolve({});}};
  window.claude={use:function(n){return Promise.resolve(n==='db'?db:n==='user'?user:null);}};
  window.OTW={submission:function(from){var ch=[];Object.keys(over).forEach(function(c){Object.keys(over[c]).forEach(function(id){ch.push({col:c,id:id,base:(SNAP[c]||{})[id]||null,mine:over[c][id]});});});
      return {otw:1,map:KEY,from:from||'',made:new Date().toISOString(),snapshot:SNAP.__made||null,changes:ch};},
    count:function(){var n={};Object.keys(over).forEach(function(c){var k=Object.keys(over[c]).length;if(k)n[c]=k;});return n;},
    changed:function(){return Object.keys(over).some(function(c){return Object.keys(over[c]).length;});},
    reset:function(){over={};try{localStorage.removeItem(KEY);}catch(e){}location.reload();}};
})();
