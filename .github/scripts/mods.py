"""The mods in mods/, read from their manifests, for the release and the site.

mods/ holds a folder for each category, and categories can hold categories of their own, such as
mods/ships/fighters. A folder with a mod.ini or a source.ini is a mod, and every other folder is a
category. A category's README.md gives its name, as its first heading, and what goes in it, as its
first paragraph, and its links to its own categories set the order the site lists them in.

A mod can also be kept in another repository, as an artist's packs are. The artist's repository is
a submodule under external/, pinned to a commit, and the mod's folder holds a source.ini in place of
the mod's files:

    [Source]
    Submodule=external/koncyptfysh
    Folder=Alliance Fighters/Coyote/mods

Folder is the folder of that repository that holds the mod's own folder, whatever that's called, so
that a new version there needs only the pin moved. external/<artist>.ini gives the artist's Name and
Url, for a mod whose mod.ini leaves its Author or its Url out.

    python3 .github/scripts/mods.py lfs-includes --packs|--thumbnails

prints, for each submodule, the Git LFS files its mods need: every file of them, or their
thumbnails alone. The workflows fetch those and no others.
"""

from __future__ import annotations

import configparser
import pathlib
import re
import subprocess
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[2]
MODS = ROOT / "mods"
REPOSITORY = "OpenReliant/openreliant-mods"


def section(path: pathlib.Path, name: str) -> dict[str, str]:
    """The section `name` of the ini file at `path`, by its keys in lower case; empty if there's
    none."""
    parsed = configparser.ConfigParser(delimiters=("=",), interpolation=None, strict=False, comment_prefixes=(";", "#"))
    parsed.read(path, encoding="utf-8")
    return dict(parsed[name]) if parsed.has_section(name) else {}


class Source:
    """Where a mod kept in another repository is: the submodule under external/ that holds that
    repository, pinned to a commit, and the folder of it that holds the mod's own folder."""

    def __init__(self, ini: pathlib.Path):
        found = section(ini, "Source")
        self.ini = ini.relative_to(ROOT).as_posix()
        self.submodule = found.get("submodule", "").strip("/")
        self.folder = found.get("folder", "").strip("/")
        self.root = ROOT / self.submodule
        # The artist's name and web page, for the mods that don't give their own.
        self.artist = section(ROOT / f"{self.submodule}.ini", "Artist")

    def url(self) -> str | None:
        """The repository's web address, as .gitmodules gives it; None if no submodule is there."""
        for line in git_lines("config", "-f", ".gitmodules", "--get-regexp", r"^submodule\..*\.path$"):
            key, _, path = line.partition(" ")
            if path == self.submodule:
                url = git("config", "-f", ".gitmodules", key.removesuffix(".path") + ".url")
                return url.removesuffix(".git")
        return None

    def commit(self) -> str:
        """The commit the submodule is pinned to, as checked out."""
        return git("-C", str(self.root), "rev-parse", "HEAD")

    def link(self, kind: str, path: str) -> str:
        """The repository's web page for `path` at the pinned commit: `tree` for a folder, `blob`
        for a file."""
        return f"{self.url()}/{kind}/{self.commit()}/{urllib.parse.quote(path)}"

    def find(self) -> pathlib.Path | str:
        """The mod's own folder: the folder in Folder with a mod.ini, the one of the highest Version
        if there are several. A problem's description where there's none."""
        if not self.submodule or not self.folder:
            return f"{self.ini}: Submodule and Folder name where the mod is kept"
        if self.url() is None:
            return f"{self.ini}: {self.submodule} isn't a submodule in .gitmodules"
        if not self.root.is_dir() or not any(self.root.iterdir()):
            return f"{self.ini}: {self.submodule} isn't checked out; run git submodule update --init"
        holder = self.root / self.folder
        if not holder.is_dir():
            return f"{self.ini}: {self.submodule} has no folder {self.folder}"
        found = sorted((folder for folder in holder.iterdir() if (folder / "mod.ini").exists()),
                       key=lambda folder: version_tuple(section(folder / "mod.ini", "Mod").get("version", "")), reverse=True)
        if not found:
            return f"{self.ini}: no folder in {self.submodule}/{self.folder} has a mod.ini"
        versions = [version_tuple(section(folder / "mod.ini", "Mod").get("version", "")) for folder in found[:2]]
        if len(found) > 1 and versions[0] == versions[1]:
            return f"{self.ini}: {found[0].name} and {found[1].name} in {self.submodule}/{self.folder} have the same Version"
        return found[0]


