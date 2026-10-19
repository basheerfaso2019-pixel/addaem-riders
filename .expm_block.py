# staff: per-employee welcome text after sign-in (staff.welcome), expiry by minutes/hours and a per-login session length (fadhel 2026-10-19), and a logged-in employee is signed out as soon as the expiry passes
js=rep(js,'''<option value="">مدة سريعة…</option><option value="1">يوم</option>''','''<option value="">مدة سريعة…</option><option value="m">عدد دقائق…</option><option value="'+(2/1440)+'">دقيقتان</option><option value="'+(5/1440)+'">5 دقائق</option><option value="'+(10/1440)+'">10 دقائق</option><option value="'+(30/1440)+'">30 دقيقة</option><option value="'+(1/24)+'">ساعة</option><option value="'+(3/24)+'">3 ساعات</option><option value="'+(12/24)+'">12 ساعة</option><option value="1">يوم</option>''')
js=rep(js,'if(t.dataset.aexpq!=null&&t.value!==""){var dq=+t.value;','if(t.dataset.aexpq!=null&&t.value!==""){if(t.value==="m"){var mq=prompt("كم دقيقة؟","2");mq=mq&&+digits(mq);if(!mq||mq<=0){t.value="";return}t.value=String(mq/1440);if(t.value!==String(mq/1440)){var o=document.createElement("option");o.value=String(mq/1440);o.textContent=mq+" دقيقة";t.appendChild(o);t.value=o.value}}var dq=+t.value;')
js=rep(js,'    isAdmin=s.role==="admin";staff=isAdmin?null:','    isAdmin=s.role==="admin";if(!isAdmin)expWatch(user.id,s.expires_at);staff=isAdmin?null:')
# session length: employee is signed out N minutes after each login (fadhel 2026-10-19); staff.session_min, read via list_accounts3
js=rep(js,'sb.rpc("list_accounts2")','sb.rpc("list_accounts3")')
js=rep(js,'p:a.perms||[],x:x,o:JSON.stringify([a.name||"",a.role||"",a.perms||[],x])','p:a.perms||[],x:x,sm:a.session_min||"",o:JSON.stringify([a.name||"",a.role||"",a.perms||[],x,a.session_min||""])')
js=rep(js,'return JSON.stringify([a.n,a.r,a.p,a.x||""])!==a.o','return JSON.stringify([a.n,a.r,a.p,a.x||"",a.sm?+a.sm:""])!==a.o')
js=rep(js,'expires_at:a.r==="staff"&&a.x?a.x:null},{onConflict:"user_id"})','expires_at:a.r==="staff"&&a.x?a.x:null,session_min:a.r==="staff"&&a.sm?+a.sm:null},{onConflict:"user_id"})')
js=rep(js,"style=\"font-size:12px;margin-top:4px\"><br>'+st+'</td>'}","style=\"font-size:12px;margin-top:4px\"><br>'+st+sessCell(s,i)+'</td>'}")
js=rep(js,'sb.from("staff").select("name,role,perms,expires_at").eq("user_id",user.id)','sb.from("staff").select("name,role,perms,expires_at,session_min,welcome").eq("user_id",user.id)')
js=rep(js,'if(!isAdmin)expWatch(user.id,s.expires_at);','if(!isAdmin)expWatch(user.id,s.expires_at,s.session_min);STAFF_WEL=s.welcome||"";')
js=rep(js,'return enterStaff(r.data.user,nm)','try{localStorage.setItem("hs_sess_"+r.data.user.id,String(Date.now()))}catch(e){}return enterStaff(r.data.user,nm).then(function(x){if(STAFF_WEL&&(isAdmin||staff)){var w=STAFF_WEL;setTimeout(function(){deShow(\'<p class="denwel">\'+esc(w)+\'</p>\',"den-high den-wel")},2700)}return x})')
js=rep(js,'function vSoon(){',r'''/* ---------- employee access expiry while logged in ---------- */
var STAFF_WEL="",EXPW={t:null,i:null,sm:null,uid:null},SESS_OPTS=[2,5,10,15,30,60,120,240,480];
try{var _em=sessionStorage.getItem("hs_expmsg");if(_em){sessionStorage.removeItem("hs_expmsg");ui.msg=_em;ui.msgOk=false;ui0.who="staff"}}catch(e){}
function sessTxt(m){m=+m;return m%60===0?(m===60?"ساعة":m===120?"ساعتان":(m/60)+" ساعات"):m===2?"دقيقتان":m+(m>2&&m<=10?" دقائق":" دقيقة")}
function sessCell(s,i){var v=s.sm?+s.sm:"",o=SESS_OPTS.slice();if(v&&o.indexOf(v)<0)o.push(v);o.sort(function(a,b){return a-b});
  return '<div style="margin-top:6px;font-size:12px">مدة الجلسة بعد كل دخول:<br><select data-asess="'+i+'" style="font-size:12px"><option value=""'+(v?"":" selected")+'>بدون حد</option>'+o.map(function(m){return '<option value="'+m+'"'+(m===v?" selected":"")+'>'+sessTxt(m)+'</option>'}).join("")+'<option value="m">عدد دقائق…</option></select></div>'}
document.addEventListener("change",function(e){var t=e.target;if(!t||!t.dataset||t.dataset.asess==null)return;var v=t.value;
  if(v==="m"){var q=prompt("كم دقيقة بعد تسجيل الدخول؟","2");q=q&&+digits(q);if(!q||q<=0){render();return}v=String(Math.round(q))}
  ui.acc[+t.dataset.asess].sm=v;render()});
function sessStart(uid){var k="hs_sess_"+uid,v=null;try{v=+localStorage.getItem(k)}catch(e){}if(!v){v=Date.now();try{localStorage.setItem(k,String(v))}catch(e){}}return v}
function expKick(why){clearTimeout(EXPW.t);clearInterval(EXPW.i);
  try{if(EXPW.uid)localStorage.removeItem("hs_sess_"+EXPW.uid);sessionStorage.setItem("hs_expmsg",why==="sess"?"انتهت مدة الجلسة ("+sessTxt(EXPW.sm)+"). سجّل الدخول من جديد.":"انتهت صلاحية حسابك. تواصل مع المدير لتجديدها.")}catch(e){}
  sb.auth.signOut().then(function(){location.reload()},function(){location.reload()})}
function expArm(iso,sm){clearTimeout(EXPW.t);EXPW.sm=sm||null;var now=Date.now(),a=iso?new Date(iso).getTime():Infinity,b=sm?sessStart(EXPW.uid)+sm*6e4:Infinity,end=Math.min(a,b),why=b<a?"sess":"exp";
  if(end===Infinity)return;if(end<=now)return expKick(why);if(end-now<2147483000)EXPW.t=setTimeout(function(){expKick(why)},end-now+300)}
/* re-read expiry and session length every 20s so a change by the manager applies without a re-login */
function expWatch(uid,iso,sm){EXPW.uid=uid;expArm(iso,sm);clearInterval(EXPW.i);EXPW.i=setInterval(function(){sb.from("staff").select("expires_at,role,session_min").eq("user_id",uid).maybeSingle().then(function(r){if(r.error)return;if(!r.data)return expKick();if(r.data.role!=="admin")expArm(r.data.expires_at,r.data.session_min)})},20000)}
function vSoon(){''')
css+='''
.den-wel{text-align:center}.denwel{font-size:30px;font-weight:800;margin:14px 0 12px!important;color:#0f4c4a}
'''
