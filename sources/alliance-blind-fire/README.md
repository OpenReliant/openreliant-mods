# Alliance Blind Fire: sources

`records.luau` is the mod's whole source, so there's nothing to build. It sets `blind_fire` in the
records of the six Alliance fighters that lack it, and of their `t_` twins
(`records.ship_types`). It needs an OpenReliant that has that field.

`mod.svg` is the mod's thumbnail, an original drawing of two tracers bent onto a target under
blind fire's sight, beside the reticle. `mod.png` is made from it with headless Chrome:

```bash
chrome --headless=new --hide-scrollbars --window-size=320,240 \
  --screenshot=../../mods/gameplay/alliance-blind-fire/mod.png mod.svg
```
