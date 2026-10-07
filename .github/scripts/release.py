"""Releases every mod whose mod.ini gives a version that has no release yet: packs its folder into
<mod>.hog with sltool, with <mod>.hog.sha256 beside it, tags the version as <mod>-v<version>, and
publishes a release with both attached.

    python3 .github/scripts/release.py [--dry-run]

--dry-run packs every mod into dist/ and publishes nothing, to check that they pack. SLTOOL names
the sltool to run; sltool on the PATH by default.
"""

import os
import pathlib
import subprocess
import sys

from mods import ROOT, git, problems, tree

DIST = ROOT / "dist"


def pack(mod) -> pathlib.Path:
    DIST.mkdir(exist_ok=True)
    archive = DIST / mod.archive
    subprocess.run([os.environ.get("SLTOOL", "sltool"), "hog", "pack", str(mod.folder), str(archive), "--checksum"], check=True)
    return archive


def notes(mod) -> str:
    """The release's notes: what the mod is, what it needs, how to install it, and its changes
    since its last release."""
    earlier = [tag for tag in git("tag", "--list", f"{mod.id}-v*", "--sort=-creatordate").splitlines() if tag]
    since = [f"{earlier[0]}..HEAD"] if earlier else []
    changes = git("log", "--format=- %s", *since, "--", mod.path, f"sources/{mod.id}")
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
        f"Credits and licence: [license.txt](https://github.com/OpenReliant/openreliant-mods/blob/{mod.tag}/{mod.path}/license.txt).",
        "",
        "## Changes" if not earlier else f"## Changes since {earlier[0]}",
        "",
        changes or "- First release.",
    ]
    return "\n".join(line for line in lines if line is not None)


def main() -> int:
    dry_run = "--dry-run" in sys.argv[1:]
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
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
