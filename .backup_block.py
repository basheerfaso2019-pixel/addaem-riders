# admin backup: download every table (+ rider photos) as one JSON file, and restore from it (fadhel 2026-10-15)
js=rep(js,'function vSoon(){','''var BK_T=["settings","riders","rider_private","daily","quality","wallet","fuel_label","fuel_map","sheet_extra"],bk={};
function bkAll(t){var out=[];function pg(i){return sb.from(t).select("*").range(i,i+999).then(function(r){if(r.error)throw r.error;out=out.concat(r.data);return r.data.length<1000?out:pg(i+1000)})}return pg(0)}
function b64(blob){return new Promise(function(ok,no){var f=new FileReader();f.onload=function(){ok(String(f.result).split(",")[1])};f.onerror=no;f.readAsDataURL(blob)})}
function bkPhotos(){var st=sb.storage.from("rider-photos");return st.list("",{limit:2000}).then(function(r){var fs=(r.data||[]).filter(function(f){return /\\.jpg$/.test(f.name)}),o={};
  return fs.reduce(function(p,f){return p.then(function(){return st.download(f.name).then(function(d){if(d.data)return b64(d.data).then(function(s){o[f.name]=s})})})},Promise.resolve()).then(function(){return o})})}
function bkSet(m,ok){bk.msg=m;bk.ok=ok;var e=document.getElementById("bkMsg");if(e){e.textContent=m;e.style.color=ok?"var(--good)":"var(--bad)"}}
function bkDownload(){if(bk.busy)return;bk.busy=true;var res={app:"addaem-riders",version:1,created:new Date().toISOString(),tables:{}};
  BK_T.reduce(function(p,t){return p.then(function(){bkSet("جارٍ تنزيل "+t+"…",true);return bkAll(t).then(function(rows){res.tables[t]=rows})})},Promise.resolve())
  .then(function(){bkSet("جارٍ تنزيل صور المناديب…",true);return bkPhotos()}).then(function(ph){res.photos=ph;
    var a=document.createElement("a");a.href=URL.createObjectURL(new Blob([JSON.stringify(res)],{type:"application/json"}));a.download="addaem-backup-"+new Date().toISOString().slice(0,10)+".json";document.body.appendChild(a);a.click();a.remove();
    var n=BK_T.reduce(function(s,t){return s+res.tables[t].length},0);bk.busy=false;bkSet("تم تنزيل النسخة الاحتياطية ("+n+" سجل و"+Object.keys(ph).length+" صورة). احفظ الملف في مكان آمن.",true)})
  .catch(function(e){bk.busy=false;bkSet("تعذّر التنزيل: "+((e&&e.message)||e),false)})}
function bkChunks(a,n){var o=[];for(var i=0;i<a.length;i+=n)o.push(a.slice(i,i+n));return o}
function bkRestore(file){var fr=new FileReader();fr.onload=function(){var d;try{d=JSON.parse(fr.result)}catch(e){bkSet("الملف ليس نسخة احتياطية صحيحة.",false);return}
  if(!d||d.app!=="addaem-riders"||!d.tables){bkSet("الملف ليس نسخة احتياطية من هذا النظام.",false);return}
  if(!confirm("استرجاع النسخة المؤرخة "+String(d.created).slice(0,10)+"؟ ستُستبدل السجلات الموجودة بنفس المفاتيح، وتبقى السجلات الأخرى كما هي."))return;
  bk.busy=true;var keys={settings:"key",riders:"id",rider_private:"rider_id",daily:"day,rider_id",quality:"month,rider_id",wallet:"rider_id",fuel_label:"month,label",fuel_map:"label",sheet_extra:"month,rider_id"};
  BK_T.reduce(function(p,t){var rows=d.tables[t]||[];return p.then(function(){bkSet("جارٍ استرجاع "+t+"…",true);return bkChunks(rows,500).reduce(function(q,c){return q.then(function(){return sb.from(t).upsert(c,{onConflict:keys[t]}).then(function(r){if(r.error)throw r.error})})},Promise.resolve())})},Promise.resolve())
  .then(function(){var iq=(d.tables.rider_private||[]).filter(function(r){return r.iqama}).map(function(r){return{id:r.rider_id,iqama:r.iqama}});bkSet("جارٍ تفعيل دخول المناديب…",true);
    return bkChunks(iq,100).reduce(function(q,c){return q.then(function(){return sb.rpc("set_riders",{p_rows:c}).then(function(r){if(r.error)throw r.error})})},Promise.resolve())})
  .then(function(){var ph=d.photos||{},st=sb.storage.from("rider-photos");bkSet("جارٍ استرجاع الصور…",true);
    return Object.keys(ph).reduce(function(q,n){return q.then(function(){var b=atob(ph[n]),u=new Uint8Array(b.length);for(var i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return st.upload(n,new Blob([u],{type:"image/jpeg"}),{upsert:true})})},Promise.resolve())})
  .then(function(){bk.busy=false;bkSet("تم الاسترجاع. حدّث الصفحة لرؤية البيانات.",true)})
  .catch(function(e){bk.busy=false;bkSet("تعذّر الاسترجاع: "+((e&&e.message)||e),false)})};fr.readAsText(file)}
function bkPanel(){if(!isAdmin)return "";
  return '<section class="panel bkp"><h2>النسخة الاحتياطية</h2><p class="hint">نزّل نسخة كاملة من بيانات النظام (المناديب، الإقامات، الأداء اليومي، الجودة، المحافظ، الشيت، صور البطاقات) في ملف واحد. احفظه في جهازك أو في Google Drive، ويُفضّل كل أسبوع.</p>'+
    '<div class="row"><button class="btn pri" id="bkDl">تنزيل نسخة احتياطية</button><label class="btn">استرجاع من نسخة<input type="file" id="bkFile" accept=".json,application/json" hidden></label></div>'+
    '<p class="hint" id="bkMsg" style="color:'+(bk.ok?"var(--good)":"var(--bad)")+'">'+esc(bk.msg||"")+'</p>'+
    '<p class="hint">الملف فيه أرقام الإقامة، فلا ترسله لأحد.</p></section>'}
var _vData=vData;vData=function(){return _vData()+bkPanel()};
document.addEventListener("click",function(e){if(e.target&&e.target.id==="bkDl")bkDownload()});
document.addEventListener("change",function(e){if(e.target&&e.target.id==="bkFile"&&e.target.files.length){bkRestore(e.target.files[0]);e.target.value=""}});
function vSoon(){''')
css+='''
.bkp{margin-top:16px}
'''
