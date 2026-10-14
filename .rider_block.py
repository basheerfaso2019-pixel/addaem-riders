# manager rider panel: completed orders per month (month picker + per-month totals) and the quality segment with its reasons (fadhel 2026-10-14)
js=rep(js,'function vSoon(){',r'''/* ---------- rider panel: months + quality reasons ---------- */
function rdMonths(id){var m={};days().forEach(function(d){if(data.days[d][id])m[d.slice(0,7)]=1});return Object.keys(m).sort().reverse()}
/* each factor behind the segment, weakest first; the weakest one(s) below 100% are what pulls the segment down */
function qReasons(q){if(!q)return "";var pc=function(v){return v==null||isNaN(v)?null:v*100};
  var R=[{n:"التوصيل في الوقت",e:"On Time Score",v:pc(q.ot),d:q.cp!=null?'<span class="num">'+fmt(q.it,0)+'</span> في الوقت من <span class="num">'+fmt(q.cp,0)+'</span> طلب مكتمل · <b>'+fmt(Math.max(0,(+q.cp||0)-(+q.it||0)),0)+'</b> طلب متأخر':""},
    {n:"درجة الفشل",e:"Fail Rate Score",v:pc(q.fr),d:'<b>'+fmt(q.f||0,0)+'</b> طلب فشل بسبب المندوب من <span class="num">'+fmt(q.g,0)+'</span> طلب'},
    {n:"نجاح التحقق",e:"Verification Rate",v:pc(q.vr),d:q.vt?'<span class="num">'+fmt(q.vs,0)+'</span> نجح من <span class="num">'+fmt(q.vt,0)+'</span> طلب تحقق · <b>'+fmt(Math.max(0,(+q.vt||0)-(+q.vs||0)),0)+'</b> لم ينجح':"لا توجد طلبات تحقق"}].filter(function(r){return r.v!=null});
  var low=R.filter(function(r){return r.v<100}).sort(function(a,b){return a.v-b.v}),min=low.length?low[0].v:null;
  var row=function(r){var bad=r.v<100,main=bad&&r.v===min,col=r.v>=95?"var(--good)":r.v>=85?"var(--warn)":"var(--bad)";
    return '<div class="qrs'+(main?" main":"")+'"><div class="qrh"><b>'+r.n+' <small>'+r.e+'</small></b><span class="num" style="color:'+col+';font-weight:700">'+fmt(r.v,2)+'%</span></div><div class="qrbar"><i style="width:'+Math.max(0,Math.min(100,r.v))+'%;background:'+col+'"></i></div><div class="hint" style="margin:4px 0 0">'+r.d+(main?' · <b style="color:var(--bad)">السبب الرئيسي لانخفاض التصنيف</b>':bad?' · يؤثر على التصنيف':' · ممتاز')+'</div></div>'};
  return '<div class="qreasons"><div class="qrtop"><span>'+segPill(q.s)+'</span><span>درجة الجودة النهائية <b class="num">'+fmt(pc(q.sc),2)+'%</b></span></div>'+
    '<h3 style="margin:10px 0 6px;font-size:15px">أسباب التصنيف</h3>'+R.map(row).join("")+
    (low.length?'':'<p class="hint">كل العوامل 100%، التصنيف مبني على درجة الجودة النهائية وعدد الطلبات.</p>')+'</div>'}
function rdQuality(id){var qq=(data.couriers[id]&&data.couriers[id].q)||{},ms=Object.keys(qq).sort().reverse();if(!ms.length)return '<section class="panel"><h2>تصنيف المندوب</h2><p class="hint" style="margin:0">لم تُرفع بيانات جودة التوصيل لهذا المندوب.</p></section>';
  var m=ui0.rqm&&qq[ui0.rqm]?ui0.rqm:ms[0];
  return '<section class="panel"><div class="stmthead"><h2>تصنيف المندوب · '+monLabel(m)+'</h2>'+(ms.length>1?'<div class="stmttools"><select id="rqMon" aria-label="الشهر">'+ms.map(function(x){return '<option value="'+x+'"'+(x===m?" selected":"")+'>'+monTxt(x)+'</option>'}).join("")+'</select></div>':'')+'</div>'+qReasons(qq[m])+'</section>'}
function vSoon(){''')
old='''  if(ui.sel){var id=ui.sel,ds=days().slice(-30),ser=ds.map(function(d){var v=data.days[d][id];return{d:d,v:v?+v[CP]||0:0}}),tot=agg(days().filter(function(d){return data.days[d][id]}).map(function(d){return{d:d,id:id,x:data.days[d][id]}}));'''
new='''  if(ui.sel){var id=ui.sel,rms=rdMonths(id),rm=ui0.rdm&&rms.indexOf(ui0.rdm)>=0?ui0.rdm:rms[0],mdays=days().filter(function(d){return d.slice(0,7)===rm}),ds=mdays,ser=ds.map(function(d){var v=data.days[d][id];return{d:d,v:v?+v[CP]||0:0}}),tot=agg(mdays.filter(function(d){return data.days[d][id]}).map(function(d){return{d:d,id:id,x:data.days[d][id]}}));
    var mtot=rms.map(function(m){var t=0;days().forEach(function(d){if(d.slice(0,7)===m&&data.days[d][id])t+=+data.days[d][id][CP]||0});return '<button class="mchip'+(m===rm?" on":"")+'" data-rdm="'+m+'">'+monTxt(m)+' <b class="num">'+fmt(t,0)+'</b></button>'}).join("");'''
