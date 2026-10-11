# English toggle (runtime translation of rendered text) + credit line + entry splash (fadhel 2026-10-10)
import json as _json
exec(open('i18n_en.py',encoding='utf8').read())
_ph=sorted(PH.items(),key=lambda kv:-len(kv[0]))
js=rep(js,'function render(){',r'''var LANG=(function(){try{return localStorage.getItem("hs_lang")||"ar"}catch(e){return "ar"}})();
var I18N_EN='''+_json.dumps(EN,ensure_ascii=False)+r''',I18N_PH='''+_json.dumps(_ph,ensure_ascii=False)+r''';
var AR_RE=/[؀-ۿ]/,I18N_PHRE=I18N_PH.map(function(p){return [new RegExp("(^|[\\s()·،,.:«»/\\-])"+p[0].replace(/[.*+?^${}()|[\]\\]/g,"\\$&")+"(?=$|[\\s()·،,.:«»/\\-])","g"),p[1]]});
function trText(s){if(!AR_RE.test(s))return s;var t=s.trim(),k=t.replace(/\s+/g," ");if(I18N_EN[k]!=null)return s.replace(t,I18N_EN[k]);
  var o=s.replace(/يـ(\d+)/g,"D$1");I18N_PHRE.forEach(function(p){o=o.replace(p[0],function(m,a){return a+p[1]})});return o}
var I18N_SKIP={SCRIPT:1,STYLE:1,TEXTAREA:1,OPTION:0};
function trTree(n){if(LANG!=="en"||!n)return;
  if(n.nodeType===3){if(n.parentNode&&(I18N_SKIP[n.parentNode.nodeName]||n.parentNode.closest&&n.parentNode.closest(".shn,.noi18n")))return;var nx=n.nextSibling;if(AR_RE.test(n.nodeValue)&&nx&&nx.nodeName==="BR"&&nx.nextSibling&&/[A-Za-z]/.test(nx.nextSibling.textContent||"")){nx.remove();n.nodeValue="";return}var v=trText(n.nodeValue);if(v!==n.nodeValue)n.nodeValue=v;return}
  if(n.nodeType!==1||I18N_SKIP[n.nodeName])return;
  ["placeholder","aria-label","title"].forEach(function(a){var v=n.getAttribute&&n.getAttribute(a);if(v&&AR_RE.test(v))n.setAttribute(a,trText(v))});
  if(n.nodeName==="INPUT"&&(n.type==="submit"||n.type==="button")&&AR_RE.test(n.value))n.value=trText(n.value);
  for(var c=n.firstChild;c;c=c.nextSibling)trTree(c)}
var I18N_OBS=new MutationObserver(function(ms){if(LANG!=="en")return;I18N_OBS.disconnect();ms.forEach(function(m){if(m.type==="characterData")trTree(m.target);else m.addedNodes.forEach(trTree)});i18nWatch()});
function i18nWatch(){I18N_OBS.observe(document.body,{childList:true,subtree:true,characterData:true})}
var STATIC_AR={};
function applyLang(){var en=LANG==="en";document.documentElement.lang=en?"en":"ar";document.documentElement.dir=en?"ltr":"rtl";document.title=en?"Rider Performance Portal":"بوابة أداء المناديب";
  ["tickerTxt","splashTxt"].forEach(function(id){var el=document.getElementById(id);if(!el)return;if(STATIC_AR[id]==null)STATIC_AR[id]=el.innerHTML;el.innerHTML=en?'Prepared by Eng. <b>Fadhel Al-Omaisi</b>':STATIC_AR[id]});
  var sc=document.getElementById("splashCo");if(sc){if(STATIC_AR.co==null)STATIC_AR.co=sc.textContent;sc.textContent=en?"Al-Daem Al-Mutawwar Logistics Services":STATIC_AR.co}}
function setLang(l){LANG=l;try{localStorage.setItem("hs_lang",l)}catch(e){}applyLang();render()}
function showSplash(ms){var s=document.getElementById("splash");if(!s)return;s.hidden=false;s.classList.remove("out");clearTimeout(showSplash.t);showSplash.t=setTimeout(function(){s.classList.add("out");setTimeout(function(){s.hidden=true},450)},ms||2400)}
var WAS_IN=null;
applyLang();i18nWatch();showSplash(2600);
function render(){''')
# after each render: translate, and greet on sign-in
js=rep(js,'  root.innerHTML=html;','  root.innerHTML=html;trTree(root);\n  var isIn=!!(me||isAdmin||staff);if(WAS_IN===false&&isIn)showSplash(2200);WAS_IN=isIn;')
# language button in the header bar
js=rep(js,"""(roleName()?'<span class="chip">'+esc(roleName())+'</span>':"")+'</header>'}""","""(roleName()?'<span class="chip">'+esc(roleName())+'</span>':"")+'<button class="chip langbtn noi18n" id="langBtn" type="button">'+(LANG==="en"?"العربية":"English")+'</button></header>'}""")
js=rep(js,'  if(t.id==="logout"){','  if(t.id==="langBtn"){setLang(LANG==="en"?"ar":"en");return}\n  if(t.id==="logout"){')
# credit under the company name
js=rep(js,"""<span class="coname">'+esc(data.company||"شركة التشغيل")+'</span>""","""<span class="coname">'+esc(data.company||"شركة التشغيل")+'</span><span class="coby">إعداد المهندس / <b>فاضل العميسي</b></span>""")
css+='''
html[lang=en] body{direction:ltr}html[lang=en] .side small{display:none}
.coband{flex-direction:column;align-items:center;gap:2px}
.coband{position:relative}
.coby{position:absolute;right:20px;top:50%;transform:translateY(-50%);font-size:16.5px;font-weight:600;color:var(--head-fg);white-space:nowrap;text-align:right}.coby b{color:var(--gold);font-weight:700}
@media (max-width:860px){.coby{position:static;transform:none;align-self:stretch;text-align:right;font-size:15px;margin-top:4px}}
.langbtn{border:1px solid color-mix(in srgb,var(--bar-fg) 30%,transparent);cursor:pointer;font:600 13px/1.4 var(--f-body,system-ui);color:var(--bar-fg)}
.langbtn:hover{background:var(--surface)}
.splash{position:fixed;inset:0;z-index:100;display:grid;place-items:center;background:color-mix(in srgb,var(--head) 94%,transparent);transition:opacity .45s ease}
.splash.out{opacity:0}
.splash>div{text-align:center;padding:28px 34px;border-radius:14px;border:1px solid color-mix(in srgb,var(--gold) 55%,transparent);background:color-mix(in srgb,var(--head) 70%,#000 0%);box-shadow:0 10px 40px rgba(0,0,0,.35);animation:spin .6s ease both}
.splash .sco{display:block;font-family:var(--f-display,inherit);font-weight:700;font-size:clamp(20px,4vw,30px);color:var(--gold);margin-bottom:10px}
.splash .sby{display:block;font-size:clamp(15px,2.6vw,19px);color:var(--head-fg)}.splash .sby b{color:var(--gold)}
@keyframes spin{from{opacity:0;transform:translateY(10px) scale(.97)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){.splash>div{animation:none}.splash{transition:none}}
@media print{.splash,.langbtn{display:none!important}}
'''
