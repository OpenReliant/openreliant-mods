"""Writes the mods' site into site/: the index page, which browses the mods by category, with each
mod's thumbnail, name, version, author, what it needs, its description and the download of its
latest release; and updates/, every mod's releases, newest first.

    python3 .github/scripts/site.py
"""

from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import sys

from mods import ROOT, REPOSITORY, Category, all_categories, git, problems, tree

SITE = ROOT / "site"

STYLE = """
/* Newtown, by Roger White, from Roger's Fonts: the face OpenReliant draws the game's menus in, from
   the OpenReliant website on the same host. */
@font-face { font-family: "Newtown"; src: url("/openreliant/fonts/Newtown.ttf") format("truetype"); font-display: swap; }
:root {
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
}
* { box-sizing: border-box; }
[hidden] { display: none !important; }
html { background: var(--bg); }
body {
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
}
main { max-width: 1000px; margin: 0 auto; padding: 0 16px 64px; }
nav.top { display: flex; justify-content: space-between; align-items: center; padding: 20px 0 36px; font-family: var(--display); font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; }
nav.top .brand { color: var(--text); text-decoration: none; font-family: var(--title); font-weight: normal; font-size: 19px; letter-spacing: 0.03em; }
nav.top .brand span, nav.top .links a.current { color: var(--accent); }
nav.top .links a { color: var(--muted); text-decoration: none; margin-left: 22px; font-size: 15px; }
nav.top .links a:hover { color: var(--accent); }
@media (max-width: 520px) { nav.top .links a:not(.keep) { display: none; } nav.top .links a { margin-left: 16px; } }
header { margin-bottom: 36px; }
h1 { font-family: var(--title); margin: 2px 0 10px; font-size: clamp(34px, 7vw, 54px); line-height: 1; letter-spacing: 0.02em; text-transform: uppercase; font-weight: normal; }
header p { margin: 0; max-width: 640px; color: var(--muted); font-size: 17px; }
a { color: var(--accent); text-underline-offset: 2px; }
.mod {
  display: grid; grid-template-columns: 340px 1fr; gap: 24px; padding: 22px; margin-bottom: 22px;
  background: var(--brackets), linear-gradient(180deg, #141824, var(--card));
  background-repeat: no-repeat; box-shadow: inset 0 0 0 1px var(--card-edge);
}
.shot { position: relative; }
.shot img { display: block; width: 100%; aspect-ratio: 4 / 3; object-fit: cover; background: #000; clip-path: var(--cut); }
.mod h2 { font-family: var(--title); margin: 0 0 8px; font-size: 28px; line-height: 1.1; letter-spacing: 0.03em; text-transform: uppercase; font-weight: normal; }
.where { margin: 0 0 4px; font-family: var(--display); font-weight: 600; font-size: 14px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }
.where a { color: var(--muted); text-decoration: none; }
.where a:hover { color: var(--accent); }
.badges { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 14px; }
.badge { font-family: var(--display); font-weight: 600; font-size: 14px; letter-spacing: 0.06em; text-transform: uppercase; padding: 2px 10px; border: 1px solid var(--card-edge); color: var(--muted); background: #0b0e15; }
.badge.version { color: var(--accent); border-color: var(--accent-dim); }
.description { margin: 0 0 18px; overflow-wrap: anywhere; color: #cfd3dd; }
.download {
  display: inline-block; background: var(--accent); color: #140a02; font-family: var(--display);
  font-size: 18px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
  text-decoration: none; padding: 9px 22px; clip-path: var(--cut);
}
.download:hover { background: #ff9d45; }
.links { margin-top: 12px; font-size: 14px; color: var(--muted); }
.links a { margin-right: 14px; }
.unreleased { color: var(--muted); font-style: italic; margin: 0; }
.engine {
  margin-bottom: 30px; padding: 20px 22px; background: var(--brackets), #0e111a;
  background-repeat: no-repeat; box-shadow: inset 0 0 0 1px var(--card-edge);
}
.engine h2 { font-family: var(--title); margin: 0 0 4px; font-size: 22px; letter-spacing: 0.04em; text-transform: uppercase; font-weight: normal; }
.engine h2 span { color: var(--accent); }
.engine p { margin: 0 0 14px; color: var(--muted); font-size: 14px; }
.builds { display: flex; flex-wrap: wrap; gap: 10px; }
.build, .kind {
  font-family: var(--display); font-weight: 600; font-size: 16px; letter-spacing: 0.05em; text-transform: uppercase;
  text-decoration: none; color: var(--text); padding: 7px 14px; border: 1px solid var(--card-edge); background: #141824;
  clip-path: var(--cut);
}
.build:hover, .kind:hover { border-color: var(--accent-dim); color: var(--accent); }
.build.yours { background: var(--accent); color: #140a02; border-color: var(--accent); }
.build.yours::before { content: "For this computer: "; }
.badge.waiting { color: #e6b24a; border-color: #6b5212; }
.install {
  margin-top: 36px; padding: 18px 22px; border-left: 3px solid var(--accent); background: #0e111a; color: #cfd3dd;
}
.install h3 { font-family: var(--title); margin: 0 0 6px; font-size: 17px; text-transform: uppercase; letter-spacing: 0.04em; font-weight: normal; color: var(--accent); }
.install p { margin: 0; }
code { background: #1a1f2c; padding: 1px 6px; border-radius: 4px; font-size: 14px; }
footer { color: var(--muted); font-size: 14px; margin-top: 28px; }
@media (max-width: 760px) { .mod { grid-template-columns: 1fr; } }

/* Browsing by category: where you are, the categories in it, and the search, sort and filter. */
.browse { margin-bottom: 22px; }
.crumbs ol { display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 10px; margin: 0 0 6px; padding: 0; list-style: none; font-family: var(--title); font-size: 22px; letter-spacing: 0.04em; text-transform: uppercase; }
.crumbs li + li::before { content: "/"; color: var(--accent-dim); margin-right: 10px; }
.crumbs a { color: var(--muted); text-decoration: none; }
.crumbs a:hover { color: var(--accent); }
.crumbs [aria-current] { color: var(--text); }
.about { margin: 0 0 14px; color: var(--muted); max-width: 640px; }
.kinds { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 18px; }
.kinds:empty { display: none; }
.kind .n { margin-left: 8px; color: var(--accent); }
.kind.none { color: var(--muted); }
.kind.none .n { color: var(--muted); }
.tools { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 18px; padding: 12px 14px; background: #0e111a; box-shadow: inset 0 0 0 1px var(--card-edge); }
.tools input[type="search"], .tools select {
  font: 15px system-ui, -apple-system, "Segoe UI", sans-serif; color: var(--text); background: #141824;
  border: 1px solid var(--card-edge); padding: 7px 10px;
}
.tools input[type="search"] { flex: 1 1 220px; min-width: 0; }
.tools input[type="search"]:focus, .tools select:focus { outline: none; border-color: var(--accent); }
.tools label { font-family: var(--display); font-weight: 600; font-size: 15px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); display: flex; align-items: center; gap: 8px; }
.count { margin: 14px 0 0; font-family: var(--display); font-weight: 600; font-size: 15px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }
.empty { padding: 22px; color: var(--muted); background: #0e111a; box-shadow: inset 0 0 0 1px var(--card-edge); }
.empty p { margin: 0; }

/* The updates: each release, newest first. */
.updates { list-style: none; margin: 0; padding: 0; }
.update {
  display: grid; grid-template-columns: 120px 1fr; gap: 20px; padding: 18px 22px; margin-bottom: 16px;
  background: var(--brackets), linear-gradient(180deg, #141824, var(--card));
  background-repeat: no-repeat; box-shadow: inset 0 0 0 1px var(--card-edge);
}
.update img { display: block; width: 100%; aspect-ratio: 4 / 3; object-fit: cover; background: #000; clip-path: var(--cut); }
.update h2 { font-family: var(--title); margin: 0 0 8px; font-size: 22px; line-height: 1.15; letter-spacing: 0.03em; text-transform: uppercase; font-weight: normal; display: flex; flex-wrap: wrap; align-items: center; gap: 6px 12px; }
.update h2 a { color: var(--text); text-decoration: none; }
.update h2 a:hover { color: var(--accent); }
.when { font-family: var(--display); font-weight: 600; font-size: 15px; letter-spacing: 0.08em; color: var(--accent); margin: 0 0 2px; }
.changes { margin: 0; padding-left: 20px; color: #cfd3dd; }
.changes li { margin: 2px 0; }
@media (max-width: 520px) { .update { grid-template-columns: 1fr; } .update img { max-width: 200px; } }
"""

