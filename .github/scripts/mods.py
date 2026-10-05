"""The mods in mods/, read from their manifests, for the release and the site."""

import configparser
import pathlib
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
        manifest = configparser.ConfigParser(delimiters=("=",), interpolation=None, strict=False, comment_prefixes=(";", "#"))
        manifest.read(folder / "mod.ini", encoding="utf-8")
        about = manifest["Mod"] if manifest.has_section("Mod") else {}
        self.name = about.get("name", self.id)
        self.version = about.get("version", "")
        self.author = about.get("author", "")
        self.description = about.get("description", "")
        self.needs = about.get("openreliant", "")
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


def all_mods() -> list[Mod]:
    return [Mod(folder) for folder in sorted(MODS.iterdir()) if (folder / "mod.ini").exists()]


def git(*arguments: str) -> str:
    return subprocess.run(["git", *arguments], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def tag_exists(tag: str) -> bool:
    return git("tag", "--list", tag) == tag
