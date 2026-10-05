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
<style>
:root {{ --bg: #0b0d12; --card: #151922; --text: #e6e8ee; --muted: #9aa3b5; --accent: #e8792b; --line: #262c39; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--text); font: 16px/1.5 system-ui, sans-serif; }}
main {{ max-width: 980px; margin: 0 auto; padding: 32px 16px 64px; }}
h1 {{ margin: 0 0 4px; font-size: 28px; }}
header p {{ margin: 0 0 28px; color: var(--muted); }}
a {{ color: var(--accent); }}
.mod {{ display: grid; grid-template-columns: 320px 1fr; gap: 20px; background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 16px; margin-bottom: 16px; }}
.mod img {{ width: 100%; aspect-ratio: 4 / 3; object-fit: cover; border-radius: 6px; background: #000; }}
.mod h2 {{ margin: 0; font-size: 22px; }}
.meta {{ color: var(--muted); font-size: 14px; margin: 4px 0 12px; }}
.description {{ margin: 0 0 14px; overflow-wrap: anywhere; }}
.download {{ display: inline-block; background: var(--accent); color: #111; font-weight: 600; text-decoration: none; padding: 8px 14px; border-radius: 6px; }}
.links {{ margin-top: 10px; font-size: 14px; }}
.unreleased {{ color: var(--muted); font-style: italic; }}
footer {{ color: var(--muted); font-size: 14px; margin-top: 32px; }}
@media (max-width: 700px) {{ .mod {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<main>
<header>
<h1>OpenReliant mods</h1>
<p>Mods for <a href="https://github.com/OpenReliant/openreliant">OpenReliant</a>, checked to work and to be free to share. You need OpenReliant and your own copy of StarLancer.</p>
</header>
{mods}
<footer>
<p>To install a mod, put its <code>.hog</code> file and its <code>.hog.sha256</code> file in the <code>mods</code> folder of your game folder, next to <code>resource.hog</code>, and turn it on in OpenReliant's mods screen.</p>
<p><a href="https://github.com/{repository}">The mods' sources</a>, with each mod's credits and licence. Updated {updated}.</p>
</footer>
</main>
</body>
</html>
"""


def card(mod) -> str:
    text = html.escape
    picture = f'<img src="thumbs/{text(mod.id)}.png" alt="{text(mod.name)}">' if mod.thumbnail else '<img alt="">'
    meta = [f"Version {text(mod.version)}" if mod.version else "", f"by {text(mod.author)}" if mod.author else "",
            f"needs OpenReliant {text(mod.needs)}" if mod.needs else ""]
    if mod.released():
        download = (f'<a class="download" href="{text(mod.download())}">Download {text(mod.archive)}</a>'
                    f'<div class="links"><a href="{text(mod.download())}.sha256">Checksum</a> · '
                    f'<a href="{text(mod.release_page())}">Release notes</a> · ')
    else:
        download = '<p class="unreleased">Not released yet.</p><div class="links">'
    download += f'<a href="https://github.com/{REPOSITORY}/blob/main/mods/{text(mod.id)}/license.txt">Credits and licence</a></div>'
    return (f'<article class="mod">{picture}<div><h2>{text(mod.name)}</h2>'
            f'<div class="meta">{" · ".join(part for part in meta if part)}</div>'
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
