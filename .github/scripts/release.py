"""Releases every mod whose mod.ini gives a version that has no release yet: packs its folder into
<mod>.hog with sltool, with <mod>.hog.sha256 beside it, tags the version as <mod>-v<version>, and
publishes a release with both attached.

    python3 .github/scripts/release.py [--dry-run]

--dry-run packs every mod into dist/ and publishes nothing, to check that they pack. SLTOOL names
the sltool to run; sltool on the PATH by default.
"""

import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from mods import REPOSITORY, ROOT, SITE_URL, Mod, git, problems, tree

DIST = ROOT / "dist"


def pack(mod) -> pathlib.Path:
    # A file whose contents weren't fetched would go into the archive as its pointer.
    if pointers := mod.lfs_pointers():
        sys.exit(f"{mod.id}: {len(pointers)} of its files are Git LFS pointers, such as {pointers[0].relative_to(ROOT)}; "
                 "fetch them first, as the README says")
    DIST.mkdir(exist_ok=True)
    archive = DIST / mod.archive
    subprocess.run([os.environ.get("SLTOOL", "sltool"), "hog", "pack", str(mod.files), str(archive), "--checksum"], check=True)
    return archive


def pin_at(tag: str, submodule: str) -> str | None:
    """The commit `submodule` was pinned to at `tag`; None if it wasn't there yet."""
    found = git("ls-tree", tag, submodule).split()
    return found[2] if len(found) >= 3 and found[1] == "commit" else None


def changes(mod, earlier: str | None) -> str:
    """What changed in the mod since its release `earlier`, as a list: the commits that touch its
    folder, here, or for an artist's mod, in their repository between the two pins."""
    if mod.artist:
        before = pin_at(earlier, mod.artist.submodule) if earlier else None
        if before is None:
            return ""
        return git("-C", str(mod.artist.root), "log", "--format=- %s", f"{before}..{mod.artist.commit()}", "--", mod.kept_in())
    since = [f"{earlier}..HEAD"] if earlier else []
    return git("log", "--format=- %s", *since, "--", mod.path, f"sources/{mod.id}")


def credits(mod) -> str:
    """The notes' line for the mod's credits and licence, and for an artist's mod, where it's
    kept."""
    if not mod.artist:
        return f"Credits and licence: [license.txt](https://github.com/OpenReliant/openreliant-mods/blob/{mod.tag}/{mod.path}/license.txt)."
    label, address = mod.credits()
    name = urllib.parse.unquote(address.rsplit("/", 1)[-1])
    kept = f"From {mod.author}'s repository: [{mod.kept_in()}]({mod.source_page()})."
    return kept if label == "Source" else f"{kept} Credits and licence: [{name}]({address})."


def notes(mod) -> str:
    """The release's notes: what the mod is, what it needs, how to install it, and its changes
    since its last release."""
    earlier = [tag for tag in git("tag", "--list", f"{mod.id}-v*", "--sort=-creatordate").splitlines() if tag]
    changed = changes(mod, earlier[0] if earlier else None)
    lines = [
        mod.description,
        "",
        f"Needs OpenReliant {mod.needs} or later." if mod.needs else "",
        "",
        "## Installing",
        "",
        f"Put `{mod.archive}` and `{mod.archive}.sha256` in the `mods` folder of your game folder, next to "
        "`resource.hog`, and turn the mod on in OpenReliant's mods screen. OpenReliant checks the "
        "archive against its checksum as it loads it.",
        "",
        credits(mod),
        "",
        "## Changes" if not earlier else f"## Changes since {earlier[0]}",
        "",
        changed or ("- First release." if not earlier else "- No changes to its files."),
    ]
    return "\n".join(line for line in lines if line is not None)


def announce(mod: Mod, webhook: str) -> None:
    """Post the mod's page and release notes once GitHub has the files."""
    page = SITE_URL + urllib.parse.quote(mod.page)
    tag = urllib.parse.quote(mod.tag, safe="")
    release = f"https://github.com/{REPOSITORY}/releases/tag/{tag}"
    payload = {
        "content": f"**{mod.name} {mod.version}**\n[Mod page]({page}) · [Release notes]({release})",
        "allowed_mentions": {"parse": []},
    }
    request = urllib.request.Request(
        f"{webhook}?wait=true",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "OpenReliant Mods GitHub Actions"},
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=15):
                return
        except urllib.error.HTTPError as error:
            with error:
                if error.code != 429 or attempt == 3:
                    print(f"::warning::Could not post {mod.tag} to Discord (HTTP {error.code}).", file=sys.stderr)
                    return
                delay = float(error.headers.get("Retry-After", "1"))
            time.sleep(delay)
        except (urllib.error.URLError, TimeoutError):
            print(f"::warning::Could not reach Discord to post {mod.tag}.", file=sys.stderr)
            return


def main() -> int:
    dry_run = "--dry-run" in sys.argv[1:]
    webhook = os.environ.get("DISCORD_MOD_RELEASES_WEBHOOK")
    root = tree()
    # A layout that's wrong releases nothing.
    if found := problems(root):
        for problem in found:
            print(problem, file=sys.stderr)
        return 1
    failed = False
    for mod in root.all_mods():
        if not mod.version:
            print(f"{mod.id}: mod.ini gives no Version, so it isn't released", file=sys.stderr)
            failed = True
            continue
        if dry_run:
            pack(mod)
            continue
        if mod.released():
            print(f"{mod.id}: {mod.tag} is released already")
            continue
        archive = pack(mod)
        (DIST / f"{mod.id}-notes.md").write_text(notes(mod), encoding="utf-8")
        subprocess.run(
            [
                "gh", "release", "create", mod.tag, str(archive), f"{archive}.sha256",
                "--title", f"{mod.name} {mod.version}",
                "--notes-file", str(DIST / f"{mod.id}-notes.md"),
                "--target", os.environ.get("GITHUB_SHA") or git("rev-parse", "HEAD"),
                "--latest=false",
            ],
            check=True,
        )
        print(f"{mod.id}: released {mod.tag}")
        if webhook:
            announce(mod, webhook)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
