# riders see Payable KM only, never Total KM (fadhel 2026-10-21). Manager distance pages keep both.
js=rep(js,'if(d.slice(0,7)===mon)km+=+x[DI]||0});var qx','if(d.slice(0,7)===mon)km+=+x[DP]||0});var qx')
js=rep(js,'''tile("distance","المسافة المقطوعة",''','''tile("distance","المسافة المستحقة",''')
js=rep(js,'''(v[DI]!=null?kpi("المسافة",N(v[DI],1)+''','''(v[DP]!=null?kpi("المسافة المستحقة",N(v[DP],1)+''')
js=rep(js,'tk+=+data.days[d][id][DI]||0;tp+=+data.days[d][id][DP]||0','tk+=+data.days[d][id][DP]||0;tp=tk')
js=rep(js,'''<span class="hero-num num">'+fmt(data.days[dd][id][DI],1)+'</span><span>كم في '+dl(dd)+'</span></div><div class="kpis" style="margin-top:12px">'+kpi("المسافة المدفوعة",N(data.days[dd][id][DP],1)+' كم',"Payable KM")+kpi''',
 '''<span class="hero-num num">'+fmt(data.days[dd][id][DP],1)+'</span><span>كم مستحقة في '+dl(dd)+'</span></div><div class="kpis" style="margin-top:12px">'+kpi''')
js=rep(js,'N(data.days[dd][id][DI]/data.days[dd][id][CP],1)','N((+data.days[dd][id][DP]||0)/data.days[dd][id][CP],1)')
js=rep(js,'''<span>كم في '+monLabel(mon3)+'</span></div><div class="kpis" style="margin-block:12px">'+kpi("المسافة المدفوعة",N(tp,1)+' كم',"Payable KM")+'</div><p class="hint">''','''<span>كم مستحقة في '+monLabel(mon3)+'</span></div><p class="hint" style="margin-top:12px">''')
js=rep(js,'return{d:d,v:+data.days[d][id][DI]||0}});\n    return sampleNote()+head+\'<section class="panel"><h2>المسافة المقطوعة</h2>','return{d:d,v:+data.days[d][id][DP]||0}});\n    return sampleNote()+head+\'<section class="panel"><h2>المسافة المستحقة <small>Payable KM</small></h2>')
js=rep(js,'''<h2>المسافة اليومية</h2><p class="hint">كيلومتر لكل يوم في الشهر''','''<h2>المسافة المستحقة اليومية</h2><p class="hint">كيلومتر مستحق لكل يوم في الشهر''')
