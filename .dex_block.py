# rider portal (fadhel 2026-10-19): weak-performance notice (month daily avg < 85% of the average on the same days) and 10-second notice after login listing this month's days with rejected orders above the 2/day allowance (fadhel 2026-10-19)
js=rep(js,'me=cid;portalToData(r.data);ui.msg="";ui0.cs="home";ui.cday=null;render()});','me=cid;portalToData(r.data);ui.msg="";ui0.cs="home";ui.cday=null;render();setTimeout(function(){if(me===cid)deNotice(cid)},2700)});')
js=rep(js,'function vSoon(){',r'''/* ---------- rider: rejected-orders notice after login ---------- */
var DEN_T=null;
function deWeak(id,mon){var md=days().filter(function(d){return d.slice(0,7)===mon&&data.days[d][id]});if(!md.length)return false;
  var a=agg(md.map(function(d){return{d:d,id:id,x:data.days[d][id]}})),sw=0,sn=0;md.forEach(function(d){var x=data.days[d][id];if(x.av!=null&&x.cn){sw+=x.av*x.cn;sn+=x.cn}});
  if(!a.days||!sn||!(sw/sn))return false;return (a.cp/a.days)/(sw/sn)<.85}
function deNotice(id){var mon=curMonth(),ds=days().filter(function(d){return d.slice(0,7)===mon&&data.days[d][id]&&deX(data.days[d][id][DE])>0}),weak=deWeak(id,mon);if(!ds.length&&!weak)return;
  var tot=0,li=ds.map(function(d){var v=+data.days[d][id][DE]||0,x=deX(v);tot+=x;return '<li>'+dl(d)+': رفضت <b class="num">'+v+'</b> طلب، الزائد <b class="num">'+x+'</b></li>'}).join("");
  var old=document.getElementById("deN");if(old)old.remove();clearTimeout(DEN_T);
  var el=document.createElement("div");el.id="deN";el.className="den noi18n";el.setAttribute("role","alert");
  el.innerHTML='<button class="denx" aria-label="إغلاق">×</button>'+
    (weak?'<div class="denh">⚠️ تنبيه الأداء</div><p class="denw">يا <b>'+esc(cname(id))+'</b>، شغلك ضعيف، شد حيلك الله يرضى عليك 🤲</p><p class="dene" dir="ltr">Hi <b>'+esc(cname(id))+'</b>, your performance is weak. Please work harder, may God be pleased with you 🤲</p>':'')+
    (ds.length?(weak?'<hr>':'')+'<div class="denh">⚠️ تنبيه الطلبات المرفوضة</div><p>'+(weak?'':'يا <b>'+esc(cname(id))+'</b>، ')+'لقد رفضت <b class="num">'+tot+'</b> طلب زيادة عن المسموح (طلبين في اليوم) خلال '+monTxt(mon)+':</p><p class="dene" dir="ltr">'+(weak?'You':'Hi <b>'+esc(cname(id))+'</b>, you')+' rejected <b>'+tot+'</b> orders above the allowed limit (2 per day) this month:</p><ul>'+li+'</ul>':'')+'<div class="denbar"><i></i></div>';
  document.body.appendChild(el);el.querySelector(".denx").onclick=function(){el.remove()};
  DEN_T=setTimeout(function(){el.remove()},10000)}
function vSoon(){''')
css+='''
.den{position:fixed;z-index:200;top:16px;left:50%;transform:translateX(-50%);width:min(92vw,460px);background:#fff4f2;color:#5a1010;border:2px solid #c62828;border-radius:14px;box-shadow:0 14px 40px rgba(0,0,0,.25);padding:14px 16px 10px;direction:rtl;font-size:15px;animation:denIn .3s ease-out}
.den p{margin:6px 0}.den hr{border:0;border-top:1px solid #f3c5c0;margin:8px 0}.denw{font-size:16.5px}.dene{text-align:left;font-size:14px;color:#7a2a2a;margin-top:2px!important}.den ul{margin:4px 0 8px;padding-right:20px;max-height:40vh;overflow:auto}.den li{margin:3px 0}
.denh{font-weight:700;font-size:17px;color:#c62828}
.denx{position:absolute;left:10px;top:6px;background:none;border:0;font-size:24px;line-height:1;cursor:pointer;color:#8a1212}
.denbar{height:4px;background:#f3c5c0;border-radius:3px;overflow:hidden}.denbar i{display:block;height:100%;background:#c62828;animation:denBar 10s linear forwards}
@keyframes denBar{from{width:100%}to{width:0}}@keyframes denIn{from{opacity:0;transform:translate(-50%,-12px)}to{opacity:1;transform:translate(-50%,0)}}
'''