class Mod:
    """A mod: where it is in the categories, and the [Mod] section of its mod.ini. Its files are
    in its folder, or, where the folder holds a source.ini, in another repository (`Source`). Keys
    can be written in any case."""

    def __init__(self, folder: pathlib.Path):
        self.folder = folder
        # The folder's name is what the mod's things are named after, as viper:viper, and what its
        # archive is called.
        self.id = folder.name
        # Where it is in the repository, such as mods/ships/fighters/viper, and its category's
        # path, such as ships/fighters.
        self.path = folder.relative_to(ROOT).as_posix()
        self.category = folder.parent.relative_to(MODS).as_posix()
        self.source = Source(folder / "source.ini") if (folder / "source.ini").exists() else None
        # Where its files are, and what's wrong where they can't be found.
        self.files: pathlib.Path | None = folder
        self.problem: str | None = None
        if self.source:
            found = self.source.find()
            if isinstance(found, str):
                self.files, self.problem = None, found
            else:
                self.files = found
        about = section(self.files / "mod.ini", "Mod") if self.files else {}
        artist = self.source.artist if self.source else {}
        self.name = about.get("name", self.id)
        self.version = about.get("version", "")
        self.author = about.get("author", artist.get("name", ""))
        self.description = about.get("description", "")
        self.needs = about.get("openreliant", "")
        self.url = about.get("url", artist.get("url", ""))
        self.thumbnail = self.files / "mod.png" if self.files and (self.files / "mod.png").exists() else None

    def credits(self) -> tuple[str, str]:
        """Where its credits and licence are, as a link's text and address: its license.txt, or
        for a mod kept in another repository, the licence or credits file there, else its folder."""
        if not self.source:
            return "Credits and licence", f"https://github.com/{REPOSITORY}/blob/main/{self.path}/license.txt"
        if self.files:
            pack = self.files.relative_to(self.source.root)
            # A licence before credits, and the mod's own before the repository's.
            for pattern in (r"licen[cs]", r"credits"):
                for holder in (pack, pathlib.Path(".")):
                    for name in sorted(entry.name for entry in (self.source.root / holder).iterdir()):
                        if re.match(pattern, name, re.IGNORECASE):
                            return "Credits and licence", self.source.link("blob", (holder / name).as_posix())
        return "Source", self.source_page()

    def lfs_pointers(self) -> list[pathlib.Path]:
        """Its files that are still Git LFS pointers, whose contents weren't fetched."""
        if not self.files:
            return []
        return [path for path in sorted(self.files.rglob("*")) if path.is_file() and path.stat().st_size < 1024
                and path.read_bytes().startswith(b"version https://git-lfs.github.com/spec/")]

    def source_page(self) -> str:
        """For a mod kept in another repository, its folder there at the pinned commit."""
        assert self.source is not None
        return self.source.link("tree", self.files.relative_to(self.source.root).as_posix() if self.files else self.source.folder)

    @property
    def tag(self) -> str:
        """The release tag of its current version, such as viper-v1.0."""
        return f"{self.id}-v{self.version}"

    @property
    def archive(self) -> str:
        return f"{self.id}.hog"

    def released(self) -> bool:
        """Whether its current version has a release tag."""
        return tag_exists(self.tag)

    def download(self) -> str:
        return f"https://github.com/{REPOSITORY}/releases/download/{self.tag}/{self.archive}"

    def release_page(self) -> str:
        return f"https://github.com/{REPOSITORY}/releases/tag/{self.tag}"