# Puts the build for this computer first and lights it: the system from the user agent, the
# processor from the browser where it says, else the usual one (Apple silicon on a Mac).
BUILD_SCRIPT = """
(function () {
  const agent = navigator.userAgent;
  const system = /Windows/.test(agent) ? "windows" : /Mac/.test(agent) ? "macos" : /Linux|X11/.test(agent) && !/Android/.test(agent) ? "linux" : null;
  if (!system) return;
  const light = (processor) => {
    const build = document.querySelector(`.build[data-build="${system}-${processor}"]`);
    if (!build) return;
    document.querySelectorAll(".build.yours").forEach((other) => other.classList.remove("yours"));
    build.classList.add("yours");
    build.parentElement.prepend(build);
  };
  light(system === "macos" ? "aarch64" : "x86_64");
  if (navigator.userAgentData && navigator.userAgentData.getHighEntropyValues) {
    navigator.userAgentData.getHighEntropyValues(["architecture"]).then((values) => {
      if (values.architecture === "arm") light("aarch64");
      else if (values.architecture === "x86") light("x86_64");
    }).catch(() => {});
  }
})();
"""

# Browses the mods: the category, the search and the sort are in the address, as
# ?category=ships/fighters&q=viper&sort=updated, so a link keeps them. Without scripts the page
# lists every mod.
BROWSE_SCRIPT = """
(function () {
  const categories = JSON.parse(document.getElementById("categories").textContent);
  const byPath = new Map(categories.map((category) => [category.path, category]));
  const browse = document.querySelector(".browse");
  const list = document.querySelector(".mods");
  const cards = Array.from(list.querySelectorAll(".mod"));
  const crumbs = browse.querySelector(".crumbs ol");
  const about = browse.querySelector(".about");
  const kinds = browse.querySelector(".kinds");
  const search = document.getElementById("search");
  const sort = document.getElementById("sort");
  const count = browse.querySelector(".count");
  const empty = document.querySelector(".empty");
  const emptyText = empty.querySelector("p");
  const state = { category: "", q: "", sort: "name" };

  const inside = (path, category) => category === "" || path === category || path.startsWith(category + "/");
  const trail = (path) => {
    const found = [];
    for (let at = byPath.get(path); at; at = at.parent === null ? null : byPath.get(at.parent)) found.unshift(at);
    return found;
  };
  // The category's slashes are kept as they are, so that the address reads as the folders do.
  const address = (category) => {
    const parts = [];
    if (category) parts.push("category=" + encodeURIComponent(category).replace(/%2F/g, "/"));
    if (state.q) parts.push("q=" + encodeURIComponent(state.q));
    if (state.sort !== "name") parts.push("sort=" + state.sort);
    return parts.length ? "?" + parts.join("&") : location.pathname;
  };
  const read = () => {
    const query = new URLSearchParams(location.search);
    const category = query.get("category") || "";
    state.category = byPath.has(category) ? category : "";
    state.q = query.get("q") || "";
    state.sort = query.get("sort") === "updated" ? "updated" : "name";
    search.value = state.q;
    sort.value = state.sort;
  };
  const go = (category) => {
    state.category = category;
    history.pushState(null, "", address(category));
    show();
  };
  const categoryLink = (category, text) => {
    const link = document.createElement("a");
    link.href = address(category.path);
    link.textContent = text;
    link.addEventListener("click", (event) => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) return;
      event.preventDefault();
      go(category.path);
    });
    return link;
  };
  const plural = (n) => n === 1 ? "1 mod" : `${n} mods`;

  function show() {
    const here = byPath.get(state.category);
    crumbs.replaceChildren(...trail(state.category).map((category) => {
      const item = document.createElement("li");
      if (category === here) {
        const current = document.createElement("span");
        current.textContent = category.name;
        current.setAttribute("aria-current", "page");
        item.append(current);
      } else item.append(categoryLink(category, category.name));
      return item;
    }));
    about.textContent = here.text;
    kinds.replaceChildren(...categories.filter((category) => category.parent === here.path).map((category) => {
      const link = categoryLink(category, category.name);
      link.className = "kind" + (category.count === 0 ? " none" : "");
      link.setAttribute("aria-label", `${category.name}, ${plural(category.count).replace(/^0 mods$/, "no mods")}`);
      const n = document.createElement("span");
      n.className = "n";
      n.textContent = category.count;
      link.append(n);
      return link;
    }));
    const words = state.q.toLowerCase().split(/\\s+/).filter(Boolean);
    const shown = cards.filter((card) => {
      const fits = inside(card.dataset.category, state.category)
        && words.every((word) => card.dataset.text.includes(word));
      card.hidden = !fits;
      return fits;
    });
    const order = state.sort === "updated"
      ? (a, b) => (b.dataset.updated || "").localeCompare(a.dataset.updated || "") || a.dataset.name.localeCompare(b.dataset.name)
      : (a, b) => a.dataset.name.localeCompare(b.dataset.name);
    shown.sort(order).forEach((card) => list.append(card));
    count.textContent = shown.length ? plural(shown.length) : "";
    empty.hidden = shown.length > 0;
    const hereCount = cards.filter((card) => inside(card.dataset.category, state.category)).length;
    emptyText.replaceChildren();
    if (hereCount === 0) {
      emptyText.append("No mods here yet. Made one? ");
      const how = document.createElement("a");
      how.href = "https://github.com/OpenReliant/openreliant-mods#adding-a-mod";
      how.textContent = "Here's how to send it in";
      emptyText.append(how, ".");
    } else emptyText.append("No mods here match the search.");
    document.title = here.path ? `${here.name}: OpenReliant mods` : "OpenReliant mods";
  }

  search.addEventListener("input", () => { state.q = search.value.trim(); history.replaceState(null, "", address(state.category)); show(); });
  sort.addEventListener("change", () => { state.sort = sort.value; history.replaceState(null, "", address(state.category)); show(); });
  window.addEventListener("popstate", () => { read(); show(); });
  read();
  browse.hidden = false;
  show();
})();
"""


