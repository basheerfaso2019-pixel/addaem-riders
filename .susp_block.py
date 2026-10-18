# «المناديب الموقوفون»: rider status = leave (until a date) / suspended / contract ended (fadhel 2026-10-18)
# ended riders: no rider-portal login (rider_portal returns 'ended') and leave شيت الأداء from the month after the end date
js=rep(js,'["susp","المناديب الموقوفون","Suspension Riders",1]','["susp","المناديب الموقوفون","Suspension Riders"]')
js=rep(js,'cards:isAdmin&&vCards}[view]','cards:isAdmin&&vCards,susp:vSusp}[view]')
js=rep(js,'all("riders","id,name,vehicle,tga,phone,category,sheet_pos,region","id").then(function(rs){rs.forEach(function(r){var c=C(r.id);',
 'all("riders","id,name,vehicle,tga,phone,category,sheet_pos,region,st,st_from,st_until,st_note","id").then(function(rs){rs.forEach(function(r){var c=C(r.id);if(r.st)c.st={t:r.st,f:r.st_from,u:r.st_until,n:r.st_note||""};')
js=rep(js,'return normCat(data.couriers[id].cat)&&!data.couriers[id].rg})','return normCat(data.couriers[id].cat)&&!data.couriers[id].rg&&!stGone(id,SHMON)})')
js=rep(js,'var rows=shRiders().map(','SHMON=mon;var rows=shRiders().map(')
js=rep(js,'function riderErr(e){return e==="locked"?','function riderErr(e){return e==="ended"?"تم إنهاء عقدك مع الشركة، لذلك لا يمكنك الدخول. للاستفسار تواصل مع الإدارة.":e==="locked"?')
js=rep(js,'function vSoon(){',r'''/* ---------- rider status: leave / suspended / ended ---------- */
var SHMON=null,stUi={msg:"",ok:true,busy:false},ST_T={leave:"إجازة",susp:"موقوف",ended:"منتهي العقد"};
function stToday(){var d=new Date();return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")}
function stGone(id,mon){var s=data.couriers[id]&&data.couriers[id].st;return !!(s&&s.t==="ended"&&s.f&&mon&&s.f.slice(0,7)<mon)}
function stDays(a,b){return Math.round((Date.parse(b)-Date.parse(a))/864e5)}
function stLastDay(id){var ds=days();for(var i=ds.length-1;i>=0;i--){var r=data.days[ds[i]][id];if(r&&(r[CP]||0)>0)return ds[i]}return ""}
function stState(s){var t=stToday();if(s.t==="ended")return {cls:"st-end",txt:"منتهي العقد"};
  if(s.u&&s.u<t)return {cls:"st-done",txt:(s.t==="leave"?"انتهت الإجازة":"انتهى الإيقاف")};
  if(s.f&&s.f>t)return {cls:"st-wait",txt:ST_T[s.t]+" تبدأ "+s.f};
  return {cls:s.t==="leave"?"st-leave":"st-susp",txt:ST_T[s.t]+(s.u?" — باقي "+stDays(t,s.u)+" يوم":"")}}
function vSusp(){
  var t=stToday(),ids=Object.keys(data.couriers).filter(function(id){return data.couriers[id].n}).sort(function(a,b){return cname(a).localeCompare(cname(b),"ar")});
  var form=isAdmin?'<section class="panel"><h2 style="margin:0 0 10px">تسجيل حالة مندوب</h2><div class="tgaform">'+
    '<label>المندوب<select id="stR"><option value="">اختر المندوب…</option>'+ids.map(function(id){return '<option value="'+esc(id)+'">'+esc(cname(id))+' — '+esc(id)+'</option>'}).join("")+'</select></label>'+
    '<label>الحالة<select id="stT"><option value="leave">إجازة</option><option value="susp">إيقاف</option><option value="ended">إنهاء عقد</option></select></label>'+
    '<label><span id="stFl">من تاريخ</span><input id="stF" type="date" value="'+t+'"></label>'+
    '<label id="stUl">إلى تاريخ<input id="stU" type="date"></label>'+
    '<label>السبب / ملاحظة<input id="stN" autocomplete="off" placeholder="مثال: حادث"></label>'+
    '<button class="btn pri" id="stSave"'+(stUi.busy?" disabled":"")+'>حفظ</button></div>'+
    '<p class="hint" style="margin:8px 0 0">منتهي العقد: لا يستطيع الدخول لبوابة المندوب، ويختفي من شيت الأداء ابتداءً من الشهر التالي لتاريخ الإنهاء. الإجازة والإيقاف للتسجيل والمتابعة فقط.</p>'+
    '<p class="hint" id="stMsg" style="margin:6px 0 0;color:'+(stUi.ok?"inherit":"#c00")+'">'+esc(stUi.msg)+'</p></section>':'';
  var rs=Object.keys(data.couriers).filter(function(id){return data.couriers[id].st}),ord={"st-leave":0,"st-susp":1,"st-wait":2,"st-done":3,"st-end":4};
  rs.sort(function(a,b){var x=stState(data.couriers[a].st),y=stState(data.couriers[b].st);return ord[x.cls]-ord[y.cls]||cname(a).localeCompare(cname(b),"ar")});
  var cnt=function(c){return rs.filter(function(id){return stState(data.couriers[id].st).cls===c}).length};
  var tiles='<div class="sttiles"><div><b class="num">'+cnt("st-leave")+'</b>في إجازة</div><div><b class="num">'+cnt("st-susp")+'</b>موقوف</div><div><b class="num">'+cnt("st-end")+'</b>منتهي العقد</div></div>';
  var body=rs.map(function(id,i){var s=data.couriers[id].st,x=stState(s),c=catOf(id);
    return '<tr><td class="num">'+(i+1)+'</td><td>'+esc(cname(id))+'</td><td class="num">'+esc(id)+'</td><td>'+(c?'<span class="catp cat-'+({"أ":"a","ب":"b","خ":"k"}[c]||"r")+'">'+esc(c)+'</span>':'')+'</td>'+
      '<td><span class="stchip '+x.cls+'">'+esc(x.txt)+'</span></td><td class="num">'+esc(s.f||"")+'</td><td class="num">'+esc(s.u||"")+'</td><td style="white-space:normal">'+esc(s.n)+'</td><td class="num">'+esc(stLastDay(id))+'</td>'+
      (isAdmin?'<td><button class="btn sm" data-stedit="'+esc(id)+'">تعديل</button> <button class="btn sm'+(x.cls==="st-done"?" pri":"")+'" data-stclear="'+esc(id)+'">'+(s.t==="ended"?"إعادة تفعيل":"رجع للعمل")+'</button></td>':'')+'</tr>'}).join("");
  return form+'<section class="panel"><h2 style="margin:0 0 10px">المناديب في إجازة أو موقوفون أو منتهية عقودهم</h2>'+tiles+
    '<div class="tbl"><table data-catdone="1"><thead><tr><th>م</th><th>الاسم</th><th>Rider Id</th><th>الفئة</th><th>الحالة</th><th>من</th><th>إلى</th><th>السبب</th><th>آخر يوم عمل</th>'+(isAdmin?'<th></th>':'')+'</tr></thead><tbody>'+
    (body||'<tr><td class="empty" colspan="10">لا يوجد مندوب في إجازة أو موقوف حالياً.</td></tr>')+'</tbody></table></div></section>'}
function stSet(m,ok){stUi.msg=m;stUi.ok=ok!==false;var e=document.getElementById("stMsg");if(e){e.textContent=m;e.style.color=stUi.ok?"inherit":"#c00"}}
function stType(){var v=(document.getElementById("stT")||{}).value,u=document.getElementById("stUl"),f=document.getElementById("stFl");if(u)u.style.display=v==="ended"?"none":"";if(f)f.textContent=v==="ended"?"تاريخ الإنهاء":"من تاريخ"}
function stSave(id,o){stUi.busy=true;stSet("جارٍ الحفظ…");
  return sb.from("riders").update(o).eq("id",id).then(function(r){stUi.busy=false;if(r.error){stSet("تعذّر الحفظ: "+r.error.message,false);render();return false}
    var c=data.couriers[id];if(o.st)c.st={t:o.st,f:o.st_from,u:o.st_until,n:o.st_note||""};else delete c.st;return true})}
document.addEventListener("change",function(e){if(e.target&&e.target.id==="stT")stType()});
document.addEventListener("click",function(e){var t=e.target.closest&&e.target.closest("#stSave,[data-stedit],[data-stclear]");if(!t)return;
  if(t.id==="stSave"){var id=document.getElementById("stR").value,ty=document.getElementById("stT").value,f=document.getElementById("stF").value||null,u=ty==="ended"?null:(document.getElementById("stU").value||null),n=document.getElementById("stN").value.trim();
    if(!id)return stSet("اختر المندوب أولاً.",false);if(u&&f&&u<f)return stSet("تاريخ النهاية قبل تاريخ البداية.",false);
    if(ty==="ended"&&!confirm("إنهاء عقد "+cname(id)+"؟ لن يستطيع الدخول لبوابة المندوب."))return;
    t.disabled=true;stSave(id,{st:ty,st_from:f,st_until:u,st_note:n||null}).then(function(ok){if(ok){stUi.msg="تم تسجيل "+cname(id)+": "+ST_T[ty]+(u?" حتى "+u:"")+".";stUi.ok=true}render()});return}
  if(t.dataset.stedit){var id2=t.dataset.stedit,s=data.couriers[id2].st;window.scrollTo(0,0);
    document.getElementById("stR").value=id2;document.getElementById("stT").value=s.t;document.getElementById("stF").value=s.f||"";document.getElementById("stU").value=s.u||"";document.getElementById("stN").value=s.n||"";stType();stSet("عدّل البيانات ثم اضغط حفظ.");return}
  if(t.dataset.stclear){var id3=t.dataset.stclear;if(!confirm("إلغاء حالة "+cname(id3)+" وإرجاعه مندوباً فعّالاً؟"))return;t.disabled=true;
    stSave(id3,{st:null,st_from:null,st_until:null,st_note:null}).then(function(ok){if(ok){stUi.msg="رجع "+cname(id3)+" مندوباً فعّالاً.";stUi.ok=true}render()});return}});
function vSoon(){''')
css+='''
.tgaform{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;align-items:end}
.tgaform label{display:flex;flex-direction:column;gap:4px;font-size:13.5px}
.tgaform select,.tgaform input{width:100%}
.btn.sm{padding:3px 10px;font-size:12.5px}
.sttiles{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 12px}
.sttiles>div{flex:1 1 120px;border:1px solid var(--line,#ddd);border-radius:10px;padding:8px 12px;font-size:13px}
.sttiles b{display:block;font-size:22px}
.stchip{display:inline-block;border-radius:10px;padding:1px 9px;font-size:12.5px;font-weight:700;white-space:nowrap}
.st-leave{background:#fff1c2;color:#6b4e00}.st-susp{background:#ffd9b3;color:#7a3a00}.st-end{background:#fde0e0;color:#8a1212}
.st-done{background:#e6e6e6;color:#444}.st-wait{background:#dbe9f7;color:#1f3864}
'''
