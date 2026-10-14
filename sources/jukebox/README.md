# Jukebox

## The pictures

The pictures for the mod's page, in `screenshots`, are frames of the CD player that OpenReliant 0.14
drew at 1280 by 960 with the mod: the Reliant's player turned to the Yamato's page, and the Yamato's
turned round to the Reliant's, each with a piece chosen and the pointer over the right arrow.

## The thumbnail

`mod.png` is 700 by 280, the shape that fills the mods screen's box: the Reliant's frame, cropped to
the player's screen and the plate under it, over a blurred, darkened copy of the Yamato's, with the
mod's name in Newtown, the public domain font built into OpenReliant (`deps/newtown/Newtown.ttf` in
its repository). With ImageMagick 7:

```bash
magick screenshots/01-reliant.png -crop 960x720+170+220 +repage crop.png
magick screenshots/02-yamato.png -resize 700x -gravity center -crop 700x280+0+0 +repage \
    -blur 0x12 -fill black -colorize 50% background.png
magick crop.png -filter Lanczos -resize x280 -unsharp 0x0.6 cover.png
magick cover.png \( +clone -background black -shadow 70x8+0+0 \) +swap -background none \
    -layers merge +repage shadowed.png
magick background.png shadowed.png -gravity west -geometry -12+0 -composite \
    -font Newtown.ttf -fill white -pointsize 56 -gravity northwest -annotate +392+78 "JUKEBOX" \
    -fill "rgb(255,150,40)" -pointsize 21 -annotate +394+160 "All 24 tracks on" \
    -annotate +394+188 "both CD players" -strip -define png:compression-level=9 mod.png
```
