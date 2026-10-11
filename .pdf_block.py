# overall view: PDF export of top / middle / low order riders (fadhel 2026-10-11)
js=rep(js,'function vSoon(){',r'''/* ---------- overall: tier PDFs ---------- */
var H2P_URL="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js",OV_BUSY="";
function loadH2P(){return window.html2pdf?Promise.resolve(window.html2pdf):new Promise(function(ok,no){var s=document.createElement("script");s.src=H2P_URL;s.onload=function(){ok(window.html2pdf)};s.onerror=function(){no(new Error("lib"))};document.head.appendChild(s)})}
function ovMonths(){var m={};days().forEach(function(d){m[d.slice(0,7)]=1});return Object.keys(m).sort().reverse()}
function ovMon(){var ms=ovMonths();return ui0.ovm&&ms.indexOf(ui0.ovm)>=0?ui0.ovm:ms[0]}
/* riders with completed orders in the month, highest first, split into three near-equal groups */
function ovTiers(mon){var ds=days().filter(function(d){return d.slice(0,7)===mon}),g={};
  ds.forEach(function(d){var r=data.days[d];for(var id in r)(g[id]||(g[id]=[])).push({d:d,id:id,x:r[id]})});
  var rows=Object.keys(g).map(function(id){var a=agg(g[id]),wd=g[id].filter(function(o){return (+o.x[CP]||0)>0}).length;return {id:id,cp:a.cp,ar:a.ar,ac:a.ac,wd:wd}}).filter(function(r){return r.cp>0});
  rows.sort(function(a,b){return b.cp-a.cp||(+a.id)-(+b.id)});
  var n=rows.length,a=Math.ceil(n/3),b=Math.ceil((n-a)/2);
  return {ds:ds,top:rows.slice(0,a),mid:rows.slice(a,a+b),low:rows.slice(a+b)}}
var OV_T={top:"المناديب الأعلى طلبات",mid:"المناديب متوسطو الطلبات",low:"المناديب الأقل طلبات"};
function ovPanel(){var ms=ovMonths();if(!ms.length)return "";var m=ovMon(),t=ovTiers(m);
  var btn=function(k,c){var L=t[k];return '<button class="btn '+c+'" data-ovpdf="'+k+'"'+(OV_BUSY||!L.length?" disabled":"")+'>'+(OV_BUSY===k?"جارٍ التصدير…":"PDF · "+OV_T[k])+' <span class="num">('+L.length+')</span></button>'};
  return '<section class="panel"><div class="stmthead"><h2>تقارير المناديب حسب الطلبات</h2><div class="stmttools"><select id="ovMon" aria-label="الشهر">'+ms.map(function(x){return '<option value="'+x+'"'+(x===m?" selected":"")+'>'+monTxt(x)+'</option>'}).join("")+'</select></div></div>'+
    '<p class="hint">المناديب الذين أكملوا طلبات في '+monLabel(m)+' مرتبون من الأعلى إلى الأقل ومقسومون إلى ثلاث فئات متساوية تقريباً.</p>'+
    '<div class="row" style="gap:10px;flex-wrap:wrap">'+btn("top","pri")+btn("mid","")+btn("low","")+'</div></section>'}
function ovDoc(k,m,t){var L=t[k],off=k==="top"?0:k==="mid"?t.top.length:t.top.length+t.mid.length,tot=0;L.forEach(function(r){tot+=r.cp});
  var ds=t.ds,f=function(n,d){return fmt(n,d)},th='background:#0f4c4a;color:#fff;font-weight:700;padding:6px 3px;border:1px solid #0f4c4a;font-size:10px;line-height:1.35',td='padding:5px 3px;border:1px solid #d5dedd;font-size:10.5px;overflow:hidden;text-align:center';
  var rows=L.map(function(r,i){var c=data.couriers[r.id]||{};return '<tr style="page-break-inside:avoid;background:'+(i%2?"#f4f8f7":"#fff")+'"><td style="'+td+'">'+(off+i+1)+'</td><td style="'+td+'">'+esc(r.id)+'</td><td style="'+td+';text-align:right">'+esc(c.n||"—")+'</td><td style="'+td+'">'+esc(normCat(c.cat)||"—")+'</td><td style="'+td+'">'+esc(c.v||"—")+'</td><td style="'+td+'">'+r.wd+'</td><td style="'+td+';font-weight:700">'+f(r.cp,0)+'</td><td style="'+td+'">'+(r.wd?f(r.cp/r.wd,1):"—")+'</td><td style="'+td+'">'+(r.ar==null?"—":f(r.ar,1)+"%")+'</td><td style="'+td+'">'+f(r.ac,1)+'</td><td style="'+td+'">'+(r.ac?f(r.cp/r.ac,2):"—")+'</td></tr>'}).join("");
  return '<div class="noi18n" dir="rtl" style="box-sizing:border-box;width:100%;padding:14px 10px;background:#fff;color:#14302f;font-family:\'IBM Plex Sans Arabic\',Tahoma,sans-serif;direction:rtl">'+
    '<div style="display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px solid #c9a24a;padding-bottom:10px;margin-bottom:12px"><div><div style="font-size:20px;font-weight:700;color:#0f4c4a">'+esc(OV_T[k])+'</div><div style="font-size:12.5px;color:#4a6261;margin-top:2px">'+esc(data.company||"")+'</div></div>'+
    '<div style="text-align:left;font-size:12px;color:#4a6261"><div style="font-size:15px;font-weight:700;color:#0f4c4a">'+monTxt(m)+'</div><div>من '+ds[0]+' إلى '+ds[ds.length-1]+'</div></div></div>'+
    '<div style="display:flex;gap:10px;margin-bottom:12px">'+[["عدد المناديب",L.length],["إجمالي الطلبات",f(tot,0)],["متوسط الطلبات للمندوب",L.length?f(tot/L.length,1):"0"],["الترتيب",(off+1)+" – "+(off+L.length)+" من "+(t.top.length+t.mid.length+t.low.length)]].map(function(x){return '<div style="flex:1;border:1px solid #d5dedd;border-radius:8px;padding:7px 10px"><div style="font-size:10.5px;color:#4a6261">'+x[0]+'</div><div style="font-size:15px;font-weight:700;color:#0f4c4a">'+x[1]+'</div></div>'}).join("")+'</div>'+
    '<table style="width:100%;border-collapse:collapse;table-layout:fixed"><colgroup>'+[4,9,25,5,8,7,9,8,8,8,9].map(function(w){return '<col style="width:'+w+'%">'}).join("")+'</colgroup><thead><tr>'+["#","Rider ID","الاسم","الفئة","المركبة","أيام العمل","الطلبات المكتملة","المتوسط اليومي","نسبة القبول","ساعات العمل","طلب لكل ساعة"].map(function(h){return '<th style="'+th+'">'+h+'</th>'}).join("")+'</tr></thead><tbody>'+rows+'</tbody></table>'+
    '<div style="margin-top:14px;display:flex;justify-content:space-between;font-size:10.5px;color:#6b7f7e"><span>تاريخ التصدير '+new Date().toISOString().slice(0,10)+'</span><span>تصميم المهندس / فاضل العميسي</span></div></div>'}
/* html2canvas drops spaces between Arabic words, so each word gets its own box */
function ovWords(el){var tw=document.createTreeWalker(el,NodeFilter.SHOW_TEXT),ns=[],n;while(n=tw.nextNode())if(/\S\s+\S/.test(n.nodeValue)&&/[؀-ۿ]/.test(n.nodeValue))ns.push(n);
  ns.forEach(function(n){var f=document.createDocumentFragment();n.nodeValue.trim().split(/\s+/).forEach(function(w){var s=document.createElement("span");s.style.cssText="display:inline-block;margin:0 .15em";s.textContent=w;f.appendChild(s)});n.parentNode.replaceChild(f,n)})}
function ovPdf(k){var m=ovMon(),t=ovTiers(m);if(!t[k].length)return;OV_BUSY=k;render();
  loadH2P().then(function(h2p){var w=document.createElement("div");w.innerHTML=ovDoc(k,m,t);var el=w.firstChild;ovWords(el);
    return (document.fonts&&document.fonts.ready||Promise.resolve()).then(function(){return h2p().set({margin:[8,6,10,6],filename:OV_T[k]+" - "+m+".pdf",image:{type:"jpeg",quality:0.95},html2canvas:{scale:2,useCORS:true,backgroundColor:"#ffffff"},jsPDF:{unit:"mm",format:"a4",orientation:"portrait"},pagebreak:{mode:["css","legacy"],avoid:"tr"}}).from(el).save()})})
  .catch(function(){alert("تعذر تحميل مكتبة PDF، تأكد من الاتصال بالإنترنت وحاول مرة أخرى.")})
  .then(function(){OV_BUSY="";render()})}
function vSoon(){''')
js=rep(js,"""<th>المدينة</th><th>المناديب</th><th>المكتملة</th><th>القبول</th><th>الساعات</th></tr></thead><tbody>'+cityT+'</tbody></table></div></section></div>';""",
 """<th>المدينة</th><th>المناديب</th><th>المكتملة</th><th>القبول</th><th>الساعات</th></tr></thead><tbody>'+cityT+'</tbody></table></div></section></div>'+ovPanel();""")
js=rep(js,'  if(t.id==="shXlsx"){shExport();return}','  if(t.id==="shXlsx"){shExport();return}\n  if(t.dataset.ovpdf){ovPdf(t.dataset.ovpdf);return}')
js=rep(js,'  if(t.id==="aMon"){ui0.am=t.value;render()}','  if(t.id==="aMon"){ui0.am=t.value;render()}\n  if(t.id==="ovMon"){ui0.ovm=t.value;render()}')
