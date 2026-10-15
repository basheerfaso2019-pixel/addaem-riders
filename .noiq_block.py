# riders outside sponsorship (no Iqama on file) log in with their ID only (fadhel 2026-10-15)
js=rep(js,'<label>رقم الإقامة<input id="iq" inputmode="numeric" maxlength="10" required></label>','<label>رقم الإقامة<input id="iq" inputmode="numeric" maxlength="10"><small class="iqhint">مناديب خارج الكفالة: اترك هذه الخانة فارغة وادخل برقم الـ ID فقط</small></label>')
js=rep(js,'"أدخل رقم الإقامة ورقم الـ ID الخاص بك في هنقرستيشن."','"أدخل رقم الإقامة ورقم الـ ID الخاص بك في هنقرستيشن. مناديب خارج الكفالة يدخلون برقم الـ ID فقط."')
js=rep(js,':"رقم الإقامة أو الـ ID غير صحيح، أو لم يُسجَّل رقم إقامتك بعد."}',':"رقم الإقامة أو الـ ID غير صحيح."}')
css+='''
.iqhint{display:block;font-size:12px;font-weight:400;color:var(--muted,#6b7280);margin-top:4px}
'''
