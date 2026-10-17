# «أكواد الهيئة»: TGA codes per rider, visible alert, red cells in شيت الأداء (fadhel 2026-10-17)
js=rep(js,'["tga","مخالفات هيئة النقل","TGA Violations",1]','["tga","أكواد الهيئة","TGA Codes"]')
js=rep(js,'cards:isAdmin&&vCards}[view]','cards:isAdmin&&vCards,tga:vTga}[view]')
# sheet: codes column shows the rider's codes, red when any
js=rep(js,'tga:0,','tga:tgaOf(id),')
js=rep(js,'''<td class="num">0</td><td class="num">'+fmt(r.h)''','''<td'+(r.tga.length?' class="tgared" title="'+esc(r.tga.map(function(c){return c.code+(c.issued?" ("+c.issued+")":"")}).join("، "))+'"':' class="num"')+'>'+(r.tga.length?esc(r.tga.map(function(c){return c.code}).join("، ")):"0")+'</td><td class="num">'+fmt(r.h)''')
js=rep(js,'''<td colspan="6">الإجمالي</td><td class="num">0</td>''','''<td colspan="6">الإجمالي</td><td class="num'+(S.rows.some(function(r){return r.tga.length})?' tgared':'')+'">'+S.rows.reduce(function(a,r){return a+r.tga.length},0)+'</td>''')
js=rep(js,'xc("G"+R,15,0)','xc("G"+R,r.tga.length?TGA_XF:15,r.tga.length?r.tga.map(function(c){return c.code}).join("، "):0)')
js=rep(js,'if(L==="J"){t.push(xc("J"+tr,36,null));continue}','if(L==="J"){t.push(xc("J"+tr,36,null));continue}if(L==="G"){t.push(xc("G"+tr,36,S.rows.reduce(function(a,r){return a+r.tga.length},0)));continue}')
js=rep(js,'''.then(function(a){return a[0].loadAsync(a[1])}).then(function(zip){
    return Promise.all([zip.file("xl/worksheets/sheet1.xml")''','''.then(function(a){return a[0].loadAsync(a[1])}).then(function(zip){return zip.file("xl/styles.xml").async("string").then(function(st){zip.file("xl/styles.xml",tgaStyles(st));return zip})}).then(function(zip){
    return Promise.all([zip.file("xl/worksheets/sheet1.xml")''')
