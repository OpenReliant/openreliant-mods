# StarLancer Prequel Missions: sources

The mod's missions, lines, movies and ending picture are the StarLancer trial's own files, from
the demo disc's install (`sldemo`), with new names where they would replace the game's:

| In the mod | From the trial |
|---|---|
| `mission91.dte`, `mission92.dte` | `mission1.dte` and `mission2.dte` in `resource.hog` |
| `DMS1_*`, `dms2_*` | the lines of the same names in `ms_speech/msspeech.hog` |
| `prequel_m01.bik`, `prequel_m02.bik` | `New_m01.bik` and `new_m02.bik` |
| `blurb.png` | `blurb.tga` in `resource.hog` |

`sltool hog extract` takes the files out of the two archives, and ImageMagick 7 turns the blurb into
a PNG:

```bash
sltool hog extract sldemo/resource.hog trial
sltool hog extract sldemo/ms_speech/msspeech.hog trial-speech
magick trial/blurb.tga blurb.png
```

The scripts are the mod's own. `menu.luau` registers the game mode with the trial's objectives and
draws the ending, `records.luau` gives the trial's ship stats and classes, text, faces and ITAC
text for the mode's missions, and `global.luau` picks the movie that plays when a mission is lost.

`mod.png` is a picture OpenReliant draws of mission 91, with the prequel in the game's `mods`
folder: the player's Naginata just after its launch, with the Yamato behind. ImageMagick 7 crops it
to the thumbnail:

```bash
openreliant <game> --no-sound --no-intro --mission 91 --skip-launch --watch Player \
    --watch-from 0.9,-0.5,2.4 --size 1440x1080 --screenshot shot.png --screenshot-ticks 60
magick shot.png -crop 960x720+150+63 +repage -level 0%,88% -resize 320x240 -strip mod.png
```