js=rep(js,old,new)
js=rep(js,'''<button class="btn" data-sel="">إغلاق</button></div></div>'+
      '<div class="kpis" style="margin-block:12px">'+kpi("الطلبات المكتملة (كل الأيام)",N(tot.cp,0),'خلال <span class="num">'+tot.days+'</span> يوم')''','''<button class="btn" data-sel="">إغلاق</button></div></div>'+
      '<div class="mchips"><span class="hint">الطلبات المكتملة حسب الشهر:</span>'+mtot+'</div>'+
      '<div class="kpis" style="margin-block:12px">'+kpi("الطلبات المكتملة · "+(rm?monTxt(rm):""),N(tot.cp,0),'خلال <span class="num">'+tot.days+'</span> يوم عمل')''')
js=rep(js,'''bars(ser,{h:170,label:"الطلبات المكتملة يومياً"})+'</section>'+stmtPanel(id);}''','''bars(ser,{h:170,label:"الطلبات المكتملة يومياً"})+'</section>'+rdQuality(id)+stmtPanel(id);}''')
js=rep(js,'  if(t.dataset.ovpdf){ovPdf(t.dataset.ovpdf);return}','  if(t.dataset.ovpdf){ovPdf(t.dataset.ovpdf);return}\n  if(t.dataset.rdm){ui0.rdm=t.dataset.rdm;render();return}')
js=rep(js,'  if(t.id==="ovMon"){ui0.ovm=t.value;render()}','  if(t.id==="ovMon"){ui0.ovm=t.value;render()}\n  if(t.id==="rqMon"){ui0.rqm=t.value;render()}')
# rider's own quality page gets the same reasons list
js=rep(js,'''      '<p class="hint" style="margin-top:12px">التصنيف من A (الأفضل) إلى F. ارتفاع نسبة التوصيل في الوقت يرفع تصنيفك.</p></section>'+''','''      '<p class="hint" style="margin-top:12px">التصنيف من A (الأفضل) إلى F. ارتفاع نسبة التوصيل في الوقت يرفع تصنيفك.</p>'+qReasons(q)+'</section>'+''')
css+='\n.mchips{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:10px}.mchip{font:inherit;font-size:13px;border:1px solid var(--line);background:var(--surface);color:inherit;border-radius:999px;padding:4px 12px;cursor:pointer}.mchip b{margin-inline-start:4px}.mchip.on{background:var(--accent);border-color:var(--accent);color:#fff}'+\
 '.qreasons{margin-top:6px}.qrtop{display:flex;gap:14px;align-items:center;font-size:15px}.qrtop .pill{font-size:20px}.qrs{border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin-bottom:8px}.qrs.main{border-color:var(--bad);background:var(--bad-soft)}.qrh{display:flex;justify-content:space-between;align-items:baseline;gap:8px}.qrh small{color:var(--muted);font-weight:400}.qrbar{height:8px;background:var(--sunk);border-radius:6px;overflow:hidden;margin-top:6px}.qrbar i{display:block;height:100%}\n'
