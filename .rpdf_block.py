# «أداء المناديب»: city + rider-category pickers that filter the table, and a PDF of the selection (fadhel 2026-10-19)
js=rep(js,"||1):0;\n  var body=rows.map(function(a){var s=status(a,avg)","||1):0;rows=rpFilter(rows,avg);\n  var body=rows.map(function(a){var s=status(a,avg)")
js=rep(js,"return sampleNote()+filters()+det+","return sampleNote()+filters()+rpBar()+det+")
js=rep(js,'var QK={c:"qcs",s:"qss",k:"qks"};','var QK={c:"qcs",s:"qss",k:"qks",rc:"rcs",rk:"rks",rs:"rss"};')
js=rep(js,'  if(t.id==="qPdf"){qPdf();return}','  if(t.id==="qPdf"){qPdf();return}\n  if(t.id==="rpPdf"){rpPdf();return}')
js=rep(js,'function vSoon(){',r'''/* ---------- riders performance: city/category selection + PDF ---------- */
var RP=null,RP_HEAD=["#","Rider ID","الاسم","الفئة","المدينة","أيام العمل","الورديات","الساعات المخططة","الساعات الفعلية","الاستراحة","القبول","عدم الحضور","المكتملة","المرفوضة >2","المسافة كم","الحالة"];
function rpCat(id){return catOf(id)||"—"}
function rpCatName(k){return k==="—"?"بدون فئة":k==="الرياض"?"مناديب الرياض":"فئة "+k}
var RP_ST=["أعلى من المتوسط","ضمن المتوسط","أقل من المتوسط","لم يحضر"];
function rpFilter(rows,avg){rows.forEach(function(a){a.stt=status(a,avg)[1]});var cc={},kc={},sc={};rows.forEach(function(a){var c=a.city||"—",k=rpCat(a.id);cc[c]=(cc[c]||0)+1;kc[k]=(kc[k]||0)+1;sc[a.stt]=(sc[a.stt]||0)+1});
  var sts=RP_ST.filter(function(x){return sc[x]});ui0.rss=(ui0.rss||[]).filter(function(x){return sts.indexOf(x)>=0});
  var cities=Object.keys(cc).sort(),kats=Object.keys(kc).sort(function(a,b){return shCatOrder(a)-shCatOrder(b)});
  ui0.rcs=(ui0.rcs||[]).filter(function(c){return cities.indexOf(c)>=0});ui0.rks=(ui0.rks||[]).filter(function(k){return kats.indexOf(k)>=0});
  var out=rows.filter(function(a){return (!ui0.rcs.length||ui0.rcs.indexOf(a.city||"—")>=0)&&(!ui0.rks.length||ui0.rks.indexOf(rpCat(a.id))>=0)&&(!ui0.rss.length||ui0.rss.indexOf(a.stt)>=0)});
  RP={f:F(),rows:out,cities:cities.map(function(c){return [c,c+" ("+cc[c]+")"]}),kats:kats.map(function(k){return [k,rpCatName(k)+" ("+kc[k]+")"]}),sts:sts.map(function(x){return [x,x+" ("+sc[x]+")"]})};return out}
function rpSelTxt(){var k=(ui0.rks||[]).map(rpCatName).join(" + "),c=(ui0.rcs||[]).join(" + "),t=(ui0.rss||[]).join(" + ");return (k?" - "+k:"")+(c?" - "+c:"")+(t?" - "+t:"")}
function rpBar(){if(!RP)return "";
  return '<div class="filters rpbar">'+qMsel("rk","فئة المندوب",RP.kats,ui0.rks||[])+qMsel("rc","المدينة",RP.cities,ui0.rcs||[])+qMsel("rs","الحالة",RP.sts,ui0.rss||[])+
    '<div class="row" style="gap:8px;align-self:flex-end"><button class="btn pri" id="rpPdf"'+(RP.rows.length&&!OV_BUSY?"":" disabled")+'>'+(OV_BUSY==="rp"?"جارٍ التجهيز…":"⬇ تحميل PDF")+'</button><span class="hint">'+RP.rows.length+' مندوب</span></div></div>'}
function rpVals(a,i){return [i+1,a.id,cname(a.id),rpCat(a.id)==="—"?"":rpCat(a.id),a.city||"",fmt(a.days,0),fmt(a.sh,0),fmt(a.pl,1),fmt(a.ac,1),fmt(a.br,1),a.ar==null||isNaN(a.ar)?"—":fmt(a.ar*100,0)+"%",fmt(a.ns,0),fmt(a.cp,0),fmt(a.de||0,0),a.di==null?"—":fmt(a.di,1),a.stt||""]}
function rpDoc(Q){var th='background:#0f4c4a;color:#fff;font-weight:700;padding:6px 3px;border:1px solid #0f4c4a;font-size:9.5px;line-height:1.35',td='padding:5px 3px;border:1px solid #d5dedd;font-size:10px;text-align:center;overflow:hidden';
  var tot=Q.rows.reduce(function(s,a){s.cp+=a.cp||0;s.days+=a.days||0;s.ac+=a.ac||0;return s},{cp:0,days:0,ac:0});
  var rows=Q.rows.map(function(a,i){return '<tr style="page-break-inside:avoid;background:'+(i%2?"#f4f8f7":"#fff")+'">'+rpVals(a,i).map(function(x,j){return '<td style="'+td+(j===2?';text-align:right':'')+(j===12?';font-weight:700':'')+'">'+esc(x===""?"—":x)+'</td>'}).join("")+'</tr>'}).join("");
  var box=function(l,v){return '<div style="border:1px solid #d5dedd;border-radius:8px;padding:6px 14px;font-size:11px;color:#4a6261;text-align:center"><div>'+l+'</div><div style="font-size:15px;font-weight:700;color:#0f4c4a">'+v+'</div></div>'};
  return '<div class="noi18n" dir="rtl" style="box-sizing:border-box;width:100%;padding:14px 10px;background:#fff;color:#14302f;font-family:\'IBM Plex Sans Arabic\',Tahoma,sans-serif;direction:rtl">'+
    '<div style="display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px solid #c9a24a;padding-bottom:10px;margin-bottom:12px"><div><div style="font-size:19px;font-weight:700;color:#0f4c4a">'+esc("أداء المناديب"+rpSelTxt())+'</div><div style="font-size:12.5px;color:#4a6261;margin-top:2px">'+esc(data.company||"")+'</div></div>'+
    '<div style="text-align:left;font-size:12px;color:#4a6261"><div style="font-size:14px;font-weight:700;color:#0f4c4a" dir="ltr">'+esc(Q.f.from)+' → '+esc(Q.f.to)+'</div><div>الفترة</div></div></div>'+
    '<div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap">'+box("عدد المناديب",Q.rows.length)+box("الطلبات المكتملة",fmt(tot.cp,0))+box("متوسط يومي للمندوب",tot.days?fmt(tot.cp/tot.days,1):"—")+box("الساعات الفعلية",fmt(tot.ac,0))+'</div>'+
    '<table style="width:100%;border-collapse:collapse;table-layout:fixed"><colgroup>'+[3,6,16,4,7,4,5,5,5,5,5,5,6,6,5,9].map(function(w){return '<col style="width:'+w+'%">'}).join("")+'</colgroup><thead><tr>'+RP_HEAD.map(function(h){return '<th style="'+th+'">'+h+'</th>'}).join("")+'</tr></thead><tbody>'+rows+'</tbody></table>'+
    '<div style="margin-top:14px;display:flex;justify-content:space-between;font-size:10.5px;color:#6b7f7e"><span>تاريخ التصدير '+new Date().toISOString().slice(0,10)+'</span><span>تصميم المهندس / فاضل العميسي</span></div></div>'}
function rpPdf(){if(!RP||!RP.rows.length)return;var Q={f:RP.f,rows:RP.rows.slice()};OV_BUSY="rp";render();
  loadH2P().then(function(h2p){var w=document.createElement("div");w.innerHTML=rpDoc(Q);var el=w.firstChild;ovWords(el);
    return (document.fonts&&document.fonts.ready||Promise.resolve()).then(function(){return h2p().set({margin:[8,6,10,6],filename:"أداء المناديب"+rpSelTxt()+" "+Q.f.from+" إلى "+Q.f.to+".pdf",image:{type:"jpeg",quality:0.95},html2canvas:{scale:2,useCORS:true,backgroundColor:"#ffffff"},jsPDF:{unit:"mm",format:"a4",orientation:"landscape"},pagebreak:{mode:["css","legacy"],avoid:"tr"}}).from(el).save()})})
  .catch(function(){alert("تعذر تحميل مكتبة PDF، تأكد من الاتصال بالإنترنت وحاول مرة أخرى.")})
  .then(function(){OV_BUSY="";render()})}
function vSoon(){''')
css+='''
.rpbar{margin-top:-4px}
'''