js=rep(js,'function vSoon(){','''var TGA={},TGA_XF=15,tgaUi={msg:"",ok:true,busy:false};
function tgaOf(id){return TGA[id]||[]}
function tgaRiders(){return Object.keys(TGA).filter(function(id){return TGA[id].length})}
function tgaStyles(st){var m=st.match(/<cellXfs count="(\\d+)"/);if(!m)return st;TGA_XF=+m[1];
  var fm=st.match(/<fills count="(\\d+)"/),fid=+fm[1];
  st=st.replace(/<fills count="\\d+"/,'<fills count="'+(fid+1)+'"').replace("</fills>",'<fill><patternFill patternType="solid"><fgColor rgb="FFFF4D4D"/><bgColor indexed="64"/></patternFill></fill></fills>');
  return st.replace(/<cellXfs count="\\d+"/,'<cellXfs count="'+(TGA_XF+1)+'"').replace("</cellXfs>",'<xf numFmtId="0" fontId="0" fillId="'+fid+'" borderId="2" applyFill="1" applyAlignment="1" xfId="0"><alignment horizontal="center" vertical="center" wrapText="1" /></xf></cellXfs>')}
function tgaLoad(){if(!canSee("tga"))return Promise.resolve();
  return all("tga_codes","id,rider_id,code,issued,note,created_at",["id","id"]).then(function(rs){var o={};rs.forEach(function(r){(o[r.rider_id]||(o[r.rider_id]=[])).push(r)});TGA=o},function(){TGA={}})}
var _lsdT=loadStaffData;loadStaffData=function(){return _lsdT.apply(this,arguments).then(function(){return tgaLoad()})};
function tgaPh(id){var p=String((data.couriers[id]&&data.couriers[id].ph)||"").replace(/^966/,"");return /^5/.test(p)?"0"+p:p}
function tgaIq(id){return SHIQ&&SHIQ!=="loading"?(SHIQ[id]||""):""}
function tgaBanner(){var ids=tgaRiders();if(!ids.length)return "";var n=ids.reduce(function(a,id){return a+TGA[id].length},0);
  return '<div class="tgaalert" role="alert"><b>⚠ تنبيه أكواد الهيئة:</b> يوجد <span class="num">'+ids.length+'</span> مندوب عليهم <span class="num">'+n+'</span> كود. '+
    ids.slice(0,6).map(function(id){return '<span class="tgachip">'+esc(cname(id))+' <span class="num">('+TGA[id].length+')</span></span>'}).join("")+(ids.length>6?' …':'')+
    (view!=="tga"?' <button class="btn" data-tab="tga">عرض الأكواد</button>':'')+'</div>'}
function vTga(){
  if(isAdmin&&!SHIQ){SHIQ="loading";all("rider_private","rider_id,iqama","rider_id").then(function(rs){SHIQ={};rs.forEach(function(r){SHIQ[r.rider_id]=r.iqama});render()},function(){SHIQ={};render()})}
  var ids=Object.keys(data.couriers).filter(function(id){return data.couriers[id].n}).sort(function(a,b){return cname(a).localeCompare(cname(b),"ar")});
  var form=isAdmin?'<section class="panel"><h2 style="margin:0 0 10px">إضافة كود هيئة على مندوب</h2><div class="tgaform">'+
    '<label>المندوب<select id="tgaR"><option value="">اختر المندوب…</option>'+ids.map(function(id){return '<option value="'+esc(id)+'">'+esc(cname(id))+' — '+esc(id)+'</option>'}).join("")+'</select></label>'+
    '<label>كود الهيئة<input id="tgaC" autocomplete="off" placeholder="مثال: 1045"></label>'+
    '<label>التاريخ<input id="tgaD" type="date" value="'+new Date().toISOString().slice(0,10)+'"></label>'+
    '<label>ملاحظة<input id="tgaN" autocomplete="off" placeholder="اختياري"></label>'+
    '<button class="btn pri" id="tgaAdd"'+(tgaUi.busy?" disabled":"")+'>إضافة الكود</button></div>'+
    '<div id="tgaInfo" class="hint" style="margin-top:8px"></div><p class="hint" id="tgaMsg" style="margin:6px 0 0;color:'+(tgaUi.ok?"inherit":"#c00")+'">'+esc(tgaUi.msg)+'</p></section>':'';
  var rs=tgaRiders().sort(function(a,b){return TGA[b].length-TGA[a].length||cname(a).localeCompare(cname(b),"ar")}),k=0;
  var body=rs.map(function(id){var L=TGA[id];return L.map(function(c,i){k++;var f=i===0,sp=' rowspan="'+L.length+'"';
    return '<tr>'+(f?'<td class="num"'+sp+'>'+(rs.indexOf(id)+1)+'</td><td'+sp+' class="tganame">'+esc(cname(id))+'</td><td'+sp+'>'+(catOf(id)?'<span class="catp cat-'+({"أ":"a","ب":"b","خ":"k"}[catOf(id)]||"r")+'">'+esc(catOf(id))+'</span>':'')+'</td><td class="num"'+sp+'>'+esc(tgaIq(id))+'</td><td class="num"'+sp+'>'+esc(id)+'</td><td class="num"'+sp+'>'+esc(tgaPh(id))+'</td><td class="num tgared"'+sp+'>'+L.length+'</td>':'')+
      '<td class="tgared">'+esc(c.code)+'</td><td class="num">'+esc(c.issued||"")+'</td><td style="white-space:normal">'+esc(c.note||"")+'</td>'+(isAdmin?'<td><button class="btn danger sm" data-tgadel="'+c.id+'">حذف</button></td>':'')+'</tr>'}).join("")}).join("");
  return tgaBanner()+form+'<section class="panel"><div class="shhead"><div><h2 style="margin:0">أكواد الهيئة على المناديب</h2><p class="hint" style="margin:4px 0 0">كل مندوب عليه كود يظهر هنا، ويتلوّن عمود «اكواد الهيئة» بالأحمر في شيت الأداء.</p></div>'+
    (rs.length?'<div class="stmttools"><button class="btn pri" id="tgaXlsx">تصدير Excel</button></div>':'')+'</div>'+
    '<div class="tbl"><table data-catdone="1"><thead><tr><th>م</th><th>الاسم</th><th>الفئة</th><th>الإقامة</th><th>Rider Id</th><th>الجوال</th><th>عدد الأكواد</th><th>كود الهيئة</th><th>التاريخ</th><th>ملاحظة</th>'+(isAdmin?'<th></th>':'')+'</tr></thead><tbody>'+
    (body||'<tr><td class="empty" colspan="11">لا توجد أكواد هيئة مسجلة على أي مندوب.</td></tr>')+'</tbody></table></div></section>'}
function tgaSet(m,ok){tgaUi.msg=m;tgaUi.ok=ok!==false;var e=document.getElementById("tgaMsg");if(e){e.textContent=m;e.style.color=tgaUi.ok?"inherit":"#c00"}}
function tgaInfo(){var id=(document.getElementById("tgaR")||{}).value,e=document.getElementById("tgaInfo");if(!e)return;if(!id){e.textContent="";return}
  var L=tgaOf(id);e.innerHTML='الإقامة: <span class="num">'+esc(tgaIq(id)||"—")+'</span> · الجوال: <span class="num">'+esc(tgaPh(id)||"—")+'</span>'+(L.length?' · <b style="color:#c00">عليه '+L.length+' كود: '+esc(L.map(function(c){return c.code}).join("، "))+'</b>':'')}
document.addEventListener("change",function(e){if(e.target&&e.target.id==="tgaR")tgaInfo()});
document.addEventListener("click",function(e){var t=e.target.closest&&e.target.closest("#tgaAdd,[data-tgadel],#tgaXlsx");if(!t)return;
  if(t.id==="tgaAdd"){var id=document.getElementById("tgaR").value,code=digits(document.getElementById("tgaC").value).trim(),d=document.getElementById("tgaD").value||null,n=document.getElementById("tgaN").value.trim();
    if(!id)return tgaSet("اختر المندوب أولاً.",false);if(!code)return tgaSet("اكتب كود الهيئة.",false);
    tgaUi.busy=true;t.disabled=true;tgaSet("جارٍ الحفظ…");
    sb.from("tga_codes").insert({rider_id:id,code:code,issued:d,note:n||null}).select().then(function(r){tgaUi.busy=false;if(r.error){tgaSet("تعذّر الحفظ: "+r.error.message,false);render();return}
      (TGA[id]||(TGA[id]=[])).push(r.data[0]);tgaUi.msg="تمت إضافة الكود "+code+" على "+cname(id)+".";tgaUi.ok=true;render()});return}
  if(t.dataset.tgadel){if(!confirm("حذف هذا الكود؟"))return;var cid=+t.dataset.tgadel;t.disabled=true;
    sb.from("tga_codes").delete().eq("id",cid).then(function(r){if(r.error){tgaSet("تعذّر الحذف: "+r.error.message,false);t.disabled=false;return}
      Object.keys(TGA).forEach(function(k){TGA[k]=TGA[k].filter(function(c){return c.id!==cid});if(!TGA[k].length)delete TGA[k]});tgaUi.msg="تم حذف الكود.";tgaUi.ok=true;render()});return}
  if(t.id==="tgaXlsx"){loadXLSX().then(function(X){var rows=[["م","الاسم","الإقامة","Rider Id","الجوال","الفئة","كود الهيئة","التاريخ","ملاحظة"]],i=0;
    tgaRiders().forEach(function(id){i++;TGA[id].forEach(function(c){rows.push([i,cname(id),tgaIq(id),id,tgaPh(id),catOf(id),c.code,c.issued||"",c.note||""])})});
    var ws=X.utils.aoa_to_sheet(rows);ws["!cols"]=[{wch:5},{wch:32},{wch:13},{wch:11},{wch:12},{wch:8},{wch:14},{wch:12},{wch:30}];var wb=X.utils.book_new();wb.Workbook={Views:[{RTL:true}]};X.utils.book_append_sheet(wb,ws,"أكواد الهيئة");
    X.writeFile(wb,"أكواد الهيئة "+new Date().toISOString().slice(0,10)+".xlsx")},function(){tgaSet("تعذّر تحميل مكتبة Excel.",false)})}});
var _renderT=render;render=function(){var r=_renderT.apply(this,arguments);try{
  if(view!=="courier"&&(isAdmin||staff)&&canSee("tga")){var n=tgaRiders().length,b=document.querySelector('nav.side button[data-tab="tga"]');
    if(b&&n){var s=document.createElement("span");s.className="tgabadge num";s.textContent=n;b.appendChild(s)}
    var mc=document.querySelector("main.content");if(mc&&n&&view!=="tga"){var d=document.createElement("div");d.innerHTML=tgaBanner();var el=d.firstChild;mc.insertBefore(el,mc.firstChild);try{trTree(el)}catch(e){}}}
  if(view==="tga")tgaInfo()}catch(e){}return r};
function vSoon(){''')
css+='''
.tgaalert{background:#fde8e8;border:2px solid #e04545;color:#8a1212;border-radius:12px;padding:10px 14px;margin:0 0 14px;line-height:1.9}
.tgaalert .btn{margin-inline-start:6px;padding:4px 12px}
.tgachip{display:inline-block;background:#e04545;color:#fff;border-radius:10px;padding:0 9px;margin:2px 3px;font-size:13px}
.tgared{background:#ff4d4d!important;color:#fff!important;font-weight:700}
.tgabadge{display:inline-block;background:#e04545;color:#fff;border-radius:10px;min-width:20px;padding:0 6px;margin-inline-start:6px;font-size:12px;text-align:center}
.tgaform{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;align-items:end}
.tgaform label{display:flex;flex-direction:column;gap:4px;font-size:13.5px}
.tgaform select,.tgaform input{width:100%}
.btn.danger{background:#c62828;color:#fff;border-color:#c62828}.btn.sm{padding:3px 10px;font-size:12.5px}
'''
