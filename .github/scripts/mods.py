"""The mods in mods/, read from their manifests, for the release and the site.

mods/ holds a folder for each category, and categories can hold categories of their own, such as
mods/ships/fighters. A folder with a mod.ini is a mod, and every other folder is a category. A
category's README.md gives its name, as its first heading, and what goes in it, as its first
paragraph, and its links to its own categories set the order the site lists them in.
"""

from __future__ import annotations

import configparser
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
MODS = ROOT / "mods"
REPOSITORY = "OpenReliant/openreliant-mods"


class Mod:
    """A mod's folder and the [Mod] section of its mod.ini. Keys can be written in any case."""

    def __init__(self, folder: pathlib.Path):
        self.folder = folder
        # The folder's name is what the mod's things are named after, as viper:viper.
        self.id = folder.name
        # Where it is in the repository, such as mods/ships/fighters/viper, and its category's
        # path, such as ships/fighters.
        self.path = folder.relative_to(ROOT).as_posix()
        self.category = folder.parent.relative_to(MODS).as_posix()
        manifest = configparser.ConfigParser(delimiters=("=",), interpolation=None, strict=False, comment_prefixes=(";", "#"))
        manifest.read(folder / "mod.ini", encoding="utf-8")
        about = manifest["Mod"] if manifest.has_section("Mod") else {}
        self.name = about.get("name", self.id)
        self.version = about.get("version", "")
        self.author = about.get("author", "")
        self.description = about.get("description", "")
        self.needs = about.get("openreliant", "")
        self.url = about.get("url", "")
        self.thumbnail = folder / "mod.png" if (folder / "mod.png").exists() else None

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
            if (entry / "mod.ini").exists():
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
    """What's wrong with how mods/ is laid out: a mod outside any category, or two mods with one
    name, which their archives and their things are named after."""
    found = [f"{mod.path}: a mod goes in a category's folder, such as mods/ships/fighters" for mod in root.mods]
    seen: dict[str, str] = {}
    for mod in root.all_mods():
        if mod.id in seen:
            found.append(f"{mod.path}: {seen[mod.id]} has the same name, and a mod's name must be its own")
        seen.setdefault(mod.id, mod.path)
    return found


def git(*arguments: str) -> str:
    return subprocess.run(["git", *arguments], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def tag_exists(tag: str) -> bool:
    return git("tag", "--list", tag) == tag
