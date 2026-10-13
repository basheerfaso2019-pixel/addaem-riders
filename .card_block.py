# HungerStation rider ID cards (fadhel 2026-10-12, layout from his Word template "قالب بطائق هنقرستيشن")
js=rep(js,'شيت الأداء اليومي<small>Daily Sheet</small></button>','شيت الأداء اليومي<small>Daily Sheet</small></button><button data-tab="cards" aria-current="\'+(view==="cards")+\'">بطاقات المناديب<small>Rider ID Cards</small></button>')
js=rep(js,'sheet:isAdmin&&vSheet}[view];','sheet:isAdmin&&vSheet,cards:isAdmin&&vCards}[view];')
js=rep(js,'view!=="sheet"&&!canSee(view)','view!=="sheet"&&view!=="cards"&&!canSee(view)')
js=rep(js,'view==="perm"||view==="sheet")?vCourier:vSoon;','view==="perm"||view==="sheet"||view==="cards")?vCourier:vSoon;')
js=rep(js,'TITLES.sheet="شيت الأداء اليومي";','TITLES.sheet="شيت الأداء اليومي";TITLES.cards="بطاقات المناديب";')
js=rep(js,'function vSoon(){',r'''/* ---------- rider ID cards ---------- */
var CARD={sel:{},q:"",cat:"",reg:"",ph:null,photos:{},msg:"",cfg:null,mode:"duplex"};
var CARD_DEF={phone:"0502774745",email:"d.almutawir@gmail.com"};
function cardCfgLoad(){if(CARD.cfg)return;CARD.cfg="loading";sb.from("settings").select("key,value").in("key",["card_phone","card_email"]).then(function(r){var o={phone:CARD_DEF.phone,email:CARD_DEF.email};(r.data||[]).forEach(function(x){if(x.key==="card_phone"&&x.value)o.phone=x.value;if(x.key==="card_email"&&x.value)o.email=x.value});CARD.cfg=o;render()},function(){CARD.cfg={phone:CARD_DEF.phone,email:CARD_DEF.email};render()})}
function cardPhotosLoad(){if(CARD.ph)return;CARD.ph="loading";sb.storage.from("rider-photos").list("",{limit:2000}).then(function(r){var o={};(r.data||[]).forEach(function(f){var m=String(f.name).match(/^(\w+)\.jpg$/);if(m)o[m[1]]=1});CARD.ph=o;render()},function(){CARD.ph={};render()})}
function blobUrl(b){return new Promise(function(ok){var fr=new FileReader();fr.onload=function(){ok(fr.result)};fr.readAsDataURL(b)})}
/* photo as a data url (needed inside the print frame); fetched once */
function cardPhoto(id){var p=CARD.photos[id];if(p&&p!=="loading")return Promise.resolve(p);if(!CARD.ph||CARD.ph==="loading"||!CARD.ph[id])return Promise.resolve("");
  CARD.photos[id]="loading";return sb.storage.from("rider-photos").download(id+".jpg").then(function(r){if(r.error||!r.data)throw 0;return blobUrl(r.data)}).then(function(u){CARD.photos[id]=u;return u},function(){CARD.photos[id]="";return ""})}
function cardIqLoad(){if(!SHIQ){SHIQ="loading";all("rider_private","rider_id,iqama","rider_id").then(function(rs){SHIQ={};rs.forEach(function(r){SHIQ[r.rider_id]=r.iqama});render()},function(){SHIQ={};render()})}}
function cardIq(id){return SHIQ&&SHIQ!=="loading"&&SHIQ[id]?String(SHIQ[id]):""}
function cardPh(id){var p=String((data.couriers[id]&&data.couriers[id].ph)||"");return /^9665\d{8}$/.test(p)?"0"+p.slice(3):p}
function cardCatOf(id){var c=data.couriers[id]||{};return c.rg?"ر":normCat(c.cat)||"—"}
function cardRiders(){return Object.keys(data.couriers).filter(function(id){return data.couriers[id].n}).sort(function(a,b){return data.couriers[a].n.localeCompare(data.couriers[b].n,"ar")})}
function cardList(){var q=CARD.q.trim().toLowerCase();return cardRiders().filter(function(id){var c=data.couriers[id];
  if(CARD.cat&&cardCatOf(id)!==CARD.cat)return false;if(q&&String(c.n).toLowerCase().indexOf(q)<0&&id.indexOf(q)<0&&cardIq(id).indexOf(q)<0)return false;return true})}
/* the card itself, sized in mm so screen preview and print match (56 x 88 mm, portrait) */
var CARD_CSS='.hcard{width:56mm;height:88mm;border-radius:4mm;overflow:hidden;position:relative;background:#ffff00;font-family:"IBM Plex Sans Arabic",Calibri,Tahoma,sans-serif;direction:rtl;-webkit-print-color-adjust:exact;print-color-adjust:exact;box-shadow:0 0 0 .2mm #d8d8d8;flex:none}'+
 '.hcard .wave{position:absolute;left:0;right:0;bottom:0;background:#00b0f0}.hcard .wave svg{position:absolute;left:0;top:-5.7mm;width:100%;height:6mm;display:block}'+
 '.hcard .pic{position:absolute;top:5mm;left:50%;transform:translateX(-50%);width:31mm;height:31mm;border-radius:50%;overflow:hidden;background:#fff;box-shadow:0 0 0 .9mm #fff,0 .6mm 2mm rgba(0,0,0,.25)}.hcard .pic img{width:100%;height:100%;object-fit:cover;display:block}.hcard .pic i{display:flex;height:100%;align-items:center;justify-content:center;color:#bbb;font:600 8pt sans-serif}'+
 '.hcard .inf{position:absolute;top:40mm;right:4mm;left:3.5mm;display:grid;grid-template-columns:auto 1fr;gap:1.4mm 2mm;align-items:baseline}.hcard .inf b{color:#111;font-weight:800;font-size:9.5pt;white-space:nowrap}.hcard .inf span{color:#0075b2;font-weight:800;font-size:10pt;line-height:1.25;overflow:hidden}.hcard .inf span.n{color:#00b0f0;font-size:12pt;letter-spacing:.2mm;font-family:Calibri,Arial,sans-serif;direction:ltr;text-align:right}'+
 '.hcard .inf span.nm{line-height:1.2}.hcard .inf span.nm.s{font-size:9pt}.hcard .inf span.nm.xs{font-size:8.2pt}'+
 '.hcard .hs{position:absolute;left:0;right:0;text-align:center;font:800 13pt/1.15 Calibri,Arial,sans-serif;letter-spacing:.3mm;direction:ltr}'+
 '.hcard.back .msg{position:absolute;left:4mm;right:4mm;bottom:6mm;color:#fff;text-align:center;font-weight:700;font-size:7.6pt;line-height:1.5}.hcard.back .msg p{margin:0 0 2.4mm}.hcard.back .msg .en{direction:ltr;font-family:Calibri,Arial,sans-serif;font-style:italic;font-size:7.4pt}';
var CARD_WAVE='<svg viewBox="0 0 100 10" preserveAspectRatio="none"><path d="M0 4 C 18 0, 32 0, 50 4 S 82 9, 100 2 L100 10 L0 10 Z" fill="#00b0f0"/></svg>';
function cardFront(id,photo){var c=data.couriers[id]||{},n=String(c.n||"").trim(),cls=n.length>26?" xs":n.length>20?" s":"";
  return '<div class="hcard"><div class="pic">'+(photo?'<img src="'+photo+'" alt="">':'<i>صورة</i>')+'</div>'+
    '<div class="inf"><b>الاسم:</b><span class="nm'+cls+'">'+esc(n)+'</span><b>الإقامة:</b><span class="n">'+esc(cardIq(id)||"—")+'</span><b>الجوال:</b><span class="n">'+esc(cardPh(id)||"—")+'</span></div>'+
    '<div class="wave" style="height:21mm">'+CARD_WAVE+'<div class="hs" style="color:#fff;top:4mm">HUNGER<br>STATION</div></div></div>'}
function cardBack(){var g=CARD.cfg&&CARD.cfg!=="loading"?CARD.cfg:CARD_DEF;
  return '<div class="hcard back"><div class="hs" style="color:#806000;top:13mm;font-size:15pt">HUNGER<br>STATION</div>'+
    '<div class="wave" style="height:50mm">'+CARD_WAVE+'</div><div class="msg"><p>إذا تم العثور على هذه البطاقة يرجى التواصل على الرقم '+esc(g.phone)+'</p><p class="en">If this card is found please contact us<br>'+esc(g.phone)+'<br>Email: '+esc(g.email)+'</p></div></div>'}
function vCards(){cardIqLoad();cardPhotosLoad();cardCfgLoad();
  var list=cardList(),sel=Object.keys(CARD.sel).filter(function(id){return CARD.sel[id]&&data.couriers[id]}),nSel=sel.length,ph=CARD.ph&&CARD.ph!=="loading"?CARD.ph:{};
  var first=sel[0]||list[0];if(first&&ph[first]&&CARD.photos[first]===undefined)cardPhoto(first).then(render);
  var cats=[["","الكل"],["أ","فئة أ"],["ب","فئة ب"],["خ","فئة خ"],["ر","مناديب الرياض"],["—","بدون فئة"]];
  var rows=list.slice(0,400).map(function(id){var c=data.couriers[id],on=!!CARD.sel[id];return '<tr'+(on?' class="csel"':'')+'><td><input type="checkbox" data-csel="'+esc(id)+'"'+(on?" checked":"")+'></td><td class="num">'+esc(id)+'</td><td class="s">'+esc(c.n)+'</td><td>'+esc(cardCatOf(id)==="ر"?"الرياض":cardCatOf(id))+'</td><td class="num">'+esc(cardIq(id)||"—")+'</td><td class="num">'+esc(cardPh(id)||"—")+'</td>'+
    '<td style="white-space:nowrap"><label class="btn cphoto'+(ph[id]?"":" pri")+'">'+(ph[id]?"✓ صورة":"+ صورة")+'<input type="file" accept="image/*" data-cphoto="'+esc(id)+'" hidden></label>'+(ph[id]?' <button class="btn cphoto" data-cedit="'+esc(id)+'">ضبط</button>':'')+'</td></tr>'}).join("");
  var noPhoto=sel.filter(function(id){return !ph[id]}).length,noIq=sel.filter(function(id){return !cardIq(id)}).length;
  var g=CARD.cfg&&CARD.cfg!=="loading"?CARD.cfg:CARD_DEF;
  return '<style>'+CARD_CSS+'</style><div class="cardsgrid"><section class="panel"><h2>معاينة البطاقة</h2><p class="hint">'+(first?esc(cname(first)):"اختر مندوباً")+'</p><div class="cprev">'+(first?cardFront(first,CARD.photos[first]||""):"")+cardBack()+'</div>'+
    '<div class="row" style="margin-top:12px;flex-wrap:wrap"><label style="flex:1 1 140px">رقم التواصل في الخلف<input id="cPhone" inputmode="tel" value="'+esc(g.phone)+'"></label><label style="flex:1 1 180px">البريد<input id="cEmail" value="'+esc(g.email)+'"></label></div></section>'+
    '<section class="panel"><div class="stmthead"><h2>اختيار المناديب</h2><div class="stmttools"><select id="cCat" aria-label="الفئة">'+cats.map(function(x){return '<option value="'+x[0]+'"'+(x[0]===CARD.cat?" selected":"")+'>'+x[1]+'</option>'}).join("")+'</select><input id="cQ" placeholder="بحث بالاسم أو ID أو الإقامة" value="'+esc(CARD.q)+'" style="min-width:200px"></div></div>'+
    '<div class="row" style="gap:8px;flex-wrap:wrap;margin-bottom:10px"><button class="btn" data-call="1">تحديد الظاهرين (<span class="num">'+list.length+'</span>)</button><button class="btn" data-call="0"'+(nSel?"":" disabled")+'>إلغاء التحديد</button>'+
    '<select id="cMode" aria-label="طريقة الطباعة"><option value="duplex"'+(CARD.mode==="duplex"?" selected":"")+'>وجه وخلف (طباعة على الوجهين)</option><option value="side"'+(CARD.mode==="side"?" selected":"")+'>الوجه والخلف متجاورين</option><option value="front"'+(CARD.mode==="front"?" selected":"")+'>الوجه فقط</option></select>'+
    '<button class="btn pri" id="cPrint"'+(nSel&&!CARD.busy?"":" disabled")+'>'+(CARD.busy?"جارٍ التجهيز…":'طباعة / PDF (<span class="num">'+nSel+'</span>)')+'</button></div>'+
    (nSel&&(noPhoto||noIq)?'<p class="hint" style="color:var(--bad)">'+(noPhoto?'<span class="num">'+noPhoto+'</span> بدون صورة. ':'')+(noIq?'<span class="num">'+noIq+'</span> بدون رقم إقامة.':'')+'</p>':'')+
    '<p class="hint" id="cMsg" style="min-height:1.4em;margin:0 0 6px">'+esc(CARD.msg)+'</p>'+
    '<div class="tbl" style="box-shadow:none;max-height:560px;overflow:auto"><table><thead><tr><th></th><th>Rider Id</th><th>الاسم</th><th>الفئة</th><th>الإقامة</th><th>الجوال</th><th>الصورة</th></tr></thead><tbody>'+(rows||'<tr><td class="empty" colspan="7">لا يوجد مناديب بهذا البحث.</td></tr>')+'</tbody></table></div></section></div>'}
/* photo crop: the circle on the card shows exactly what the manager frames here (drag to move, slider to zoom) */
var CROP=null,CROP_C=300;
function cardPhotoUpload(id,file){var img=new Image(),u=URL.createObjectURL(file);img.onload=function(){cropOpen(id,img,file)};img.onerror=function(){URL.revokeObjectURL(u);CARD.msg="الملف ليس صورة.";render()};img.src=u}
function cardPhotoEdit(id){CARD.msg="جارٍ فتح الصورة…";render();var bk=sb.storage.from("rider-photos");
  bk.download("orig/"+id+".jpg").then(function(r){if(r.error||!r.data)return bk.download(id+".jpg");return r}).then(function(r){if(r.error||!r.data)throw 0;
    var img=new Image(),u=URL.createObjectURL(r.data);img.onload=function(){CARD.msg="";render();cropOpen(id,img,null)};img.src=u}).catch(function(){CARD.msg="تعذّر فتح الصورة.";render()})}
function cropCover(){return Math.max(CROP_C/CROP.img.width,CROP_C/CROP.img.height)}
function cropContain(){return Math.min(CROP_C/CROP.img.width,CROP_C/CROP.img.height)}
function cropSet(s,cx,cy){var w0=CROP.img.width*CROP.s,h0=CROP.img.height*CROP.s;if(cx==null){cx=CROP_C/2;cy=CROP_C/2}
  var fx=(cx-CROP.x)/w0,fy=(cy-CROP.y)/h0;CROP.s=s;var w=CROP.img.width*s,h=CROP.img.height*s;CROP.x=cx-fx*w;CROP.y=cy-fy*h;cropClamp()}
function cropClamp(){var w=CROP.img.width*CROP.s,h=CROP.img.height*CROP.s;
  CROP.x=w>=CROP_C?Math.min(0,Math.max(CROP_C-w,CROP.x)):Math.max(0,Math.min(CROP_C-w,CROP.x));CROP.y=h>=CROP_C?Math.min(0,Math.max(CROP_C-h,CROP.y)):Math.max(0,Math.min(CROP_C-h,CROP.y))}
function cropDraw(){var cv=document.getElementById("cropCv");if(!cv)return;var g=cv.getContext("2d"),k=cv.width/CROP_C;g.setTransform(k,0,0,k,0,0);
  g.fillStyle="#fff";g.fillRect(0,0,CROP_C,CROP_C);g.drawImage(CROP.img,CROP.x,CROP.y,CROP.img.width*CROP.s,CROP.img.height*CROP.s);
  g.fillStyle="rgba(20,35,43,.55)";g.beginPath();g.rect(0,0,CROP_C,CROP_C);g.arc(CROP_C/2,CROP_C/2,CROP_C/2-1,0,Math.PI*2,true);g.fill("evenodd");
  g.strokeStyle="#fff";g.lineWidth=2;g.beginPath();g.arc(CROP_C/2,CROP_C/2,CROP_C/2-1,0,Math.PI*2);g.stroke();
  var z=document.getElementById("cropZ");if(z)z.value=String(Math.round(CROP.s/cropCover()*100))}
function cropOpen(id,img,file){CROP={id:id,img:img,file:file,s:1,x:0,y:0};
  /* start filled: whole circle covered, portrait photos framed a little above centre where the face usually is */
  CROP.s=cropCover();var h=img.height*CROP.s;CROP.x=(CROP_C-img.width*CROP.s)/2;CROP.y=h>CROP_C?-(h-CROP_C)*0.2:0;cropClamp();
  var o=document.getElementById("cropDlg");if(o)o.remove();o=document.createElement("div");o.id="cropDlg";o.className="addov";o.setAttribute("dir","rtl");
  var mn=Math.round(cropContain()/cropCover()*100);
  o.innerHTML='<div class="addbox" style="max-width:380px;text-align:center"><h2 style="margin:0 0 4px;font-size:17px">ضبط صورة '+esc(cname(id))+'</h2><p class="hint" style="margin:0 0 10px">اسحب الصورة لتحريكها وكبّر أو صغّر بالشريط. اللي داخل الدائرة هو اللي يطلع في البطاقة.</p>'+
    '<canvas id="cropCv" width="600" height="600" style="width:'+CROP_C+'px;height:'+CROP_C+'px;max-width:100%;touch-action:none;cursor:grab;border-radius:8px"></canvas>'+
    '<div class="row" style="gap:8px;align-items:center;margin:10px 0"><span class="hint">−</span><input id="cropZ" type="range" min="'+Math.min(mn,100)+'" max="400" value="100" style="flex:1"><span class="hint">+</span></div>'+
    '<div class="row" style="gap:6px;justify-content:center;flex-wrap:wrap;margin-bottom:10px"><button class="btn" id="cropFill">ملء الدائرة</button><button class="btn" id="cropFit">الصورة كاملة</button></div>'+
    '<div class="row" style="gap:8px;justify-content:center"><button class="btn pri" id="cropSave">حفظ الصورة</button><button class="btn" id="cropCancel">إلغاء</button></div></div>';
  document.body.appendChild(o);if(typeof trTree==="function")try{trTree(o)}catch(e){}
  var cv=document.getElementById("cropCv"),drag=null;
  cv.addEventListener("pointerdown",function(e){drag={x:e.clientX,y:e.clientY,ox:CROP.x,oy:CROP.y,k:CROP_C/cv.getBoundingClientRect().width};cv.setPointerCapture(e.pointerId);cv.style.cursor="grabbing"});
  cv.addEventListener("pointermove",function(e){if(!drag)return;CROP.x=drag.ox+(e.clientX-drag.x)*drag.k;CROP.y=drag.oy+(e.clientY-drag.y)*drag.k;cropClamp();cropDraw()});
  cv.addEventListener("pointerup",function(){drag=null;cv.style.cursor="grab"});
  cv.addEventListener("wheel",function(e){e.preventDefault();var r=cv.getBoundingClientRect(),k=CROP_C/r.width;cropSet(Math.max(cropContain(),Math.min(cropCover()*4,CROP.s*(e.deltaY<0?1.08:1/1.08))),(e.clientX-r.left)*k,(e.clientY-r.top)*k);cropDraw()},{passive:false});
  document.getElementById("cropZ").addEventListener("input",function(e){cropSet(cropCover()*(+e.target.value)/100);cropDraw()});
  cropDraw()}
function cropClose(){var o=document.getElementById("cropDlg");if(o)o.remove();if(CROP&&CROP.img&&/^blob:/.test(CROP.img.src))URL.revokeObjectURL(CROP.img.src);CROP=null}
function cropSave(){var C=CROP,id=C.id,cv=document.createElement("canvas"),k=600/CROP_C;cv.width=cv.height=600;var g=cv.getContext("2d");
  g.fillStyle="#fff";g.fillRect(0,0,600,600);g.drawImage(C.img,C.x*k,C.y*k,C.img.width*C.s*k,C.img.height*C.s*k);
  var b=document.getElementById("cropSave");if(b){b.disabled=true;b.textContent="جارٍ الحفظ…"}
  var bk=sb.storage.from("rider-photos");
  /* keep the original (max 1600px) so the framing can be changed later without re-uploading */
  var orig=C.file?new Promise(function(ok){var m=Math.min(1,1600/Math.max(C.img.width,C.img.height)),o=document.createElement("canvas");o.width=Math.round(C.img.width*m);o.height=Math.round(C.img.height*m);
      o.getContext("2d").drawImage(C.img,0,0,o.width,o.height);o.toBlob(function(ob){bk.upload("orig/"+id+".jpg",ob,{upsert:true,contentType:"image/jpeg"}).then(function(){ok()},function(){ok()})},"image/jpeg",0.9)}):Promise.resolve();
  cv.toBlob(function(bl){orig.then(function(){return bk.upload(id+".jpg",bl,{upsert:true,contentType:"image/jpeg"})}).then(function(r){if(r.error)throw r.error;if(CARD.ph&&CARD.ph!=="loading")CARD.ph[id]=1;return blobUrl(bl)})
    .then(function(d){CARD.photos[id]=d;CARD.sel[id]=true;CARD.msg="تم حفظ صورة "+cname(id);cropClose();render()},function(e){if(b){b.disabled=false;b.textContent="حفظ الصورة"}CARD.msg="تعذّر رفع الصورة: "+((e&&e.message)||e);render()})},"image/jpeg",0.9)}
document.addEventListener("click",function(e){var t=e.target;if(!CROP||!t.closest||!t.closest("#cropDlg"))return;
  if(t.id==="cropSave")cropSave();else if(t.id==="cropCancel"||t.id==="cropDlg")cropClose();
  else if(t.id==="cropFill"){cropSet(cropCover());cropDraw()}else if(t.id==="cropFit"){cropSet(cropContain());cropDraw()}});
function cardPrint(){var ids=Object.keys(CARD.sel).filter(function(id){return CARD.sel[id]&&data.couriers[id]}).sort(function(a,b){return data.couriers[a].n.localeCompare(data.couriers[b].n,"ar")});if(!ids.length)return;
  CARD.busy=true;render();
  ids.reduce(function(p,id){return p.then(function(){return cardPhoto(id)})},Promise.resolve()).then(function(){
    var per=CARD.mode==="side"?3:9,pages=[];for(var i=0;i<ids.length;i+=per)pages.push(ids.slice(i,i+per));
    var html=pages.map(function(pg){
      if(CARD.mode==="side")return '<div class="pg side">'+pg.map(function(id){return '<div class="pair">'+cardFront(id,CARD.photos[id]||"")+cardBack()+'</div>'}).join("")+'</div>';
      var f='<div class="pg">'+pg.map(function(id){return cardFront(id,CARD.photos[id]||"")}).join("")+'</div>';if(CARD.mode==="front")return f;
      /* backs mirrored per row so they line up when printed on both sides (flip on long edge) */
      var b=[];for(var r=0;r<pg.length;r+=3){var row=pg.slice(r,r+3).map(function(){return cardBack()});while(row.length<3)row.push('<div class="hcard" style="visibility:hidden"></div>');b=b.concat(row.reverse())}
      return f+'<div class="pg">'+b.join("")+'</div>'}).join("");
    var doc='<!doctype html><html dir="rtl"><head><meta charset="utf-8"><title>بطاقات المناديب</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;600;700&display=swap"><style>@page{size:A4;margin:8mm}body{margin:0}'+CARD_CSS+
      '.pg{display:grid;grid-template-columns:repeat(3,56mm);gap:4mm 6mm;justify-content:center;page-break-after:always;break-after:page}.hcard{break-inside:avoid}.pg:last-child{page-break-after:auto;break-after:auto}.pg.side{grid-template-columns:auto;gap:5mm}.pair{display:flex;gap:2mm}.hcard{box-shadow:0 0 0 .15mm #bbb}</style></head><body>'+html+'</body></html>';
    var f=document.createElement("iframe");f.style.cssText="position:fixed;right:0;bottom:0;width:0;height:0;border:0";document.body.appendChild(f);
    f.onload=function(){setTimeout(function(){try{f.contentWindow.focus();f.contentWindow.print()}catch(e){}setTimeout(function(){f.remove()},2000)},700)};f.srcdoc=doc;
    CARD.busy=false;CARD.msg="اختر «حفظ بتنسيق PDF» من نافذة الطباعة إذا تريد ملف PDF.";render()})}
function cardSaveCfg(){var g={phone:(document.getElementById("cPhone")||{}).value||CARD_DEF.phone,email:(document.getElementById("cEmail")||{}).value||CARD_DEF.email};CARD.cfg=g;
  sb.from("settings").upsert([{key:"card_phone",value:g.phone},{key:"card_email",value:g.email}]).then(function(r){CARD.msg=r.error?"تعذّر الحفظ: "+r.error.message:"تم حفظ بيانات التواصل";render()})}
document.addEventListener("input",function(e){if(e.target.id!=="cQ")return;CARD.q=e.target.value;var pos=e.target.selectionStart;render();var el=document.getElementById("cQ");if(el){el.focus();try{el.setSelectionRange(pos,pos)}catch(x){}}});
function vSoon(){''')
js=rep(js,'  if(t.dataset.ovpdf){ovPdf(t.dataset.ovpdf);return}','''  if(t.dataset.ovpdf){ovPdf(t.dataset.ovpdf);return}
  if(t.dataset.cedit){cardPhotoEdit(t.dataset.cedit);return}
  if(t.dataset.call!=null){if(t.dataset.call==="1")cardList().forEach(function(id){CARD.sel[id]=true});else CARD.sel={};render();return}
  if(t.id==="cPrint"){cardPrint();return}''')
js=rep(js,'  if(t.id==="ovMon"){ui0.ovm=t.value;render()}','''  if(t.id==="ovMon"){ui0.ovm=t.value;render()}
  if(t.dataset.csel!=null){CARD.sel[t.dataset.csel]=t.checked;render();return}
  if(t.dataset.cphoto!=null&&t.files&&t.files[0]){cardPhotoUpload(t.dataset.cphoto,t.files[0]);t.value="";return}
  if(t.id==="cCat"){CARD.cat=t.value;render();return}
  if(t.id==="cMode"){CARD.mode=t.value;render();return}
  if(t.id==="cPhone"||t.id==="cEmail"){cardSaveCfg();return}''')
css+="\n.cardsgrid{display:grid;grid-template-columns:300px 1fr;gap:16px;align-items:start}.cardsgrid>.panel{margin:0}.cprev{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}.cphoto{cursor:pointer;padding:5px 12px;font-size:13px;white-space:nowrap}tr.csel td{background:rgba(15,76,74,.06)}@media(max-width:900px){.cardsgrid{grid-template-columns:1fr}}"
