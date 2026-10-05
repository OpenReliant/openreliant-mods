"""Writes the mods' index page into site/: each mod's thumbnail, name, version, author, what it
needs, its description, and the download of its latest release.

    python3 .github/scripts/site.py
"""

from __future__ import annotations

import html
import json
import shutil
import subprocess

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
/* Newtown, by Roger White, from Roger's Fonts: the face OpenReliant draws the game's menus in, from
   the OpenReliant website on the same host. */
@font-face {{ font-family: "Newtown"; src: url("/openreliant/fonts/Newtown.ttf") format("truetype"); font-display: swap; }}
:root {{
  --bg: #07080c; --card: #10131b; --card-edge: #232938; --text: #e8eaf0; --muted: #9aa3b5;
  --accent: #f08a2c; --accent-dim: #8a4a14; --red: #c8352a;
  --display: "Rajdhani", system-ui, sans-serif;
  --title: "Newtown", "Rajdhani", system-ui, sans-serif;
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
main {{ max-width: 1000px; margin: 0 auto; padding: 0 16px 64px; }}
nav {{ display: flex; justify-content: space-between; align-items: center; padding: 20px 0 36px; font-family: var(--display); font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; }}
nav .brand {{ color: var(--text); text-decoration: none; font-family: var(--title); font-weight: normal; font-size: 19px; letter-spacing: 0.03em; }}
nav .brand span, nav .links a.current {{ color: var(--accent); }}
nav .links a {{ color: var(--muted); text-decoration: none; margin-left: 22px; font-size: 15px; }}
nav .links a:hover {{ color: var(--accent); }}
@media (max-width: 520px) {{ nav .links a:not(.keep) {{ display: none; }} }}
header {{ margin-bottom: 36px; }}
h1 {{ font-family: var(--title); margin: 2px 0 10px; font-size: clamp(34px, 7vw, 54px); line-height: 1; letter-spacing: 0.02em; text-transform: uppercase; font-weight: normal; }}
header p {{ margin: 0; max-width: 640px; color: var(--muted); font-size: 17px; }}
a {{ color: var(--accent); text-underline-offset: 2px; }}
.mod {{
  display: grid; grid-template-columns: 340px 1fr; gap: 24px; padding: 22px; margin-bottom: 22px;
  background: var(--brackets), linear-gradient(180deg, #141824, var(--card));
  background-repeat: no-repeat; box-shadow: inset 0 0 0 1px var(--card-edge);
}}
.shot {{ position: relative; }}
.shot img {{ display: block; width: 100%; aspect-ratio: 4 / 3; object-fit: cover; background: #000; clip-path: var(--cut); }}
.mod h2 {{ font-family: var(--title); margin: 0 0 8px; font-size: 28px; line-height: 1.1; letter-spacing: 0.03em; text-transform: uppercase; font-weight: normal; }}
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
.engine {{
  margin-bottom: 30px; padding: 20px 22px; background: var(--brackets), #0e111a;
  background-repeat: no-repeat; box-shadow: inset 0 0 0 1px var(--card-edge);
}}
.engine h2 {{ font-family: var(--title); margin: 0 0 4px; font-size: 22px; letter-spacing: 0.04em; text-transform: uppercase; font-weight: normal; }}
.engine h2 span {{ color: var(--accent); }}
.engine p {{ margin: 0 0 14px; color: var(--muted); font-size: 14px; }}
.builds {{ display: flex; flex-wrap: wrap; gap: 10px; }}
.build {{
  font-family: var(--display); font-weight: 600; font-size: 16px; letter-spacing: 0.05em; text-transform: uppercase;
  text-decoration: none; color: var(--text); padding: 7px 14px; border: 1px solid var(--card-edge); background: #141824;
  clip-path: var(--cut);
}}
.build:hover {{ border-color: var(--accent-dim); color: var(--accent); }}
.build.yours {{ background: var(--accent); color: #140a02; border-color: var(--accent); }}
.build.yours::before {{ content: "For this computer: "; }}
.badge.waiting {{ color: #e6b24a; border-color: #6b5212; }}
.install {{
  margin-top: 36px; padding: 18px 22px; border-left: 3px solid var(--accent); background: #0e111a; color: #cfd3dd;
}}
.install h3 {{ font-family: var(--title); margin: 0 0 6px; font-size: 17px; text-transform: uppercase; letter-spacing: 0.04em; font-weight: normal; color: var(--accent); }}
.install p {{ margin: 0; }}
code {{ background: #1a1f2c; padding: 1px 6px; border-radius: 4px; font-size: 14px; }}
footer {{ color: var(--muted); font-size: 14px; margin-top: 28px; }}
@media (max-width: 760px) {{ .mod {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<main>
<nav>
<a class="brand" href="https://openreliant.github.io/openreliant/">Open<span>Reliant</span></a>
<div class="links">
<a class="keep" href="https://openreliant.github.io/openreliant/#download">Download</a>
<a href="https://openreliant.github.io/openreliant/docs/">Docs</a>
<a class="keep current" href="./">Mods</a>
<a href="https://github.com/OpenReliant/openreliant-mods">GitHub</a>
</div>
</nav>
<header>
<h1>Mods</h1>
<p>Mods for <a href="https://openreliant.github.io/openreliant/">OpenReliant</a>, checked to work and to be free to share. You need OpenReliant and your own copy of StarLancer.</p>
</header>
{engine}
{mods}
<section class="install">
<h3>Installing a mod</h3>
<p>Download its <code>.hog</code> file and its <code>.hog.sha256</code> file, put both in the <code>mods</code> folder of your game folder, next to <code>resource.hog</code>, and turn the mod on in OpenReliant's mods screen. OpenReliant checks the archive against its checksum as it loads it.</p>
</section>
<footer>
<p><a href="https://github.com/{repository}">The mods' sources</a>, with each mod's credits and licence. Updated {updated}. Headings are set in Newtown, by Roger White, from Roger's Fonts.</p>
</footer>
</main>
<script>
// Puts the build for this computer first and lights it: the system from the user agent, the
// processor from the browser where it says, else the usual one (Apple silicon on a Mac).
(function () {{
  const agent = navigator.userAgent;
  const system = /Windows/.test(agent) ? "windows" : /Mac/.test(agent) ? "macos" : /Linux|X11/.test(agent) && !/Android/.test(agent) ? "linux" : null;
  if (!system) return;
  const light = (processor) => {{
    const build = document.querySelector(`.build[data-build="${{system}}-${{processor}}"]`);
    if (!build) return;
    document.querySelectorAll(".build.yours").forEach((other) => other.classList.remove("yours"));
    build.classList.add("yours");
    build.parentElement.prepend(build);
  }};
  light(system === "macos" ? "aarch64" : "x86_64");
  if (navigator.userAgentData && navigator.userAgentData.getHighEntropyValues) {{
    navigator.userAgentData.getHighEntropyValues(["architecture"]).then((values) => {{
      if (values.architecture === "arm") light("aarch64");
      else if (values.architecture === "x86") light("x86_64");
    }}).catch(() => {{}});
  }}
}})();
</script>
</body>
</html>
"""


# OpenReliant's builds, in the order the page lists them, by the name in each archive.
BUILDS = [
    ("windows-x86_64", "Windows"), ("windows-aarch64", "Windows on Arm"),
    ("macos-aarch64", "macOS, Apple silicon"), ("macos-x86_64", "macOS, Intel"),
    ("linux-x86_64", "Linux"), ("linux-aarch64", "Linux on Arm"),
]


def latest_openreliant() -> dict | None:
    """OpenReliant's latest release: its version, page, date and archives; None where it can't be
    read."""
    try:
        found = subprocess.run(
            ["gh", "release", "view", "--repo", "OpenReliant/openreliant", "--json", "tagName,url,publishedAt,assets"],
            check=True, capture_output=True, text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return json.loads(found)


def version_tuple(text: str) -> tuple[int, ...]:
    return tuple(int(part) for part in text.lstrip("v").split(".") if part.isdigit())


def engine_panel(release: dict | None) -> str:
    text = html.escape
    if not release:
        return ('<section class="engine"><h2>Get <span>OpenReliant</span></h2>'
                '<p><a href="https://github.com/OpenReliant/openreliant/releases/latest">Download the latest release</a>.</p></section>')
    archives = {asset["name"]: asset["url"] for asset in release["assets"]}
    links = []
    for key, label in BUILDS:
        found = next((url for name, url in archives.items() if f"-{key}." in name), None)
        if found:
            links.append(f'<a class="build" data-build="{key}" href="{text(found)}">{text(label)}</a>')
    return (f'<section class="engine"><h2>Get <span>OpenReliant {text(release["tagName"].lstrip("v"))}</span></h2>'
            f'<p>The latest release, from {text(release["publishedAt"][:10])}. '
            f'<a href="{text(release["url"])}">Release notes</a>. You also need your own copy of StarLancer.</p>'
            f'<div class="builds">{"".join(links)}</div></section>')


def card(mod, release: dict | None = None) -> str:
    text = html.escape
    picture = f'<img src="thumbs/{text(mod.id)}.png" alt="{text(mod.name)}">' if mod.thumbnail else '<img alt="">'
    badges = [f'<span class="badge version">Version {text(mod.version)}</span>' if mod.version else "",
              f'<span class="badge">by {text(mod.author)}</span>' if mod.author else "",
              f'<span class="badge">Needs OpenReliant {text(mod.needs)}</span>' if mod.needs else ""]
    if mod.needs and release and version_tuple(release["tagName"]) < version_tuple(mod.needs):
        badges.append(f'<span class="badge waiting">OpenReliant {text(mod.needs)} is coming soon</span>')
    licence = f'<a href="https://github.com/{REPOSITORY}/blob/main/mods/{text(mod.id)}/license.txt">Credits and licence</a>'
    # The mod's own page, where its manifest gives one other than this collection.
    if mod.url and REPOSITORY not in mod.url:
        licence += f'<a href="{text(mod.url)}">Website</a>'
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
    release = latest_openreliant()
    for mod in mods:
        if mod.thumbnail:
            shutil.copy(mod.thumbnail, SITE / "thumbs" / f"{mod.id}.png")
    updated = git("log", "-1", "--format=%cs")
    page = PAGE.format(engine=engine_panel(release), mods="\n".join(card(mod, release) for mod in mods), repository=REPOSITORY, updated=updated)
    (SITE / "index.html").write_text(page, encoding="utf-8")
    print(f"wrote {SITE / 'index.html'}: {len(mods)} mods")


if __name__ == "__main__":
    main()
