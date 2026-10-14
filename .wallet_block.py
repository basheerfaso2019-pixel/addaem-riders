# wallet: PDF of riders whose balance is at least an amount the manager types (fadhel 2026-10-13)
js=rep(js,'function vSoon(){',r'''/* ---------- wallet PDF ---------- */
var W_BUSY=false;
/* amount typed with Arabic or English digits; balances are mostly negative (money the rider owes), so "owes" is the default direction */
function wMin(){var v=parseFloat(String(ui0.wmin||"").replace(/[٠-٩]/g,function(d){return d.charCodeAt(0)-1632}).replace(/[۰-۹]/g,function(d){return d.charCodeAt(0)-1776}).replace(/[٫,]/g,".").replace(/[^\d.]/g,""));return isNaN(v)?null:v}
function wOwe(){return ui0.wdir!=="has"}
function wHit(b){var m=wMin();return wOwe()?b<=-m:b>=m}
QK.wc="wcs";QK.wk="wks";
/* rider city = city on his latest day of data, else his region */
function wCity(id){var ds=days();for(var i=ds.length-1;i>=0;i--){var x=data.days[ds[i]][id];if(x&&x[CI])return String(x[CI])}var c=data.couriers[id];return c&&c.rg||"—"}
function wKat(id){var c=data.couriers[id]||{};return c.rg?"الرياض":normCat(c.cat)||"—"}
var WK_ORDER=["أ","ب","خ","الرياض","—"],WK_TXT={"أ":"فئة أ","ب":"فئة ب","خ":"فئة خ","الرياض":"مناديب الرياض","—":"بدون فئة"};
function wFiltTxt(){var a=[];if((ui0.wcs||[]).length)a.push(ui0.wcs.map(function(c){return c==="—"?"غير محدد":c}).join("، "));if((ui0.wks||[]).length)a.push(ui0.wks.map(function(k){return WK_TXT[k]}).join("، "));return a.join(" · ")}
function wList(){var m=wMin();if(m==null)return [];var cs=ui0.wcs||[],ks=ui0.wks||[];return courierIds().filter(function(id){var w=data.couriers[id]&&data.couriers[id].w;return w&&wHit(+w.b||0)&&(!cs.length||cs.indexOf(wCity(id))>=0)&&(!ks.length||ks.indexOf(wKat(id))>=0)}).sort(function(a,b){return wOwe()?data.couriers[a].w.b-data.couriers[b].w.b:data.couriers[b].w.b-data.couriers[a].w.b})}
function wPanel(){var L=wList(),m=wMin(),tot=0;L.forEach(function(id){tot+=+data.couriers[id].w.b||0});
  var all=courierIds().filter(function(id){return data.couriers[id]&&data.couriers[id].w}),cc={},kc={};all.forEach(function(id){var c=wCity(id),k=wKat(id);cc[c]=(cc[c]||0)+1;kc[k]=(kc[k]||0)+1});
  ui0.wcs=(ui0.wcs||[]).filter(function(c){return cc[c]});ui0.wks=(ui0.wks||[]).filter(function(k){return kc[k]});
  var cityI=Object.keys(cc).sort(function(a,b){return a==="—"?1:b==="—"?-1:a.localeCompare(b)}).map(function(c){return [c,(c==="—"?"غير محدد":c)+" ("+cc[c]+")"]}),
      katI=WK_ORDER.filter(function(k){return kc[k]}).map(function(k){return [k,WK_TXT[k]+" ("+kc[k]+")"]});
  return '<section class="panel"><div class="stmthead"><h2>تصدير المحافظ حسب المبلغ</h2><div class="stmttools">'+qMsel("wc","المدينة",cityI,ui0.wcs)+qMsel("wk","الفئة",katI,ui0.wks)+'<select id="wDir" aria-label="نوع الرصيد"><option value="owe"'+(wOwe()?" selected":"")+'>عليه مبلغ</option><option value="has"'+(wOwe()?"":" selected")+'>له مبلغ</option></select><input id="wMin" type="text" inputmode="decimal" autocomplete="off" placeholder="مثال 200" value="'+esc(ui0.wmin||"")+'" style="width:110px"><span class="hint">ر.س فأكثر</span>'+
    '<button class="btn pri" id="wPdf"'+(L.length&&!W_BUSY?"":" disabled")+'>'+(W_BUSY?"جارٍ التصدير…":'تصدير PDF (<span class="num">'+L.length+'</span>)')+'</button></div></div>'+
    '<p class="hint" id="wHint" style="margin:0">'+(m==null?"اختر «عليه مبلغ» أو «له مبلغ» واكتب المبلغ، ويطلع لك عدد المناديب.":!L.length?'<b style="color:var(--bad)">لا يوجد مناديب '+(wOwe()?"عليهم":"لهم")+' '+fmt(m,2)+' ر.س فأكثر'+(wFiltTxt()?" ("+esc(wFiltTxt())+")":"")+'.</b>':'<span class="num">'+L.length+'</span> مندوب '+(wOwe()?"عليهم":"لهم")+' '+fmt(m,2)+' ر.س فأكثر، بمجموع '+fmt(Math.abs(tot),2)+' ر.س.'+(wFiltTxt()?' ('+esc(wFiltTxt())+')':''))+'</p></section>'}
function wDoc(L,m){var tot=0,th='background:#0f4c4a;color:#fff;font-weight:700;padding:6px 4px;border:1px solid #0f4c4a;font-size:11px',td='padding:5px 4px;border:1px solid #d5dedd;font-size:11px;text-align:center';
  var rows=L.map(function(id,i){var c=data.couriers[id],w=c.w;tot+=+w.b||0;return '<tr style="page-break-inside:avoid;background:'+(i%2?"#f4f8f7":"#fff")+'"><td style="'+td+'">'+(i+1)+'</td><td style="'+td+'">'+esc(id)+'</td><td style="'+td+';text-align:right">'+esc(c.n||"—")+'</td><td style="'+td+'">'+esc(wCity(id))+'</td><td style="'+td+'">'+esc(normCat(c.cat)||(c.rg?"الرياض":"—"))+'</td><td style="'+td+'" dir="ltr">'+esc(c.ph?"0"+String(c.ph).replace(/^966/,""):"—")+'</td><td style="'+td+';font-weight:700">'+fmt(w.b,2)+'</td><td style="'+td+'">'+(w.c==null?"—":fmt(w.c,2))+'</td><td style="'+td+'">'+esc(w.d||"—")+'</td></tr>'}).join("");
  return '<div class="noi18n" dir="rtl" style="box-sizing:border-box;width:100%;padding:14px 10px;background:#fff;color:#14302f;font-family:\'IBM Plex Sans Arabic\',Tahoma,sans-serif;direction:rtl">'+
    '<div style="display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px solid #c9a24a;padding-bottom:10px;margin-bottom:12px"><div><div style="font-size:20px;font-weight:700;color:#0f4c4a">مناديب '+(wOwe()?"عليهم":"لهم")+' '+fmt(m,2)+' ر.س فأكثر</div><div style="font-size:12.5px;color:#4a6261;margin-top:2px">'+esc(wFiltTxt()||"كل المدن والفئات")+'</div></div>'+
    '<div style="text-align:left;font-size:12px;color:#4a6261">تاريخ التصدير <span dir="ltr">'+new Date().toISOString().slice(0,10)+'</span></div></div>'+
    '<div style="display:flex;gap:10px;margin-bottom:12px">'+[["عدد المناديب",L.length],["الحد",fmt(m,2)+" ر.س فأكثر"],[wOwe()?"المبلغ المستحق عليهم":"إجمالي أرصدتهم",fmt(Math.abs(tot),2)+" ر.س"]].map(function(x){return '<div style="flex:1;border:1px solid #d5dedd;border-radius:8px;padding:7px 10px"><div style="font-size:10.5px;color:#4a6261">'+x[0]+'</div><div style="font-size:15px;font-weight:700;color:#0f4c4a">'+x[1]+'</div></div>'}).join("")+'</div>'+
    '<table style="width:100%;border-collapse:collapse;table-layout:fixed"><colgroup>'+[5,10,25,10,7,13,11,10,9].map(function(w){return '<col style="width:'+w+'%">'}).join("")+'</colgroup><thead><tr>'+["#","Rider ID","الاسم","المدينة","الفئة","الجوال","رصيد المحفظة","النقد المحصّل","بتاريخ"].map(function(h){return '<th style="'+th+'">'+h+'</th>'}).join("")+'</tr></thead><tbody>'+rows+'</tbody>'+
    '<tfoot><tr><td colspan="6" style="'+td+';font-weight:700;background:#eef3f4">الإجمالي</td><td style="'+td+';font-weight:700;background:#eef3f4">'+fmt(tot,2)+'</td><td colspan="2" style="'+td+';background:#eef3f4"></td></tr></tfoot></table>'+
    '<div style="margin-top:14px;display:flex;justify-content:flex-end;font-size:10.5px;color:#6b7f7e"><span>تصميم المهندس / فاضل العميسي</span></div></div>'}
function wPdf(){var L=wList(),m=wMin();if(!L.length)return;W_BUSY=true;render();
  loadH2P().then(function(h2p){var w=document.createElement("div");w.innerHTML=wDoc(L,m);var el=w.firstChild;ovWords(el);
    return (document.fonts&&document.fonts.ready||Promise.resolve()).then(function(){return h2p().set({margin:[8,6,10,6],filename:"مناديب "+(wOwe()?"عليهم ":"لهم ")+m+" فأكثر"+(wFiltTxt()?" - "+wFiltTxt().replace(/[\\/:*?"<>|]/g," "):"")+" - "+new Date().toISOString().slice(0,10)+".pdf",image:{type:"jpeg",quality:0.95},html2canvas:{scale:2,useCORS:true,backgroundColor:"#ffffff"},jsPDF:{unit:"mm",format:"a4",orientation:"portrait"},pagebreak:{mode:["css","legacy"],avoid:"tr"}}).from(el).save()})})
  .catch(function(){alert("تعذر تحميل مكتبة PDF، تأكد من الاتصال بالإنترنت وحاول مرة أخرى.")})
  .then(function(){W_BUSY=false;render()})}
/* typing the amount only refreshes the panel, so the box keeps focus */
document.addEventListener("input",function(e){if(e.target.id!=="wMin")return;ui0.wmin=e.target.value;var tmp=document.createElement("div");tmp.innerHTML=wPanel();
  ["wHint","wPdf"].forEach(function(k){var o=document.getElementById(k),n=tmp.querySelector("#"+k);if(o&&n)o.replaceWith(n)});if(typeof trTree==="function")try{trTree(document.getElementById("wHint"));trTree(document.getElementById("wPdf"))}catch(x){}});
function vSoon(){''')
js=rep(js,"""  return sampleNote()+'<div class="filters">'+riderPick()+'</div>'+
    '<div class="tbl"><table><thead><tr><th>Rider Id</th><th>الاسم</th><th>رصيد المحفظة<br>Balance</th>""","""  return sampleNote()+'<div class="filters">'+riderPick()+'</div>'+(ids.length?wPanel():"")+
    '<div class="tbl"><table><thead><tr><th>Rider Id</th><th>الاسم</th><th>رصيد المحفظة<br>Balance</th>""")
js=rep(js,'  if(t.id==="ovMon"){ui0.ovm=t.value;render()}','  if(t.id==="ovMon"){ui0.ovm=t.value;render()}\n  if(t.id==="wDir"){ui0.wdir=t.value;render()}')
js=rep(js,'  if(t.dataset.ovpdf){ovPdf(t.dataset.ovpdf);return}','  if(t.dataset.ovpdf){ovPdf(t.dataset.ovpdf);return}\n  if(t.id==="wPdf"){wPdf();return}')
