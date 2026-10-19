# staff expiry by minutes/hours (fadhel 2026-10-19), and a logged-in employee is signed out as soon as the expiry passes
js=rep(js,'''<option value="">مدة سريعة…</option><option value="1">يوم</option>''','''<option value="">مدة سريعة…</option><option value="m">عدد دقائق…</option><option value="'+(2/1440)+'">دقيقتان</option><option value="'+(5/1440)+'">5 دقائق</option><option value="'+(10/1440)+'">10 دقائق</option><option value="'+(30/1440)+'">30 دقيقة</option><option value="'+(1/24)+'">ساعة</option><option value="'+(3/24)+'">3 ساعات</option><option value="'+(12/24)+'">12 ساعة</option><option value="1">يوم</option>''')
js=rep(js,'if(t.dataset.aexpq!=null&&t.value!==""){var dq=+t.value;','if(t.dataset.aexpq!=null&&t.value!==""){if(t.value==="m"){var mq=prompt("كم دقيقة؟","2");mq=mq&&+digits(mq);if(!mq||mq<=0){t.value="";return}t.value=String(mq/1440);if(t.value!==String(mq/1440)){var o=document.createElement("option");o.value=String(mq/1440);o.textContent=mq+" دقيقة";t.appendChild(o);t.value=o.value}}var dq=+t.value;')
js=rep(js,'    isAdmin=s.role==="admin";staff=isAdmin?null:','    isAdmin=s.role==="admin";if(!isAdmin)expWatch(user.id,s.expires_at);staff=isAdmin?null:')
js=rep(js,'function vSoon(){',r'''/* ---------- employee access expiry while logged in ---------- */
var EXPW={t:null,i:null};
try{var _em=sessionStorage.getItem("hs_expmsg");if(_em){sessionStorage.removeItem("hs_expmsg");ui.msg=_em;ui.msgOk=false;ui0.who="staff"}}catch(e){}
function expKick(){clearTimeout(EXPW.t);clearInterval(EXPW.i);try{sessionStorage.setItem("hs_expmsg","انتهت صلاحية حسابك. تواصل مع المدير لتجديدها.")}catch(e){}
  sb.auth.signOut().then(function(){location.reload()},function(){location.reload()})}
function expArm(iso){clearTimeout(EXPW.t);if(!iso)return;var ms=new Date(iso)-new Date();if(ms<=0)return expKick();if(ms<2147483000)EXPW.t=setTimeout(expKick,ms+500)}
/* re-read the expiry every 20s so a change by the manager applies without a re-login */
function expWatch(uid,iso){expArm(iso);clearInterval(EXPW.i);EXPW.i=setInterval(function(){sb.from("staff").select("expires_at,role").eq("user_id",uid).maybeSingle().then(function(r){if(r.error)return;if(!r.data)return expKick();if(r.data.role!=="admin")expArm(r.data.expires_at)})},20000)}
function vSoon(){''')
