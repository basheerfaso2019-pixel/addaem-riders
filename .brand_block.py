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
# ocean background (fadhel 2026-10-21, from the company profile cover): deep sea-blue page in both modes, navy panels,
# white text and orange accents. Print keeps the light letterhead colours.
_OC="""  --bg:#0a2a55; --surface:#0f2b55; --sunk:#0c2449; --fg:#eef3ff; --muted:#a9bbd8; --line:#23457a;
  --bar:#0c3166; --bar-fg:#ffffff; --head:#081d3d; --head-fg:#ffffff; --menu-sel:#173f74;
  --hint:#ffa04d; --accent:#8fb4ff; --gold:#f7941d; --cofg:#f7941d;"""
_LG="  --good:#2b7a4b; --good-soft:#ddf0e4; --warn:#9b5d08; --warn-soft:#f7e8cd; --bad:#b5362f; --bad-soft:#f8dedc; --mid-soft:#ececea;"
_DG="  --good:#64c48e; --good-soft:#18301f; --warn:#e6a64e; --warn-soft:#3a2b14; --bad:#ef7d75; --bad-soft:#3d1d1b; --mid-soft:#262a30; color-scheme:dark"
assert css.count(_L3)==1 and css.count(_D3)==2 and css.count(_LG)==1 and css.count(_DG)==2
css=css.replace(_L3,_OC).replace(_D3,_OC).replace(_LG,_DG.replace("#262a30","#1a3561")+";").replace("--mid-soft:#262a30","--mid-soft:#1a3561")
css+='''
body{background:radial-gradient(ellipse at 15% 0%,#14589c 0%,transparent 55%),linear-gradient(160deg,#0b3a72 0%,#0a2a55 45%,#071a3a 100%) fixed #0a2a55}
.coband::before{background:linear-gradient(90deg,#3a64a8,#8fb4ff 70%,#ffffff)}
.side{background:color-mix(in srgb,var(--surface) 88%,transparent)}
@media print{:root{'''+_L3.replace("\n"," ")+_LG+''' color-scheme:light}body{background:#fff!important}}
'''
css=css.replace("var(--card,#fff)","var(--surface)");js=js.replace("var(--card,#fff)","var(--surface)")
