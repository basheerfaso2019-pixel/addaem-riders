# hide the performance summary (ملخص الأداء) everywhere; wallet and fuel stay (fadhel 2026-10-15)
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
