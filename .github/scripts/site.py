"""Writes the mods' index page into site/: each mod's thumbnail, name, version, author, what it
needs, its description, and the download of its latest release.

    python3 .github/scripts/site.py
"""

import html
import shutil

from mods import ROOT, REPOSITORY, all_mods, git

SITE = ROOT / "site"

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OpenReliant mods</title>
<meta name="description" content="Mods for OpenReliant, checked to work and to be free to share.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #07080c; --card: #10131b; --card-edge: #232938; --text: #e8eaf0; --muted: #9aa3b5;
  --accent: #f08a2c; --accent-dim: #8a4a14; --red: #c8352a;
  --display: "Rajdhani", system-ui, sans-serif;
  /* The display's corner brackets, as round the wing's icons: four short orange corners. */
  --brackets:
    linear-gradient(var(--accent), var(--accent)) top left / 18px 2px,
    linear-gradient(var(--accent), var(--accent)) top left / 2px 18px,
    linear-gradient(var(--accent), var(--accent)) top right / 18px 2px,
    linear-gradient(var(--accent), var(--accent)) top right / 2px 18px,
    linear-gradient(var(--accent), var(--accent)) bottom left / 18px 2px,
    linear-gradient(var(--accent), var(--accent)) bottom left / 2px 18px,
    linear-gradient(var(--accent), var(--accent)) bottom right / 18px 2px,
    linear-gradient(var(--accent), var(--accent)) bottom right / 2px 18px;
  /* A panel with its corners cut, as the game's windows have. */
  --cut: polygon(12px 0, 100% 0, 100% calc(100% - 12px), calc(100% - 12px) 100%, 0 100%, 0 12px);
}}
* {{ box-sizing: border-box; }}
html {{ background: var(--bg); }}
body {{
  margin: 0; color: var(--text); font: 16px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif;
  background:
    radial-gradient(1px 1px at 12% 18%, #fff8 50%, transparent 51%),
    radial-gradient(1px 1px at 72% 9%, #fff6 50%, transparent 51%),
    radial-gradient(1px 1px at 38% 62%, #fff5 50%, transparent 51%),
    radial-gradient(1px 1px at 88% 44%, #fff7 50%, transparent 51%),
    radial-gradient(1px 1px at 55% 88%, #fff4 50%, transparent 51%),
    radial-gradient(1.5px 1.5px at 25% 80%, #fff6 50%, transparent 51%),
    radial-gradient(ellipse at 80% -10%, #3a1d0c 0%, transparent 55%),
    radial-gradient(ellipse at -10% 110%, #101a3a 0%, transparent 50%),
    var(--bg);
  background-attachment: fixed; min-height: 100vh;
}}
main {{ max-width: 1000px; margin: 0 auto; padding: 48px 16px 64px; }}
header {{ margin-bottom: 36px; }}
.eyebrow {{ font-family: var(--display); color: var(--accent); letter-spacing: 0.3em; font-size: 15px; font-weight: 700; text-transform: uppercase; }}
h1 {{ font-family: var(--display); margin: 2px 0 10px; font-size: clamp(34px, 7vw, 54px); line-height: 1; letter-spacing: 0.06em; text-transform: uppercase; font-weight: 700; }}
header p {{ margin: 0; max-width: 640px; color: var(--muted); font-size: 17px; }}
a {{ color: var(--accent); text-underline-offset: 2px; }}
.mod {{
  display: grid; grid-template-columns: 340px 1fr; gap: 24px; padding: 22px; margin-bottom: 22px;
  background: var(--brackets), linear-gradient(180deg, #141824, var(--card));
  background-repeat: no-repeat; box-shadow: inset 0 0 0 1px var(--card-edge);
}}
.shot {{ position: relative; }}
.shot img {{ display: block; width: 100%; aspect-ratio: 4 / 3; object-fit: cover; background: #000; clip-path: var(--cut); }}
.mod h2 {{ font-family: var(--display); margin: 0 0 8px; font-size: 30px; line-height: 1.1; letter-spacing: 0.05em; text-transform: uppercase; font-weight: 700; }}
.badges {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 14px; }}
.badge {{ font-family: var(--display); font-weight: 600; font-size: 14px; letter-spacing: 0.06em; text-transform: uppercase; padding: 2px 10px; border: 1px solid var(--card-edge); color: var(--muted); background: #0b0e15; }}
.badge.version {{ color: var(--accent); border-color: var(--accent-dim); }}
.description {{ margin: 0 0 18px; overflow-wrap: anywhere; color: #cfd3dd; }}
.download {{
  display: inline-block; background: var(--accent); color: #140a02; font-family: var(--display);
  font-size: 18px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
  text-decoration: none; padding: 9px 22px; clip-path: var(--cut);
}}
.download:hover {{ background: #ff9d45; }}
.links {{ margin-top: 12px; font-size: 14px; color: var(--muted); }}
.links a {{ margin-right: 14px; }}
.unreleased {{ color: var(--muted); font-style: italic; margin: 0; }}
.install {{
  margin-top: 36px; padding: 18px 22px; border-left: 3px solid var(--accent); background: #0e111a; color: #cfd3dd;
}}
.install h3 {{ font-family: var(--display); margin: 0 0 6px; font-size: 18px; text-transform: uppercase; letter-spacing: 0.14em; color: var(--accent); }}
.install p {{ margin: 0; }}
code {{ background: #1a1f2c; padding: 1px 6px; border-radius: 4px; font-size: 14px; }}
footer {{ color: var(--muted); font-size: 14px; margin-top: 28px; }}
@media (max-width: 760px) {{ .mod {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<main>
<header>
<div class="eyebrow">OpenReliant</div>
<h1>Mods</h1>
<p>Mods for <a href="https://github.com/OpenReliant/openreliant">OpenReliant</a>, checked to work and to be free to share. You need OpenReliant and your own copy of StarLancer.</p>
</header>
{mods}
<section class="install">
<h3>Installing a mod</h3>
<p>Download its <code>.hog</code> file and its <code>.hog.sha256</code> file, put both in the <code>mods</code> folder of your game folder, next to <code>resource.hog</code>, and turn the mod on in OpenReliant's mods screen. OpenReliant checks the archive against its checksum as it loads it.</p>
</section>
<footer>
<p><a href="https://github.com/{repository}">The mods' sources</a>, with each mod's credits and licence. Updated {updated}.</p>
</footer>
</main>
</body>
</html>
"""


def card(mod) -> str:
    text = html.escape
    picture = f'<img src="thumbs/{text(mod.id)}.png" alt="{text(mod.name)}">' if mod.thumbnail else '<img alt="">'
    badges = [f'<span class="badge version">Version {text(mod.version)}</span>' if mod.version else "",
              f'<span class="badge">by {text(mod.author)}</span>' if mod.author else "",
              f'<span class="badge">Needs OpenReliant {text(mod.needs)}</span>' if mod.needs else ""]
    licence = f'<a href="https://github.com/{REPOSITORY}/blob/main/mods/{text(mod.id)}/license.txt">Credits and licence</a>'
    if mod.released():
        download = (f'<a class="download" href="{text(mod.download())}">Download {text(mod.archive)}</a>'
                    f'<div class="links"><a href="{text(mod.download())}.sha256">Checksum</a>'
                    f'<a href="{text(mod.release_page())}">Release notes</a>{licence}</div>')
    else:
        download = f'<p class="unreleased">Not released yet.</p><div class="links">{licence}</div>'
    return (f'<article class="mod"><div class="shot">{picture}</div><div><h2>{text(mod.name)}</h2>'
            f'<div class="badges">{"".join(badges)}</div>'
            f'<p class="description">{text(mod.description)}</p>{download}</div></article>')


def main() -> None:
    shutil.rmtree(SITE, ignore_errors=True)
    (SITE / "thumbs").mkdir(parents=True)
    mods = all_mods()
    for mod in mods:
        if mod.thumbnail:
            shutil.copy(mod.thumbnail, SITE / "thumbs" / f"{mod.id}.png")
    updated = git("log", "-1", "--format=%cs")
    page = PAGE.format(mods="\n".join(card(mod) for mod in mods), repository=REPOSITORY, updated=updated)
    (SITE / "index.html").write_text(page, encoding="utf-8")
    print(f"wrote {SITE / 'index.html'}: {len(mods)} mods")


if __name__ == "__main__":
    main()
