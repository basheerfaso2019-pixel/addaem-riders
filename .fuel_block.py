# fuel: Aldrees "تقرير استهلاك المحروقات - التفاصيل" upload -> sheet fuel column (fadhel 2026-10-11)
# the report names a card holder ("السائق"), not a rider id, so each label is mapped to a rider once (fuel_map)
js=rep(js,'function parseRows(rows,fallbackDate){','function parseRows(rows,fallbackDate){\n  var fz=parseFuel(rows);if(fz)return fz;')
js=rep(js,'function vSoon(){',r'''/* ---------- fuel (Aldrees) ---------- */
function parseFuel(rows){var hi=-1,h;for(var k=0;k<Math.min(rows.length,40);k++){var t=rows[k].map(function(x){return String(x).trim()});if(t.indexOf("السائق")>=0&&t.indexOf("المبلغ")>=0){hi=k;h=t;break}}
  if(hi<0)return null;
  var I={d:h.indexOf("السائق"),a:h.indexOf("المبلغ"),l:h.indexOf("اللترات"),p:h.indexOf("رقم اللوحة"),t:h.indexOf("التاريخ")};
  var out={type:"fuel",days:{},people:{},quality:{},fuel:{},rows:0,bad:0,skippedToday:0,multiDay:false},ds=[];
  rows.slice(hi+1).forEach(function(r){var lb=String(r[I.d]||"").replace(/\s+/g," ").trim(),a=toNum(r[I.a]);if(!lb&&!a)return;
    var d=I.t>=0?normDate(r[I.t]):null;if(!lb||!d){out.bad++;return}
    var m=d.slice(0,7),o=(out.fuel[m]||(out.fuel[m]={}))[lb]||(out.fuel[m][lb]={a:0,l:0,n:0,p:"",t:""});
    o.a+=a;o.l+=I.l>=0?toNum(r[I.l]):0;o.n++;if(I.p>=0&&r[I.p])o.p=String(r[I.p]).trim();if(d>o.t)o.t=d;ds.push(d);out.rows++});
  ds.sort();out.from=ds[0];out.to=ds[ds.length-1];out.dayCount=0;out.ids=0;return out}
function fNorm(s){return String(s||"").replace(/[إأآا]/g,"ا").replace(/ة/g,"ه").replace(/ى/g,"ي").replace(/عبد\s+ال/g,"عبدال").replace(/عبد\s+رب/g,"عبدرب")}
function fToks(s){return fNorm(s).split(/[^؀-ۿ]+/).filter(function(t){return t&&["حتي","من","الي","المهندس","سياره","الشركه"].indexOf(t)<0})}
/* card label -> rider id: the holder is the name after the last "/", every word must be in exactly one rider's name */
function fuelGuess(lb){var dt=fToks(lb.split("/").pop());if(!dt.length)return null;var best=[],bs=0;
  Object.keys(data.couriers).forEach(function(id){var n=data.couriers[id].n;if(!n)return;var rt=fToks(n),rj=rt.join(""),hit=0;
    dt.forEach(function(t){var u=t.replace(/^ال/,"");if(rt.indexOf(t)>=0||rt.some(function(x){return x.replace(/^ال/,"")===u})||(t.length>3&&rj.indexOf(u)>=0))hit++});
    if(!hit)return;var sc=hit/dt.length;if(sc>bs){bs=sc;best=[id]}else if(sc===bs)best.push(id)});
  return bs>=1&&best.length===1?best[0]:null}
var FUEL={};
function fuelLoad(m){if(FUEL[m])return;FUEL[m]="loading";
  Promise.all([sb.from("fuel_label").select("label,amount,plate,tx,last_ts").eq("month",m),all("fuel_map","label,rider_id","label")]).then(function(rs){
    var mp={};(rs[1]||[]).forEach(function(x){mp[x.label]=x.rider_id||""});FUEL[m]={labels:(rs[0].data||[]).sort(function(a,b){return b.amount-a.amount}),map:mp};render()},function(){FUEL[m]={labels:[],map:{}};render()})}
/* recompute every rider's fuel for the month from the stored card totals and the mapping */
function fuelRecalc(m){return Promise.all([sb.from("fuel_label").select("label,amount").eq("month",m),all("fuel_map","label,rider_id","label")]).then(function(rs){
    if(rs[0].error)throw rs[0].error;var mp={},add=[];(rs[1]||[]).forEach(function(x){mp[x.label]=x.rider_id});
    var tot={};(rs[0].data||[]).forEach(function(x){if(!(x.label in mp)){var g=fuelGuess(x.label);mp[x.label]=g;add.push({label:x.label,rider_id:g})}var id=mp[x.label];if(id&&data.couriers[id])tot[id]=(tot[id]||0)+(+x.amount||0)});
    Object.keys(mp).forEach(function(lb){var id=mp[lb];if(id&&data.couriers[id]&&!(id in tot))tot[id]=0});
    var up=Object.keys(tot).map(function(id){return {month:m,rider_id:id,fuel:round2(tot[id]),updated_at:new Date().toISOString()}});
    return (add.length?upsertAll("fuel_map",add,"label"):Promise.resolve()).then(function(){return upsertAll("sheet_extra",up,"month,rider_id")})
      .then(function(){delete FUEL[m];delete SHX[m];return up.length})})}
function fuelApply(list){var rows=[],ms={};list.forEach(function(p){if(p.type!=="fuel")return;Object.keys(p.fuel).forEach(function(m){ms[m]=1;Object.keys(p.fuel[m]).forEach(function(lb){var o=p.fuel[m][lb];
    rows.push({month:m,label:lb,amount:round2(o.a),liters:round2(o.l),tx:o.n,plate:o.p||null,last_ts:o.t||null,updated_at:new Date().toISOString()})})})});
  if(!rows.length)return Promise.resolve();
  /* the report is month-to-date, so it replaces the month's cards (a renamed card must not count twice) */
  return Object.keys(ms).reduce(function(p,m){return p.then(function(){return sb.from("fuel_label").delete().eq("month",m).then(function(r){if(r.error)throw r.error})})},Promise.resolve())
    .then(function(){return upsertAll("fuel_label",rows,"month,label")}).then(function(){return Object.keys(ms).reduce(function(p,m){return p.then(function(){return fuelRecalc(m)})},Promise.resolve())})}
function fuelPanel(mon){var F=FUEL[mon];fuelLoad(mon);if(!F||F==="loading")return "";if(!F.labels.length)return '<section class="panel"><h2>بطاقات البنزين</h2><p class="hint" style="margin:0">لم يُرفع تقرير المحروقات لهذا الشهر. ارفعه من «رفع البيانات» ويتعبأ عمود البنزين تلقائياً.</p></section>';
  var ids=Object.keys(data.couriers).filter(function(id){return data.couriers[id].n}).sort(function(a,b){return data.couriers[a].n.localeCompare(data.couriers[b].n,"ar")});
  var un=F.labels.filter(function(x){return !F.map[x.label]}),tot=0,unt=0;F.labels.forEach(function(x){tot+=+x.amount;if(!F.map[x.label])unt+=+x.amount});
  var opts=function(sel){return '<option value="">— غير مربوط —</option>'+ids.map(function(id){return '<option value="'+esc(id)+'"'+(id===sel?" selected":"")+'>'+esc(data.couriers[id].n)+' · '+esc(id)+'</option>'}).join("")};
  var list=un.concat(F.labels.filter(function(x){return F.map[x.label]}));
  var body=list.map(function(x){var id=F.map[x.label]||"";return '<tr'+(id?"":' style="background:#fdf3e1"')+'><td class="s" style="white-space:normal">'+esc(x.label)+'</td><td class="num">'+esc(x.plate||"")+'</td><td class="num">'+N(x.amount,2)+'</td><td><select data-fmap="'+esc(x.label)+'" style="max-width:260px">'+opts(id)+'</select></td></tr>'}).join("");
  return '<section class="panel"><details'+(un.length?" open":"")+'><summary style="cursor:pointer"><h2 style="display:inline">بطاقات البنزين</h2> <span class="hint">· <span class="num">'+F.labels.length+'</span> بطاقة بمجموع '+N(tot,2)+' ر.س'+(un.length?' · <b style="color:var(--bad)"><span class="num">'+un.length+'</span> غير مربوطة ('+N(unt,2)+' ر.س)</b>':' · كلها مربوطة')+'</span></summary>'+
    '<p class="hint">تقرير الدريس يذكر اسم حامل البطاقة وليس رقم المندوب. اختر المندوب لكل بطاقة مرة واحدة، والنظام يتذكره في كل تقرير قادم ويحدّث عمود البنزين.</p>'+
    '<div class="tbl" style="box-shadow:none"><table><thead><tr><th>اسم البطاقة</th><th>اللوحة</th><th>المبلغ</th><th>المندوب</th></tr></thead><tbody>'+body+'</tbody></table></div></details></section>'}
function fuelSetMap(lb,id,mon){SH_MSG="جارٍ تحديث البنزين…";render();
  sb.from("fuel_map").upsert({label:lb,rider_id:id||null,updated_at:new Date().toISOString()}).then(function(r){if(r.error)throw r.error;
    var old=FUEL[mon]&&FUEL[mon].map?FUEL[mon].map[lb]:"";
    /* the rider the card was taken from loses it: recompute his total from his remaining cards */
    return fuelRecalc(mon).then(function(){if(!old||old===id)return;return sb.from("fuel_map").select("label").eq("rider_id",old).then(function(q){var ls=(q.data||[]).map(function(x){return x.label});
      return (ls.length?sb.from("fuel_label").select("amount").eq("month",mon).in("label",ls):Promise.resolve({data:[]})).then(function(s){var t=0;(s.data||[]).forEach(function(x){t+=+x.amount});
        return sb.from("sheet_extra").upsert({month:mon,rider_id:old,fuel:round2(t),updated_at:new Date().toISOString()})})})})})
  .then(function(){SH_MSG="تم تحديث البنزين";render()},function(e){SH_MSG="تعذّر الحفظ: "+((e&&e.message)||e);render()})}
function vSoon(){''')
js=rep(js,"(body||'<tr><td class=\"empty\" colspan=\"45\">لا يوجد مناديب في الكشف. ارفع ملف المناديب مع عمود الفئة.</td></tr>')+'</tbody><tfoot>'+foot+'</tfoot></table></div></section>';",
 "(body||'<tr><td class=\"empty\" colspan=\"45\">لا يوجد مناديب في الكشف. ارفع ملف المناديب مع عمود الفئة.</td></tr>')+'</tbody><tfoot>'+foot+'</tfoot></table></div></section>'+fuelPanel(mon);")
js=rep(js,'roster:"بيانات المناديب (الإقامة والأسماء)"};','roster:"بيانات المناديب (الإقامة والأسماء)",fuel:"تقرير استهلاك المحروقات (الدريس)"};')
js=rep(js,'    .then(function(){var now=new Date().toLocaleString("en-CA"','    .then(function(){return fuelApply(list)})\n    .then(function(){var now=new Date().toLocaleString("en-CA"')
js=rep(js,'  if(t.id==="ovMon"){ui0.ovm=t.value;render()}','  if(t.id==="ovMon"){ui0.ovm=t.value;render()}\n  if(t.dataset.fmap!=null){fuelSetMap(t.dataset.fmap,t.value,SH_MON||shMonths()[0]);return}')
