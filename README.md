# OpenReliant mods

Mods for [OpenReliant](https://github.com/OpenReliant/openreliant), the open-source reimplementation
of StarLancer's engine. Each mod here is checked by the OpenReliant maintainers: it works with the
OpenReliant version its manifest names, and its licence lets you share it.

You need OpenReliant and your own copy of StarLancer. No mod here holds any of the game's files.

## Mods

| Mod | What it adds | Needs | Licence |
|---|---|---|---|
| [Viper Mk II](mods/viper) | A new ship type for the player: a fast, agile gunfighter with two kinetic guns, no blind fire, light shields and a strong hull | OpenReliant 0.7 | Model and pictures CC-BY-NC-4.0, by LocoPixel ([credits](mods/viper/license.txt)) |

## Installing a mod

Copy the mod's folder from `mods/` into the `mods` folder of your game folder, next to
`resource.hog`, keeping its name: `mods/viper` becomes `<game>/mods/viper`. Then turn it on in
OpenReliant's mods screen. The folder's name matters: the game and the mod's scripts know what a mod
adds by it, such as `viper:viper` for the Viper.

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

## Sources

`sources/` holds what each mod was built from, with the steps to build it again, so that anyone can
change it.

## Licences

Each mod gives its licence in its folder, and its art keeps its author's licence. Everything else,
such as the manifests, scripts and build scripts, is under the Mozilla Public License 2.0
([LICENSE](LICENSE)).