def page(title: str, description: str, current: str, base: str, body: str, scripts: list[str]) -> str:
    """A page of the site, with the top bar's `current` link lit: `body` under it, then `scripts`.
    `base` leads from the page back to the site's top, such as ../ from updates/."""
    lit = lambda name: ' current' if name == current else ''
    script_tags = "".join(f"<script>{script}</script>" for script in scripts)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet">
<style>{STYLE}</style>
</head>
<body>
<main>
<nav class="top">
<a class="brand" href="https://openreliant.github.io/openreliant/">Open<span>Reliant</span></a>
<div class="links">
<a class="keep" href="https://openreliant.github.io/openreliant/#download">Download</a>
<a href="https://openreliant.github.io/openreliant/docs/">Docs</a>
<a class="keep{lit('mods')}" href="{base or './'}">Mods</a>
<a class="keep{lit('updates')}" href="{base}updates/">Updates</a>
<a href="https://github.com/{REPOSITORY}">GitHub</a>
</div>
</nav>
{body}
</main>
{script_tags}
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


def mod_releases() -> list[dict]:
    """The mods' releases, newest first, each with its tag, its date and its notes: from GitHub, or
    from the git tags, without notes, where GitHub can't be read."""
    try:
        found = subprocess.run(
            ["gh", "api", f"repos/{REPOSITORY}/releases", "--paginate",
             "--jq", ".[] | select(.draft | not) | {tag: .tag_name, date: .published_at, notes: .body}"],
            check=True, capture_output=True, text=True,
        ).stdout
        releases = [json.loads(line) for line in found.splitlines() if line.strip()]
    except (OSError, subprocess.CalledProcessError):
        tags = git("tag", "--list", "--format=%(refname:short) %(creatordate:iso-strict)").splitlines()
        releases = [{"tag": tag, "date": date, "notes": ""} for tag, date in (line.split(" ", 1) for line in tags if " " in line)]
    return sorted(releases, key=lambda release: release["date"], reverse=True)


