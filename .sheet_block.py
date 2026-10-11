# daily performance sheet (شيت الأداء اليومي), admin only, exported in fadhel's own xlsx layout
js=rep(js,'all("riders","id,name,vehicle,tga,phone,category","id").then(function(rs){rs.forEach(function(r){var c=C(r.id);',
 'all("riders","id,name,vehicle,tga,phone,category,sheet_pos","id").then(function(rs){rs.forEach(function(r){var c=C(r.id);if(r.sheet_pos!=null)c.sp=r.sheet_pos;')
js=rep(js,'''<button data-tab="perm" aria-current="'+(view==="perm")+'">الصلاحيات<small>Roles</small></button>''',
 '''<button data-tab="sheet" aria-current="'+(view==="sheet")+'">شيت الأداء اليومي<small>Daily Sheet</small></button><button data-tab="perm" aria-current="'+(view==="perm")+'">الصلاحيات<small>Roles</small></button>''')
js=rep(js,'data:isAdmin&&vData,perm:isAdmin&&vPerm}[view];','data:isAdmin&&vData,perm:isAdmin&&vPerm,sheet:isAdmin&&vSheet}[view];')
js=rep(js,'if(view!=="courier"&&view!=="data"&&view!=="perm"&&!canSee(view))V=staff?','if(view!=="courier"&&view!=="data"&&view!=="perm"&&view!=="sheet"&&!canSee(view))V=staff?')
js=rep(js,'else if(!V)V=(view==="data"||view==="perm")?vCourier:vSoon;','else if(!V)V=(view==="data"||view==="perm"||view==="sheet")?vCourier:vSoon;')
js=rep(js,'TITLES.perm="الصلاحيات";','TITLES.perm="الصلاحيات";TITLES.sheet="شيت الأداء اليومي";')
js=rep(js,'root.addEventListener("change",function(e){\n  var t=e.target,f=F();',r'''root.addEventListener("change",function(e){
  var t=e.target,f=F();
  if(t.id==="shMon"){SH_MON=t.value;render();return}
  if(t.dataset.shf!=null||t.dataset.shn!=null){shSave(t);return}''')
