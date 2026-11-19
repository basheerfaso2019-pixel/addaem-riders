/* Salary details (تفاصيل الراتب): turn the rows of a rider account statement into the salary-details sheet.
   Used by salary.html in the browser and by node for checks. No DOM here. */
(function(root){
"use strict";
var AR_DIG="٠١٢٣٤٥٦٧٨٩",FA_DIG="۰۱۲۳۴۵۶۷۸۹";
function latin(s){return String(s==null?"":s).replace(/[٠-٩]/g,function(d){return AR_DIG.indexOf(d)}).replace(/[۰-۹]/g,function(d){return FA_DIG.indexOf(d)}).replace(/٫/g,".").replace(/٬/g,",")}
/* "2.346,53" / "2,346.53" / "2346.53" / "-1.253,42" -> number */
function num(x){
  if(typeof x==="number")return isFinite(x)?x:0;
  var s=latin(x).replace(/[^\d.,\-−]/g,"").replace("−","-");if(!s||s==="-")return 0;
  var neg=s.charAt(0)==="-";s=s.replace(/-/g,"");
  var d=s.lastIndexOf("."),c=s.lastIndexOf(",");
  if(d>=0&&c>=0){if(c>d)s=s.replace(/\./g,"").replace(",",".");else s=s.replace(/,/g,"")}
  else if(c>=0){s=/,\d{1,2}$/.test(s)&&s.split(",").length===2?s.replace(",","."):s.replace(/,/g,"")}
  else if(d>=0&&s.split(".").length>2)s=s.replace(/\./g,"");
  var v=parseFloat(s);if(!isFinite(v))return 0;return neg?-v:v}
function r2(v){return Math.round((+v||0)*100)/100}
function norm(s){return latin(s).replace(/[ً-ْـ]/g,"").replace(/[أإآ]/g,"ا").replace(/ة/g,"ه").replace(/ى/g,"ي")}

var FIXED=[
  {k:"prev",label:"المتبقي عليك سابقا"},
  {k:"com",label:"عمولة الشركة",re:/عموله/},
  {k:"abs",label:"خصم عدم حضور وغياب",re:/غياب|عدم\s*حضور/},
  {k:"multi",label:"خصم الطلبات المتعددة",re:/متعدد/},
  {k:"wal",label:"المحفظة",re:/محفظه/},
  {k:"fuel",label:"البنزين",re:/بنزين|محروقات|وقود/},
  {k:"rent",label:"ايجار سيارة",re:/قسط\s*ايجار|ايجار\s*(ال)?سياره/}
];
var REV_RE=/عدد\s*الطلبات|ايراد|ابراد|اثبات|اتبات|ابات/;

/* strip the rider's name / Iqama and stray separators from a statement line */
function cleanDesc(desc,name){
  var s=latin(desc).replace(/\s+/g," ").trim();
  if(name){var n=latin(name).replace(/\s+/g," ").trim();if(n){s=s.split(n).join(" ").replace(/\s+/g," ").trim();
    /* the name is often cut at the line end: drop a trailing part of it ("…-موسى عبدالله") */
    var w=n.split(" ");for(var k=w.length;k>0;k--){var pre=w.slice(0,k).join(" ");if(s.length>pre.length&&s.slice(-pre.length)===pre&&/[\s\-–\/م]$/.test(s.slice(0,-pre.length))){s=s.slice(0,-pre.length);break}}}}
  s=s.replace(/\/?\s*\b\d{10}\b/g," ").replace(/\/\s*[\d\s]{6,}/g," ").replace(/\s+/g," ");
  s=s.replace(/([\d)])م(?=[\s\-–\/]|$)/g,"$1").replace(/[\s\-–\/،,.]+$/,"").replace(/^[\s\-–\/،,.]+/,"").replace(/\s+/g," ").trim();
  return s}

function revenueIndex(rows){
  var idx=-1;rows.forEach(function(r,i){if(num(r.credit)>0&&REV_RE.test(norm(r.desc)))idx=i});
  if(idx<0){var best=0;rows.forEach(function(r,i){var c=num(r.credit);if(c>best){best=c;idx=i}})}
  return idx}

/* rows: [{date,desc,debit,credit,balance}] in statement order. meta: {name,iqama} */
function derive(rows,meta){
  meta=meta||{};rows=(rows||[]).filter(function(r){return r&&(String(r.desc||"").trim()||num(r.debit)||num(r.credit))});
  var S={name:(meta.name||"").trim(),iqama:(meta.iqama||"").trim(),month:"",orders:"",level:"",dist:"",salary:0,items:[],endBal:null,warn:[]};
  var ri=revenueIndex(rows);
  if(ri<0){S.warn.push("لم يتم العثور على سطر إيراد الراتب (مبلغ دائن) في الكشف.")}
  var rev=ri>=0?rows[ri]:null,rd=rev?norm(rev.desc):"";
  if(rev){
    S.salary=r2(num(rev.credit));
    var m=rd.match(/لشهر\s+([^\s\d(]+)\s*(\d{4})?/);if(m)S.month=(m[1]+(m[2]?" "+m[2]:"")).replace(/م$/,"");
    if(S.month){/* restore spelling from the original line */var o=latin(rev.desc).match(/لشهر\s+([^\s\d(]+)\s*(\d{4})?/);if(o)S.month=(o[1]+(o[2]?" "+o[2]:"")).replace(/م$/,"")}
    m=rd.match(/عدد\s*الطلبات\s*[(:\s]*\s*(\d+)/);if(m)S.orders=+m[1];
    m=rd.match(/المسا\S{1,3}\s*[(:\s]*\s*([\d.,]+)/)||rd.match(/مبلغ\s*\S+\s*[(:]\s*([\d.,]+)/);if(m)S.dist=r2(num(m[1]));
    m=rd.match(/المستوي\s*[(:\s]*\s*([A-Fa-f])\b/);if(m)S.level=m[1].toUpperCase();
  }
  var prev=0;for(var i=0;i<ri;i++)prev+=num(rows[i].debit)-num(rows[i].credit);
  var fx={};FIXED.forEach(function(f){fx[f.k]={k:f.k,label:f.label,v:0}});fx.prev.v=r2(prev);
  var extras=[];
  rows.forEach(function(r,i){
    if(i<=ri)return;
    var d=norm(r.desc),v=r2(num(r.debit)-num(r.credit));if(!v)return;
    if(/^\s*تحويل|\sتحويل\s/.test(" "+d)&&v>0){extras.push({k:"x",label:"دفعة مستلمة من الراتب - تحويل بتاريخ "+(r.date||""),v:v});return}
    for(var j=1;j<FIXED.length;j++){if(FIXED[j].re.test(d)){fx[FIXED[j].k].v=r2(fx[FIXED[j].k].v+v);return}}
    extras.push({k:"x",label:cleanDesc(r.desc,S.name)||"بند آخر",v:v})});
  S.items=FIXED.map(function(f){return fx[f.k]}).concat(extras);
  var last=rows.length?rows[rows.length-1]:null;
  if(last&&last.balance!==""&&last.balance!=null)S.endBal=r2(num(last.balance));
  return S}

function totals(S){var t=0;S.items.forEach(function(it){t+=num(it.v)});t=r2(t);return {ded:t,salary:r2(num(S.salary)),rem:r2(t-num(S.salary))}}
function title(S){return "حساب المندوب / "+(S.name||"")+(S.month?" - راتب شهر "+S.month:"")}

/* ---------- Excel: rebuild sheet1 of the template, keeping its styles ---------- */
function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;")}
function cS(ref,s,t){return '<c r="'+ref+'" s="'+s+'" t="inlineStr"><is><t xml:space="preserve">'+esc(t)+'</t></is></c>'}
function cN(ref,s,v){return v===""||v==null?'<c r="'+ref+'" s="'+s+'"/>':'<c r="'+ref+'" s="'+s+'"><v>'+r2(num(v))+'</v></c>'}
function cF(ref,s,f,v){return '<c r="'+ref+'" s="'+s+'"><f>'+f+'</f><v>'+r2(v)+'</v></c>'}
function cE(ref,s){return '<c r="'+ref+'" s="'+s+'"/>'}
function row(r,ht,cells){return '<row r="'+r+'" spans="1:6"'+(ht?' ht="'+ht+'" customHeight="1"':'')+'>'+cells.join("")+'</row>'}
var WRAP=21;
function sheetXml(S){
  var T=totals(S),rows=[],merges=["A1:F1","A5:F5"];
  rows.push(row(1,37.2,[cS("A1",3,title(S)),cE("B1",3),cE("C1",3),cE("D1",3),cE("E1",3),cE("F1",3)]));
  rows.push(row(2,24.6,[cS("A2",4,"عدد الطلبات"),cN("B2",5,S.orders),cS("C2",6,"الفئة / "+(S.level||"")),cS("D2",5,"المسافات /"),cN("E2",5,S.dist),cE("F2",5)]));
  rows.push(row(3,16.2,[cS("A3",7,"الراتب /"),cN("B3",5,S.salary),cS("C3",8,"ريال"),cE("D3",5),cE("E3",5),cE("F3",5)]));
  rows.push(row(4,4.2,[cE("A4",4),cE("B4",5),cE("C4",5),cE("D4",5),cE("E4",5),cE("F4",5)]));
  rows.push(row(5,32.4,[cS("A5",9,"مستحقات الشركه مع المديونية على المندوب"),cE("B5",9),cE("C5",9),cE("D5",9),cE("E5",9),cE("F5",9)]));
  var r=6;
  S.items.forEach(function(it){
    var alt=it.k==="abs"||it.k==="multi",vs=alt?1:15,es=alt?17:16,lab=it.label||"",lines=Math.max(1,Math.ceil(lab.length/30));
    rows.push(row(r,Math.max(30.6,lines*17+6),[cS("A"+r,lines>1?WRAP:10,lab),cE("B"+r,11),cN("C"+r,vs,num(it.v)),cE("D"+r,es),cE("E"+r,es),cE("F"+r,es)]));
    merges.push("A"+r+":B"+r,"C"+r+":F"+r);r++});
  var last=r-1,tr=r,sr=r+1,rr=r+2,br=r+3;
  rows.push(row(tr,37.8,[cS("A"+tr,12,"اجمالي الخصومات"),cE("B"+tr,13),cF("C"+tr,18,"SUM(C6:C"+last+")",T.ded),cE("D"+tr,19),cE("E"+tr,19),cE("F"+tr,19)]));
  rows.push(row(sr,37.8,[cS("A"+sr,12,"الراتب"),cE("B"+sr,13),cF("C"+sr,18,"B3",T.salary),cE("D"+sr,19),cE("E"+sr,19),cE("F"+sr,19)]));
  rows.push(row(rr,37.8,[cS("A"+rr,14,"المتبقي عليك ++ المتبقي لك --"),cE("B"+rr,14),cF("C"+rr,20,"C"+tr+"-C"+sr,T.rem),cE("D"+rr,20),cE("E"+rr,20),cE("F"+rr,20)]));
  rows.push(row(br,0,[cE("C"+br,2),cE("D"+br,2),cE("E"+br,2),cE("F"+br,2)]));
  merges.push("A"+tr+":B"+tr,"C"+tr+":F"+tr,"A"+sr+":B"+sr,"C"+sr+":F"+sr,"A"+rr+":B"+rr,"C"+rr+":F"+rr,"C"+br+":F"+br);
  return {data:'<sheetData>'+rows.join("")+'</sheetData>',merges:'<mergeCells count="'+merges.length+'">'+merges.map(function(m){return '<mergeCell ref="'+m+'"/>'}).join("")+'</mergeCells>',dim:"A1:F"+br}}

/* JSZip: the JSZip constructor; buf: template ArrayBuffer/Uint8Array. Returns a promise of the zip (call generateAsync). */
function buildZip(JSZip,buf,S){
  return JSZip.loadAsync(buf).then(function(z){
    var p="xl/worksheets/sheet1.xml";
    return Promise.all([z.file(p).async("string"),z.file("xl/styles.xml").async("string"),z.file("xl/workbook.xml").async("string"),z.file("[Content_Types].xml").async("string"),z.file("xl/_rels/workbook.xml.rels").async("string")]).then(function(a){
      var X=sheetXml(S),sh=a[0];
      sh=sh.replace(/<sheetData[\s\S]*?<\/sheetData>|<sheetData\/>/,X.data).replace(/<mergeCells[\s\S]*?<\/mergeCells>/,X.merges).replace(/<dimension ref="[^"]*"\/>/,'<dimension ref="'+X.dim+'"/>').replace(/<selection [^>]*\/>/,'<selection activeCell="A1" sqref="A1"/>');
      z.file(p,sh);
      var st=a[1];if(!/<cellXfs count="22"/.test(st)){st=st.replace(/<cellXfs count="\d+"/,'<cellXfs count="22"').replace("</cellXfs>",'<xf numFmtId="0" fontId="7" fillId="3" borderId="5" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf></cellXfs>');z.file("xl/styles.xml",st)}
      z.file("xl/workbook.xml",a[2].replace(/<calcPr([^>]*?)\/>/,function(m,g){return /fullCalcOnLoad/.test(g)?m:'<calcPr'+g+' fullCalcOnLoad="1"/>'}));
      if(z.file("xl/calcChain.xml")){z.remove("xl/calcChain.xml");z.file("[Content_Types].xml",a[3].replace(/<Override PartName="\/xl\/calcChain.xml"[^>]*\/>/,""));z.file("xl/_rels/workbook.xml.rels",a[4].replace(/<Relationship [^>]*Target="calcChain.xml"\/>/,""))}
      return z})})}

var PROMPT="هذه صورة كشف حساب مندوب من نظام محاسبي (أعمدة: التاريخ، رقم القيد، البيان، المستند، مدين، دائن، الرصيد).\n"+
"استخرج كل السطور بالترتيب من الأعلى إلى الأسفل بدون حذف أي سطر، بما فيها سطر «رصيد أول الفترة»، وأرجع JSON بهذا الشكل:\n"+
'{"name":"اسم صاحب الحساب بدون رقم الهوية","iqama":"رقم الهوية/الإقامة المكون من 10 أرقام إن وجد","account_no":"رقم الحساب","rows":[{"date":"DD-MM-YYYY","desc":"نص البيان كاملاً كما هو مكتوب في سطر واحد","debit":0,"credit":0,"balance":0}],"total_debit":0,"total_credit":0,"total_balance":0}\n'+
"قواعد الأرقام: الصورة تستخدم النقطة للآلاف والفاصلة للكسور (2.346,53 تعني 2346.53). أرجع أرقام JSON عادية. الخانة الفارغة = 0. الرصيد المكتوب بجانبه «د» أو بإشارة سالب يكون سالباً، والمكتوب بجانبه «م» يكون موجباً. انسخ الأرقام داخل البيان (عدد الطلبات، مبلغ المسافة، المستوى) كما هي.";

/* ---------- free on-device reading (Tesseract) ----------
   api: {W,H (base image size), rec(kind, rect, scale) -> Promise<{text, lines:[{bbox,words:[{text,bbox}]}]}>, progress(msg)}
   kinds: "page" (eng, whole image, words with boxes), "num" (digits . , - one line), "date" (digits and -), "ara" (Arabic block).
   rect is in base-image pixels; scale = extra upscaling for that pass. */
var CONF={"6":"85","8":"603","5":"6","3":"8","0":"8","1":"7","7":"1","9":"8"};
function cents(t){var s=latin(t).replace(/[−–—]/g,"-"),neg=/-\s*\d/.test(s)||/^\s*-/.test(s),d=s.replace(/\D/g,"");if(!d)return null;var v=parseInt(d,10);return neg?-v:v}
/* candidate values (in cents) with a cost: readings from several passes, plus one confusable-digit swap */
function cands(reads,signed){
  var m={},add=function(v,c){if(v==null)return;var k=String(v);if(m[k]==null||c<m[k])m[k]=c},cnt={};
  reads.forEach(function(r){var v=cents(r);var k=v==null?"e":String(v);cnt[k]=(cnt[k]||0)+1});
  var best=Object.keys(cnt).sort(function(a,b){return cnt[b]-cnt[a]})[0];
  Object.keys(cnt).forEach(function(k){var base=k===best?0:0.4;var v=k==="e"?0:+k;add(v,k==="e"?(best==="e"?0:0.6):base);
    if(k==="e")return;var neg=v<0,d=String(Math.abs(v));
    if(signed)add(-v,base+0.7);
    for(var i=0;i<d.length;i++){var alt=CONF[d[i]];if(!alt)continue;for(var j=0;j<alt.length;j++){var nv=+(d.slice(0,i)+alt[j]+d.slice(i+1));add(neg?-nv:nv,base+1);if(signed)add(neg?nv:-nv,base+1.7)}}
    if(d.length>3)for(i=0;i<d.length;i++){var dv=+(d.slice(0,i)+d.slice(i+1));add(neg?-dv:dv,base+1.2)}});
  if(!signed&&m["0"]==null)add(0,best==="e"?0:2.5);
  return {m:m,best:best==="e"?0:+best}}
function fuzzy(w,t){w=w.toLowerCase().replace(/[^a-z]/g,"");return w===t||(t.length>4&&w.length>=t.length-1&&(w.indexOf(t.slice(0,4))===0||w.indexOf(t.slice(-4))>=0))}
function ocrStatement(api){
  var W=api.W,H=api.H,P=api.progress||function(){};
  P("قراءة شكل الكشف…");
  return api.rec("page",{left:0,top:0,width:W,height:H},1).then(function(pg){
    var words=[];(pg.lines||[]).forEach(function(l){(l.words||[]).forEach(function(w){words.push({t:w.text,x0:w.bbox.x0,x1:w.bbox.x1,y0:w.bbox.y0,y1:w.bbox.y1,cy:(w.bbox.y0+w.bbox.y1)/2})})});
    var hdr={},keys=["balance","credit","debit","doc","description","entry","date"];
    words.forEach(function(w){keys.forEach(function(k){if(!hdr[k]&&fuzzy(w.t,k))hdr[k]=w})});
    var hy=null;["debit","credit","balance","date","entry"].forEach(function(k){if(hdr[k]&&hy==null)hy=hdr[k].y1});
    /* keep header words that sit on the header line */
    if(hy!=null)keys.forEach(function(k){if(hdr[k]&&Math.abs(hdr[k].y1-hy)>H*0.03)delete hdr[k]});
    var R={balance:.115,credit:.253,debit:.374,doc:.475,description:.62,entry:.799,date:.913},X={};
    keys.forEach(function(k){X[k]=hdr[k]?hdr[k].x0:R[k]*W});
    var col={bal:[X.balance-W*.006,X.credit-W*.006],cre:[X.credit-W*.006,X.debit-W*.006],deb:[X.debit-W*.006,X.doc-W*.006],
      desc:[X.doc+W*.045,X.entry-W*.006],date:[X.date-W*.02,W]};
    if(hy==null)hy=H*.33;
    var tot=null;words.forEach(function(w){if(/total/i.test(w.t)&&w.cy>hy&&(!tot||w.cy<tot.cy))tot=w});
    var bottom=tot?tot.y0-H*.005:H;
    /* one anchor per statement line: its date, or its balance (every line has one) */
    var ys=[];words.forEach(function(w){var cx=(w.x0+w.x1)/2;if(w.cy<=hy+H*.01||w.cy>=bottom)return;
      if((cx>col.date[0]&&w.t.replace(/\D/g,"").length>=5)||(cx>col.bal[0]&&cx<col.bal[1]&&/\d[.,]?\d\d\s*$/.test(latin(w.t))))ys.push(w.cy)});
    ys.sort(function(a,b){return a-b});var anchors=[],grp=[];
    ys.forEach(function(y){if(grp.length&&y-grp[0]>H*.025){anchors.push(grp.reduce(function(a,b){return a+b},0)/grp.length);grp=[]}grp.push(y)});
    if(grp.length)anchors.push(grp.reduce(function(a,b){return a+b},0)/grp.length);
    if(!anchors.length)throw {code:"no_rows"};
    var bands=anchors.map(function(c,i){var up=i?(c-anchors[i-1])/2:(anchors.length>1?(anchors[1]-c)/2:H*.05),dn=i<anchors.length-1?(anchors[i+1]-c)/2:up;
      return [Math.max(hy+2,c-up),Math.min(bottom,c+dn)]});
    var out=[],i=0;
    function cell(kind,c,b,sc){return api.rec(kind,{left:Math.max(0,Math.round(c[0])),top:Math.round(b[0]),width:Math.round(Math.min(W,c[1])-Math.max(0,c[0])),height:Math.round(b[1]-b[0])},sc).then(function(r){return (r.text||"").replace(/\s+/g," ").trim()})}
    function nums(c,b){var rs=[];return [1,1.5,2].reduce(function(p,sc){return p.then(function(){return cell("num",c,b,sc).then(function(t){rs.push(t)})})},Promise.resolve()).then(function(){return rs})}
    function next(){if(i>=bands.length)return Promise.resolve();var b=bands[i],o={};P("قراءة السطر "+(i+1)+" من "+bands.length+"…");
      return cell("date",col.date,b,1.5).then(function(t){o.date=t;return cell("ara",col.desc,b,1)}).then(function(t){o.desc=t;return nums(col.deb,b)}).then(function(r){o.dr=r;return nums(col.cre,b)}).then(function(r){o.cr=r;return nums(col.bal,b)}).then(function(r){o.br=r;out.push(o);i++;return next()})}
    var totals=null,meta={name:"",iqama:""},hTop=Math.max(0,(hdr.date||hdr.debit||{y0:hy}).y0-H*.045);
    return cell("ara",[W*.15,W*.75],[0,hTop],1).then(function(t){
      var m=latin(t).match(/([\u0600-\u06FF][\u0600-\u06FF\s]{4,}?)\s*\/\s*(\d[\d\s]{8,})/);
      if(m){meta.name=m[1].replace(/\s+/g," ").trim();meta.iqama=m[2].replace(/\s/g,"")}}).then(next).then(function(){if(!tot)return;var b=[tot.y0-H*.02,tot.y1+H*.02];var t={};
      return nums(col.deb,b).then(function(r){t.dr=r;return nums(col.cre,b)}).then(function(r){t.cr=r;return nums(col.bal,b)}).then(function(r){t.br=r;totals=t})}).then(function(){
      P("مطابقة الأرقام مع تسلسل الرصيد…");var res=solve(out,totals);res.dbg={X:X,col:col,anchors:anchors,hy:hy,raw:out};res.name=meta.name;res.iqama=meta.iqama;
      /* the grade letter (A-F) inside the Arabic salary line is read better by the English model */
      var ri=revenueIndex(res.rows);if(ri<0)return res;
      return cell("page",col.desc,bands[ri],2).then(function(t){var m=t.match(/\(\s*([A-F])/);
        if(m)res.rows[ri].desc=res.rows[ri].desc.replace(/(المستو[ىي]\s*\(\s*)[^)]{0,3}(\s*\))/,"$1"+m[1].toUpperCase()+"$2");return res},function(){return res})})})}

/* pick per-row debit/credit/balance so that balance(i) = balance(i-1) + debit - credit, with the fewest corrections */
function solve(rows,totals){
  var n=rows.length,L=[];
  rows.forEach(function(o){L.push({D:cands(o.dr),C:cands(o.cr),B:cands(o.br,true)})});
  var prev={"0":{c:0,from:null}},trail=[];
  for(var i=0;i<n;i++){var cur={},Li=L[i];
    Object.keys(prev).forEach(function(pk){var pv=+pk,pc=prev[pk].c;
      Object.keys(Li.D.m).forEach(function(dk){var dv=+dk,dc=Li.D.m[dk];if(dv<0)return;
        Object.keys(Li.C.m).forEach(function(ck){var cv=+ck,cc=Li.C.m[ck];if(cv<0||(dv>0&&cv>0))return;
          var b=pv+dv-cv,bc=Li.B.m[String(b)];if(bc==null)return;var tc=pc+dc+cc+bc;
          if(!cur[b]||tc<cur[b].c)cur[b]={c:tc,from:pk,d:dv,cr:cv,ok:true}})})});
    if(!Object.keys(cur).length){/* nothing consistent: keep the raw readings and mark the row */
      var bp=Object.keys(prev).sort(function(a,b){return prev[a].c-prev[b].c})[0],d=Math.max(0,Li.D.best),c=Math.max(0,Li.C.best),b=Li.B.best;
      cur[b]={c:prev[bp].c+10,from:bp,d:d,cr:c,ok:false}}
    trail.push(cur);prev=cur}
  var fin=Object.keys(prev);
  if(totals){var TB=cands(totals.br,true);fin.forEach(function(k){if(TB.m[k]==null)prev[k].c+=3;else prev[k].c+=TB.m[k]})}
  var k=fin.sort(function(a,b){return prev[a].c-prev[b].c})[0],res=[];
  for(i=n-1;i>=0;i--){var st=trail[i][k];res[i]={d:st.d,c:st.cr,b:+k,ok:st.ok};k=st.from}
  var sd=0,sc=0,out=rows.map(function(o,i){var r=res[i],Li=L[i];sd+=r.d;sc+=r.c;
    var fixed=r.ok&&(r.d!==Math.max(0,Li.D.best)||r.c!==Math.max(0,Li.C.best)||r.b!==Li.B.best);
    return {date:fixDate(o.date),desc:o.desc,debit:r.d/100,credit:r.c/100,balance:r.b/100,flag:!r.ok?"bad":fixed?"fixed":""}});
  var T=null;if(totals){var td=cands(totals.dr),tc=cands(totals.cr),tb=cands(totals.br,true);
    T={debit:td.m[sd]!=null,credit:tc.m[sc]!=null,balance:tb.m[res.length?res[res.length-1].b:0]!=null}}
  /* the opening line has its amount in debit or credit only */
  return {rows:out,totals:T}}
function fixDate(t){var d=latin(t).replace(/[^\d]/g,"");if(d.length===8)return d.slice(0,2)+"-"+d.slice(2,4)+"-"+d.slice(4);return latin(t).replace(/[^\d\-\/.:]/g,"").replace(/[.:\/]/g,"-")}

var API={ocrStatement:ocrStatement,solve:solve,cands:cands,num:num,r2:r2,norm:norm,derive:derive,totals:totals,title:title,cleanDesc:cleanDesc,buildZip:buildZip,sheetXml:sheetXml,PROMPT:PROMPT,FIXED:FIXED};
if(typeof module!=="undefined"&&module.exports)module.exports=API;else root.SALC=API;
})(this);
