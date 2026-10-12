# category A (target) riders do not see kilometres in their portal (fadhel 2026-10-12)
js=rep(js,'function vSoon(){','function kmHide(id){return normCat(data.couriers[id]&&data.couriers[id].cat)==="أ"}\nfunction vSoon(){')
js=rep(js,'''+tile("distance","المسافة المقطوعة",'<span class="num">'+fmt(km,1)+'</span> <span style="font-size:15px">كم</span>',"هذا الشهر حتى أمس")''','''+(kmHide(id)?"":tile("distance","المسافة المقطوعة",'<span class="num">'+fmt(km,1)+'</span> <span style="font-size:15px">كم</span>',"هذا الشهر حتى أمس"))''')
js=rep(js,'  if(cs==="home"){\n    var lv=ld&&cRec(ld)','  if(cs==="distance"&&kmHide(id))cs="home";\n  if(cs==="home"){\n    var lv=ld&&cRec(ld)')
