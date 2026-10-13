# menu items with no data yet (class soon) go to the bottom of the menu, above sign out (fadhel 2026-10-13)
js=rep(js,'''  return '<nav class="side">'+co+items.map(function(m){return '<button data-tab="'+m[0]+'" aria-current="'+(view===m[0])+'"'+(m[3]?' class="soon"':"")+'>'+m[1]+'<small>'+m[2]+'</small></button>'}).join("")+extra+'</nav>';''',
'''  var mb=function(m){return '<button data-tab="'+m[0]+'" aria-current="'+(view===m[0])+'"'+(m[3]?' class="soon"':"")+'>'+m[1]+'<small>'+m[2]+'</small></button>'},soon=items.filter(function(m){return m[3]}).map(mb).join(""),out='<button id="staffOut">';
  if(soon)extra=extra.replace(out,'<hr>'+soon+out);
  return '<nav class="side">'+co+items.filter(function(m){return !m[3]}).map(mb).join("")+extra+'</nav>';''')
