import re
src=open('hs/index.html',encoding='utf8').read()
css=src[src.index('<style id="css">')+len('<style id="css">'):src.index('</style>')]
app=src[src.index('<script id="app">')+len('<script id="app">'):src.rindex('</script>')]
def cut(a,b):
    i=app.index(a); j=app.index(b,i); return app[i:j]
def rep(s,a,b,cnt=1):
    assert s.count(a)==cnt,(a,s.count(a)); return s.replace(a,b)

views=cut('/* ---------- derived ---------- */','/* ---------- upload parsing ---------- */')
parse=cut('/* ---------- upload parsing ---------- */','var NREC=22;')

# ---- view edits ----
views=rep(views,'function days(){return Object.keys(data.days).filter(function(d){return d<TODAY}).sort()}\nfunction lastDay(){var a=days();return a.length?a[a.length-1]:null}',
 'function days(){return Object.keys(data.days).filter(function(d){return d<TODAY}).sort()}\nfunction lastDay(){if(LAST)return LAST;var a=days();return a.length?a[a.length-1]:null}')
views=rep(views,'function courierIds(){var s={};Object.keys(data.couriers)','function courierIds(){var s={};Object.keys(data.couriers)')
# admin menu: courier preview becomes a link, add sign-out
views=rep(views,"""var extra=isAdmin?'<hr><button data-tab="courier" aria-current="'+(view==="courier")+'">شاشة المندوب<small>Rider login</small></button><button data-tab="perm\"""",
 """var extra=isAdmin?'<hr><a class="navlink" href="#rider" target="_blank" rel="noopener">شاشة المندوب<small>Rider link</small></a><button data-tab="perm\"""")
views=rep(views,"""<button data-tab="data" aria-current="'+(view==="data")+'">رفع البيانات<small>Upload</small></button>':'<hr><button id="staffOut">تسجيل خروج<small>Sign out</small></button>';""",
 """<button data-tab="data" aria-current="'+(view==="data")+'">رفع البيانات<small>Upload</small></button><button id="staffOut">تسجيل خروج<small>Sign out</small></button>':'<hr><button id="staffOut">تسجيل خروج<small>Sign out</small></button>';""")
views=rep(views,'function sampleNote(){return data.sample?','function sampleNote(){return false?')
# perm view rewritten
i=views.index('var PERMS=');j=views.index('/* courier */')
views=views[:i]+r'''var PERMS=MENU.filter(function(m){return !m[3]});
var STAFF_DOMAIN="staff.example.com";
function uname(e){e=String(e||"");return e.slice(-STAFF_DOMAIN.length-1)==="@"+STAFF_DOMAIN?e.slice(0,-STAFF_DOMAIN.length-1):e}
function genPw(){var c="abcdefghjkmnpqrstuvwxyz23456789",a=new Uint32Array(10),o="";crypto.getRandomValues(a);for(var i=0;i<10;i++)o+=c[a[i]%c.length];return o}
function siteUrl(){return location.origin+location.pathname}
function staffFn(body){return sb.functions.invoke("staff-admin",{body:body}).then(function(r){var d=r.data;if(r.error&&!d&&r.error.context&&r.error.context.json)return r.error.context.json().then(function(j){throw new Error(j.error)},function(){throw new Error(r.error.message)});if(r.error)throw new Error((d&&d.error)||r.error.message);if(d&&d.error)throw new Error(d.error);return d})}
function staffErr(e){var m=e&&e.message;return m==="taken"?"اسم المستخدم مستخدم من قبل، اختر اسماً آخر.":m==="bad_username"?"اسم المستخدم: حروف إنجليزية وأرقام فقط، من 3 إلى 30.":m==="short_password"?"كلمة المرور 8 أحرف على الأقل.":m==="not_allowed"?"هذه العملية للمدير فقط.":"تعذّر الحفظ: "+m}
function vPerm(){
  if(!ui.acc){ui.acc="loading";sb.rpc("list_accounts").then(function(r){if(r.error){ui.acc=[];ui.msg="تعذّر تحميل الحسابات: "+r.error.message;ui.msgOk=false}else ui.acc=r.data.map(function(a){return{id:a.user_id,e:a.email,n:a.name||"",r:a.role||"",p:a.perms||[],o:JSON.stringify([a.name||"",a.role||"",a.perms||[]])}});render()});}
  if(ui.acc==="loading")return '<div class="panel"><p class="hint" style="margin:0">جارٍ التحميل…</p></div>';
  var dr=ui.acc,dirty=dr.some(function(a){return JSON.stringify([a.n,a.r,a.p])!==a.o});
  var rows=dr.map(function(s,i){var self=s.id===myUid;return '<tr><td class="s"><input data-aname="'+i+'" value="'+esc(s.n)+'" placeholder="الاسم" style="min-width:120px"><br><span class="num" style="color:var(--muted);font-size:12px" dir="ltr">'+esc(uname(s.e))+'</span>'+(self||!s.r?'':' <button class="btn" style="padding:2px 8px;font-size:12px" data-newpw="'+i+'"'+(ui.busy?" disabled":"")+'>كلمة مرور جديدة</button>')+(self?'<br><span style="color:var(--muted);font-size:12px">هذا حسابك، مدير بكل الصلاحيات</span>':'')+'</td>'+
    '<td><select data-arole="'+i+'"'+(self?" disabled":"")+'><option value=""'+(!s.r?" selected":"")+'>بدون دخول</option><option value="staff"'+(s.r==="staff"?" selected":"")+'>موظف</option><option value="admin"'+(s.r==="admin"?" selected":"")+'>مدير</option></select></td>'+
    PERMS.map(function(m){return '<td><input type="checkbox" data-perm="'+i+'|'+m[0]+'"'+((s.p||[]).indexOf(m[0])>=0||s.r==="admin"?" checked":"")+(s.r!=="staff"?" disabled":"")+' aria-label="'+esc(m[1])+'"></td>'}).join("")+'</tr>'}).join("");
  return '<section class="panel"><h2>أنواع الصلاحيات</h2><ul class="cols" style="margin-top:8px"><li><b>المدير</b> <span>كل الأقسام، ورفع البيانات، وإدارة الحسابات.</span></li><li><b>الموظف</b> <span>يرى فقط الأقسام التي تحددها له هنا.</span></li><li><b>المندوب</b> <span>يدخل برقم الإقامة والـ ID من رابط المناديب.</span></li></ul></section>'+
    '<section class="panel"><h2>الحسابات</h2><p class="hint">حدّد أقسام كل موظف ثم اضغط «حفظ الصلاحيات». اختيار «بدون دخول» يوقف حسابه.</p>'+
    '<div class="tbl" style="box-shadow:none"><table><thead><tr><th>الحساب</th><th>الدور</th>'+PERMS.map(function(m){return '<th>'+m[1]+'</th>'}).join("")+'</tr></thead><tbody>'+(rows||'<tr><td class="empty" colspan="'+(PERMS.length+2)+'">لا توجد حسابات بعد.</td></tr>')+'</tbody></table></div>'+(dr.length<2?'<p class="hint" style="margin-top:10px">لا يوجد موظفون بعد. أضف أول موظف من النموذج بالأسفل.</p>':'')+
    '<p class="'+(ui.msgOk?"ok":"err")+'" style="margin-top:10px">'+esc(ui.msg)+'</p>'+
    '<div class="row"><button class="btn pri" id="saveStaff"'+(dirty&&!ui.busy?"":" disabled")+'>حفظ الصلاحيات</button></div></section>'+
    (ui.cred?'<section class="panel" style="border-inline-start:4px solid var(--gold)"><h2>أرسل هذه البيانات للموظف</h2><p class="hint">انسخها الآن، كلمة المرور لا تظهر مرة أخرى.</p><pre id="credTxt" style="white-space:pre-wrap;background:var(--sunk);padding:12px;border-radius:6px;font:15px/1.8 var(--f-body)">'+esc(ui.cred)+'</pre><div class="row"><button class="btn pri" id="copyCred">نسخ</button><button class="btn" id="hideCred">تم</button></div></section>':'')+
    '<section class="panel"><h2>إضافة موظف</h2><p class="hint">اكتب اسم الموظف واسم مستخدم بالإنجليزي. كلمة المرور تُولَّد تلقائياً ويمكنك تغييرها. بعد الإضافة تظهر لك البيانات لترسلها له.</p>'+
    '<form id="addStaff" class="row" autocomplete="off"><label>اسم الموظف<input id="sn" required></label><label>اسم المستخدم<input id="su" required dir="ltr" autocapitalize="none" pattern="[A-Za-z0-9._\\-]{3,30}" title="حروف إنجليزية وأرقام، من 3 إلى 30"></label><label>كلمة المرور<input id="sp" required dir="ltr" minlength="8" value="'+esc(ui.genpw||(ui.genpw=genPw()))+'"></label><button class="btn pri" type="submit"'+(ui.busy?" disabled":"")+'>إضافة موظف</button></form></section>';
}

'''+views[j:]
# courier screen
views=rep(views,"""    var demo=data.sample&&who==="courier"?'<p class="hint" style="margin-top:10px">للتجربة: رقم الإقامة <code class="num">'+sampleIq(0)+'</code> والـ ID <code class="num">100201</code></p>':"";""",
 """    if(RIDER_ONLY)who="courier";var su=ui0.signup;
    var demo=su?'<p class="hint" style="margin-top:12px"><a href="#" data-su="0">رجوع لتسجيل الدخول</a></p>':"";""")