def changes(notes: str) -> list[str]:
    """The changes a release's notes list, under their `## Changes` heading, each without its
    Conventional Commits type, as `1.3, a ship of its own` for `feat(viper): 1.3, a ship of its own`."""
    listed: list[str] = []
    under = False
    for line in (notes or "").splitlines():
        if line.startswith("## "):
            under = line.startswith("## Changes")
            continue
        if under and line.startswith("- "):
            listed.append(re.sub(r"^[a-z]+(\([^)]*\))?!?:\s*", "", line[2:].strip()))
    return listed


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


def where(category: Category, by_path: dict[str, Category], base: str) -> str:
    """The category's place, as links to it and the categories it's in: Ships / Fighters."""
    trail = []
    at: Category | None = category
    while at is not None and at.path:
        trail.insert(0, at)
        at = by_path.get(at.parent_path) if at.parent_path is not None else None
    links = [f'<a href="{base}?category={html.escape(step.path)}">{html.escape(step.name)}</a>' for step in trail]
    return f'<p class="where">{" / ".join(links)}</p>'


def card(mod, by_path: dict[str, Category], release: dict | None, updated: str) -> str:
    text = html.escape
    picture = f'<img src="thumbs/{text(mod.id)}.png" alt="{text(mod.name)}">' if mod.thumbnail else '<img alt="">'
    badges = [f'<span class="badge version">Version {text(mod.version)}</span>' if mod.version else "",
              f'<span class="badge">by {text(mod.author)}</span>' if mod.author else "",
              f'<span class="badge">Needs OpenReliant {text(mod.needs)}</span>' if mod.needs else "",
              f'<span class="badge">Updated {text(updated[:10])}</span>' if updated else ""]
    if mod.needs and release and version_tuple(release["tagName"]) < version_tuple(mod.needs):
        badges.append(f'<span class="badge waiting">OpenReliant {text(mod.needs)} is coming soon</span>')
    licence = f'<a href="https://github.com/{REPOSITORY}/blob/main/{text(mod.path)}/license.txt">Credits and licence</a>'
    # The mod's own page, where its manifest gives one other than this collection.
    if mod.url and REPOSITORY not in mod.url:
        licence += f'<a href="{text(mod.url)}">Website</a>'
    if mod.released():
        download = (f'<a class="download" href="{text(mod.download())}">Download {text(mod.archive)}</a>'
                    f'<div class="links"><a href="{text(mod.download())}.sha256">Checksum</a>'
                    f'<a href="{text(mod.release_page())}">Release notes</a>{licence}</div>')
    else:
        download = f'<p class="unreleased">Not released yet.</p><div class="links">{licence}</div>'
    searched = " ".join([mod.name, mod.author, mod.description]).lower()
    data = (f'data-category="{text(mod.category)}" data-name="{text(mod.name.lower())}" data-updated="{text(updated)}" '
            f'data-text="{text(searched)}"')
    return (f'<article class="mod" {data}><div class="shot">{picture}</div><div>{where(by_path[mod.category], by_path, "")}'
            f'<h2>{text(mod.name)}</h2><div class="badges">{"".join(badges)}</div>'
            f'<p class="description">{text(mod.description)}</p>{download}</div></article>')


