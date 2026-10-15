# rider portal: orders between two days of ONE month (month picker, then from/to inside it) (fadhel 2026-10-15)
js=rep(js,'function vSoon(){','''function rgEnd(m,ld){var y=+m.slice(0,4),mo=+m.slice(5,7),e=m+"-"+String(new Date(Date.UTC(y,mo,0)).getUTCDate()).padStart(2,"0");return e>ld?ld:e}
function rgPanel(id,mine,ld){if(!ld)return "";var ms={};mine.forEach(function(d){ms[d.slice(0,7)]=1});ms[ld.slice(0,7)]=1;var ml=Object.keys(ms).sort().reverse();
  var m=ui0.rgm&&ms[ui0.rgm]?ui0.rgm:ml[0],lo=m+"-01",hi=rgEnd(m,ld),f=ui0.rgf&&ui0.rgf.slice(0,7)===m?ui0.rgf:lo,t=ui0.rgt&&ui0.rgt.slice(0,7)===m?ui0.rgt:hi;
  if(f<lo)f=lo;if(t>hi)t=hi;if(f>t){var x=f;f=t;t=x}
  var ins=mine.filter(function(d){return d>=f&&d<=t}),sum=ins.reduce(function(a,d){return a+(+data.days[d][id][CP]||0)},0);
  return '<section class="panel"><h2>عدد طلباتي خلال فترة من الشهر</h2><div class="row rgrow"><label class="fcard">الشهر<select id="rgM">'+ml.map(function(k){return '<option value="'+k+'"'+(k===m?" selected":"")+'>'+monTxt(k)+'</option>'}).join("")+'</select></label>'+
    '<label class="fcard">من يوم<input type="date" id="rgF" min="'+lo+'" max="'+hi+'" value="'+f+'"></label><label class="fcard">إلى يوم<input type="date" id="rgT" min="'+lo+'" max="'+hi+'" value="'+t+'"></label></div>'+
    '<div class="hero"><span class="hero-num num">'+fmt(sum,0)+'</span><span>طلب مكتمل من <span class="num">'+f+'</span> إلى <span class="num">'+t+'</span></span></div>'+
    '<div class="kpis" style="margin-top:12px">'+kpi("أيام العمل",N(ins.length,0),"")+kpi("متوسط يومي",N(ins.length?sum/ins.length:0,1),"")+'</div>'+
    '<p class="hint">كل شهر يُحسب لوحده. البيانات متاحة حتى <span class="num">'+ld+'</span>.</p></section>'}
function vSoon(){''')
js=rep(js,'''<section class="panel"><h2>عدد طلبات يوم محدد</h2>'+res+'</section>'+''','''<section class="panel"><h2>عدد طلبات يوم محدد</h2>'+res+'</section>'+rgPanel(id,mine,ld)+''')
js=rep(js,'  if(t.id==="cday"){ui.cday=t.value>YEST?YEST:t.value;render()}','''  if(t.id==="cday"){ui.cday=t.value>YEST?YEST:t.value;render()}
  if(t.id==="rgM"){ui0.rgm=t.value;ui0.rgf=ui0.rgt=null;render()}
  if((t.id==="rgF"||t.id==="rgT")&&t.value){var mm=t.value.slice(0,7);if(mm!==ui0.rgm){ui0.rgm=mm;ui0.rgf=ui0.rgt=null}if(t.id==="rgF")ui0.rgf=t.value;else ui0.rgt=t.value;render()}''')
css+='''
.rgrow .fcard{flex:1;min-width:130px}
.rgrow input,.rgrow select{width:100%}
'''
