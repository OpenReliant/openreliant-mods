# OpenReliant mods

Mods for [OpenReliant](https://github.com/OpenReliant/openreliant), the open-source reimplementation
of StarLancer's engine. Each mod here is checked by the OpenReliant maintainers: it works with the
OpenReliant version its manifest names, and its licence lets you share it.

You need OpenReliant and your own copy of StarLancer. No mod here holds the game's archives or its
files as they ship. Some art packs rework the game's own models and textures, and work over your
copy of the game all the same.

**[Browse and download the mods](https://openreliant.github.io/openreliant-mods/)**, by category,
each from its latest release, and see [the latest updates](https://openreliant.github.io/openreliant-mods/updates/).

## Mods

| Mod | Category | What it adds | Needs | Licence |
|---|---|---|---|---|
| [Instructor, Shut Up](mods/gameplay/instructor-shut-up) | Gameplay | Instant Action truly becomes Instant | OpenReliant 0.7 | MPL-2.0 |
| [Coyote Worn](mods/ships/fighters/alliance/coyote-worn) | Ships / Fighters / Alliance | KonCyptFysh's worn restoration of the Coyote, with material maps | OpenReliant 0.6.3 | His restoration work CC-BY-NC-SA-4.0, by KonCyptFysh ([credits](https://github.com/KonCyptFysh/OpenReliant-Art-Packs/blob/main/Alliance%20Fighters/Coyote/mods/30-coyote-worn-v4/license.txt)) |
| [Predator Worn](mods/ships/fighters/alliance/predator-worn) | Ships / Fighters / Alliance | KonCyptFysh's worn restoration of the Predator, with material maps | OpenReliant 0.6.3 | His restoration work CC-BY-NC-SA-4.0, by KonCyptFysh ([credits](https://github.com/KonCyptFysh/OpenReliant-Art-Packs/blob/main/Alliance%20Fighters/Predator/mods/40-predator-worn-v14/license.txt)) |
| [Reaper Worn](mods/ships/fighters/alliance/reaper-worn) | Ships / Fighters / Alliance | KonCyptFysh's worn restoration of the Reaper, with material maps | OpenReliant 0.6.3 | His restoration work CC-BY-NC-SA-4.0, by KonCyptFysh ([credits](https://github.com/KonCyptFysh/OpenReliant-Art-Packs/blob/main/Alliance%20Fighters/Reaper/mods/50-reaper-worn-v3/license.txt)) |
| [Wolverine Worn](mods/ships/fighters/alliance/wolverine-worn) | Ships / Fighters / Alliance | KonCyptFysh's worn restoration of the Wolverine, with material maps | OpenReliant 0.6.3 | His restoration work CC-BY-NC-SA-4.0, by KonCyptFysh ([credits](https://github.com/KonCyptFysh/OpenReliant-Art-Packs/blob/main/Alliance%20Fighters/Wolverine/mods/60-wolverine-worn-v1/license.txt)) |
| [Viper Mk II](mods/ships/fighters/viper) | Ships / Fighters | Fly the Viper Mk II from Battlestar Galactica: fast and agile, with two kinetic guns, light shields and a strong hull | OpenReliant 0.7 | Model and pictures CC-BY-NC-4.0, by LocoPixel ([credits](mods/ships/fighters/viper/license.txt)) |

## Installing a mod

Download the mod's `.hog` file and its `.hog.sha256` file from its latest release, and put both in
the `mods` folder of your game folder, next to `resource.hog`. Then turn it on in OpenReliant's mods
screen. OpenReliant checks the archive against its checksum as it loads it.

To try the latest changes before they're released, copy the mod's own folder into the same `mods`
folder instead, keeping its name: `mods/ships/fighters/viper` becomes `<game>/mods/viper`. The name
matters: the game and the mod's scripts know what a mod adds by it, such as `viper:viper` for the
Viper, and `viper.hog` gives the same names. For a mod kept in another repository, copy its folder
from there, renamed as the mod is called here: `Alliance Fighters/Coyote/mods/30-coyote-worn-v4`
becomes `<game>/mods/coyote-worn`.

```text
StarLancer/
  resource.hog
  mods/
    viper/
      mod.ini
      viper.shp
      ...
```

OpenReliant's [modding guide](https://github.com/OpenReliant/openreliant/blob/main/docs/guide/modding.md)
says how mods work.

## Adding a mod

A mod is a folder with a `mod.ini`, in the folder of its category under [`mods/`](mods), such as
`mods/ships/fighters/viper`. The folder's name is the mod's name, which its archive and its things
are named after, so it must be the only mod of that name in the collection. Give it a `mod.png`
thumbnail and a `license.txt` with its credits and licence, and open a pull request.

Every other folder under `mods/` is a category, and a category can hold categories of its own,
such as `ships/fighters/alliance`. Its `README.md` gives its name as its first heading and what goes
in it as the paragraph after, and links to its own categories in the order the site lists them. A
category with no mods yet still shows on the site, with none in it. To add a category, add a folder
with its `README.md`, and link to it from the README of the category it's in.

## Mods kept in other repositories

An artist can keep their mods in their own repository, and the collection packs and releases them
from there. The repository is a submodule under `external/`, pinned to a commit:

```sh
git submodule add https://github.com/<artist>/<repository>.git external/<artist>
```

`external/<artist>.ini` gives the artist's name and web page, for the mods whose `mod.ini` leaves
them out:

```ini
[Artist]
Name=KonCyptFysh
Url=https://koncyptfysh.github.io/OpenReliant-Art-Packs/
```

Each mod gets a folder in its category, named as the mod is to be called here, holding a
`source.ini` in place of the mod's files:

```ini
[Source]
Submodule=external/koncyptfysh
Folder=Alliance Fighters/Coyote/mods
```

`Folder` is the folder of the artist's repository that holds the mod's own folder, whatever that's
called, so the mod's folder there can carry its version in its name. Where it holds more than one,
the one with the highest `Version` is the mod. The card links to the artist's licence or credits
file, from the mod's folder or the top of the repository, and to the mod's folder there.

To release a new version, the artist raises the `Version` in the mod's `mod.ini` in their
repository, and opens a pull request here that moves the pin:

```sh
git -C external/<artist> pull origin main
git add external/<artist>
```

The workflows fetch the Git LFS files of the mods' own folders and no others, and cache them by the
pins, so that each pin costs the artist's LFS bandwidth once. To work with the mods locally, check
out the submodules without their LFS files, then fetch the same files:

```sh
GIT_LFS_SKIP_SMUDGE=1 git submodule update --init
python3 .github/scripts/mods.py lfs-includes --packs | while IFS=$'\t' read -r submodule include; do
  git -C "$submodule" lfs pull --include "$include"
done
```

## Releasing a mod

A mod's version is the `Version` in its `mod.ini`. To release it, raise the version and push to
`main`. The Publish workflow then:

1. packs the mod's files into `<mod>.hog` with `sltool hog pack --checksum`, with
   `<mod>.hog.sha256` beside it. `sltool` comes from OpenReliant's latest release. To build it
   from a branch of OpenReliant instead, give that branch as the `source` of
   `.github/actions/sltool`;
2. publishes the release `<mod>-v<version>`, such as `viper-v1.0`, with both files attached and
   the commits that changed the mod since its last release as its notes;
3. rebuilds the [site](https://openreliant.github.io/openreliant-mods/): the mods by category, and
   [the updates](https://openreliant.github.io/openreliant-mods/updates/), every release with what
   changed in it, newest first.

A version that has a release already is left alone, so other changes to `main` release nothing. On
a pull request, the Check workflow packs every mod and builds the site, to catch a mod that doesn't
pack or isn't in a category. `python3 .github/scripts/release.py --dry-run` does the same locally,
into `dist/`, and `python3 .github/scripts/site.py` writes the site into `site/`.

## Sources

`sources/` holds what each mod was built from, with the steps to build it again, so that anyone can
change it.

## Licences

Each mod gives its licence in its folder, and its art keeps its author's licence. Everything else,
such as the manifests, scripts and build scripts, is under the Mozilla Public License 2.0
([LICENSE](LICENSE)).
