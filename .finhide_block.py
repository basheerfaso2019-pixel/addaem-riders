# hide the performance summary (ملخص الأداء) and fuel amounts everywhere; the wallet stays (fadhel 2026-10-15)
# rider portal: tile, export button and the statement view
js=rep(js,'(function(){var st=!stmtBlock(id)&&stmtCalc(id);return st?tile("stmt","ملخص الأداء",money(st.total),"مستحقات "+monLabel(st.mon)):""})()','""')
js=rep(js,'''(cs!=="stmt"&&!stmtBlock(id)?'<button class="btn pri" data-cs="stmt">تصدير ملخص الأداء</button>':"")''','""')
js=rep(js,'if(cs==="stmt"){','if(false){')
# manager: riders table column, rider panel button and the statement panel
js=rep(js,'<th>ملخص الأداء</th>','')
js=rep(js,'''<td><button class="btn" style="padding:4px 10px;font-size:12.5px;white-space:nowrap" data-stmt="'+esc(a.id)+'">ملخص الأداء</button></td>''','')
js=rep(js,'colspan="19"','colspan="18"')
js=rep(js,'''<button class="btn pri" data-stmt="'+esc(id)+'">تصدير ملخص الأداء</button>''','')
js=rep(js,"rdQuality(id)+stmtPanel(id);}","rdQuality(id);}")
# performance sheet: no fuel column, total, hint, fuel-card panel or Excel values
js=rep(js,'<th>البنزين</th>','')
js=rep(js,'''<td><input class="shin num" inputmode="decimal" data-shf="'+esc(r.id)+'" value="'+(r.f==null?"":r.f)+'"></td>''','')
js=rep(js,'''<td class="num">'+fmt(tot("f"))+'</td>''','')
js=rep(js,'. البنزين والملاحظة تكتبها هنا وتُحفظ تلقائياً.</p>','. الملاحظة تكتبها هنا وتُحفظ تلقائياً.</p>')
js=rep(js,'colspan="45"','colspan="44"')
js=rep(js,"</table></div></section>'+fuelPanel(mon);","</table></div></section>';")
js=rep(js,'xc("AR"+R,18,r.f)','xc("AR"+R,18,null)')
