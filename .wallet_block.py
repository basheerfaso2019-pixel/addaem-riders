# wallet: PDF of riders whose balance is at least an amount the manager types (fadhel 2026-10-13)
js=rep(js,'function vSoon(){',r'''/* ---------- wallet PDF ---------- */
var W_BUSY=false;
function wMin(){var v=parseFloat(ui0.wmin);return isNaN(v)?null:v}
function wList(){var m=wMin();if(m==null)return [];return courierIds().filter(function(id){var w=data.couriers[id]&&data.couriers[id].w;return w&&(+w.b||0)>=m}).sort(function(a,b){return data.couriers[b].w.b-data.couriers[a].w.b})}
function wPanel(){var L=wList(),m=wMin(),tot=0;L.forEach(function(id){tot+=+data.couriers[id].w.b||0});
  return '<section class="panel"><div class="stmthead"><h2>تصدير المحافظ حسب المبلغ</h2><div class="stmttools"><label class="hint" for="wMin">الرصيد من</label><input id="wMin" type="number" step="any" inputmode="decimal" placeholder="مثال 500" value="'+esc(ui0.wmin||"")+'" style="width:120px"><span class="hint">ر.س فأكثر</span>'+
    '<button class="btn pri" id="wPdf"'+(L.length&&!W_BUSY?"":" disabled")+'>'+(W_BUSY?"جارٍ التصدير…":'تصدير PDF (<span class="num">'+L.length+'</span>)')+'</button></div></div>'+
    '<p class="hint" id="wHint" style="margin:0">'+(m==null?"اكتب المبلغ، ويطلع لك عدد المناديب اللي رصيدهم يساويه أو أكبر.":'<span class="num">'+L.length+'</span> مندوب رصيدهم '+fmt(m,2)+' ر.س فأكثر، بمجموع '+fmt(tot,2)+' ر.س.')+'</p></section>'}
function wDoc(L,m){var tot=0,th='background:#0f4c4a;color:#fff;font-weight:700;padding:6px 4px;border:1px solid #0f4c4a;font-size:11px',td='padding:5px 4px;border:1px solid #d5dedd;font-size:11px;text-align:center';
  var rows=L.map(function(id,i){var c=data.couriers[id],w=c.w;tot+=+w.b||0;return '<tr style="page-break-inside:avoid;background:'+(i%2?"#f4f8f7":"#fff")+'"><td style="'+td+'">'+(i+1)+'</td><td style="'+td+'">'+esc(id)+'</td><td style="'+td+';text-align:right">'+esc(c.n||"—")+'</td><td style="'+td+'">'+esc(normCat(c.cat)||(c.rg?"الرياض":"—"))+'</td><td style="'+td+'" dir="ltr">'+esc(c.ph?"0"+String(c.ph).replace(/^966/,""):"—")+'</td><td style="'+td+';font-weight:700">'+fmt(w.b,2)+'</td><td style="'+td+'">'+(w.c==null?"—":fmt(w.c,2))+'</td><td style="'+td+'">'+esc(w.d||"—")+'</td></tr>'}).join("");
  return '<div class="noi18n" dir="rtl" style="box-sizing:border-box;width:100%;padding:14px 10px;background:#fff;color:#14302f;font-family:\'IBM Plex Sans Arabic\',Tahoma,sans-serif;direction:rtl">'+
    '<div style="display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px solid #c9a24a;padding-bottom:10px;margin-bottom:12px"><div><div style="font-size:20px;font-weight:700;color:#0f4c4a">محافظ المناديب '+fmt(m,2)+' ر.س فأكثر</div><div style="font-size:12.5px;color:#4a6261;margin-top:2px">'+esc(data.company||"")+'</div></div>'+
    '<div style="text-align:left;font-size:12px;color:#4a6261">تاريخ التصدير <span dir="ltr">'+new Date().toISOString().slice(0,10)+'</span></div></div>'+
    '<div style="display:flex;gap:10px;margin-bottom:12px">'+[["عدد المناديب",L.length],["إجمالي الأرصدة",fmt(tot,2)+" ر.س"],["الحد الأدنى",fmt(m,2)+" ر.س"]].map(function(x){return '<div style="flex:1;border:1px solid #d5dedd;border-radius:8px;padding:7px 10px"><div style="font-size:10.5px;color:#4a6261">'+x[0]+'</div><div style="font-size:15px;font-weight:700;color:#0f4c4a">'+x[1]+'</div></div>'}).join("")+'</div>'+
    '<table style="width:100%;border-collapse:collapse;table-layout:fixed"><colgroup>'+[5,11,30,7,14,12,11,10].map(function(w){return '<col style="width:'+w+'%">'}).join("")+'</colgroup><thead><tr>'+["#","Rider ID","الاسم","الفئة","الجوال","رصيد المحفظة","النقد المحصّل","بتاريخ"].map(function(h){return '<th style="'+th+'">'+h+'</th>'}).join("")+'</tr></thead><tbody>'+rows+'</tbody>'+
    '<tfoot><tr><td colspan="5" style="'+td+';font-weight:700;background:#eef3f4">الإجمالي</td><td style="'+td+';font-weight:700;background:#eef3f4">'+fmt(tot,2)+'</td><td colspan="2" style="'+td+';background:#eef3f4"></td></tr></tfoot></table>'+
    '<div style="margin-top:14px;display:flex;justify-content:flex-end;font-size:10.5px;color:#6b7f7e"><span>تصميم المهندس / فاضل العميسي</span></div></div>'}
function wPdf(){var L=wList(),m=wMin();if(!L.length)return;W_BUSY=true;render();
  loadH2P().then(function(h2p){var w=document.createElement("div");w.innerHTML=wDoc(L,m);var el=w.firstChild;ovWords(el);
    return (document.fonts&&document.fonts.ready||Promise.resolve()).then(function(){return h2p().set({margin:[8,6,10,6],filename:"محافظ المناديب "+m+" فأكثر - "+new Date().toISOString().slice(0,10)+".pdf",image:{type:"jpeg",quality:0.95},html2canvas:{scale:2,useCORS:true,backgroundColor:"#ffffff"},jsPDF:{unit:"mm",format:"a4",orientation:"portrait"},pagebreak:{mode:["css","legacy"],avoid:"tr"}}).from(el).save()})})
  .catch(function(){alert("تعذر تحميل مكتبة PDF، تأكد من الاتصال بالإنترنت وحاول مرة أخرى.")})
  .then(function(){W_BUSY=false;render()})}
/* typing the amount only refreshes the panel, so the box keeps focus */
document.addEventListener("input",function(e){if(e.target.id!=="wMin")return;ui0.wmin=e.target.value;var tmp=document.createElement("div");tmp.innerHTML=wPanel();
  ["wHint","wPdf"].forEach(function(k){var o=document.getElementById(k),n=tmp.querySelector("#"+k);if(o&&n)o.replaceWith(n)});if(typeof trTree==="function")try{trTree(document.getElementById("wHint"));trTree(document.getElementById("wPdf"))}catch(x){}});
function vSoon(){''')
js=rep(js,"""  return sampleNote()+'<div class="filters">'+riderPick()+'</div>'+
    '<div class="tbl"><table><thead><tr><th>Rider Id</th><th>الاسم</th><th>رصيد المحفظة<br>Balance</th>""","""  return sampleNote()+'<div class="filters">'+riderPick()+'</div>'+(ids.length?wPanel():"")+
    '<div class="tbl"><table><thead><tr><th>Rider Id</th><th>الاسم</th><th>رصيد المحفظة<br>Balance</th>""")
js=rep(js,'  if(t.dataset.ovpdf){ovPdf(t.dataset.ovpdf);return}','  if(t.dataset.ovpdf){ovPdf(t.dataset.ovpdf);return}\n  if(t.id==="wPdf"){wPdf();return}')