js=rep(js,'  if(t.dataset.sp){stmtPrint(t.dataset.sp);return}','  if(t.dataset.sp){stmtPrint(t.dataset.sp);return}\n  if(t.id==="shXlsx"){shExport();return}')
js=rep(js,'function stmtCalc(id){',r'''/* ---------- daily performance sheet ---------- */
var SH_MON="",SHX={},SHIQ=null,SH_MSG="";
var JSZIP_URL="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js";
function loadZip(){return window.JSZip?Promise.resolve(window.JSZip):new Promise(function(ok,no){var s=document.createElement("script");s.src=JSZIP_URL;s.onload=function(){ok(window.JSZip)};s.onerror=function(){no(new Error("lib"))};document.head.appendChild(s)})}
function shMonths(){var m={};days().forEach(function(d){m[d.slice(0,7)]=1});return Object.keys(m).sort().reverse()}
function shCatOrder(c){return c==="ب"?0:c==="خ"?1:c==="أ"?2:3}
function shRiders(){return Object.keys(data.couriers).filter(function(id){return normCat(data.couriers[id].cat)}).sort(function(a,b){var x=data.couriers[a],y=data.couriers[b];
  var px=x.sp==null?1e9:x.sp,py=y.sp==null?1e9:y.sp;if(px!==py)return px-py;var cx=shCatOrder(normCat(x.cat)),cy=shCatOrder(normCat(y.cat));return cx!==cy?cx-cy:(+a)-(+b)})}
function shLoad(mon){
  if(!SHIQ){SHIQ="loading";all("rider_private","rider_id,iqama","rider_id").then(function(rs){SHIQ={};rs.forEach(function(r){SHIQ[r.rider_id]=r.iqama});render()},function(){SHIQ={};render()})}
  if(!SHX[mon]){SHX[mon]="loading";sb.from("sheet_extra").select("rider_id,fuel,note").eq("month",mon).then(function(r){var o={};(r.data||[]).forEach(function(x){o[x.rider_id]={f:x.fuel==null?null:+x.fuel,n:x.note||""}});SHX[mon]=o;render()})}
}
function shCalc(mon){
  var ds=days().filter(function(d){return d.slice(0,7)===mon}),last=ds.length?ds[ds.length-1]:null,nd=last?+last.slice(8,10):0;
  var cnt={},x=SHX[mon]&&SHX[mon]!=="loading"?SHX[mon]:{};
  var rows=shRiders().map(function(id){var c=data.couriers[id],cat=normCat(c.cat);cnt[cat]=(cnt[cat]||0)+1;
    var lv=last&&data.days[last][id],q=c.q&&c.q[mon],dd=[];
    for(var i=1;i<=nd;i++){var d=mon+"-"+(i<10?"0":"")+i,r=data.days[d]&&data.days[d][id];dd.push(r&&r[CP]!=null?+r[CP]:0)}
    var ph=String(c.ph||"").replace(/^966/,""),e=x[id]||{};
    return {no:cnt[cat],cat:cat,name:c.n||"",iq:SHIQ&&SHIQ!=="loading"?(SHIQ[id]||""):"",ph:ph,id:id,tga:0,h:lv&&lv[AC]!=null?+lv[AC]:0,de:lv&&lv[DE]!=null?+lv[DE]:0,
      q:q&&q.s||"",w:c.w&&c.w.b!=null?c.w.b:null,dd:dd,tot:dd.reduce(function(a,b){return a+b},0),f:e.f==null?null:e.f,n:e.n||""}});
  return {mon:mon,last:last,nd:nd,rows:rows};
}
function shSave(t){var mon=SH_MON||shMonths()[0],id=t.dataset.shf!=null?t.dataset.shf:t.dataset.shn,o=SHX[mon]&&SHX[mon]!=="loading"?SHX[mon]:(SHX[mon]={}),e=o[id]||(o[id]={f:null,n:""});
  if(t.dataset.shf!=null){var v=String(t.value).trim();e.f=v===""?null:+v}else e.n=String(t.value).trim();
  SH_MSG="جارٍ الحفظ…";var m=document.getElementById("shMsg");if(m)m.textContent=SH_MSG;
  sb.from("sheet_extra").upsert({month:mon,rider_id:id,fuel:e.f,note:e.n||null,updated_at:new Date().toISOString()}).then(function(r){SH_MSG=r.error?"تعذّر الحفظ: "+r.error.message:"تم الحفظ";var m=document.getElementById("shMsg");if(m)m.textContent=SH_MSG})}
var SH_COLS=["م","فئه","الأســـــم","الإقامة","جـــوال","I.D","اكواد الهيئة","ساعات العمل","الطلبات المرفوضة","جودة التوصيل","مبلغ المحفظة"];
function vSheet(){
  var ms=shMonths();if(!ms.length)return '<div class="panel"><p class="hint" style="margin:0">لا توجد بيانات بعد.</p></div>';
  var mon=SH_MON&&ms.indexOf(SH_MON)>=0?SH_MON:ms[0];shLoad(mon);
  var S=shCalc(mon),catBg={"ب":"#92d050","خ":"#c55a11","أ":"#ffce3c"},catFg={"خ":"#fff"};
  var dh="";for(var i=1;i<=31;i++)dh+='<th class="shd">يـ'+i+'</th>';
  var body=S.rows.map(function(r){var dc="";for(var i=0;i<31;i++)dc+='<td class="num">'+(i<r.dd.length?r.dd[i]:"")+'</td>';
    return '<tr><td class="num">'+r.no+'</td><td style="background:'+(catBg[r.cat]||"")+';color:'+(catFg[r.cat]||"#000")+';font-weight:700">'+esc(r.cat)+'</td><td class="shn">'+esc(r.name)+'</td><td class="num shb">'+esc(r.iq)+'</td><td class="num shb">'+esc(r.ph?(/^5/.test(r.ph)?"0"+r.ph:r.ph):"")+'</td><td class="num">'+esc(r.id)+'</td>'+
      '<td class="num">0</td><td class="num">'+fmt(r.h)+'</td><td class="num">'+r.de+'</td><td>'+esc(r.q)+'</td><td class="num">'+(r.w==null?"":fmt(r.w))+'</td>'+dc+
      '<td class="num shq">'+r.tot+'</td><td><input class="shin num" inputmode="decimal" data-shf="'+esc(r.id)+'" value="'+(r.f==null?"":r.f)+'"></td><td><input class="shin shnote" data-shn="'+esc(r.id)+'" value="'+esc(r.n)+'"></td></tr>'}).join("");
  var tot=function(k){return S.rows.reduce(function(a,r){return a+(+r[k]||0)},0)},dt="";
  for(var j=0;j<31;j++)dt+='<td class="num">'+(j<S.nd?S.rows.reduce(function(a,r){return a+r.dd[j]},0):"")+'</td>';
  var foot='<tr class="shtot"><td colspan="6">الإجمالي</td><td class="num">0</td><td class="num">'+fmt(tot("h"))+'</td><td class="num">'+tot("de")+'</td><td></td><td class="num">'+fmt(tot("w"))+'</td>'+dt+'<td class="num">'+tot("tot")+'</td><td class="num">'+fmt(tot("f"))+'</td><td></td></tr>';
  var busy=SHIQ==="loading"||SHX[mon]==="loading";
  return '<section class="panel"><div class="shhead"><div><h2 style="margin:0">شيت الأداء شهر '+monTxt(mon)+'</h2><p class="hint" style="margin:4px 0 0">يُبنى تلقائياً من البيانات المرفوعة حتى <span class="num">'+(S.last||"—")+'</span>. البنزين والملاحظة تكتبها هنا وتُحفظ تلقائياً.</p></div>'+
    '<div class="stmttools"><select id="shMon" aria-label="الشهر">'+ms.map(function(m){return '<option value="'+m+'"'+(m===mon?" selected":"")+'>'+monTxt(m)+'</option>'}).join("")+'</select><button class="btn pri" id="shXlsx"'+(busy?" disabled":"")+'>تصدير Excel</button></div></div>'+
    '<p class="hint" id="shMsg" style="min-height:1.5em;margin:6px 0">'+esc(SH_MSG)+'</p>'+
    '<div class="tbl shtbl" style="box-shadow:none"><table><thead><tr>'+SH_COLS.map(function(h,i){return '<th'+(i===1?' class="shcat"':'')+'>'+h+'</th>'}).join("")+dh+'<th>إجمالي الطلبات</th><th>البنزين</th><th>ملاحظة</th></tr></thead><tbody>'+
    (body||'<tr><td class="empty" colspan="45">لا يوجد مناديب في الكشف. ارفع ملف المناديب مع عمود الفئة.</td></tr>')+'</tbody><tfoot>'+foot+'</tfoot></table></div></section>';
}
function xe(s){return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]})}
function colL(n){var s="";while(n>0){var m=(n-1)%26;s=String.fromCharCode(65+m)+s;n=(n-m-1)/26}return s}
function xc(ref,s,v){if(v==null||v==="")return '<c r="'+ref+'" s="'+s+'" t="n" />';if(typeof v==="number")return '<c r="'+ref+'" s="'+s+'" t="n"><v>'+v+'</v></c>';return '<c r="'+ref+'" s="'+s+'" t="inlineStr"><is><t>'+xe(v)+'</t></is></c>'}
function xf(ref,s,f){return '<c r="'+ref+'" s="'+s+'"><f>'+f+'</f><v /></c>'}
function shExport(){
  var mon=SH_MON||shMonths()[0],S=shCalc(mon),title="شيت الأداء شهر "+monTxt(mon),sname="شيت "+monTxt(mon);
  var b=document.getElementById("shXlsx");if(b){b.disabled=true;b.textContent="جارٍ التجهيز…"}
  var done=function(){var b=document.getElementById("shXlsx");if(b){b.disabled=false;b.textContent="تصدير Excel"}};
  Promise.all([loadZip(),fetch("sheet-template.xlsx",{cache:"no-cache"}).then(function(r){if(!r.ok)throw new Error("template");return r.arrayBuffer()})]).then(function(a){return a[0].loadAsync(a[1])}).then(function(zip){
    return Promise.all([zip.file("xl/worksheets/sheet1.xml").async("string"),zip.file("xl/workbook.xml").async("string")]).then(function(x){
      var catS={"ب":11,"خ":21,"أ":27},rows="",n=S.rows.length,tr=n+3;
      S.rows.forEach(function(r,i){var R=i+3,c=[];
        c.push(xc("A"+R,10,r.no),xc("B"+R,catS[r.cat]||11,r.cat),xc("C"+R,12,r.name),xc("D"+R,13,/^\d+$/.test(r.iq)?+r.iq:r.iq),xc("E"+R,14,/^\d+$/.test(r.ph)?+r.ph:r.ph),xc("F"+R,10,/^\d+$/.test(r.id)?+r.id:r.id),
          xc("G"+R,15,0),xc("H"+R,15,r.h),xc("I"+R,15,r.de),xc("J"+R,15,r.q||null),xc("K"+R,15,r.w));
        for(var d=1;d<=31;d++)c.push(xc(colL(11+d)+R,d===31?18:15,d<=r.dd.length?r.dd[d-1]:null));
        c.push(xf("AQ"+R,17,"SUM(L"+R+":AP"+R+")"),xc("AR"+R,18,r.f),xc("AS"+R,19,r.n||null));
        rows+='<row r="'+R+'" ht="22.5" customHeight="1">'+c.join("")+'</row>'});
      var t=[xc("A"+tr,36,"الإجمالي")];["B","C","D","E"].forEach(function(L){t.push(xc(L+tr,43,null))});t.push(xc("F"+tr,44,null));
      for(var k=7;k<=44;k++){var L=colL(k);if(L==="J"){t.push(xc("J"+tr,36,null));continue}t.push(xf(L+tr,L==="AQ"?37:L==="AR"?38:36,"SUBTOTAL(9,"+L+"3:"+L+(tr-1)+")"))}
      t.push(xc("AS"+tr,39,null));
      rows+='<row r="'+tr+'" ht="23.25" customHeight="1">'+t.join("")+'</row>';
      [23.25,23.25,27.75,12,12].forEach(function(h,i){rows+='<row r="'+(tr+1+i)+'" ht="'+h+'" customHeight="1"></row>'});
      var s=x[0].replace("<!--ROWS-->",rows).replace(/<dimension ref="[^"]*"/,'<dimension ref="A1:AS'+tr+'"').replace(/<autoFilter ref="[^"]*"/,'<autoFilter ref="A2:AR'+(tr+2)+'"')
        .replace(/<mergeCell ref="A\d+:F\d+" \/>/,'<mergeCell ref="A'+tr+':F'+tr+'" />').replace(/<t>شيت الأداء شهر [^<]*<\/t>/,"<t>"+xe(title)+"</t>");
      var w=x[1].replace(/<sheet name="[^"]*"/,'<sheet name="'+xe(sname)+'"').replace(/>'[^']*'!\$A\$2:\$AR\$\d+</,">'"+xe(sname)+"'!$A$2:$AR$"+(tr+2)+"<");
      zip.file("xl/worksheets/sheet1.xml",s);zip.file("xl/workbook.xml",w);
      return zip.generateAsync({type:"blob",mimeType:"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",compression:"DEFLATE"});
    })}).then(function(blob){var a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download=title+".xlsx";document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove()},1500);done()},
    function(e){done();SH_MSG="تعذّر تجهيز الملف: "+(e&&e.message||e);var m=document.getElementById("shMsg");if(m)m.textContent=SH_MSG})}
function stmtCalc(id){''')
css+='''
.shhead{display:flex;flex-wrap:wrap;gap:10px;align-items:flex-start;justify-content:space-between}
.shtbl table{font:700 12px/1.3 Arial,var(--f-body),sans-serif;border-collapse:collapse}
.shtbl th,.shtbl td{border:1px solid #b9c3c7;padding:3px 6px;text-align:center;white-space:nowrap;color:#000;background:#fff}
.shtbl thead th{background:#ffff00;color:#002060;position:static}
.shtbl thead th.shcat{background:#8eb4e3}
.shtbl .shtitle th{background:#ffff00;color:#002060;font-size:13px}
.shtbl td.shn{background:#fbe5d6;text-align:center}
.shtbl td.shb{background:#dae3f3}
.shtbl td.shq{background:#ddebf7}
.shtbl tfoot td{background:#ffc000;font-weight:700}
.shtbl .shin{width:70px;border:1px solid #c9d3d6;border-radius:4px;padding:2px 4px;font:inherit;text-align:center;background:#fffef5;color:#000}
.shtbl .shin.shnote{width:190px;text-align:right}
'''
