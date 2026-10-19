# rider portal (fadhel 2026-10-19): riders on leave (riders.st) get only a «إجازة سعيدة» notice; performance notice (month daily avg vs the riders' average on the same days: <85% weak, >=115% hero, else average) and 10-second notice after login listing this month's days with rejected orders above the 2/day allowance (fadhel 2026-10-19)
js=rep(js,'me=cid;portalToData(r.data);ui.msg="";ui0.cs="home";ui.cday=null;render()});','me=cid;portalToData(r.data);ui.msg="";ui0.cs="home";ui.cday=null;render();setTimeout(function(){if(me===cid)deNotice(cid)},2700)});')
js=rep(js,'if(res.rider&&res.rider.category)c.cat=res.rider.category;','if(res.rider&&res.rider.category)c.cat=res.rider.category;if(res.rider&&res.rider.st)c.st={t:res.rider.st,f:res.rider.st_from,u:res.rider.st_until,n:""};')
js=rep(js,'function vSoon(){',r'''/* ---------- rider: rejected-orders notice after login ---------- */
var DEN_T=null,DEN_M={low:["⚠️ تنبيه الأداء","شغلك ضعيف، شد حيلك الله يرضى عليك 🤲","your performance is weak. Please work harder, may God be pleased with you 🤲"],
  mid:["💪 أداؤك متوسط","شغلك متوسط، شد حيلك شوي، أنت ذيبان 💪","your performance is average. Push a little harder, you are a wolf 💪"],
  high:["🏆 أداء ممتاز","أنت ذيبان، استمر 🏆","you are a wolf, keep it up 🏆"]};
function deWeak(id,mon){var md=days().filter(function(d){return d.slice(0,7)===mon&&data.days[d][id]});if(!md.length)return false;
  var a=agg(md.map(function(d){return{d:d,id:id,x:data.days[d][id]}})),sw=0,sn=0;md.forEach(function(d){var x=data.days[d][id];if(x.av!=null&&x.cn){sw+=x.av*x.cn;sn+=x.cn}});
  if(!a.days||!sn||!(sw/sn))return false;var x=(a.cp/a.days)/(sw/sn);return x<.85?"low":x>=1.15?"high":"mid"}
function deLeave(id){var s=data.couriers[id]&&data.couriers[id].st,t=stToday();return s&&s.t==="leave"&&(!s.f||s.f<=t)&&(!s.u||s.u>=t)?s:null}
function deNotice(id){var lv=deLeave(id);if(lv){deShow('<div class="denh">🌴 إجازة سعيدة</div><p class="denw">إجازة سعيدة يا <b>'+esc(cname(id))+'</b>، مشتاقين لك 🤍</p><p class="dene" dir="ltr">Happy vacation, <b>'+esc(cname(id))+'</b>! We miss you 🤍</p>'+(lv.u?'<p class="hint" style="margin:4px 0">إجازتك حتى <span class="num">'+esc(lv.u)+'</span></p>':''),"den-high");return}
  var mon=curMonth(),ds=days().filter(function(d){return d.slice(0,7)===mon&&data.days[d][id]&&deX(data.days[d][id][DE])>0}),lvl=deWeak(id,mon),weak=!!lvl;if(!ds.length&&!weak)return;
  var tot=0,li=ds.map(function(d){var v=+data.days[d][id][DE]||0,x=deX(v);tot+=x;return '<li>'+dl(d)+': رفضت <b class="num">'+v+'</b> طلب، الزائد <b class="num">'+x+'</b></li>'}).join("");
  deShow((weak?'<div class="denh">'+DEN_M[lvl][0]+'</div><p class="denw">يا <b>'+esc(cname(id))+'</b>، '+DEN_M[lvl][1]+'</p><p class="dene" dir="ltr">Hi <b>'+esc(cname(id))+'</b>, '+DEN_M[lvl][2]+'</p>':'')+
    (ds.length?(weak?'<hr>':'')+'<div class="denh">⚠️ تنبيه الطلبات المرفوضة</div><p>'+(weak?'':'يا <b>'+esc(cname(id))+'</b>، ')+'لقد رفضت <b class="num">'+tot+'</b> طلب زيادة عن المسموح (طلبين في اليوم) خلال '+monTxt(mon)+':</p><p class="dene" dir="ltr">'+(weak?'You':'Hi <b>'+esc(cname(id))+'</b>, you')+' rejected <b>'+tot+'</b> orders above the allowed limit (2 per day) this month:</p><ul>'+li+'</ul>':''),ds.length?"":" den-"+lvl)}
function deShow(html,cls){var old=document.getElementById("deN");if(old)old.remove();clearTimeout(DEN_T);
  var el=document.createElement("div");el.id="deN";el.className="den noi18n"+(cls?" "+cls:"");el.setAttribute("role","alert");
  el.innerHTML='<button class="denx" aria-label="إغلاق">×</button>'+html+'<div class="denbar"><i></i></div>';
  document.body.appendChild(el);el.querySelector(".denx").onclick=function(){el.remove()};
  DEN_T=setTimeout(function(){el.remove()},10000)}
function vSoon(){''')
css+='''
.den{position:fixed;z-index:200;top:16px;left:50%;transform:translateX(-50%);width:min(92vw,460px);background:#fff4f2;color:#5a1010;border:2px solid #c62828;border-radius:14px;box-shadow:0 14px 40px rgba(0,0,0,.25);padding:14px 16px 10px;direction:rtl;font-size:15px;animation:denIn .3s ease-out}
.den p{margin:6px 0}.den hr{border:0;border-top:1px solid #f3c5c0;margin:8px 0}.denw{font-size:16.5px}.den-mid{background:#fff8e6;border-color:#c9a24a;color:#5a4210}.den-mid .denh{color:#9a7414}.den-mid .denbar{background:#f1e2b8}.den-mid .denbar i{background:#c9a24a}.den-mid .dene,.den-mid .denx{color:#7a5a10}.den-high{background:#ecf8f1;border-color:#1f8a4c;color:#0f4c2a}.den-high .denh{color:#1f8a4c}.den-high .denbar{background:#c4e8d3}.den-high .denbar i{background:#1f8a4c}.den-high .dene,.den-high .denx{color:#1f6a3c}.dene{text-align:left;font-size:14px;color:#7a2a2a;margin-top:2px!important}.den ul{margin:4px 0 8px;padding-right:20px;max-height:40vh;overflow:auto}.den li{margin:3px 0}
.denh{font-weight:700;font-size:17px;color:#c62828}
.denx{position:absolute;left:10px;top:6px;background:none;border:0;font-size:24px;line-height:1;cursor:pointer;color:#8a1212}
.denbar{height:4px;background:#f3c5c0;border-radius:3px;overflow:hidden}.denbar i{display:block;height:100%;background:#c62828;animation:denBar 10s linear forwards}
@keyframes denBar{from{width:100%}to{width:0}}@keyframes denIn{from{opacity:0;transform:translate(-50%,-12px)}to{opacity:1;transform:translate(-50%,0)}}
'''
