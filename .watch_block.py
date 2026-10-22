# «متابعة الفئة أ» daily PDF (fadhel 2026-10-22): category أ riders with quality E/F, OR wallet <= -300, OR actual hours < 8 on the chosen day
# (no perf row that day = did not work = 0 h). Riders on leave or whose contract ended are skipped. Panel on نظرة عامة.
js=rep(js,"'+cityT+'</tbody></table></div></section></div>'+ovPanel();","'+cityT+'</tbody></table></div></section></div>'+ovPanel()+waPanel();")
js=rep(js,'  if(t.id==="shXlsx"){shExport();return}','  if(t.id==="shXlsx"){shExport();return}\n  if(t.id==="waPdf"){waPdf();return}')
js=rep(js,'  if(t.id==="ovMon"){ui0.ovm=t.value;render()}','  if(t.id==="ovMon"){ui0.ovm=t.value;render()}\n  if(t.id==="waDay"){ui0.wad=t.value;render()}')
js=rep(js,'function vSoon(){',r'''/* ---------- daily watch list: category أ ---------- */
var WA_WAL=-300,WA_HRS=8;
function waDays(){return Object.keys(data.days||{}).filter(function(d){var o=data.days[d];return Object.keys(o).some(function(id){return o[id][AC]!=null})}).sort().reverse()}
function waQ(c,day){var q=c&&c.q;if(!q)return null;var ms=Object.keys(q).filter(function(m){return m<=day.slice(0,7)}).sort();return ms.length?{m:ms[ms.length-1],s:q[ms[ms.length-1]].s}:null}
function waOff(c,day){var s=c&&c.st;if(!s||!s.t)return false;if(s.t==="ended")return !s.f||s.f<=day;if(s.t==="leave"||s.t==="susp")return (!s.f||s.f<=day)&&(!s.u||s.u>=day);return false}
function waRows(day){var out=[],o=data.days[day]||{};
  Object.keys(data.couriers||{}).forEach(function(id){if(catOf(id)!=="أ")return;var c=data.couriers[id];if(waOff(c,day))return;
    var x=o[id],ac=x&&x[AC]!=null?+x[AC]:null,pl=x&&x[PL]!=null?+x[PL]:null,q=waQ(c,day),w=c.w&&c.w.b!=null?+c.w.b:null,why=[];
    if(q&&(q.s==="E"||q.s==="F"))why.push("جودة التوصيل "+q.s);
    if(w!=null&&w<=WA_WAL)why.push("المحفظة "+fmt(w,2));
    if(ac==null)why.push("لم يعمل هذا اليوم");else if(ac<WA_HRS)why.push("ساعات العمل "+fmt(ac,2));
    if(why.length)out.push({id:id,city:x&&x[CI]||"",q:q,w:w,ac:ac,pl:pl,why:why})});
  return out.sort(function(a,b){return b.why.length-a.why.length||(a.w==null?0:a.w)-(b.w==null?0:b.w)})}
function waPanel(){var ds=waDays();if(!ds.length)return "";var day=ui0.wad&&ds.indexOf(ui0.wad)>=0?ui0.wad:ds[0],R=waRows(day);
  var cnt=function(re){return R.filter(function(r){return r.why.some(function(w){return re.test(w)})}).length};
  var body=R.slice(0,12).map(function(r,i){return '<tr><td>'+(i+1)+'</td><td class="num">'+esc(r.id)+'</td><td class="s">'+esc(cname(r.id))+'</td><td>'+(r.q?segPill(r.q.s):"—")+'</td><td class="num"'+(r.w!=null&&r.w<=WA_WAL?' style="color:var(--bad);font-weight:700"':'')+'>'+(r.w==null?"—":fmt(r.w,2))+'</td><td class="num"'+(r.ac==null||r.ac<WA_HRS?' style="color:var(--bad);font-weight:700"':'')+'>'+(r.ac==null?"0":fmt(r.ac,2))+'</td><td class="s" style="font-size:12.5px">'+esc(r.why.join("، "))+'</td></tr>'}).join("");
  return '<section class="panel"><div class="stmthead"><h2>متابعة مناديب الفئة أ اليومية</h2><div class="stmttools"><select id="waDay" aria-label="اليوم">'+ds.map(function(d){return '<option value="'+d+'"'+(d===day?" selected":"")+'>'+wd(d)+' '+d+'</option>'}).join("")+'</select>'+
    '<button class="btn pri" id="waPdf"'+(R.length&&!OV_BUSY?"":" disabled")+'>'+(OV_BUSY==="wa"?"جارٍ التصدير…":"⬇ PDF")+' <span class="num">('+R.length+')</span></button></div></div>'+
    '<p class="hint">مناديب الفئة أ اللي عندهم واحد أو أكثر: جودة التوصيل E أو F، المحفظة '+WA_WAL+' ريال أو أقل، ساعات العمل الفعلية أقل من '+WA_HRS+' (أو لم يعمل). '+
    'جودة E/F: <b class="num">'+cnt(/^جودة/)+'</b> · المحفظة: <b class="num">'+cnt(/^المحفظة/)+'</b> · الساعات: <b class="num">'+cnt(/ساعات|لم يعمل/)+'</b></p>'+
    (R.length?'<div class="tbl" style="box-shadow:none"><table><thead><tr><th>#</th><th>Rider Id</th><th>الاسم</th><th>الجودة</th><th>المحفظة</th><th>الساعات الفعلية</th><th>السبب</th></tr></thead><tbody>'+body+'</tbody></table></div>'+(R.length>12?'<p class="hint">يظهر أول 12 هنا، والقائمة كاملة في ملف PDF.</p>':''):'<p class="hint">لا يوجد مناديب من الفئة أ تنطبق عليهم الشروط في هذا اليوم.</p>')+'</section>'}
function waDoc(day,R){var th='background:#20386b;color:#fff;font-weight:700;padding:6px 4px;border:1px solid #20386b;font-size:10.5px',td='padding:5px 4px;border:1px solid #d9deeb;font-size:10.5px;text-align:center',bad=';color:#b5362f;font-weight:700';
  var rows=R.map(function(r,i){return '<tr style="page-break-inside:avoid;background:'+(i%2?"#f3f5fa":"#fff")+'"><td style="'+td+'">'+(i+1)+'</td><td style="'+td+'">'+esc(r.id)+'</td><td style="'+td+';text-align:right">'+esc(cname(r.id))+'</td><td style="'+td+'">'+esc(r.city||"—")+'</td>'+
    '<td style="'+td+(r.q&&/[EF]/.test(r.q.s)?bad:'')+'">'+(r.q?esc(r.q.s):"—")+'</td><td style="'+td+(r.w!=null&&r.w<=WA_WAL?bad:'')+'" dir="ltr">'+(r.w==null?"—":fmt(r.w,2))+'</td>'+
    '<td style="'+td+(r.ac==null||r.ac<WA_HRS?bad:'')+'">'+(r.ac==null?"0":fmt(r.ac,2))+'</td><td style="'+td+'">'+(r.pl==null?"—":fmt(r.pl,2))+'</td><td style="'+td+';text-align:right;font-size:10px">'+esc(r.why.join("، "))+'</td></tr>'}).join("");
  var box=function(l,v){return '<div style="border:1px solid #d9deeb;border-radius:8px;padding:6px 14px;font-size:11px;color:#5b6386;text-align:center"><div>'+l+'</div><div style="font-size:16px;font-weight:700;color:#20386b">'+v+'</div></div>'};
  var cnt=function(re){return R.filter(function(r){return r.why.some(function(w){return re.test(w)})}).length};
  return '<div class="noi18n" dir="rtl" style="box-sizing:border-box;width:100%;padding:14px 12px;background:#fff;color:#141a33;font-family:\'IBM Plex Sans Arabic\',Tahoma,sans-serif;direction:rtl">'+
    '<div style="height:4px;background:linear-gradient(90deg,#e6ecf5,#2f4e86 70%,#20386b);margin-bottom:10px"></div>'+
    '<div style="display:flex;justify-content:space-between;align-items:center;border-bottom:3px solid #f28a1a;padding-bottom:10px;margin-bottom:12px"><div><div style="font-size:19px;font-weight:700;color:#20386b">متابعة مناديب الفئة أ</div><div style="font-size:12.5px;color:#5b6386;margin-top:2px">'+esc(data.company||"")+'</div></div>'+
    '<div style="text-align:center;font-size:12px;color:#5b6386"><div style="font-size:15px;font-weight:700;color:#20386b">'+esc(wd(day))+' <span dir="ltr">'+esc(day)+'</span></div><div>اليوم</div></div><img src="logo.png" style="height:42px"></div>'+
    '<div style="display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap">'+box("عدد المناديب",R.length)+box("جودة E أو F",cnt(/^جودة/))+box("المحفظة "+WA_WAL+" أو أقل",cnt(/^المحفظة/))+box("ساعات أقل من "+WA_HRS,cnt(/ساعات|لم يعمل/))+'</div>'+
    '<table style="width:100%;border-collapse:collapse;table-layout:fixed"><colgroup>'+[4,9,23,8,7,9,8,8,24].map(function(w){return '<col style="width:'+w+'%">'}).join("")+'</colgroup><thead><tr>'+["#","Rider ID","الاسم","المدينة","الجودة","المحفظة","الساعات الفعلية","المخططة","السبب"].map(function(h){return '<th style="'+th+'">'+h+'</th>'}).join("")+'</tr></thead><tbody>'+rows+'</tbody></table>'+
    '<div style="margin-top:14px;display:flex;justify-content:space-between;font-size:10.5px;color:#5b6386"><span>تاريخ التصدير '+new Date().toISOString().slice(0,10)+'</span><span>تصميم المهندس / فاضل العميسي</span></div></div>'}
function waPdf(){var ds=waDays();if(!ds.length)return;var day=ui0.wad&&ds.indexOf(ui0.wad)>=0?ui0.wad:ds[0],R=waRows(day);if(!R.length)return;OV_BUSY="wa";render();var sy=window.scrollY;window.scrollTo(0,0);
  loadH2P().then(function(h2p){var w=document.createElement("div");w.innerHTML=waDoc(day,R);var el=w.firstChild;ovWords(el);
    return (document.fonts&&document.fonts.ready||Promise.resolve()).then(function(){return h2p().set({margin:[8,6,10,6],filename:"متابعة الفئة أ - "+day+".pdf",image:{type:"jpeg",quality:0.95},html2canvas:{scale:2,useCORS:true,backgroundColor:"#ffffff"},jsPDF:{unit:"mm",format:"a4",orientation:"portrait"},pagebreak:{mode:["css","legacy"],avoid:"tr"}}).from(el).save()})})
  .catch(function(){alert("تعذر تحميل مكتبة PDF، تأكد من الاتصال بالإنترنت وحاول مرة أخرى.")})
  .then(function(){OV_BUSY="";render();window.scrollTo(0,sy)})}
function vSoon(){''')
