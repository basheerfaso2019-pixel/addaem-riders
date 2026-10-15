# category column (الفئة) next to the name in every manager table that lists riders (fadhel 2026-10-15)
js=rep(js,'function vSoon(){','''function catOf(id){var c=data.couriers&&data.couriers[id];if(!c)return "";if(c.rg)return "الرياض";return normCat(c.cat)||""}
function addCatCols(){if(view==="courier")return;var root=document.getElementById("root");if(!root)return;
  [].forEach.call(root.querySelectorAll("table"),function(tb){if(tb.closest(".shtbl")||tb.dataset.catdone)return;var hr=tb.querySelector("thead tr:last-child");if(!hr)return;
    var ths=[].slice.call(hr.children),txt=ths.map(function(th){return th.textContent.trim()});
    if(txt.some(function(t){return /^الفئة/.test(t)}))return;
    var ni=txt.findIndex(function(t){return /^الا?سم|^الأسم/.test(t)}),ii=txt.findIndex(function(t){return /^Rider Id/i.test(t)});if(ni<0||ii<0)return;
    tb.dataset.catdone=1;var th=document.createElement("th");th.textContent="الفئة";ths[ni].after(th);
    [].forEach.call(tb.querySelectorAll("tbody tr, tfoot tr"),function(tr){var tds=tr.children;
      if(tds.length===1&&tds[0].colSpan>1){tds[0].colSpan+=1;return}
      if(tds.length!==ths.length){if(tds[ni])tds[ni].after(document.createElement("td"));return}
      var id=(tds[ii].textContent||"").replace(/\\D/g,""),c=catOf(id),td=document.createElement("td");
      if(c){var s=document.createElement("span");s.className="catp cat-"+(c==="أ"?"a":c==="ب"?"b":c==="خ"?"k":"r");s.textContent=c;td.appendChild(s)}
      tds[ni].after(td)})})}
var _renderC=render;render=function(){var r=_renderC.apply(this,arguments);try{addCatCols()}catch(e){}return r};
function vSoon(){''')
css+='''
.catp{display:inline-block;min-width:22px;padding:1px 7px;border-radius:10px;font-weight:700;font-size:12.5px;text-align:center}
.catp.cat-a{background:#ffd966;color:#5a4500}.catp.cat-b{background:#a9d08e;color:#274e13}.catp.cat-k{background:#f4b183;color:#7a2e00}.catp.cat-r{background:#bdd7ee;color:#1f3864}
'''