class Category:
    """A folder of mods/ that isn't a mod: its path, such as ships/fighters ("" for mods/ itself),
    and the name and the text its README.md gives."""

    def __init__(self, folder: pathlib.Path):
        self.folder = folder
        self.path = folder.relative_to(MODS).as_posix() if folder != MODS else ""
        readme = folder / "README.md"
        lines = readme.read_text(encoding="utf-8").splitlines() if readme.exists() else []
        heading = next((line[2:].strip() for line in lines if line.startswith("# ")), None)
        self.name = heading or folder.name.replace("-", " ").capitalize()
        self.text = first_paragraph(lines)
        # The order its README lists its own categories in, by their folders' names.
        self.listed = [link.strip("/") for link in re.findall(r"\]\(([^)/]+)/?\)", "\n".join(lines))]
        self.children: list[Category] = []
        self.mods: list[Mod] = []

    @property
    def parent_path(self) -> str | None:
        """Its parent's path; None for mods/ itself."""
        if self.path == "":
            return None
        return self.path.rpartition("/")[0]

    def all_mods(self) -> list[Mod]:
        """Its mods and those of every category in it."""
        return self.mods + [mod for child in self.children for mod in child.all_mods()]


def first_paragraph(lines: list[str]) -> str:
    """The first paragraph after the heading, joined into one line."""
    paragraph: list[str] = []
    for line in lines:
        if line.startswith("#") or line.startswith("- "):
            if paragraph:
                break
            continue
        if not line.strip():
            if paragraph:
                break
            continue
        paragraph.append(line.strip())
    return " ".join(paragraph)


def tree() -> Category:
    """mods/ as a tree of categories, each with its mods, in the order the site lists them."""

    def walk(folder: pathlib.Path) -> Category:
        category = Category(folder)
        folders = sorted(entry for entry in folder.iterdir() if entry.is_dir())
        for entry in folders:
            if (entry / "mod.ini").exists() or (entry / "source.ini").exists():
                category.mods.append(Mod(entry))
            else:
                category.children.append(walk(entry))
        rank = {name: at for at, name in enumerate(category.listed)}
        category.children.sort(key=lambda child: (rank.get(child.folder.name, len(rank)), child.folder.name))
        return category

    return walk(MODS)


def all_categories(root: Category) -> list[Category]:
    """Every category of the tree, `root` first, each before its own."""
    return [root] + [category for child in root.children for category in all_categories(child)]


def all_mods() -> list[Mod]:
    return tree().all_mods()


def problems(root: Category) -> list[str]:
    """What's wrong with how mods/ is laid out: a mod outside any category, a mod kept in another
    repository that can't be found there, or two mods with one name, which their archives and their
    things are named after."""
    found = [f"{mod.path}: a mod goes in a category's folder, such as mods/ships/fighters" for mod in root.mods]
    found += [mod.problem for mod in root.all_mods() if mod.problem]
    seen: dict[str, str] = {}
    for mod in root.all_mods():
        if mod.id in seen:
            found.append(f"{mod.path}: {seen[mod.id]} has the same name, and a mod's name must be its own")
        seen.setdefault(mod.id, mod.path)
    return found


def git(*arguments: str) -> str:
    return subprocess.run(["git", *arguments], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def git_lines(*arguments: str) -> list[str]:
    """The lines git writes; none where it fails, as `git config` does for a key that's missing."""
    done = subprocess.run(["git", *arguments], cwd=ROOT, capture_output=True, text=True)
    return done.stdout.splitlines() if done.returncode == 0 else []


def version_tuple(text: str) -> tuple[int, ...]:
    return tuple(int(part) for part in text.lstrip("v").split(".") if part.isdigit())


def lfs_includes(thumbnails: bool) -> dict[str, list[str]]:
    """For each submodule, the Git LFS files the mods kept there need: every file of their folders,
    or their thumbnails alone. Read from the source.ini files, so that it works before the
    submodules' files are fetched."""
    found: dict[str, list[str]] = {}
    for ini in sorted(MODS.rglob("source.ini")):
        source = Source(ini)
        if source.submodule and source.folder:
            found.setdefault(source.submodule, []).append(f"{source.folder}/*/mod.png" if thumbnails else f"{source.folder}/**")
    return found


if __name__ == "__main__":
    if sys.argv[1:2] != ["lfs-includes"] or sys.argv[2:] not in (["--packs"], ["--thumbnails"]):
        sys.exit("usage: mods.py lfs-includes --packs|--thumbnails")
    for submodule, patterns in lfs_includes(sys.argv[2] == "--thumbnails").items():
        print(f"{submodule}\t{','.join(patterns)}")


def tag_exists(tag: str) -> bool:
    return git("tag", "--list", tag) == tag
