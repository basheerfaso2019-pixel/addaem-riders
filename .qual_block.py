# delivery quality: city + segment pickers and Excel/PDF export of the filtered list (fadhel 2026-10-12)
js=rep(js,"return r&&(!f.city||r.q.ci===f.city)&&(!f.rid||r.id===f.rid)}).sort(function(a,b){return (a.q.s||\"Z\").localeCompare(b.q.s||\"Z\")||b.q.sc-a.q.sc});\n  var cnt={};rows.forEach(function(r){cnt[r.q.s]=(cnt[r.q.s]||0)+1});",
 "return r&&(!f.rid||r.id===f.rid)}).sort(function(a,b){return (a.q.s||\"Z\").localeCompare(b.q.s||\"Z\")||b.q.sc-a.q.sc});\n"
 "  var cities={};rows.forEach(function(r){if(r.q.ci)cities[r.q.ci]=1});cities=Object.keys(cities).sort();if(ui0.qcity&&cities.indexOf(ui0.qcity)<0)ui0.qcity=\"\";\n"
 "  rows=rows.filter(function(r){return !ui0.qcity||r.q.ci===ui0.qcity});\n"
 "  var cnt={};rows.forEach(function(r){cnt[r.q.s]=(cnt[r.q.s]||0)+1});var segs=Object.keys(cnt).sort();if(ui0.qseg&&segs.indexOf(ui0.qseg)<0)ui0.qseg=\"\";\n"
 "  rows=rows.filter(function(r){return !ui0.qseg||r.q.s===ui0.qseg});QROWS={m:m,rows:rows};")
js=rep(js,"  var cities={};rows.forEach(function(r){if(r.q.ci)cities[r.q.ci]=1});\n  return sampleNote()+'<div class=\"filters\"><label class=\"fcard\"><span>الشهر Month</span><select id=\"qMon\">'+ms.map(function(x){return '<option value=\"'+x+'\"'+(x===m?\" selected\":\"\")+'>'+x+'</option>'}).join(\"\")+'</select></label>'+\n    ''+riderPick()+'</div>'+",
 "  return sampleNote()+'<div class=\"filters\"><label class=\"fcard\"><span>الشهر Month</span><select id=\"qMon\">'+ms.map(function(x){return '<option value=\"'+x+'\"'+(x===m?\" selected\":\"\")+'>'+x+'</option>'}).join(\"\")+'</select></label>'+\n"
 "    '<label class=\"fcard\"><span>المدينة City</span><select id=\"qCity\"><option value=\"\">كل المدن</option>'+cities.map(function(c){return '<option value=\"'+esc(c)+'\"'+(c===ui0.qcity?\" selected\":\"\")+'>'+esc(c)+'</option>'}).join(\"\")+'</select></label>'+\n"
 "    '<label class=\"fcard\"><span>التصنيف Segment</span><select id=\"qSeg\"><option value=\"\">كل الفئات</option>'+segs.map(function(s){return '<option value=\"'+esc(s)+'\"'+(s===ui0.qseg?\" selected\":\"\")+'>فئة '+esc(s)+' ('+cnt[s]+')</option>'}).join(\"\")+'</select></label>'+\n"
 "    riderPick()+'<div class=\"row\" style=\"gap:8px;align-self:flex-end\"><button class=\"btn pri\" id=\"qXlsx\"'+(rows.length?\"\":\" disabled\")+'>تصدير Excel</button><button class=\"btn\" id=\"qPdf\"'+(rows.length&&!OV_BUSY?\"\":\" disabled\")+'>'+(OV_BUSY===\"q\"?\"جارٍ التصدير…\":\"تصدير PDF\")+'</button></div></div>'+")
js=rep(js,"'<div class=\"kpis\">'+Object.keys(cnt).sort().map(function(s){return kpi('تصنيف '+segPill(s),N(cnt[s],0),'مندوب')}).join(\"\")+'</div>'+",
 "'<div class=\"kpis\">'+segs.map(function(s){return kpi('تصنيف '+segPill(s),N(cnt[s],0),'مندوب')}).join(\"\")+'</div>'+")