views=rep(views,"""      '<form id="staffF" autocomplete="off"><label>اسم المستخدم<input id="lu" dir="ltr" required></label><label>كلمة المرور<input id="lp" type="password" dir="ltr" required></label><p class="err">'+esc(ui.msg)+'</p><button class="btn pri" type="submit">دخول</button></form>';""",
 """      '<form id="staffF">'+(su?'<label>الاسم<input id="ln" required></label>':'')+'<label>'+(su?'البريد الإلكتروني':'اسم المستخدم')+'<input id="lu" type="'+(su?'email':'text')+'" dir="ltr" autocomplete="username" autocapitalize="none" required></label><label>كلمة المرور<input id="lp" type="password" dir="ltr" minlength="8" autocomplete="'+(su?"new-password":"current-password")+'" required></label><p class="'+(ui.msgOk?"ok":"err")+'">'+esc(ui.msg)+'</p><button class="btn pri" type="submit"'+(ui.busy?" disabled":"")+'>'+(su?"إنشاء حساب":"دخول")+'</button></form>';""")
views=rep(views,"""    return '<div class="login"><section class="panel"><div class="seg" role="group" style="margin-bottom:14px"><button data-who="courier" aria-pressed="'+(who==="courier")+'">مندوب توصيل</button><button data-who="staff" aria-pressed="'+(who==="staff")+'">موظف</button></div>'+""",
 """    return '<div class="login"><section class="panel">'+(RIDER_ONLY?'':'<div class="seg" role="group" style="margin-bottom:14px"><button data-who="courier" aria-pressed="'+(who==="courier")+'">مندوب توصيل</button><button data-who="staff" aria-pressed="'+(who==="staff")+'">موظف / مدير</button></div>')+""")
views=rep(views,'"أدخل اسم المستخدم وكلمة المرور التي أعطاك إياها المدير."','(su?"أنشئ حسابك، ثم يمنحك المدير الصلاحيات.":"أدخل اسم المستخدم وكلمة المرور التي أرسلها لك المدير. المدير يدخل ببريده.")')
views=rep(views,"""<button class="btn" id="logout">'+(isAdmin?"إغلاق":"تسجيل خروج")+'</button>""","""<button class="btn" id="logout">تسجيل خروج</button>""")
views=rep(views,"""    if(!data.days[d])res+='<div class="hero"><span class="hero-num">—</span><span>'+dl(d)+'</span></div><p class="hint">لم تُرفع بيانات هذا اليوم بعد.</p>';""",
 """    if(!LAST||d>LAST)res+='<div class="hero"><span class="hero-num">—</span><span>'+dl(d)+'</span></div><p class="hint">لم تُرفع بيانات هذا اليوم بعد.</p>';""")
views=rep(views,"""    else{var r=data.days[d],arr=Object.keys(r).map(function(k){return +r[k][CP]||0}).sort(function(a,b){return b-a}),rk=arr.indexOf(+v[CP]||0)+1;""",
 """    else{var rk=v.rk,arr={length:v.cn};""")
views=rep(views,"""kpi("ترتيبك في اليوم",'<span class="num">'+rk+'</span>""","""(rk?kpi("ترتيبك في اليوم",'<span class="num">'+rk+'</span>""")
views=rep(views,"""kpi("نسبة القبول",P(v[AR]),'<span class="num">'+fmt(v[AD],0)+'</span> مقبول من <span class="num">'+fmt(v[NT],0)+'</span>')+kpi("ساعات العمل",N(v[AC]),'من <span class="num">'+fmt(v[PL])+'</span> مخططة')+""","""(v[NT]!=null||v[AC]!=null?kpi("نسبة القبول",P(v[AR]),'<span class="num">'+fmt(v[AD],0)+'</span> مقبول من <span class="num">'+fmt(v[NT],0)+'</span>')+kpi("ساعات العمل",N(v[AC]),'من <span class="num">'+fmt(v[PL])+'</span> مخططة'):"")+""")
views=rep(views,"""'</span></span>',"")+""","""'</span></span>',v.av!=null?'متوسط المناديب <span class="num">'+fmt(v.av,1)+'</span> طلب':""):"")+""")
views=rep(views,"""(STATE.updated?'<li><span>آخر تحديث:</span> <span class="num">'+esc(STATE.updated.slice(0,16).replace("T"," "))+'</span></li>':"")""","""(LASTUP?'<li><span>آخر رفع:</span> <span class="num">'+esc(LASTUP)+'</span></li>':"")""")
views=rep(views,"""'<p class="hint">البيانات الجديدة تستبدل نفس الأيام والمناديب في اللوحة، وباقي البيانات تبقى.'+(data.sample?' ستُحذف البيانات التجريبية.':'')+'</p>'""","""'<p class="hint">البيانات الجديدة تستبدل نفس الأيام والمناديب، وباقي البيانات تبقى.</p>'""")
views=rep(views,"""'<div class="row"><button class="btn pri" id="applyUp"'+(ui.busy?" disabled":"")+'>اعتماد ونشر</button>""","""'<div class="row"><button class="btn pri" id="applyUp"'+(ui.busy?" disabled":"")+'>اعتماد وحفظ</button>""")
views=rep(views,"""يُحفظ رقم الإقامة مشفّراً.""","""يُحفظ رقم الإقامة مشفّراً ولا يمكن لأحد قراءته.""")
views=rep(views,"""(data.sample?"":'<div class="row" style="margin-top:14px">'""","""('<div class="row" style="margin-top:14px">'""")
views=rep(views,"var V={overall:vOverall,daily:vDaily,riders:vRiders,top:vTop,absence:vAbsence,wallet:vWallet,quality:vQuality,distance:vDistance,courier:vCourier,data:isAdmin&&vData,perm:isAdmin&&vPerm}[view];",
 "if(booting){root.innerHTML='<div class=\"login\" style=\"padding:60px 16px;text-align:center\"><p class=\"hint\">جارٍ التحميل…</p></div>';return}\n  if(!me&&!isAdmin&&!staff)view=\"courier\";\n  var V={overall:vOverall,daily:vDaily,riders:vRiders,top:vTop,absence:vAbsence,wallet:vWallet,quality:vQuality,distance:vDistance,courier:vCourier,data:isAdmin&&vData,perm:isAdmin&&vPerm}[view];")
views=rep(views,"if(view!==\"courier\"&&!canSee(view))V=staff?","if(view!==\"courier\"&&view!==\"data\"&&view!==\"perm\"&&!canSee(view))V=staff?")
# perm & data only for admin
views=rep(views,"else if(!V)V=vSoon;","else if(!V)V=(view===\"data\"||view===\"perm\")?vCourier:vSoon;")


# declined deliveries for the courier
views=rep(views,"""tile("distance","المسافة المقطوعة",""","""tile("declined","الطلبات المرفوضة",N(sumDE(mine,id),0),'كل الأيام حتى <span class="num">'+(ld||"—")+'</span>')+tile("distance","المسافة المقطوعة",""")
views=rep(views,"""(+v[NS]?kpi("عدم حضور",N(v[NS],0),""):"")+'</div>';}""","""(v[DE]!=null?kpi("الطلبات المرفوضة",N(v[DE],0),"Declined Deliveries"):"")+(+v[NS]?kpi("عدم حضور",N(v[NS],0),""):"")+'</div>';}""")
views=rep(views,"""kpi("عدم الحضور",N(a.ns,0),"")+'</div></section>';}""","""kpi("عدم الحضور",N(a.ns,0),"")+kpi("الطلبات المرفوضة",N(sumDE(mine,id),0),"Declined Deliveries")+'</div></section>';}""")
views=rep(views,"""  if(cs==="wallet"){""","""  if(cs==="declined"){var dd2=mine.filter(function(d){return data.days[d][id][DE]!=null}),tot=sumDE(mine,id);
    var rowsD=dd2.slice().reverse().map(function(d){var y=data.days[d][id];return '<tr class="click" data-cday="'+d+'" data-cs="day"><td>'+dl(d)+'</td><td>'+N(y[DE],0)+'</td><td>'+N(y[NT],0)+'</td><td>'+N(y[CP],0)+'</td></tr>'}).join("");
    return head+'<section class="panel"><h2>الطلبات المرفوضة</h2><div class="hero"><span class="hero-num num">'+fmt(tot,0)+'</span><span>طلب مرفوض حتى <span class="num">'+(ld||"—")+'</span></span></div>'+
      '<p class="hint">الطلبات التي وصلتك ورفضتها (Declined Deliveries). كثرة الرفض تخفض نسبة القبول.</p>'+
      (rowsD?'<div class="tbl" style="box-shadow:none"><table><thead><tr><th>اليوم</th><th>المرفوضة</th><th>المُبلّغة</th><th>المكتملة</th></tr></thead><tbody>'+rowsD+'</tbody></table></div>':'<p class="hint">لا توجد بيانات رفض مسجلة لك بعد.</p>')+'</section>';}
  if(cs==="wallet"){""")
views=rep(views,"""function curMonth(){""","""function sumDE(list,id){var t=0;list.forEach(function(d){t+=+data.days[d][id][DE]||0});return t}
function curMonth(){""")