def index_page(root: Category, release: dict | None, updated_at: dict[str, str], updated: str) -> str:
    text = html.escape
    by_path = {category.path: category for category in all_categories(root)}
    data = [{"path": category.path, "parent": category.parent_path, "name": "All mods" if not category.path else category.name,
             "text": category.text if category.path else "Every mod in the collection, by category.", "count": len(category.all_mods())}
            for category in all_categories(root)]
    mods = sorted(root.all_mods(), key=lambda mod: mod.name.lower())
    cards = "\n".join(card(mod, by_path, release, updated_at.get(mod.id, "")) for mod in mods)
    # The categories for the script; "</" kept out, so that nothing in them can end the tag.
    categories = json.dumps(data).replace("</", "<\\/")
    body = f"""<header>
<h1>Mods</h1>
<p>Mods for <a href="https://openreliant.github.io/openreliant/">OpenReliant</a>, checked to work and to be free to share. You need OpenReliant and your own copy of StarLancer.</p>
</header>
{engine_panel(release)}
<section class="browse" aria-label="Browse the mods" hidden>
<nav class="crumbs" aria-label="Category"><ol></ol></nav>
<p class="about"></p>
<div class="kinds"></div>
<div class="tools">
<input type="search" id="search" placeholder="Search the mods" aria-label="Search the mods">
<label>Sort <select id="sort"><option value="name">By name</option><option value="updated">Recently updated</option></select></label>
</div>
<p class="count" aria-live="polite"></p>
</section>
<div class="mods">
{cards}
</div>
<div class="empty" hidden><p></p></div>
<section class="install">
<h3>Installing a mod</h3>
<p>Download its <code>.hog</code> file and its <code>.hog.sha256</code> file, put both in the <code>mods</code> folder of your game folder, next to <code>resource.hog</code>, and turn the mod on in OpenReliant's mods screen. OpenReliant checks the archive against its checksum as it loads it.</p>
</section>
<footer>
<p><a href="https://github.com/{REPOSITORY}">The mods' sources</a>, with each mod's credits and licence. Updated {text(updated)}. Headings are set in Newtown, by Roger White, from Roger's Fonts.</p>
</footer>
<script type="application/json" id="categories">{categories}</script>"""
    return page("OpenReliant mods", "Mods for OpenReliant, checked to work and to be free to share.", "mods", "", body, [BUILD_SCRIPT, BROWSE_SCRIPT])