js=rep(js,'function vSoon(){',r'''/* ---------- delivery quality export ---------- */
var QROWS=null,Q_HEAD=["#","Rider ID","الاسم","المدينة","التصنيف","درجة الجودة %","التوصيل في الوقت %","درجة الفشل %","نجاح التحقق %","إجمالي الطلبات","المكتملة","في الوقت","فشل بسبب المندوب"];
function qTitle(){return "تصنيف جودة التوصيل"+(ui0.qseg?" - فئة "+ui0.qseg:"")+(ui0.qcity?" - "+ui0.qcity:"")}
function qVals(r,i){var q=r.q,pc=function(v){return v==null||isNaN(v)?"":Math.round(v*10000)/100};return [i+1,/^\d+$/.test(r.id)?+r.id:r.id,cname(r.id),q.ci||"",q.s||"",pc(q.sc),pc(q.ot),pc(q.fr),pc(q.vr),q.g,q.cp,q.it,q.f]}
function qExcel(){if(!QROWS||!QROWS.rows.length)return;var Q=QROWS;loadXLSX().then(function(X){
    var aoa=[[qTitle()+" - "+monTxt(Q.m)],[]].concat([Q_HEAD],Q.rows.map(qVals));
    var ws=X.utils.aoa_to_sheet(aoa);ws["!cols"]=[5,11,30,14,9,12,15,12,12,12,10,10,14].map(function(w){return {wch:w}});ws["!merges"]=[{s:{r:0,c:0},e:{r:0,c:12}}];
    var wb=X.utils.book_new();wb.Workbook={Views:[{RTL:true}]};X.utils.book_append_sheet(wb,ws,"جودة التوصيل");X.writeFile(wb,qTitle()+" - "+Q.m+".xlsx")})
  .catch(function(){alert("تعذر تحميل مكتبة Excel، تأكد من الاتصال بالإنترنت وحاول مرة أخرى.")})}
function qDoc(Q){var th='background:#0f4c4a;color:#fff;font-weight:700;padding:6px 3px;border:1px solid #0f4c4a;font-size:9.5px;line-height:1.35',td='padding:5px 3px;border:1px solid #d5dedd;font-size:10px;text-align:center;overflow:hidden';
  var rows=Q.rows.map(function(r,i){var v=qVals(r,i);return '<tr style="page-break-inside:avoid;background:'+(i%2?"#f4f8f7":"#fff")+'">'+v.map(function(x,j){return '<td style="'+td+(j===2?';text-align:right':'')+(j===4?';font-weight:700':'')+'">'+esc(x===""?"—":typeof x==="number"&&j>4&&j<9?fmt(x,2):x)+'</td>'}).join("")+'</tr>'}).join("");
  var cnt={};Q.rows.forEach(function(r){cnt[r.q.s]=(cnt[r.q.s]||0)+1});
  return '<div class="noi18n" dir="rtl" style="box-sizing:border-box;width:100%;padding:14px 10px;background:#fff;color:#14302f;font-family:\'IBM Plex Sans Arabic\',Tahoma,sans-serif;direction:rtl">'+
    '<div style="display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px solid #c9a24a;padding-bottom:10px;margin-bottom:12px"><div><div style="font-size:19px;font-weight:700;color:#0f4c4a">'+esc("تصنيف جودة التوصيل"+(ui0.qseg?" - فئة "+ui0.qseg:""))+(ui0.qcity?' <span dir="ltr" style="display:inline-block">· '+esc(ui0.qcity)+'</span>':'')+'</div><div style="font-size:12.5px;color:#4a6261;margin-top:2px">'+esc(data.company||"")+'</div></div>'+
    '<div style="text-align:left;font-size:12px;color:#4a6261"><div style="font-size:15px;font-weight:700;color:#0f4c4a">'+monTxt(Q.m)+'</div><div>عدد المناديب '+Q.rows.length+'</div></div></div>'+
    '<div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap">'+Object.keys(cnt).sort().map(function(s){return '<div style="border:1px solid #d5dedd;border-radius:8px;padding:6px 14px;font-size:11px;color:#4a6261;text-align:center"><div>'+esc("فئة "+s)+'</div><div style="font-size:15px;font-weight:700;color:#0f4c4a">'+cnt[s]+'</div></div>'}).join("")+'</div>'+
    '<table style="width:100%;border-collapse:collapse;table-layout:fixed"><colgroup>'+[4,9,21,9,6,7,8,7,7,6,6,5,5].map(function(w){return '<col style="width:'+w+'%">'}).join("")+'</colgroup><thead><tr>'+Q_HEAD.map(function(h){return '<th style="'+th+'">'+h+'</th>'}).join("")+'</tr></thead><tbody>'+rows+'</tbody></table>'+
    '<div style="margin-top:14px;display:flex;justify-content:space-between;font-size:10.5px;color:#6b7f7e"><span>تاريخ التصدير '+new Date().toISOString().slice(0,10)+'</span><span>تصميم المهندس / فاضل العميسي</span></div></div>'}
function qPdf(){if(!QROWS||!QROWS.rows.length)return;var Q=QROWS;OV_BUSY="q";render();
  loadH2P().then(function(h2p){var w=document.createElement("div");w.innerHTML=qDoc(Q);var el=w.firstChild;ovWords(el);
    return (document.fonts&&document.fonts.ready||Promise.resolve()).then(function(){return h2p().set({margin:[8,6,10,6],filename:qTitle()+" - "+Q.m+".pdf",image:{type:"jpeg",quality:0.95},html2canvas:{scale:2,useCORS:true,backgroundColor:"#ffffff"},jsPDF:{unit:"mm",format:"a4",orientation:"portrait"},pagebreak:{mode:["css","legacy"],avoid:"tr"}}).from(el).save()})})
  .catch(function(){alert("تعذر تحميل مكتبة PDF، تأكد من الاتصال بالإنترنت وحاول مرة أخرى.")})
  .then(function(){OV_BUSY="";render()})}
function vSoon(){''')
js=rep(js,'  if(t.dataset.ovpdf){ovPdf(t.dataset.ovpdf);return}','  if(t.dataset.ovpdf){ovPdf(t.dataset.ovpdf);return}\n  if(t.id==="qXlsx"){qExcel();return}\n  if(t.id==="qPdf"){qPdf();return}')
js=rep(js,'  if(t.id==="ovMon"){ui0.ovm=t.value;render()}','  if(t.id==="ovMon"){ui0.ovm=t.value;render()}\n  if(t.id==="qCity"){ui0.qcity=t.value;render()}\n  if(t.id==="qSeg"){ui0.qseg=t.value;render()}')