views=rep(views,"if(u.multiDay)notes.push('الملف يغطي أكثر من يوم، صدّره ليوم واحد');","if(u.multiDay)notes.push('الملف يغطي أكثر من يوم ولن يُحفظ. صدّره ليوم واحد');")
head=r'''
(function(){
"use strict";
var SB_URL="https://uukpnrpkgxmuqiqqjdel.supabase.co",SB_KEY="sb_publishable_BOF7VvUKkmq90xnCKdCUlw_Q_osg7dv";
var XLSX_URL="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js";
var sb=window.supabase.createClient(SB_URL,SB_KEY,{auth:{persistSession:true,autoRefreshToken:true}});
var root=document.getElementById("root");
var RIDER_ONLY=location.hash==="#rider";
window.addEventListener("hashchange",function(){location.reload()});

/* record layout per rider per day */
var CI=0,CO=1,SH=2,PL=3,AC=4,BR=5,AR=6,CR=7,NS=8,NT=9,CP=10,AD=11,ST=12,DI=13,QS=14,DP=15,ATT=16,LH=17,CA=18,DE=19;
/* database column for each record slot */
var DBCOL={city:CI,contract:CO,shifts:SH,planned_hours:PL,actual_hours:AC,break_hours:BR,acceptance_rate:AR,contact_rate:CR,no_shows:NS,notified:NT,completed:CP,accepted:AD,stacked:ST,distance_km:DI,payable_km:DP,attendance_rate:ATT,lost_hours:LH,cancelled:CA,declined:DE};
var PERF_COLS=["city","contract","shifts","planned_hours","actual_hours","break_hours","acceptance_rate","contact_rate","no_shows","notified","completed","accepted","stacked","attendance_rate","lost_hours","cancelled","declined"];

function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]})}
function fmt(n,d){return Number(n||0).toLocaleString("en-US",{maximumFractionDigits:d==null?2:d})}
function N(n,d){return '<span class="num">'+fmt(n,d)+'</span>'}
function P(n){return n==null||isNaN(n)?"—":'<span class="num">'+fmt(n,2)+'%</span>'}
var TODAY=new Intl.DateTimeFormat("en-CA",{timeZone:"Asia/Riyadh"}).format(new Date());
function addDays(d,n){var t=new Date(d+"T12:00:00Z");t.setUTCDate(t.getUTCDate()+n);return t.toISOString().slice(0,10)}
var YEST=addDays(TODAY,-1);
var WD=["الأحد","الاثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت"];
function wd(d){return WD[new Date(d+"T12:00:00Z").getUTCDay()]}
function dl(d){return wd(d)+' <span class="num">'+d+'</span>'}
function ss(k,v){try{if(v===undefined)return sessionStorage.getItem(k);if(v===null)sessionStorage.removeItem(k);else sessionStorage.setItem(k,v)}catch(e){return null}}

var data={company:"الدعم المطور للخدمات اللوجستية",couriers:{},days:{},staff:[]};
var isAdmin=false,view="courier",me=null,staff=null,myUid=null,LAST=null,LASTUP=null,booting=true;
var ui0={who:"courier",cs:"home",mon:null,dmode:"day",dday:null,signup:false};
var ui={f:null,sel:null,mode:"day",cday:null,upload:null,confirmReset:false,msg:"",msgOk:false,busy:false};
function num(v){return v==null?null:+v}

'''

