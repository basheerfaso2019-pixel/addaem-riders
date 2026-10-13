# staff accounts: access expiry date and delete (fadhel 2026-10-13); server checks expiry in is_staff()/can_see()
js=rep(js,'sb.rpc("list_accounts").then(function(r){if(r.error){ui.acc=[];ui.msg="تعذّر تحميل الحسابات: "+r.error.message;ui.msgOk=false}else ui.acc=r.data.map(function(a){return{id:a.user_id,e:a.email,n:a.name||"",r:a.role||"",p:a.perms||[],o:JSON.stringify([a.name||"",a.role||"",a.perms||[]])}});render()});',
 'sb.rpc("list_accounts2").then(function(r){if(r.error){ui.acc=[];ui.msg="تعذّر تحميل الحسابات: "+r.error.message;ui.msgOk=false}else ui.acc=r.data.map(function(a){var x=a.expires_at?new Date(a.expires_at).toISOString():"";return{id:a.user_id,e:a.email,n:a.name||"",r:a.role||"",p:a.perms||[],x:x,o:JSON.stringify([a.name||"",a.role||"",a.perms||[],x])}});render()});')
js=rep(js,'dirty=dr.some(function(a){return JSON.stringify([a.n,a.r,a.p])!==a.o});','dirty=dr.some(function(a){return JSON.stringify([a.n,a.r,a.p,a.x||""])!==a.o});')
js=rep(js,'''<button class="btn" style="padding:2px 8px;font-size:12px" data-newpw="'+i+'"'+(ui.busy?" disabled":"")+'>كلمة مرور جديدة</button>')''',
 '''<button class="btn" style="padding:2px 8px;font-size:12px" data-newpw="'+i+'"'+(ui.busy?" disabled":"")+'>كلمة مرور جديدة</button>')+(self||s.r==="admin"?'':' <button class="btn" style="padding:2px 8px;font-size:12px;color:var(--bad);border-color:var(--bad)" data-adel="'+i+'"'+(ui.busy?" disabled":"")+'>حذف</button>')''')
js=rep(js,'''<option value="admin"'+(s.r==="admin"?" selected":"")+'>مدير</option></select></td>'+''','''<option value="admin"'+(s.r==="admin"?" selected":"")+'>مدير</option></select></td>'+expCell(s,i)+''')
js=rep(js,"<th>الحساب</th><th>الدور</th>'+PERMS","<th>الحساب</th><th>الدور</th><th>انتهاء الصلاحية</th>'+PERMS")
js=rep(js,"colspan=\"'+(PERMS.length+2)+'\">لا توجد حسابات بعد.","colspan=\"'+(PERMS.length+3)+'\">لا توجد حسابات بعد.")
js=rep(js,'function staffErr(e){var m=e&&e.message;return ','''function expLocal(iso){if(!iso)return "";var d=new Date(iso);d.setMinutes(d.getMinutes()-d.getTimezoneOffset());return d.toISOString().slice(0,16)}
function expTxt(iso){var d=new Date(iso);return d.toLocaleDateString("en-CA")+" "+d.toTimeString().slice(0,5)}
function expPast(iso){return !!iso&&new Date(iso)<=new Date()}
/* expiry only applies to employees: managers never expire */
function expCell(s,i){if(s.r!=="staff")return '<td class="hint" style="font-size:12px">—</td>';
  var st=!s.x?'<span class="hint" style="font-size:12px">بدون انتهاء</span>':expPast(s.x)?'<b style="color:var(--bad);font-size:12px">منتهي — الحساب موقوف</b>':'<span style="font-size:12px;color:var(--good)">فعّال حتى <span class="num" dir="ltr">'+expTxt(s.x)+'</span></span>';
  return '<td style="white-space:nowrap"><select data-aexpq="'+i+'" style="font-size:12px"><option value="">مدة سريعة…</option><option value="1">يوم</option><option value="3">3 أيام</option><option value="7">أسبوع</option><option value="30">شهر</option><option value="0">بدون انتهاء</option></select><br><input type="datetime-local" data-aexp="'+i+'" value="'+expLocal(s.x)+'" style="font-size:12px;margin-top:4px"><br>'+st+'</td>'}
function staffErr(e){var m=e&&e.message;if(m==="cannot_delete_self")return "لا يمكنك حذف حسابك.";if(m==="cannot_delete_admin")return "لا يمكن حذف حساب مدير. غيّر دوره أولاً.";return ''')
js=rep(js,'upsert({user_id:a.id,name:a.n||a.e,role:a.r,perms:a.r==="staff"?a.p:[]},{onConflict:"user_id"})','upsert({user_id:a.id,name:a.n||a.e,role:a.r,perms:a.r==="staff"?a.p:[],expires_at:a.r==="staff"&&a.x?a.x:null},{onConflict:"user_id"})')
js=rep(js,'  if(t.dataset.newpw!=null){','''  if(t.dataset.adel!=null){var dl0=ui.acc[+t.dataset.adel];if(!confirm("حذف حساب الموظف «"+(dl0.n||uname(dl0.e))+"» نهائياً؟ لن يستطيع الدخول مرة أخرى."))return;ui.busy=true;render();
    staffFn({action:"delete",user_id:dl0.id}).then(function(){ui.busy=false;ui.acc=null;ui.msgOk=true;ui.msg="تم حذف حساب "+(dl0.n||uname(dl0.e))+".";render()}).catch(function(e){ui.busy=false;ui.msgOk=false;ui.msg=staffErr(e);render()});return}
  if(t.dataset.newpw!=null){''')
js=rep(js,'  if(t.dataset.arole!=null){','''  if(t.dataset.aexp!=null){ui.acc[+t.dataset.aexp].x=t.value?new Date(t.value).toISOString():"";render()}
  if(t.dataset.aexpq!=null&&t.value!==""){var dq=+t.value;ui.acc[+t.dataset.aexpq].x=dq?new Date(Date.now()+dq*864e5).toISOString():"";render()}
  if(t.dataset.arole!=null){''')
# login: an expired employee is signed out with a clear message
js=rep(js,'sb.from("staff").select("name,role,perms").eq("user_id",user.id)','sb.from("staff").select("name,role,perms,expires_at").eq("user_id",user.id)')
js=rep(js,'    isAdmin=s.role==="admin";staff=isAdmin?null:','''    if(s.role!=="admin"&&expPast(s.expires_at)){isAdmin=false;staff=null;ui.msg="انتهت صلاحية حسابك. تواصل مع المدير لتجديدها.";ui.msgOk=false;ui0.who="staff";return sb.auth.signOut()}
    isAdmin=s.role==="admin";staff=isAdmin?null:''')
# new employee: optional expiry
js=rep(js,'''<label>كلمة المرور<input id="sp" required dir="ltr" minlength="8" value="'+esc(ui.genpw||(ui.genpw=genPw()))+'"></label>''','''<label>كلمة المرور<input id="sp" required dir="ltr" minlength="8" value="'+esc(ui.genpw||(ui.genpw=genPw()))+'"></label><label>انتهاء الصلاحية (اختياري)<input id="sx" type="datetime-local"></label>''')
js=rep(js,'staffFn({action:"create",name:sn,username:su,password:sp,perms:["overall","daily"]})','staffFn({action:"create",name:sn,username:su,password:sp,perms:["overall","daily"],expires_at:(document.getElementById("sx").value?new Date(document.getElementById("sx").value).toISOString():null)})')
