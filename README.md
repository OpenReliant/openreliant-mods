# OpenReliant mods

Mods for [OpenReliant](https://github.com/OpenReliant/openreliant), the open-source reimplementation
of StarLancer's engine. Each mod here is checked by the OpenReliant maintainers: it works with the
OpenReliant version its manifest names, and its licence lets you share it.

You need OpenReliant and your own copy of StarLancer. No mod here holds any of the game's files.

**[Browse and download the mods](https://openreliant.github.io/openreliant-mods/)**, each from its
latest release.

## Mods

| Mod | What it adds | Needs | Licence |
|---|---|---|---|
| [Instructor, Shut Up](mods/instructor-shut-up) | Instant Action truly becomes Instant | OpenReliant 0.7 | MPL-2.0 |
| [Viper Mk II](mods/viper) | Fly the Viper Mk II: fast and agile, with two kinetic guns, light shields and a strong hull | OpenReliant 0.7 | Model and pictures CC-BY-NC-4.0, by LocoPixel ([credits](mods/viper/license.txt)) |

## Installing a mod

Download the mod's `.hog` file and its `.hog.sha256` file from its latest release, and put both in
the `mods` folder of your game folder, next to `resource.hog`. Then turn it on in OpenReliant's mods
screen. OpenReliant checks the archive against its checksum as it loads it.

To try the latest changes before they're released, copy the mod's folder from `mods/` into the
same `mods` folder instead, keeping its name: `mods/viper` becomes `<game>/mods/viper`. The name
matters: the game and the mod's scripts know what a mod adds by it, such as `viper:viper` for the
Viper, and `viper.hog` gives the same names.

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

## Releasing a mod

A mod's version is the `Version` in its `mod.ini`. To release it, raise the version and push to
`main`. The Publish workflow then:

1. packs the mod's folder into `<mod>.hog` with `sltool hog pack --checksum`, with
   `<mod>.hog.sha256` beside it. `sltool` is built from OpenReliant's `main` until a release can
   pack every mod here; the `source` of `.github/actions/sltool` then switches to `release`;
2. publishes the release `<mod>-v<version>`, such as `viper-v1.0`, with both files attached and
   the commits that changed the mod since its last release as its notes;
3. rebuilds the [index page](https://openreliant.github.io/openreliant-mods/).

A version that has a release already is left alone, so other changes to `main` release nothing. On
a pull request, the Check workflow packs every mod and builds the page, to catch a mod that doesn't
pack. `python3 .github/scripts/release.py --dry-run` does the same locally, into `dist/`, and
`python3 .github/scripts/site.py` writes the page into `site/`.

## Sources

`sources/` holds what each mod was built from, with the steps to build it again, so that anyone can
change it.

## Licences

Each mod gives its licence in its folder, and its art keeps its author's licence. Everything else,
such as the manifests, scripts and build scripts, is under the Mozilla Public License 2.0
([LICENSE](LICENSE)).