tail=r'''
/* ---------- database ---------- */
function all(table,cols,order){var out=[],size=1000;
  function page(from){return sb.from(table).select(cols).order(order[0]).order(order[1]).range(from,from+size-1).then(function(r){if(r.error)throw r.error;out=out.concat(r.data);return r.data.length===size?page(from+size):out})}
  return page(0)}
function rowToRec(r){var x=[];for(var k in DBCOL){var v=r[k];x[DBCOL[k]]=(k==="city"||k==="contract")?(v||""):num(v)}if(x[CP]==null&&r.completed_dist!=null)x[CP]=+r.completed_dist;return x}
function qToObj(q){return {s:q.segment||"",sc:num(q.score),ot:num(q.on_time),fr:num(q.fail_score),vr:num(q.verif_rate),vt:num(q.verif_total),vs:num(q.verif_ok),g:num(q.gross),cp:num(q.completed),it:num(q.in_time),f:num(q.failed),ci:q.city||"",co:q.contract||""}}
function loadStaffData(){
  var d={company:data.company,couriers:{},days:{},staff:[]};
  function C(id){return d.couriers[id]||(d.couriers[id]={})}
  var jobs=[
    sb.from("settings").select("key,value").then(function(r){(r.data||[]).forEach(function(s){if(s.key==="company")d.company=s.value;if(s.key==="last_upload")LASTUP=s.value})}),
    all("riders","id,name,vehicle,tga","id").then(function(rs){rs.forEach(function(r){var c=C(r.id);if(r.name)c.n=r.name;if(r.vehicle)c.v=r.vehicle;if(r.tga)c.tga=r.tga})}),
    all("daily","*",["day","rider_id"]).then(function(rs){rs.forEach(function(r){(d.days[r.day]||(d.days[r.day]={}))[r.rider_id]=rowToRec(r)})}),
    sb.rpc("riders_with_login").then(function(r){(r.data||[]).forEach(function(id){C(typeof id==="string"?id:id.riders_with_login).h=true})})];
  if(canSee("quality"))jobs.push(all("quality","*",["month","rider_id"]).then(function(rs){rs.forEach(function(q){var c=C(q.rider_id);(c.q||(c.q={}))[q.month]=qToObj(q)})}));
  if(canSee("wallet"))jobs.push(all("wallet","*",["rider_id","rider_id"]).then(function(rs){rs.forEach(function(w){C(w.rider_id).w={b:num(w.balance),c:null,d:w.as_of}})}));
  return Promise.all(jobs).then(function(){data=d;LAST=null});
}
/* fix all() call sites that pass one order column */
var _all=all;all=function(t,c,o){return _all(t,c,typeof o==="string"?[o,o]:o)};

function portalToData(res){
  me=res.rider&&res.rider.id||me;LAST=res.last_day||null;
  var d={company:res.company||data.company,couriers:{},days:{},staff:[]},c=d.couriers[me]={};
  if(res.rider&&res.rider.name)c.n=res.rider.name;
  (res.days||[]).forEach(function(r){var x=rowToRec(r);x.rk=r.rnk;x.cn=r.cnt;x.av=r.avg_completed!=null?+r.avg_completed:null;(d.days[r.day]||(d.days[r.day]={}))[me]=x});
  (res.quality||[]).forEach(function(q){(c.q||(c.q={}))[q.month]=qToObj(q)});
  if(res.wallet)c.w={b:num(res.wallet.balance),c:null,d:res.wallet.as_of};
  data=d;
}

/* staff session: read own role, first account becomes the manager */
function enterStaff(user,name){
  myUid=user.id;
  return sb.from("staff").select("name,role,perms").eq("user_id",user.id).maybeSingle().then(function(r){
    if(r.data)return r.data;
    return sb.rpc("claim_admin",{p_name:name||user.email}).then(function(c){return c.data?{name:name||user.email,role:"admin",perms:[]}:null})
  }).then(function(s){
    if(!s){isAdmin=false;staff=null;ui.msg="تم الدخول، لكن حسابك بانتظار أن يمنحك المدير الصلاحيات.";ui.msgOk=true;ui0.who="staff";return sb.auth.signOut()}
    isAdmin=s.role==="admin";staff=isAdmin?null:{n:s.name||user.email,p:s.perms||[]};
    return loadStaffData().then(function(){var v=ss("hs_view");view=v&&(canSee(v)||isAdmin&&(v==="data"||v==="perm"))?v:isAdmin?"daily":((staff.p&&staff.p[0])||"none")});
  });
}

function batches(list,n){var out=[];for(var i=0;i<list.length;i+=n)out.push(list.slice(i,i+n));return out}
function upsertAll(table,rows,conflict){return batches(rows,500).reduce(function(p,b){return p.then(function(){return sb.from(table).upsert(b,{onConflict:conflict}).then(function(r){if(r.error)throw r.error})})},Promise.resolve())}
function round2(v){return v==null?null:Math.round(v*100)/100}
/* write parsed files to the database */
function applyUpload(list){
  var riders={},meta={},daily={perf:[],dist:[]},qual=[],wal={},ros=[];
  list.forEach(function(p){
    Object.keys(p.people).forEach(function(id){var b=p.people[id];riders[id]=1;
      if(b.v||b.tga){var m=meta[id]||(meta[id]={id:id,vehicle:null,tga:null});if(b.v)m.vehicle=b.v;if(b.tga)m.tga=b.tga}
      if(b.w&&(!wal[id]||b.w.d>=wal[id].as_of))wal[id]={rider_id:id,balance:round2(b.w.b),as_of:b.w.d};
      if(p.type==="roster"){var iq=/^\d{6,}$/.test(b.iq||"")?b.iq:"";ros.push({id:id,name:b.n||"",iqama:iq})}});
    Object.keys(p.days).forEach(function(d){Object.keys(p.days[d]).forEach(function(id){var x=p.days[d][id];riders[id]=1;
      if(p.type==="dist")daily.dist.push({day:d,rider_id:id,distance_km:round2(x[DI]),payable_km:round2(x[DP]),completed_dist:x.softCP==null?null:x.softCP});
      else{var o={day:d,rider_id:id};PERF_COLS.forEach(function(k){var v=x[DBCOL[k]];o[k]=(k==="city"||k==="contract")?(v||null):(v==null?null:round2(v))});daily.perf.push(o)}})});
    Object.keys(p.quality).forEach(function(id){riders[id]=1;Object.keys(p.quality[id]).forEach(function(m){var q=p.quality[id][m];
      qual.push({month:m,rider_id:id,segment:q.s||null,score:q.sc,on_time:q.ot,fail_score:q.fr,verif_rate:q.vr,verif_total:q.vt,verif_ok:q.vs,gross:q.g,completed:q.cp,in_time:q.it,failed:q.f,city:q.ci||null,contract:q.co||null})})});
  });
  var ids=Object.keys(riders).filter(function(id){return !ros.some(function(r){return r.id===id})});
  return (ros.length?batches(ros,200).reduce(function(p,b){return p.then(function(){return sb.rpc("set_riders",{p_rows:b}).then(function(r){if(r.error)throw r.error})})},Promise.resolve()):Promise.resolve())
    .then(function(){return ids.length?batches(ids.map(function(id){return{id:id}}),500).reduce(function(p,b){return p.then(function(){return sb.from("riders").upsert(b,{onConflict:"id",ignoreDuplicates:true}).then(function(r){if(r.error)throw r.error})})},Promise.resolve()):null})
    .then(function(){var m=Object.keys(meta).map(function(k){return meta[k]});return m.length?upsertAll("riders",m.map(function(o){var r={id:o.id};if(o.vehicle)r.vehicle=o.vehicle;if(o.tga)r.tga=o.tga;return r}).filter(function(r){return r.vehicle&&r.tga}),"id"):null})
    .then(function(){return upsertAll("daily",daily.perf,"day,rider_id")})
    .then(function(){return upsertAll("daily",daily.dist,"day,rider_id")})
    .then(function(){return upsertAll("quality",qual,"month,rider_id")})
    .then(function(){return upsertAll("wallet",Object.keys(wal).map(function(k){return wal[k]}),"rider_id")})
    .then(function(){var now=new Date().toLocaleString("en-CA",{timeZone:"Asia/Riyadh",hour12:false}).slice(0,17).replace(",","");return sb.from("settings").upsert({key:"last_upload",value:now})});
}
function work(promise,okMsg){
  ui.busy=true;ui.msg="جارٍ الحفظ…";ui.msgOk=true;render();
  return promise.then(function(){return loadStaffData()}).then(function(){ui.busy=false;ui.msg=okMsg;ui.msgOk=true;render()})
  .catch(function(e){ui.busy=false;ui.msgOk=false;ui.msg="تعذّر الحفظ: "+((e&&e.message)||e);render()});
}
function riderErr(e){return e==="locked"?"محاولات كثيرة خاطئة. حاول بعد 15 دقيقة.":"رقم الإقامة أو الـ ID غير صحيح، أو لم يُسجَّل رقم إقامتك بعد."}

/* ---------- events ---------- */
root.addEventListener("click",function(e){
  var t=e.target.closest("button,a[data-su],[data-open],[data-sel],[data-cday]");if(!t)return;
  if(t.dataset.su!=null){e.preventDefault();ui0.signup=t.dataset.su==="1";ui.msg="";render();return}
  if(t.dataset.tab){view=t.dataset.tab;ui.msg="";ui.acc=null;ss("hs_view",view);render();window.scrollTo(0,0);return}
  if(t.dataset.open!=null){if(canSee("riders")){view="riders";ui.sel=t.dataset.open;render();window.scrollTo(0,0)}return}
  if(t.dataset.sel!=null){ui.sel=t.dataset.sel||null;render();return}
  if(t.dataset.cday){ui.cday=t.dataset.cday;if(t.dataset.cs)ui0.cs=t.dataset.cs;render();window.scrollTo(0,0);return}
  if(t.dataset.cs){ui0.cs=t.dataset.cs;render();window.scrollTo(0,0);return}
  if(t.dataset.who){ui0.who=t.dataset.who;ui.msg="";render();return}
  if(t.dataset.dmode){ui0.dmode=t.dataset.dmode;render();return}
  if(t.dataset.qm){ui0.qm=t.dataset.qm;render();return}
  if(t.id==="logout"){me=null;LAST=null;ss("hs_portal",null);ui.msg="";ui0.cs="home";data={company:data.company,couriers:{},days:{},staff:[]};render();return}
  if(t.id==="staffOut"){sb.auth.signOut().then(function(){location.reload()});return}
  if(t.id==="saveStaff"){var ch=ui.acc.filter(function(a){return JSON.stringify([a.n,a.r,a.p])!==a.o});
    work(ch.reduce(function(p,a){return p.then(function(){
      var q=a.r?sb.from("staff").upsert({user_id:a.id,name:a.n||a.e,role:a.r,perms:a.r==="staff"?a.p:[]},{onConflict:"user_id"}):sb.from("staff").delete().eq("user_id",a.id);
      return q.then(function(r){if(r.error)throw r.error})})},Promise.resolve()).then(function(){ui.acc=null}),"تم حفظ الصلاحيات.");return}
  if(t.dataset.newpw!=null){var ac=ui.acc[+t.dataset.newpw],npw=genPw();ui.busy=true;render();
    staffFn({action:"password",user_id:ac.id,password:npw}).then(function(){ui.busy=false;ui.cred="الرابط: "+siteUrl()+"\nاسم المستخدم: "+uname(ac.e)+"\nكلمة المرور: "+npw;ui.msg="";render()}).catch(function(e){ui.busy=false;ui.msgOk=false;ui.msg=staffErr(e);render()});return}
  if(t.id==="copyCred"){try{navigator.clipboard.writeText(ui.cred);t.textContent="تم النسخ"}catch(e){}return}
  if(t.id==="hideCred"){ui.cred=null;render();return}
  if(t.id==="cancelUp"){ui.upload=null;ui.msg="";render();return}
  if(t.id==="askReset"){ui.confirmReset=true;render();return}
  if(t.id==="noReset"){ui.confirmReset=false;render();return}
  if(t.id==="doReset"){ui.confirmReset=false;
    work(Promise.all([sb.from("daily").delete().gte("day","1900-01-01"),sb.from("quality").delete().neq("month",""),sb.from("wallet").delete().neq("rider_id","")]).then(function(rs){rs.forEach(function(r){if(r.error)throw r.error})}),"تم حذف بيانات الأداء. أسماء المناديب وأرقام الإقامة باقية.");return}
  if(t.id==="saveName"){var nm=document.getElementById("cname").value.trim();if(!nm)return;
    work(sb.from("settings").upsert({key:"company",value:nm}).then(function(r){if(r.error)throw r.error}),"تم حفظ الاسم.");return}
  if(t.id==="applyUp"){var up=ui.upload;if(!up||!up.length)return;var multi=up.filter(function(u){return u.type==="perf"&&u.multiDay});up=up.filter(function(u){return !(u.type==="perf"&&u.multiDay)});ui.upload=null;if(!up.length){ui.msgOk=false;ui.msg="لم يُحفظ شيء: تقرير الأداء يغطي أكثر من يوم. صدّره من هنقرستيشن ليوم واحد فقط ثم ارفعه مع اختيار نفس التاريخ.";render();return}work(applyUpload(up),multi.length?"تم حفظ باقي الملفات. تقرير الأداء لم يُحفظ لأنه يغطي أكثر من يوم، صدّره ليوم واحد.":"تم حفظ البيانات.");return}
  if(t.id==="saveRoster"){var ro=ui.roster;ui.roster=null;
    work(sb.rpc("set_riders",{p_rows:Object.keys(ro).map(function(id){return{id:id,name:ro[id].n||"",iqama:ro[id].iq}})}).then(function(r){if(r.error)throw r.error}),"تم حفظ أرقام الإقامة.");return}
});
root.addEventListener("input",function(e){var t=e.target;if(t.dataset.aname!=null){ui.acc[+t.dataset.aname].n=t.value;var b=document.getElementById("saveStaff");if(b)b.disabled=false}});
root.addEventListener("change",function(e){
  var t=e.target,f=F();
  if(t.id==="fFrom"){f.from=t.value>YEST?YEST:t.value;if(f.to<f.from)f.to=f.from;render()}
  if(t.id==="fTo"){f.to=t.value>YEST?YEST:t.value;if(f.from>f.to)f.from=f.to;render()}
  if(t.id==="fCity"){f.city=t.value;render()}
  if(t.id==="fCon"){f.con=t.value;render()}
  if(t.id==="fRid"){f.rid=t.value;render()}
  if(t.id==="cday"){ui.cday=t.value>YEST?YEST:t.value;render()}
  if(t.id==="dMon"){ui0.mon=t.value;ui0.dday=null;render()}
  if(t.id==="dDay"){ui0.dday=t.value;render()}
  if(t.dataset.arole!=null){var a=ui.acc[+t.dataset.arole];a.r=t.value;if(a.r==="staff"&&!a.p.length)a.p=["overall","daily"];render()}
  if(t.dataset.perm){var pr=t.dataset.perm.split("|"),s=ui.acc[+pr[0]],p=s.p=(s.p||[]).slice(),i=p.indexOf(pr[1]);if(t.checked&&i<0)p.push(pr[1]);if(!t.checked&&i>=0)p.splice(i,1);render()}
  if(t.id==="upDate"){ui.upDate=t.value>YEST?YEST:t.value}
  if(t.id==="qMon"){ui.qm=t.value;render()}
  if(t.id==="file"&&t.files.length){var fd=ui.upDate||YEST,fs=[].slice.call(t.files);ui.msg="جارٍ قراءة الملفات…";ui.msgOk=true;ui.upload=null;render();
    Promise.all(fs.map(function(f){return parseFile(f,fd).catch(function(err){return {file:f.name,error:err.message}})})).then(function(res){
      var ok=res.filter(function(u){return !u.error&&u.rows}),badF=res.filter(function(u){return u.error||!u.rows});
      ui.upload=ok.length?ok:null;ui.msgOk=false;
      ui.msg=badF.length?"لم أتعرف على: "+badF.map(function(u){return u.file+(u.error==="lib"?" (تعذّر تحميل قارئ Excel، جرّب CSV)":"")}).join("، ")+". تأكد أن الملف من تقرير 3PL Report ويحتوي على عمود Rider Id.":"";render()})}
});

root.addEventListener("submit",function(e){
  var id=e.target.id;if(id!=="loginF"&&id!=="staffF"&&id!=="addRider"&&id!=="addStaff")return;e.preventDefault();
  if(id==="addStaff"){var sn=document.getElementById("sn").value.trim(),su=document.getElementById("su").value.trim().toLowerCase(),sp=document.getElementById("sp").value;
    ui.busy=true;ui.msg="";render();
    staffFn({action:"create",name:sn,username:su,password:sp,perms:["overall","daily"]}).then(function(){ui.busy=false;ui.genpw=null;ui.acc=null;ui.msgOk=true;ui.msg="أُضيف الموظف بقسمي النظرة العامة والأداء اليومي. عدّل أقسامه من الجدول إن أردت.";
      ui.cred="الرابط: "+siteUrl()+"\nاسم المستخدم: "+su+"\nكلمة المرور: "+sp;render()}).catch(function(e){ui.busy=false;ui.msgOk=false;ui.msg=staffErr(e);render()});return}
  if(id==="loginF"){
    var iq=digits(document.getElementById("iq").value).trim(),cid=digits(document.getElementById("cid").value).trim();
    ui.busy=true;ui.msg="";
    sb.rpc("rider_portal",{p_id:cid,p_iqama:iq}).then(function(r){ui.busy=false;
      if(r.error){ui.msg="تعذّر الاتصال، حاول مرة أخرى.";render();return}
      if(r.data.error){ui.msg=riderErr(r.data.error);render();return}
      me=cid;portalToData(r.data);ui.msg="";ui0.cs="home";ui.cday=null;render()});
  }
  if(id==="staffF"){
    var em=document.getElementById("lu").value.trim().toLowerCase();if(em.indexOf("@")<0)em=em+"@"+STAFF_DOMAIN;var _x=0,pw=document.getElementById("lp").value,nmEl=document.getElementById("ln"),nm=nmEl&&nmEl.value.trim();
    ui.busy=true;ui.msg="";render();
    var p=ui0.signup?sb.auth.signUp({email:em,password:pw,options:{data:{name:nm},emailRedirectTo:location.origin+location.pathname}}):sb.auth.signInWithPassword({email:em,password:pw});
    p.then(function(r){
      if(r.error){ui.busy=false;ui.msgOk=false;ui.msg=/invalid login/i.test(r.error.message)?"اسم المستخدم أو كلمة المرور غير صحيحة.":/not confirmed/i.test(r.error.message)?"فعّل حسابك من الرسالة التي وصلت بريدك أولاً.":/registered/i.test(r.error.message)?"هذا البريد مسجّل من قبل. اختر تسجيل الدخول.":r.error.message;render();return}
      if(!r.data.session){ui.busy=false;ui.msgOk=true;ui0.signup=false;ui.msg="تم إنشاء الحساب. افتح الرسالة التي وصلت بريدك لتفعيله، ثم سجّل الدخول.";render();return}
      return enterStaff(r.data.user,nm).then(function(){ui.busy=false;if(isAdmin||staff)ui.msg="";render()});
    }).catch(function(err){ui.busy=false;ui.msgOk=false;ui.msg="تعذّر الدخول: "+(err.message||err);render()});
  }
  if(id==="addRider"){var rid=digits(document.getElementById("rid").value).trim(),riq=digits(document.getElementById("riq").value).trim();if(!rid||!riq)return;
    ui.roster=ui.roster||{};ui.roster[rid]={iq:riq,n:document.getElementById("rname").value.trim()};ui.msg="";render();return}
});

/* ---------- boot ---------- */
sb.from("settings").select("value").eq("key","company").maybeSingle().then(function(r){if(r.data&&r.data.value)data.company=r.data.value}).catch(function(){})
.then(function(){
  if(RIDER_ONLY)return null;
  return sb.auth.getSession().then(function(r){var s=r.data&&r.data.session;return s?enterStaff(s.user):null});
}).then(function(){
  ss("hs_portal",null);
}).catch(function(e){ui.msg="تعذّر الاتصال بقاعدة البيانات.";ui.msgOk=false}).then(function(){booting=false;render()});
})();
'''
parse=rep(parse,'var XLSX_URL','var XLSX_URL_X') if 'var XLSX_URL' in parse else parse
js=head+views+parse+'function loadXLSX(){return window.XLSX?Promise.resolve(window.XLSX):new Promise(function(ok,no){var s=document.createElement("script");s.src=XLSX_URL;s.onload=function(){ok(window.XLSX)};s.onerror=function(){no(new Error("lib"))};document.head.appendChild(s)})}\nfunction parseFile(file,fallbackDate){\n  return loadXLSX().then(function(X){return file.arrayBuffer().then(function(buf){\n    var wb=X.read(buf,{type:"array",cellDates:true}),ws=wb.Sheets[wb.SheetNames[0]];\n    var res=parseRows(X.utils.sheet_to_json(ws,{header:1,raw:true,defval:""}),fallbackDate);res.file=file.name;return res})});\n}\n'+tail
# ---- courier statement (كشف الحساب) + WhatsApp ----
js=rep(js,'if(res.rider&&res.rider.name)c.n=res.rider.name;','if(res.rider&&res.rider.name)c.n=res.rider.name;if(res.rider&&res.rider.phone)c.ph=res.rider.phone;')
js=rep(js,'"هذا الشهر حتى أمس")+\'</div>\'+','"هذا الشهر حتى أمس")+(function(){var st=stmtCalc(id);return st?tile("stmt","كشف الحساب",money(st.total),"مستحقات "+monLabel(st.mon)):""})()+\'</div>\'+')
js=rep(js,'  if(cs==="wallet"){',r'''  if(cs==="stmt"){var st=stmtCalc(id);if(!st)return head+'<section class="panel"><p class="hint">لا توجد بيانات لهذا الشهر بعد.</p></section>';
    var ph=data.couriers[id]&&data.couriers[id].ph,wa=ph?"https://wa.me/"+ph+"?text="+encodeURIComponent(stmtText(id,st)):"";
    return head+'<section class="panel stmt"><h2>كشف حساب المندوب</h2>'+stmtMonSel(id,st.mon)+stmtTable(id,st)+
      '<div class="row noprint" style="margin-top:14px">'+(wa?'<a class="btn pri" style="text-decoration:none" href="'+wa+'" target="_blank" rel="noopener">إرسال على واتساب</a>':'<span class="hint">لا يوجد رقم جوال مسجل لك. اطلب من الإدارة إضافته.</span>')+
      '<button class="btn" id="stmtHtml">تنزيل صفحة ويب</button><button class="btn" id="stmtPrint">طباعة / PDF</button></div>'+
      (ph?'<p class="hint noprint">يُرسل إلى الرقم المسجل: <span class="num" dir="ltr">+'+esc(ph)+'</span></p>':'')+'</section>';}
  if(cs==="wallet"){''')
