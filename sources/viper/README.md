# Viper Mk II: sources

What [`mods/viper`](../../mods/viper) is built from. The model is "Battlestar Galactica Viper Mark
2" by [LocoPixel](https://sketchfab.com/locopixel),
[on Sketchfab](https://sketchfab.com/3d-models/battlestar-galactica-viper-mark-2-1bf9872a1e8d4b39a259e14a7015a0a2),
under [CC-BY-NC-4.0](http://creativecommons.org/licenses/by-nc/4.0/); see the mod's
[credits](../../mods/viper/license.txt) for what was changed.

- `viper.gltf` and `scene.bin`: the model as Sketchfab exports it, under a node `viper` that scales
  and turns it to the game's axes, with marker nodes at the scene's root in the game's units: the
  three engine glows (`engine_glow:1`, scaled to the plume's width and length), the two gun muzzles
  at the barrels' tips, the missile hardpoints, the eject point and the jump lights.
- `textures/09_-_Default.001_baseColor.png`: the hull's original texture.
- `textures/hull_*.png`: the worn hull the model uses, its colour, roughness and metalness, and
  normal map, made by `worn/make.py`.
- `hud.py`: draws the flight display's pictures of the ship from the model.
- `views.py`: draws the model from the front, the back, the side and the top, with a grid in the
  game's units, for placing markers.

## Building

With OpenReliant's `sltool`, Python 3, ImageMagick 7 and Node.js, for
[glTF Transform](https://gltf-transform.dev):

```bash
cd worn && python3 make.py && cp hull_color.png hull_mr.png hull_normal.png ../textures/ && cd ..
npx @gltf-transform/cli weld viper.gltf welded.glb
npx @gltf-transform/cli simplify welded.glb viper.glb --ratio 0.3 --error 0.002
sltool shp from-gltf viper.glb ../../mods/viper/viper.shp
sltool shp obj ../../mods/viper/viper.shp viper.obj
python3 hud.py viper.obj ../../mods/viper scem icon wire
```

- `make.py` takes a minute and leaves its working pictures in `worn`.
- `weld` and `simplify` halve the model's triangles with meshoptimizer, from about 54,000 to about
  24,000, moving no surface by more than 0.2% of the model's radius.
- `from-gltf` writes the model's textures, `viper_0.png` to `viper_7.png` with their maps, beside the
  model.
