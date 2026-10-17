# «اكواد الهيئة» in شيت الأداء = "Error Codes" column of the Riders Performance file, red when not 0 (fadhel 2026-10-17)
js=rep(js,'var PERF_COLS=[','var EC=20;\nvar PERF_COLS=[')
js=rep(js,'if(x[CP]==null&&r.completed_dist!=null)x[CP]=+r.completed_dist;return x}','if(x[CP]==null&&r.completed_dist!=null)x[CP]=+r.completed_dist;x[EC]=r.error_codes==null?null:String(r.error_codes);return x}')
js=rep(js,'var tg=col(h,eq("tga status"));if(tg>=0)p.tga=String(r[tg]).trim();','var tg=col(h,eq("tga status"));if(tg>=0)p.tga=String(r[tg]).trim();var eci=col(h,eq("error codes","error code"));if(eci>=0)x[EC]=ecJoin(x[EC],r[eci]);')
js=rep(js,'round2(v))});daily.perf.push(o)}','round2(v))});o.error_codes=x[EC]==null?null:x[EC];daily.perf.push(o)}')
js=rep(js,'tga:0,','tga:ecMonth(id,ds),')
js=rep(js,'''<td class="num">0</td><td class="num">'+fmt(r.h)''','''<td class="'+(r.tga.length?'tgared':'num')+'">'+(r.tga.length?esc(r.tga.join("، ")):"0")+'</td><td class="num">'+fmt(r.h)''')
js=rep(js,'''<td colspan="6">الإجمالي</td><td class="num">0</td>''','''<td colspan="6">الإجمالي</td><td class="num'+(S.rows.some(function(r){return r.tga.length})?' tgared':'')+'">'+S.rows.filter(function(r){return r.tga.length}).length+'</td>''')
js=rep(js,'xc("G"+R,15,0)','xc("G"+R,r.tga.length?TGA_XF:15,r.tga.length?(r.tga.length===1&&/^\\d+$/.test(r.tga[0])?+r.tga[0]:r.tga.join("، ")):0)')
js=rep(js,'if(L==="J"){t.push(xc("J"+tr,36,null));continue}','if(L==="J"){t.push(xc("J"+tr,36,null));continue}if(L==="G"){t.push(xc("G"+tr,36,S.rows.filter(function(r){return r.tga.length}).length));continue}')
js=rep(js,'''.then(function(a){return a[0].loadAsync(a[1])}).then(function(zip){
    return Promise.all([zip.file("xl/worksheets/sheet1.xml")''','''.then(function(a){return a[0].loadAsync(a[1])}).then(function(zip){return zip.file("xl/styles.xml").async("string").then(function(st){zip.file("xl/styles.xml",tgaStyles(st));return zip})}).then(function(zip){
    return Promise.all([zip.file("xl/worksheets/sheet1.xml")''')
js=rep(js,'function vSoon(){','''var TGA_XF=15;
function ecList(v){return String(v==null?"":v).split(/[,،;|\\s]+/).map(function(s){return digits(s).trim()}).filter(function(s){return s&&s!=="0"&&s!=="-"&&!/^0+(\\.0+)?$/.test(s)})}
function ecJoin(a,b){var l=ecList(a);ecList(b).forEach(function(c){if(l.indexOf(c)<0)l.push(c)});return l.length?l.join(", "):"0"}
/* codes from the rider's latest performance day in the month (the sheet shows the state as of the last day) */
function ecMonth(id,ds){for(var i=ds.length-1;i>=0;i--){var r=data.days[ds[i]]&&data.days[ds[i]][id];if(r&&r[EC]!=null)return ecList(r[EC])}return []}
function tgaStyles(st){var m=st.match(/<cellXfs count="(\\d+)"/);if(!m)return st;TGA_XF=+m[1];
  var fm=st.match(/<fills count="(\\d+)"/),fid=+fm[1];
  st=st.replace(/<fills count="\\d+"/,'<fills count="'+(fid+1)+'"').replace("</fills>",'<fill><patternFill patternType="solid"><fgColor rgb="FFFF4D4D"/><bgColor indexed="64"/></patternFill></fill></fills>');
  return st.replace(/<cellXfs count="\\d+"/,'<cellXfs count="'+(TGA_XF+1)+'"').replace("</cellXfs>",'<xf numFmtId="0" fontId="0" fillId="'+fid+'" borderId="2" applyFill="1" applyAlignment="1" xfId="0"><alignment horizontal="center" vertical="center" wrapText="1" /></xf></cellXfs>')}
function vSoon(){''')
css+='''
.tgared{background:#ff4d4d!important;color:#fff!important;font-weight:700}
'''