js=rep(js,'function tile(cs,label,val,sub){',r'''var RATE_ORDER=8,RATE_KM=1.15,QRATE={A:2.75,B:2.25,C:1.75,D:1.25,E:0.75,F:0};
function stmtCalc(id){var ld=lastDay();if(!ld)return null;var mon=ld.slice(0,7),ds=days().filter(function(d){return d.slice(0,7)===mon&&data.days[d][id]});if(!ds.length)return null;
  var o=0,km=0;ds.forEach(function(d){var x=data.days[d][id];o+=+x[CP]||0;km+=+x[DP]||0});
  var qx=data.couriers[id]&&data.couriers[id].q,seg=qx&&qx[mon]&&String(qx[mon].s||"").trim().toUpperCase(),qr=seg&&QRATE[seg]!=null?QRATE[seg]:0;
  var r2=function(v){return Math.round(v*100)/100},a=r2(o*RATE_ORDER),b=r2(km*RATE_KM),c=r2(o*qr);
  return {mon:mon,from:ds[0],to:ds[ds.length-1],n:ds.length,orders:o,km:r2(km),seg:seg||"",qr:qr,a:a,b:b,c:c,total:r2(a+b+c)}}
function f2(v){return fmt(v,2)}
function stmtTable(id,st){
  return '<p class="hint" style="margin:0 0 10px"><b>'+esc(cname(id))+'</b> · ID <span class="num">'+esc(id)+'</span><br>الفترة من <span class="num">'+st.from+'</span> إلى <span class="num">'+st.to+'</span> ('+N(st.n,0)+' يوم)</p>'+
  '<div class="tbl" style="box-shadow:none"><table><thead><tr><th>البند</th><th>المبلغ</th></tr></thead><tbody>'+
  sRow('الطلبات المكتملة',N(st.orders,0)+' طلب × '+f2(RATE_ORDER),st.a)+
  sRow('المسافة المستحقة (Payable KM)',fmt(st.km,2)+' كم × '+f2(RATE_KM),st.b)+
  sRow('جودة التوصيل '+(st.seg?segPill(st.seg):''),st.seg?N(st.orders,0)+' طلب × '+f2(st.qr):'التصنيف غير متوفر لهذا الشهر',st.c)+
  '<tr><td style="text-align:right"><b>الإجمالي</b></td><td><b>'+money(st.total)+'</b></td></tr></tbody></table></div>'}
function sRow(l,d,v){return '<tr><td style="text-align:right;white-space:normal">'+l+'<br><span class="hint" style="font-size:12px">'+d+'</span></td><td style="white-space:nowrap">'+money(v)+'</td></tr>'}
function stmtText(id,st){return ["كشف حساب المندوب - "+(data.company||""),"الاسم: "+cname(id),"ID: "+id,"الفترة: "+st.from+" إلى "+st.to,"",
  "الطلبات: "+st.orders+" × "+RATE_ORDER+" = "+st.a.toFixed(2)+" ريال","المسافة المستحقة: "+st.km.toFixed(2)+" كم × "+RATE_KM+" = "+st.b.toFixed(2)+" ريال",
  "جودة التوصيل ("+(st.seg||"-")+"): "+st.orders+" × "+st.qr+" = "+st.c.toFixed(2)+" ريال","","الإجمالي: "+st.total.toFixed(2)+" ريال"].join("\n")}
function stmtDownload(id){var st=stmtCalc(id);if(!st)return;var cssT=(document.querySelector("style")||{}).textContent||"";
  var h='<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>كشف حساب '+esc(id)+'</title><style>'+cssT+'body{padding:16px;background:#fff}</style></head><body><section class="panel stmt"><h2>'+esc(data.company||"")+'</h2><h2>كشف حساب المندوب</h2>'+stmtTable(id,st)+'</section></body></html>';
  var a=document.createElement("a");a.href=URL.createObjectURL(new Blob([h],{type:"text/html"}));a.download="kashf-"+id+"-"+st.to+".html";document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove()},1000)}
function tile(cs,label,val,sub){''')
js=rep(js,'if(t.id==="logout"){',' if(t.id==="stmtHtml"){stmtDownload(me);return}\n  if(t.id==="stmtPrint"){document.body.classList.add("pst");window.print();setTimeout(function(){document.body.classList.remove("pst")},500);return}\n  if(t.id==="logout"){')
# statement: month picker + manager access from courier detail
js=rep(js,'function stmtCalc(id){var ld=lastDay();if(!ld)return null;var mon=ld.slice(0,7),ds=','''var SMON="";
function stmtMonths(id){var m={};days().forEach(function(d){if(data.days[d][id])m[d.slice(0,7)]=1});return Object.keys(m).sort().reverse()}
function stmtMonSel(id,cur){var ms=stmtMonths(id);if(ms.length<2)return "";return '<label class="fcard noprint" style="max-width:220px;margin-bottom:10px"><span>الشهر</span><select id="stmtMon">'+ms.map(function(m){return '<option value="'+m+'"'+(m===cur?" selected":"")+'>'+m+'</option>'}).join("")+'</select></label>'}
function stmtWa(id,st){var ph=data.couriers[id]&&data.couriers[id].ph;return ph?"https://wa.me/"+ph+"?text="+encodeURIComponent(stmtText(id,st)):""}
function stmtPanel(id){var st=stmtCalc(id);if(!st)return "";var wa=stmtWa(id,st),ph=data.couriers[id]&&data.couriers[id].ph;
  return '<section class="panel stmt"><h2>كشف حساب المندوب</h2>'+stmtMonSel(id,st.mon)+stmtTable(id,st)+
    '<div class="row noprint" style="margin-top:14px">'+(wa?'<a class="btn pri" style="text-decoration:none" href="'+wa+'" target="_blank" rel="noopener">إرسال على واتساب</a>':'<span class="hint">لا يوجد رقم جوال مسجل لهذا المندوب.</span>')+
    '<button class="btn" data-sdl="'+esc(id)+'">تنزيل صفحة ويب</button><button class="btn" id="stmtPrint">طباعة / PDF</button></div>'+
    (ph?'<p class="hint noprint">يُرسل إلى: <span class="num" dir="ltr">+'+esc(ph)+'</span></p>':'')+'</section>'}
function stmtCalc(id){var ld=lastDay();if(!ld)return null;var ms=stmtMonths(id),mon=SMON&&ms.indexOf(SMON)>=0?SMON:ld.slice(0,7),ds=''')
js=rep(js,'''+bars(ser,{h:170,label:"الطلبات المكتملة يومياً"})+'</section>';}''','''+bars(ser,{h:170,label:"الطلبات المكتملة يومياً"})+'</section>'+stmtPanel(id);}''')
js=rep(js,'if(t.id==="qMon"){ui.qm=t.value;render()}','if(t.id==="qMon"){ui.qm=t.value;render()}\n  if(t.id==="stmtMon"){SMON=t.value;render()}')
js=rep(js,' if(t.id==="stmtHtml"){stmtDownload(me);return}',' if(t.id==="stmtHtml"){stmtDownload(me);return}\n  if(t.dataset.sdl){stmtDownload(t.dataset.sdl);return}')
js=rep(js,'all("riders","id,name,vehicle,tga","id").then(function(rs){rs.forEach(function(r){var c=C(r.id);if(r.name)c.n=r.name;','all("riders","id,name,vehicle,tga,phone","id").then(function(rs){rs.forEach(function(r){var c=C(r.id);if(r.name)c.n=r.name;if(r.phone)c.ph=r.phone;')
# visible statement buttons (tile alone was not recognised as a button)
js=rep(js,'''<div class="row">'+(cs!=="home"?'<button class="btn" data-cs="home">الرجوع للقائمة</button>':"")+''','''<div class="row">'+(cs!=="stmt"?'<button class="btn pri" data-cs="stmt">تصدير كشف الحساب</button>':"")+(cs!=="home"?'<button class="btn" data-cs="home">الرجوع للقائمة</button>':"")+''')
js=rep(js,'''<td>'+N(a.di,1)+'</td><td><span class="pill '+s[0]+'">'+s[1]+'</span></td></tr>\'''','''<td>'+N(a.di,1)+'</td><td><span class="pill '+s[0]+'">'+s[1]+'</span></td><td><button class="btn" style="padding:4px 10px;font-size:12.5px;white-space:nowrap" data-stmt="'+esc(a.id)+'">كشف الحساب</button></td></tr>\'''')
js=rep(js,'<th>الحالة</th></tr></thead>','<th>الحالة</th><th>كشف الحساب</th></tr></thead>')
js=rep(js,'colspan="17">لا توجد بيانات في هذه الفترة.','colspan="18">لا توجد بيانات في هذه الفترة.')
js=rep(js,'  if(t.dataset.sel!=null){','  if(t.dataset.stmt){ui.sel=t.dataset.stmt;render();var se=document.querySelector(".stmt");if(se)se.scrollIntoView({behavior:"smooth",block:"start"});return}\n  if(t.dataset.sel!=null){')
js=rep(js,'''det='<section class="panel"><div class="who"><div><b>'+esc(cname(id))+'</b> <span class="num" style="color:var(--muted)">#'+esc(id)+'</span></div><button class="btn" data-sel="">إغلاق</button></div>'+''','''det='<section class="panel"><div class="who"><div><b>'+esc(cname(id))+'</b> <span class="num" style="color:var(--muted)">#'+esc(id)+'</span></div><div class="row"><button class="btn pri" data-stmt="'+esc(id)+'">تصدير كشف الحساب</button><button class="btn" data-sel="">إغلاق</button></div></div>'+''')
# WhatsApp: open the installed app / the same WhatsApp Web tab directly, no wa.me landing page
js=rep(js,'''(wa?'<a class="btn pri" style="text-decoration:none" href="'+wa+'" target="_blank" rel="noopener">إرسال على واتساب</a>':''','''(wa?waLinks(ph,stmtText(id,st)):''',2)
js=rep(js,'function stmtCalc(id){','''var IS_MOBILE=/Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent);
function waLinks(ph,txt){var q="phone="+ph+"&text="+encodeURIComponent(txt),st=' style="text-decoration:none"';
  var app='<a class="btn pri"'+st+' href="whatsapp://send?'+q+'">'+(IS_MOBILE?'إرسال على واتساب':'إرسال عبر تطبيق واتساب')+'</a>';
  return IS_MOBILE?app:app+'<a class="btn"'+st+' href="https://web.whatsapp.com/send?'+q+'" target="waweb" rel="noopener">إرسال عبر واتساب ويب</a>'}
function stmtCalc(id){''')
# statement toolbar (month + export at top-left) and a styled standalone statement page for download/PDF
js=rep(js,'''<section class="panel stmt"><h2>كشف حساب المندوب</h2>'+stmtMonSel(id,st.mon)+''','''<section class="panel stmt">'+stmtHead(id,st.mon)+''',2)
js=rep(js,'''<button class="btn" id="stmtHtml">تنزيل صفحة ويب</button><button class="btn" id="stmtPrint">طباعة / PDF</button></div>''','''</div>''')
js=rep(js,'''<button class="btn" data-sdl="'+esc(id)+'">تنزيل صفحة ويب</button><button class="btn" id="stmtPrint">طباعة / PDF</button></div>''','''</div>''')
js=rep(js,'function stmtDownload(id){var st=stmtCalc(id);if(!st)return;var cssT=','function stmtDownloadOld(id){var st=stmtCalc(id);if(!st)return;var cssT=')
js=rep(js,'  if(t.dataset.sdl){stmtDownload(t.dataset.sdl);return}','  if(t.dataset.sdl){stmtDownload(t.dataset.sdl);return}\n  if(t.dataset.sp){stmtPrint(t.dataset.sp);return}')
js=rep(js,'function stmtCalc(id){',r'''function monTxt(m){var M=["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"];return M[+m.slice(5,7)-1]+" "+m.slice(0,4)}
function stmtHead(id,cur){var ms=stmtMonths(id);
  return '<div class="stmthead"><h2>كشف حساب المندوب</h2><div class="stmttools noprint"><select id="stmtMon" aria-label="الشهر">'+ms.map(function(m){return '<option value="'+m+'"'+(m===cur?" selected":"")+'>'+monTxt(m)+'</option>'}).join("")+'</select>'+
    '<button class="btn pri" data-sp="'+esc(id)+'">تصدير PDF</button><button class="btn" data-sdl="'+esc(id)+'">صفحة ويب</button></div></div>'}
function n2(v){return '<span dir="ltr">'+Number(v||0).toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2})+'</span>'}
function n0(v){return '<span dir="ltr">'+Number(v||0).toLocaleString("en-US")+'</span>'}
function stmtDoc(id,st){
  var SC={A:"#2b7a4b",B:"#3f9a62",C:"#d99a0b",D:"#e07b28",E:"#c4472f",F:"#8f2d22"},seg=st.seg?'<span class="seg" style="background:'+(SC[st.seg]||"#777")+'">'+esc(st.seg)+'</span>':'—';
  var d=new Date(),today=d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");
  var row=function(c,l,q,r,v){return '<tr class="'+c+'"><td>'+l+'</td><td>'+q+'</td><td>'+r+'</td><td class="amt">'+n2(v)+'</td></tr>'};
  var css='@page{size:A4;margin:10mm}*{box-sizing:border-box}body{margin:0;background:#f3efe9;color:#2b1a14;font:14px/1.45 "IBM Plex Sans Arabic",system-ui,-apple-system,"Segoe UI",Tahoma,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}'+
    '.sheet{max-width:720px;margin:16px auto;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 2px 12px rgba(60,30,20,.10)}'+
    '.top{background:#5a2a1d;color:#fff;padding:12px 18px;display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}.top h1{margin:0;font-size:18px}.top .co{font-size:12.5px;color:#f3dcc9}.mon{background:#f5b51f;color:#5a2a1d;font-weight:700;padding:3px 12px;border-radius:999px;font-size:13px;white-space:nowrap}'+
    '.band{height:4px;background:#16b1e2}.info{display:grid;grid-template-columns:repeat(4,1fr);background:#f7fbfd;border-bottom:1px solid #e3eef3}.info div{padding:8px 14px;border-inline-start:1px solid #e3eef3}.info div:first-child{border:0}.info>div>span{display:block;font-size:11px;color:#6f8791}.info b{font-size:14px}'+
    'table{width:100%;border-collapse:collapse}th{background:#16b1e2;color:#fff;font-size:12.5px;font-weight:600;padding:7px 12px;text-align:right}td{padding:9px 12px;border-bottom:1px solid #f0e9e3}th:last-child,td.amt{text-align:left;white-space:nowrap}td.amt{font-weight:600}'+
    'tr.r1 td:first-child{border-inline-start:4px solid #16b1e2}tr.r2 td:first-child{border-inline-start:4px solid #5a2a1d}tr.r3 td:first-child{border-inline-start:4px solid #f5b51f}'+
    'tr.tot td{background:#fff6dc;font-weight:700;font-size:17px;border-top:2px solid #f5b51f;border-bottom:0}tr.tot td.amt{color:#5a2a1d}'+
    '.seg{display:inline-block;min-width:22px;text-align:center;padding:0 8px;border-radius:999px;color:#fff;font-weight:700;font-size:12.5px}'+
    '.foot{padding:8px 14px;font-size:11px;color:#8a7a72;display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;border-top:1px solid #f0e9e3}'+
    '@media print{body{background:#fff}.sheet{box-shadow:none;margin:0;max-width:none;border-radius:0}}@media(max-width:560px){.info{grid-template-columns:1fr 1fr}.info div:nth-child(3){border:0}th,td{padding:7px 8px}}';
  return '<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>كشف حساب '+esc(cname(id))+' - '+monTxt(st.mon)+'</title>'+
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;600;700&display=swap"><style>'+css+'</style></head><body><div class="sheet">'+
    '<div class="top"><div><h1>كشف حساب المندوب</h1><div class="co">'+esc(data.company||"")+'</div></div><span class="mon">'+monTxt(st.mon)+'</span></div><div class="band"></div>'+
    '<div class="info"><div><span>المندوب</span><b>'+esc(cname(id))+'</b></div><div><span>رقم ID</span><b dir="ltr">'+esc(id)+'</b></div><div><span>الفترة</span><b dir="ltr">'+st.from.slice(5)+' → '+st.to.slice(5)+'</b> <small>('+st.n+' يوم)</small></div><div><span>تصنيف الجودة</span><b>'+seg+'</b></div></div>'+
    '<table><thead><tr><th>البند</th><th>الكمية</th><th>السعر</th><th>المبلغ (ر.س)</th></tr></thead><tbody>'+
    row("r1","الطلبات المكتملة",n0(st.orders)+' طلب',n2(RATE_ORDER),st.a)+
    row("r2","المسافة المستحقة <small>Payable KM</small>",n2(st.km)+' كم',n2(RATE_KM),st.b)+
    row("r3","جودة التوصيل "+seg,n0(st.orders)+' طلب',st.seg?n2(st.qr):'—',st.c)+
    '<tr class="tot"><td colspan="3">الإجمالي المستحق</td><td class="amt">'+n2(st.total)+'</td></tr></tbody></table>'+
    '<div class="foot"><span>تاريخ الإصدار: <span dir="ltr">'+today+'</span></span><span>'+esc(data.company||"")+'</span></div></div></body></html>'}
function stmtDownload(id){var st=stmtCalc(id);if(!st)return;
  var a=document.createElement("a");a.href=URL.createObjectURL(new Blob([stmtDoc(id,st)],{type:"text/html"}));a.download="kashf-"+id+"-"+st.mon+".html";document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove()},1000)}
function stmtPrint(id){var st=stmtCalc(id);if(!st)return;var f=document.createElement("iframe");f.style.cssText="position:fixed;right:0;bottom:0;width:0;height:0;border:0";document.body.appendChild(f);
  f.onload=function(){setTimeout(function(){try{f.contentWindow.focus();f.contentWindow.print()}catch(e){window.print()}setTimeout(function(){f.remove()},2000)},400)};f.srcdoc=stmtDoc(id,st)}
function stmtCalc(id){''')
css+='\n.stmthead{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:12px}.stmthead h2{margin:0}.stmttools{display:flex;gap:6px;align-items:center;flex-wrap:wrap}.stmttools select{font:inherit;padding:7px 10px;border:1px solid var(--line,#ddd);border-radius:6px;background:var(--card,#fff);color:inherit}\n'
# rider category (فئة): statement only for ب and خ; أ = target-based riders get a message
js=rep(js,'if(res.rider&&res.rider.phone)c.ph=res.rider.phone;','if(res.rider&&res.rider.phone)c.ph=res.rider.phone;if(res.rider&&res.rider.category)c.cat=res.rider.category;')
js=rep(js,'all("riders","id,name,vehicle,tga,phone","id").then(function(rs){rs.forEach(function(r){var c=C(r.id);if(r.name)c.n=r.name;if(r.phone)c.ph=r.phone;','all("riders","id,name,vehicle,tga,phone,category","id").then(function(rs){rs.forEach(function(r){var c=C(r.id);if(r.name)c.n=r.name;if(r.phone)c.ph=r.phone;if(r.category)c.cat=r.category;')
js=rep(js,'function stmtCalc(id){','''function normCat(v){var s=String(v||"").trim().replace(/[إآا]/g,"أ");return s==="أ"||s.toUpperCase()==="A"?"أ":s==="ب"||s.toUpperCase()==="B"?"ب":s==="خ"?"خ":s}
function stmtBlock(id){var c=data.couriers[id]&&data.couriers[id].cat;if(c==="ب"||c==="خ")return "";
  return c==="أ"?"لا يوجد كشف حساب للمناديب العاملين بالتارقت.":"لا يوجد كشف حساب لهذا المندوب لأن فئته غير محددة في شيت المناديب."}
function stmtBlockedHtml(id,m){return '<section class="panel stmt"><h2>كشف حساب المندوب</h2><div class="note" style="margin:8px 0 0;padding:12px 14px;border-radius:8px;background:#fff6dc;border-inline-start:4px solid #f5b51f;color:#5a2a1d;font-weight:600">'+esc(m)+'</div></section>'}
function stmtCalc(id){''')
js=rep(js,'  if(cs==="stmt"){var st=stmtCalc(id);','  if(cs==="stmt"){var sb0=stmtBlock(id);if(sb0)return head+stmtBlockedHtml(id,sb0);var st=stmtCalc(id);')
js=rep(js,'function stmtPanel(id){var st=stmtCalc(id);','function stmtPanel(id){var sb0=stmtBlock(id);if(sb0)return stmtBlockedHtml(id,sb0);var st=stmtCalc(id);')
js=rep(js,'(function(){var st=stmtCalc(id);return st?tile(','(function(){var st=!stmtBlock(id)&&stmtCalc(id);return st?tile(')
js=rep(js,'function stmtDownload(id){var st=stmtCalc(id);','function stmtDownload(id){var st=!stmtBlock(id)&&stmtCalc(id);')
js=rep(js,'function stmtPrint(id){var st=stmtCalc(id);','function stmtPrint(id){var st=!stmtBlock(id)&&stmtCalc(id);')
# WhatsApp send moves to the top toolbar; desktop uses one reusable WhatsApp Web tab
js=rep(js,'''
    '<div class="row noprint" style="margin-top:14px">'+(wa?waLinks(ph,stmtText(id,st)):'<span class="hint">لا يوجد رقم جوال مسجل لهذا المندوب.</span>')+
    '</div>'+
    (ph?''','''
    (ph?''')
