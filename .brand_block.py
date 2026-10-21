# theme v3 (fadhel 2026-10-21): company letterhead look from his job-application form: DM logo, indigo + orange,
# blue gradient stripe and orange corner triangle in the header band. Replaces theme v2 (teal + amber).
_L3="""  --bg:#eef1f7; --surface:#ffffff; --sunk:#f3f5fa; --fg:#141a33; --muted:#5b6386; --line:#d9deeb;
  --bar:#e8ebf8; --bar-fg:#20386b; --head:#20386b; --head-fg:#ffffff; --menu-sel:#e3e6f6;
  --hint:#c26a0a; --accent:#2b3192; --gold:#f28a1a; --cofg:#2b3192;"""
_D3="""  --bg:#0e1124; --surface:#171b36; --sunk:#12152c; --fg:#eceffd; --muted:#a3a9cf; --line:#2a2f57;
  --bar:#1b2147; --bar-fg:#c9cdff; --head:#1a2350; --head-fg:#f3f4ff; --menu-sel:#262d5e;
  --hint:#ffa04d; --accent:#9ea4ff; --gold:#ff9b33; --cofg:#ff9b33;"""
assert css.count(_L_NEW)==1 and css.count(_D_NEW)==2
css=css.replace(_L_NEW,_L3).replace(_D_NEW,_D3)
for _a,_b in (("#0d3b47","#20386b"),("#14968a","#2b3192"),("#e8a33d","#f28a1a"),("#cfe9e5","#d9ddf3"),("#eef3f4","#eef1f7"),("#e6edef","#e6e9f3"),("#6b7b84","#5b6386"),("#13232b","#141a33"),("#e3f2f0","#e8ebf8"),("#d3ebe7","#e3e6f6")):
    js=js.replace(_a,_b);css=css.replace(_a,_b)
js=rep(js,'''function bar(){var ld=lastDay();return '<div class="coband">''','''function bar(){var ld=lastDay();return '<div class="coband"><img class="colog" src="logo.png" alt="DM">''')
css+='''
.coband{background:var(--surface);overflow:hidden;padding-block:20px 16px;padding-inline:150px;border-bottom:5px solid var(--gold);min-height:92px;align-items:center}
.coband::before{content:"";position:absolute;top:8px;left:0;right:64px;height:4px;background:linear-gradient(90deg,#e6ecf5,#2f4e86 70%,#20386b)}
.coband::after{content:"";position:absolute;top:0;right:0;width:58px;height:50px;background:linear-gradient(135deg,#f6a133,#f28a1a);clip-path:polygon(18% 0,100% 0,100% 100%)}
.colog{position:absolute;left:18px;top:50%;transform:translateY(-45%);height:52px;background:#fff;padding:4px 8px;border-radius:10px}
.coband .coname{color:var(--accent)}
.coband .cosub{color:var(--muted);opacity:1}
.coband .coby{right:72px;color:var(--fg)}.coband .coby b{color:var(--gold)}
.side button[aria-current="true"]{box-shadow:inset -4px 0 0 var(--gold);color:var(--accent)}
@media (max-width:860px){.coband{padding-inline:16px;padding-top:22px}.colog{position:static;transform:none;height:42px;margin-bottom:4px}}
.splash .slogo{display:block;height:64px;margin:0 auto 14px;background:#fff;padding:6px 12px;border-radius:12px}
'''
# ocean header band only (fadhel 2026-10-21: the sea-blue from the company profile cover is for the header, not the whole page)
css+='''
.coband{background:radial-gradient(ellipse at 12% 0%,#1a64ad 0%,transparent 60%),linear-gradient(160deg,#0b3a72 0%,#0a2a55 50%,#071a3a 100%)}
.coband::before{background:linear-gradient(90deg,#3a64a8,#8fb4ff 70%,#ffffff)}
.coband .coname{color:#ffffff}
.coband .cosub{color:#c9d6ee}
.coband .coby{color:#ffffff}.coband .coby b{color:#f7941d}
@media print{.coband{background:#fff}.coband .coname{color:#2b3192}}
'''
# light sidebar tint (fadhel 2026-10-21 asked for a soft colour for the menu); dark mode keeps its navy
css+='''
.side{background:linear-gradient(180deg,#c4d3eb 0%,#aec1e1 100%);border-inline-end-color:#93aad3}
.side button small,.side .navlink small{color:#33406b}.side .co small{color:#33406b}
.side hr{border-color:#93aad3}
.side button:hover,.side .navlink:hover{background:#9fb4da}
.side button[aria-current="true"]{background:#ffffff}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .side{background:var(--surface);border-inline-end-color:var(--line)}:root:not([data-theme="light"]) .side button[aria-current="true"]{background:var(--menu-sel)}:root:not([data-theme="light"]) .side button:hover{background:var(--sunk)}:root:not([data-theme="light"]) .side button small{color:var(--muted)}}
@media print{.side{background:none}}
'''
# page background = fadhel's delivery-city picture with the DM logo painted over the HS badge (bg.jpg, 2026-10-21);
# header and sidebar stay as they are. Light mode only behind the content; print stays white.
css+='''
body{background:#141414 url(bg.jpg) center/cover fixed no-repeat}
.content{background:linear-gradient(rgba(10,12,20,.18),rgba(10,12,20,.18))}
@media print{body{background:#fff!important}.content{background:none}}
.fhint{display:table;margin:-4px auto 0;background:rgba(255,255,255,.94);padding:4px 12px;border-radius:8px}
.rpcnt{background:rgba(255,255,255,.94);color:var(--fg);padding:4px 10px;border-radius:8px}
.splash{background:#111 url(bg.jpg) left top/cover no-repeat}
.splash>div{background:rgba(8,29,61,.82);backdrop-filter:blur(2px)}
'''
js=rep(js,'''<span class="hint">'+RP.rows.length+' مندوب</span>''','''<span class="hint rpcnt">'+RP.rows.length+' مندوب</span>''')
# soft ivory instead of plain white for panels/tables/fields (fadhel 2026-10-21); dark mode keeps its own rule (higher specificity); print stays white
css+='''
:root{--surface:#fbf6ea;--sunk:#f3ecda;--line:#e4d8bd;--bar:#f2ead6;--mid-soft:#ede5d2}
.fhint,.rpcnt{background:rgba(251,246,234,.95)}
@media print{:root{--surface:#fff;--sunk:#f6f6f6;--bar:#fff;--line:#ddd}}
'''
css=css.replace("var(--card,#fff)","var(--surface)");js=js.replace("var(--card,#fff)","var(--surface)")
