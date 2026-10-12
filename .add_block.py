# add a single rider from the UI (fadhel 2026-10-12): button in the sheet and cards pages, dialog outside the render root
js=rep(js,'function vSoon(){',r'''/* ---------- add rider ---------- */
var ADDB='<button class="btn" data-addr="1">+ إضافة مندوب</button>';
function addField(id,label,ph,extra){return '<label class="addf"><span>'+label+'</span><input id="'+id+'" placeholder="'+ph+'" '+(extra||"")+'></label>'}
function addOpen(){var o=document.getElementById("addDlg");if(o)o.remove();o=document.createElement("div");o.id="addDlg";o.className="addov";o.setAttribute("dir","rtl");
  o.innerHTML='<div class="addbox" role="dialog" aria-modal="true"><h2 style="margin:0 0 4px">إضافة مندوب جديد</h2><p class="hint" style="margin:0 0 12px">رقم الإقامة يصير كلمة دخول المندوب في بوابة المناديب.</p>'+
    addField("aId","Rider ID","مثال 4521234",'inputmode="numeric"')+addField("aName","الاسم","الاسم الكامل")+addField("aIq","رقم الإقامة","10 أرقام",'inputmode="numeric"')+addField("aPh","الجوال","05xxxxxxxx",'inputmode="tel"')+
    '<label class="addf"><span>الفئة</span><select id="aCat"><option value="ب">فئة ب</option><option value="أ">فئة أ (تارقت)</option><option value="خ">فئة خ</option><option value="ر">مندوب الرياض (خارج الشيت)</option></select></label>'+
    '<label class="addf"><span>المركبة</span><select id="aVeh"><option value="">—</option><option value="car">سيارة</option><option value="bike">دباب</option></select></label>'+
    '<p id="aMsg" class="hint" style="min-height:1.4em;margin:8px 0"></p><div class="row" style="gap:8px;justify-content:flex-start"><button class="btn pri" id="aSave">حفظ المندوب</button><button class="btn" id="aCancel">إلغاء</button></div></div>';
  document.body.appendChild(o);if(typeof trTree==="function")try{trTree(o)}catch(e){}document.getElementById("aId").focus()}
function addMsg(t,ok){var m=document.getElementById("aMsg");if(m){m.textContent=t;m.style.color=ok?"var(--good)":"var(--bad)"}}
function addSave(){var g=function(i){return document.getElementById(i).value.trim()},id=g("aId").replace(/\D/g,""),n=g("aName").replace(/\s+/g," "),iq=g("aIq").replace(/\D/g,""),ph=g("aPh").replace(/\D/g,""),cat=g("aCat"),veh=g("aVeh");
  if(!id)return addMsg("اكتب Rider ID (أرقام فقط).");if(!n)return addMsg("اكتب اسم المندوب.");
  if(data.couriers[id]&&data.couriers[id].n)return addMsg("هذا الرقم موجود مسبقاً باسم: "+data.couriers[id].n);
  if(iq&&iq.length!==10)return addMsg("رقم الإقامة لازم يكون 10 أرقام.");
  if(ph){if(/^05\d{8}$/.test(ph))ph="966"+ph.slice(1);else if(/^5\d{8}$/.test(ph))ph="966"+ph;if(!/^9665\d{8}$/.test(ph))return addMsg("رقم الجوال غير صحيح، اكتبه بصيغة 05xxxxxxxx.")}
  var ry=cat==="ر",b=document.getElementById("aSave");b.disabled=true;addMsg("جارٍ الحفظ…",true);
  sb.rpc("set_riders",{p_rows:[{id:id,name:n,iqama:iq,phone:ph,category:ry?"":cat}]}).then(function(r){if(r.error)throw r.error;
      return sb.from("riders").upsert({id:id,region:ry?"الرياض":null,vehicle:veh||null,updated_at:new Date().toISOString()}).then(function(u){if(u.error)throw u.error})})
    .then(function(){var c=data.couriers[id]||(data.couriers[id]={});c.n=n;if(ph)c.ph=ph;if(veh)c.v=veh;if(ry)c.rg="الرياض";else{c.cat=cat;delete c.rg}
      if(iq&&SHIQ&&typeof SHIQ==="object")SHIQ[id]=iq;if(typeof SHX==="object")for(var k in SHX)delete SHX[k];
      var o=document.getElementById("addDlg");if(o)o.remove();if(typeof SH_MSG!=="undefined")SH_MSG="تمت إضافة المندوب "+n;CARD.msg="تمت إضافة المندوب "+n;render()},
      function(e){b.disabled=false;addMsg("تعذّر الحفظ: "+((e&&e.message)||e))})}
document.addEventListener("click",function(e){var t=e.target;if(!t.closest)return;
  if(t.closest("[data-addr]")){addOpen();return}
  if(t.id==="aCancel"||t.id==="addDlg"){var o=document.getElementById("addDlg");if(o)o.remove();return}
  if(t.id==="aSave")addSave()});
document.addEventListener("keydown",function(e){if(e.key==="Escape"){var o=document.getElementById("addDlg");if(o)o.remove()}else if(e.key==="Enter"&&e.target.closest&&e.target.closest("#addDlg")&&e.target.tagName==="INPUT")addSave()});
function vSoon(){''')
js=rep(js,'''+'</select><button class="btn pri" id="shXlsx"''','''+'</select>'+(isAdmin?ADDB:'')+'<button class="btn pri" id="shXlsx"''')
js=rep(js,'''<input id="cQ" placeholder="بحث بالاسم أو ID أو الإقامة" value="'+esc(CARD.q)+'" style="min-width:200px">''','''<input id="cQ" placeholder="بحث بالاسم أو ID أو الإقامة" value="'+esc(CARD.q)+'" style="min-width:200px">'+ADDB+\'''')
css+='.addov{position:fixed;inset:0;background:rgba(10,30,30,.45);display:flex;align-items:center;justify-content:center;z-index:1000;padding:16px}.addbox{background:var(--surface,#fff);color:var(--fg);border-radius:14px;padding:18px 20px;width:100%;max-width:420px;box-shadow:0 10px 40px rgba(0,0,0,.25);max-height:90vh;overflow:auto}.addf{display:flex;flex-direction:column;gap:4px;margin:0 0 10px;font-size:13px}.addf input,.addf select{width:100%;box-sizing:border-box}'