js=rep(js,'''
      '<div class="row noprint" style="margin-top:14px">'+(wa?waLinks(ph,stmtText(id,st)):'<span class="hint">لا يوجد رقم جوال مسجل لك. اطلب من الإدارة إضافته.</span>')+
      '</div>'+
      (ph?''','''
      (ph?''')
js=rep(js,'''"'</select>'+\n    '<button class="btn pri" data-sp="'+esc(id)+'">تصدير PDF</button>''' if False else ''''</select>'+
    '<button class="btn pri" data-sp="'+esc(id)+'">تصدير PDF</button>''',''''</select>'+stmtWaBtn(id)+
    '<button class="btn pri" data-sp="'+esc(id)+'">تصدير PDF</button>''')
js=rep(js,'function stmtHead(id,cur){','''function stmtWaBtn(id){var ph=data.couriers[id]&&data.couriers[id].ph,st=stmtCalc(id);
  if(!ph||!st)return '<span class="hint" style="font-size:12.5px">لا يوجد رقم جوال مسجل</span>';
  var q="phone="+ph+"&text="+encodeURIComponent(stmtText(id,st));
  return IS_MOBILE?'<a class="btn wa" style="text-decoration:none" href="whatsapp://send?'+q+'">واتساب</a>':'<button class="btn wa" data-waweb="'+esc("https://web.whatsapp.com/send?"+q)+'" title="+'+esc(ph)+'">واتساب ويب</button>'}
function stmtHead(id,cur){''')
js=rep(js,'  if(t.dataset.sp){stmtPrint(t.dataset.sp);return}','''  if(t.dataset.sp){stmtPrint(t.dataset.sp);return}
  if(t.dataset.waweb){var w=window.open(t.dataset.waweb,WA_TAB);if(w)w.focus();return}''')