def updates_page(root: Category, releases: list[dict], updated: str) -> str:
    """Every mod's releases, newest first, with what changed in each."""
    text = html.escape
    by_path = {category.path: category for category in all_categories(root)}
    by_id = {mod.id: mod for mod in root.all_mods()}
    entries = []
    for release in releases:
        mod_id, _, version = release["tag"].rpartition("-v")
        mod = by_id.get(mod_id)
        # A mod that has left the collection keeps its releases on GitHub, not here.
        if mod is None or not version:
            continue
        listed = changes(release["notes"])
        items = "".join(f"<li>{text(change)}</li>" for change in listed)
        picture = f'<img src="../thumbs/{text(mod.id)}.png" alt="">' if mod.thumbnail else '<img alt="">'
        download = f"https://github.com/{REPOSITORY}/releases/download/{release['tag']}/{mod.archive}"
        page_url = f"https://github.com/{REPOSITORY}/releases/tag/{release['tag']}"
        entries.append(
            f'<li class="update">{picture}<div><p class="when">{text(release["date"][:10])}</p>{where(by_path[mod.category], by_path, "../")}'
            f'<h2><a href="../?category={text(mod.category)}">{text(mod.name)}</a><span class="badge version">Version {text(version)}</span></h2>'
            + (f'<ul class="changes">{items}</ul>' if items else "")
            + f'<div class="links"><a href="{text(download)}">Download</a><a href="{text(page_url)}">Release notes</a></div></div></li>')
    listing = f'<ol class="updates">{"".join(entries)}</ol>' if entries else '<div class="empty"><p>No releases yet.</p></div>'
    body = f"""<header>
<h1>Updates</h1>
<p>Every mod's releases, newest first, with what changed in each.</p>
</header>
{listing}
<footer>
<p><a href="https://github.com/{REPOSITORY}/releases">Every release on GitHub</a>. Updated {text(updated)}. Headings are set in Newtown, by Roger White, from Roger's Fonts.</p>
</footer>"""
    return page("Updates: OpenReliant mods", "The latest releases of the mods for OpenReliant.", "updates", "../", body, [])


def main() -> int:
    root = tree()
    if found := problems(root):
        for problem in found:
            print(problem, file=sys.stderr)
        return 1
    shutil.rmtree(SITE, ignore_errors=True)
    (SITE / "thumbs").mkdir(parents=True)
    (SITE / "updates").mkdir()
    mods = root.all_mods()
    for mod in mods:
        if mod.thumbnail:
            shutil.copy(mod.thumbnail, SITE / "thumbs" / f"{mod.id}.png")
    release = latest_openreliant()
    releases = mod_releases()
    # Each mod's latest release's date, from the newest first.
    updated_at: dict[str, str] = {}
    for found_release in releases:
        updated_at.setdefault(found_release["tag"].rpartition("-v")[0], found_release["date"])
    updated = git("log", "-1", "--format=%cs")
    (SITE / "index.html").write_text(index_page(root, release, updated_at, updated), encoding="utf-8")
    (SITE / "updates" / "index.html").write_text(updates_page(root, releases, updated), encoding="utf-8")
    print(f"wrote {SITE / 'index.html'} and {SITE / 'updates' / 'index.html'}: {len(mods)} mods, {len(releases)} releases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
