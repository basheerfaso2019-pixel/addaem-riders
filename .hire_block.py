# «طلب توظيف مندوب»: fadhel's job-application form generator (hiring.html) as a manager tab (fadhel 2026-10-21).
# The iframe lives outside #root so re-renders don't reload it (attachments are kept in memory only).
# Owner national ID is not in the public file: it comes from private_settings (admin-only RLS) via window.HIRE_CFG.
js=rep(js,'بطاقات المناديب<small>Rider ID Cards</small></button>','بطاقات المناديب<small>Rider ID Cards</small></button><button data-tab="hire" aria-current="\'+(view==="hire")+\'">طلب توظيف مندوب<small>Job Application</small></button>')
js=rep(js,'cards:isAdmin&&vCards,','cards:isAdmin&&vCards,hire:isAdmin&&vHire,')
js=rep(js,'view!=="sheet"&&view!=="cards"&&!canSee(view)','view!=="sheet"&&view!=="cards"&&view!=="hire"&&!canSee(view)')
js=rep(js,'view==="perm"||view==="sheet"||view==="cards")?vCourier:vSoon;','view==="perm"||view==="sheet"||view==="cards"||view==="hire")?vCourier:vSoon;')
js=rep(js,'TITLES.cards="بطاقات المناديب";','TITLES.cards="بطاقات المناديب";TITLES.hire="طلب توظيف مندوب";')
js=rep(js,'function vSoon(){',r'''/* ---------- job application form ---------- */
var HIRE={st:0,fr:null};
function hireLoad(){if(HIRE.st)return;HIRE.st=1;
  sb.from("private_settings").select("key,value").in("key",["hire_owner_id","hire_owner"]).then(function(r){var o={};(r.data||[]).forEach(function(x){if(x.key==="hire_owner_id")o.note_owner_id=x.value;if(x.key==="hire_owner")o.note_owner=x.value});window.HIRE_CFG=o;HIRE.st=2},function(){window.HIRE_CFG={};HIRE.st=2})}
function hirePos(){var s=document.getElementById("hireSlot"),f=HIRE.fr;
  if(!isAdmin){if(f){f.remove();HIRE.fr=null;HIRE.st=0;window.HIRE_CFG=null}return}
  if(!s){if(f)f.style.display="none";return}
  if(!f){if(HIRE.st!==2)return;f=HIRE.fr=document.createElement("iframe");f.src="hiring.html";f.title="طلب توظيف مندوب";f.className="hiref";document.body.appendChild(f)}
  var b=s.getBoundingClientRect();f.style.display="block";f.style.top=(b.top+window.scrollY)+"px";f.style.left=(b.left+window.scrollX)+"px";f.style.width=b.width+"px";f.style.height=b.height+"px"}
setInterval(hirePos,200);window.addEventListener("resize",hirePos);
function vHire(){hireLoad();setTimeout(hirePos,0);return '<div id="hireSlot" class="hires"><p class="hint" style="padding:16px">جارٍ فتح النموذج…</p></div>'}
function vSoon(){''')
css+='\n.hires{height:calc(100vh - 150px);min-height:540px;border:1px solid var(--line);border-radius:14px}.hiref{position:absolute;z-index:4;border:0;border-radius:14px;background:#fff;display:none}\n'
js=rep(js,'"sheet_extra","tga_codes"],bk={};','"sheet_extra","tga_codes","private_settings"],bk={};')
js=rep(js,'sheet_extra:"month,rider_id",tga_codes:"id"};\n  BK_T.reduce','sheet_extra:"month,rider_id",tga_codes:"id",private_settings:"key"};\n  BK_T.reduce')