js=rep(js,'var IS_MOBILE=','var WA_TAB="hs_whatsapp_web";var IS_MOBILE=')
css+='\n.btn.wa{background:#25d366;border-color:#25d366;color:#fff}.btn.wa:hover{background:#1ebe5b}\n'
# roster phone column
js=rep(js,'iq:col(h,function(x){return /iqama|residency|الإقامة|الاقامة|هوية/.test(x)})};','iq:col(h,function(x){return /iqama|residency|الإقامة|الاقامة|هوية/.test(x)}),ph:col(h,function(x){return /جوال|جـوال|phone|mobile|الهاتف/.test(x.replace(/ـ/g,""))})};')
js=rep(js,'if(C.iq>=0&&String(r[C.iq]).trim())p.iq=digits(r[C.iq]).trim().replace(/\\.0$/,"");','if(C.iq>=0&&String(r[C.iq]).trim())p.iq=digits(r[C.iq]).trim().replace(/\\.0$/,"");if(C.ph>=0&&String(r[C.ph]).trim())p.ph=normPh(r[C.ph]);')
js=rep(js,'ros.push({id:id,name:b.n||"",iqama:iq})','ros.push({id:id,name:b.n||"",iqama:iq,phone:b.ph||""})')
js=rep(js,'function parseRows(rows,fallbackDate){','function normPh(v){var s=digits(v).trim().replace(/\\.0$/,"").replace(/\\D/g,"");if(s.slice(0,3)==="966")s=s.slice(3);s=s.replace(/^0+/,"");return /^5\\d{8}$/.test(s)?"966"+s:""}\nfunction parseRows(rows,fallbackDate){')
js=rep(js,'ph:col(h,function(x){return /جوال|جـوال|phone|mobile|الهاتف/.test(x.replace(/ـ/g,""))})','ph:col(h,function(x){return /جوال|جـوال|phone|mobile|الهاتف/.test(x.replace(/ـ/g,""))}),cat:col(h,function(x){return /^(فئ|الفئ|category)/i.test(String(x).trim())})')
js=rep(js,'if(C.ph>=0&&String(r[C.ph]).trim())p.ph=normPh(r[C.ph]);','if(C.ph>=0&&String(r[C.ph]).trim())p.ph=normPh(r[C.ph]);if(C.cat>=0&&String(r[C.cat]).trim())p.cat=normCat(r[C.cat]);')
js=rep(js,'ros.push({id:id,name:b.n||"",iqama:iq,phone:b.ph||""})','ros.push({id:id,name:b.n||"",iqama:iq,phone:b.ph||"",category:b.cat||""})')
css+='\n@media print{body.pst .panel:not(.stmt),body.pst #root>*>.tbl,body.pst .tbl:not(.stmt .tbl),body.pst .filters,body.pst .fhint,body.pst .bar,body.pst .coband{display:none!important}}'
css+='\n@media print{.side,.top,.noprint,.who .row,.tiles{display:none!important}.panel{box-shadow:none;border:0}body{background:#fff}}\n'
css=css.replace('.side button{','.side button,.side .navlink{').replace('.side button small{','.side button small,.side .navlink small{').replace('.side button:hover{','.side button:hover,.side .navlink:hover{')
css+='\n.side .navlink{text-decoration:none;color:inherit}\n'
exec(open('sheet_block.py',encoding='utf8').read())
exec(open('month_block.py',encoding='utf8').read())
exec(open('rules_block.py',encoding='utf8').read())
exec(open('pdf_block.py',encoding='utf8').read())
exec(open('fuel_block.py',encoding='utf8').read())
exec(open('qual_block.py',encoding='utf8').read())
exec(open('card_block.py',encoding='utf8').read())
exec(open('add_block.py',encoding='utf8').read())
exec(open('hidekm_block.py',encoding='utf8').read())
exec(open('menu_block.py',encoding='utf8').read())
exec(open('perm_block.py',encoding='utf8').read())
exec(open('wallet_block.py',encoding='utf8').read())
exec(open('rider_block.py',encoding='utf8').read())
exec(open('noiq_block.py',encoding='utf8').read())
exec(open('backup_block.py',encoding='utf8').read())
exec(open('range_block.py',encoding='utf8').read())
exec(open('catcol_block.py',encoding='utf8').read())
exec(open('ec_block.py',encoding='utf8').read())
exec(open('i18n_block.py',encoding='utf8').read())
# theme v2 (2026-10-10, fadhel asked for a new palette): deep teal + amber
_L_OLD="""  --bg:#f2f2f2; --surface:#ffffff; --sunk:#f6f6f4; --fg:#1d1f24; --muted:#636873; --line:#e1e1de;
  --bar:#16b1e2; --bar-fg:#5a2a1d; --head:#5c2d21; --head-fg:#ffffff; --menu-sel:#cdd3df;
  --hint:#e2541b; --accent:#16b1e2; --gold:#f5b51f; --cofg:#5c2d21;"""
_L_NEW="""  --bg:#f3f6f7; --surface:#ffffff; --sunk:#eef3f4; --fg:#13232b; --muted:#5b6b75; --line:#dbe4e7;
  --bar:#e3f2f0; --bar-fg:#0d3b47; --head:#0d3b47; --head-fg:#ffffff; --menu-sel:#d3ebe7;
  --hint:#c2561a; --accent:#14968a; --gold:#e8a33d; --cofg:#0d3b47;"""
_D_OLD="""  --bg:#121417; --surface:#1b1e23; --sunk:#16191d; --fg:#e8e9ec; --muted:#9aa0ab; --line:#2c3037;
  --bar:#0f7fa3; --bar-fg:#fff3e6; --head:#6b3829; --head-fg:#fff6ee; --menu-sel:#2f3746;
  --hint:#ff8a57; --accent:#3cc4ef; --gold:#ffc23d; --cofg:#ffc23d;"""
_D_NEW="""  --bg:#0e1518; --surface:#162026; --sunk:#121b20; --fg:#e4edf0; --muted:#92a3ac; --line:#25323a;
  --bar:#12343c; --bar-fg:#bfe9e3; --head:#0b333e; --head-fg:#f1fbf9; --menu-sel:#1d3a40;
  --hint:#ff9a5c; --accent:#3cc2b3; --gold:#f0b860; --cofg:#f0b860;"""
assert css.count(_L_OLD)==1 and css.count(_D_OLD)==2,(css.count(_L_OLD),css.count(_D_OLD))
css=css.replace(_L_OLD,_L_NEW).replace(_D_OLD,_D_NEW)
for _a,_b in (("#5a2a1d","#0d3b47"),("#16b1e2","#14968a"),("#f5b51f","#e8a33d"),("#fff6dc","#fdf3e1"),("#f3dcc9","#cfe9e5"),("#f3efe9","#eef3f4"),("#f0e9e3","#e6edef"),("#8a7a72","#6b7b84"),("#2b1a14","#13232b")):
    js=js.replace(_a,_b);css=css.replace(_a,_b)
css=css.replace("border-top:3px solid var(--bar)","border-top:3px solid var(--accent)").replace(".meter i{display:block;height:10px;background:var(--bar)",".meter i{display:block;height:10px;background:var(--accent)")
js=js.replace("fill=\"'+(last?'var(--head)':'var(--bar)')+'\"","fill=\"'+(last?'var(--head)':'var(--accent)')+'\"")
# wording: "كشف الحساب" renamed to "ملخص أداء المندوب" (fadhel 2026-10-10)
for _a,_b in (("تصدير كشف الحساب","تصدير ملخص الأداء"),("كشف حساب المندوب","ملخص أداء المندوب"),("لا يوجد كشف حساب","لا يوجد ملخص أداء"),("كشف حساب ","ملخص أداء "),("كشف الحساب","ملخص الأداء"),('"kashf-"','"performance-"')):
    js=js.replace(_a,_b)
exec(open('finhide_block.py',encoding='utf8').read())
css+='''
body{padding-bottom:34px}
.side{padding-bottom:40px}
.ticker{position:fixed;left:0;right:0;bottom:0;height:32px;overflow:hidden;background:var(--head);color:var(--head-fg);border-top:2px solid var(--gold);z-index:50;font:600 14px/32px var(--f-body,system-ui)}
.ticker span{position:absolute;left:0;top:0;white-space:nowrap;animation:tick 12s linear infinite;font-size:15px}
.ticker b{color:var(--gold)}
@keyframes tick{from{transform:translateX(100vw)}to{transform:translateX(-100%)}}
@media (prefers-reduced-motion:reduce){.ticker span{animation:none;position:static;display:block;text-align:center}}
@media print{.ticker{display:none!important}body{padding-bottom:0}}
'''
html='''<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>بوابة أداء المناديب</title>
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Noto+Kufi+Arabic:wght@600;700&display=swap">
<style>body{margin:0;font:14px/1.5 system-ui,-apple-system,sans-serif}[hidden]{display:none!important}'''+css+'''</style>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.js"></script>
</head><body><div id="root"></div>
<div class="ticker" role="note" aria-live="off"><span id="tickerTxt">سبحان الله</span></div>
<div class="splash" id="splash" hidden role="status"><div><span class="sco" id="splashCo">الدعم المطور للخدمات اللوجستية</span><span class="sby" id="splashTxt">إعداد المهندس / <b>فاضل العميسي</b></span></div></div>
<script>'''+js+'''</script>
<script>/* bottom bar: adhkar, one phrase per pass (fadhel 2026-10-18) */
(function(){var L=["سبحان الله","الحمد لله","لا إله إلا الله","الله أكبر","اللهم صلِّ وسلم على سيدنا محمد وعلى آله وصحبه وسلم"],i=0,el=document.getElementById("tickerTxt");if(!el)return;
el.addEventListener("animationiteration",function(){i=(i+1)%L.length;el.textContent=L[i]});
if(window.matchMedia&&matchMedia("(prefers-reduced-motion:reduce)").matches)setInterval(function(){i=(i+1)%L.length;el.textContent=L[i]},5000)})();</script>
</body></html>
'''
html=html.replace('إعداد المهندس','تصميم المهندس').replace('Prepared by Eng.','Designed by Eng.')  # fadhel 2026-10-10
open('site/index.html','w',encoding='utf8').write(html)
print(len(html))
