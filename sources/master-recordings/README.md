# Master Recordings

## The pieces

The pieces come from Ian Livingstone's master recordings of the score, named by his own titles
rather than the game's. Each of the game's pieces in `music\` was matched to its master by sound,
not by name, and each is a straight cut from its master. Every file is FLAC, 44.1 kHz 16-bit
stereo, which decodes to exactly the samples of the edited recording.

- The `New_` files replace the game's pieces of the same name, wherever the game plays them. Each
  is cut from its master at the start and length of the game's piece, so that the loop table's
  loop points land on the same moment of the music: OpenReliant carries them over to the mod's
  rate and format. Takeoff and Searching Mission 10 stay the game's own: no master holds Takeoff,
  and Searching Mission 10's master turns into a different version of the piece after 10 seconds.
- The `Masters_` files are the masters in full, for the CD player's tracks after its 24, which
  `cd_player.luau` adds: the game's pieces that the CD player doesn't list, the movies' music and
  the characters' themes. Reliant Funeral and Ending come from the masters of the music alone,
  since the album's versions have the movies' sounds and voices mixed in.
- Each piece is raised towards the loudness of the game's music as far as its peaks allow, to a
  true peak of -0.3 dB, and is otherwise unchanged. Eleven of the game's pieces (Mission 01,
  Pensive, the spare piece and eight of the Searching pieces) stay 3.4 to 7 dB quieter than the
  game's copies, which were made louder than plain gain can take the masters. Most of the movies'
  music already peaks at full scale, so it stays quieter than the game's music too.

## The thumbnail

`mod.png` is 700 by 280, the shape that fills the mods screen's box: the waveform of Big Intro over
a dark background, with the mod's name in Newtown, the public domain font built into OpenReliant
(`deps/newtown/Newtown.ttf` in its repository). With FFmpeg and ImageMagick 7:

```bash
ffmpeg -i "Masters_Big Intro.flac" -filter_complex \
    "aformat=channel_layouts=mono,showwavespic=s=1328x400:colors=0xff9628:scale=lin:filter=peak" \
    -frames:v 1 wave.png
magick wave.png -filter Lanczos -resize 332x200\! wave-small.png
magick -size 332x1 xc: -fx "min(1, min(i, w-1-i)/48)" -scale 332x200\! fade.png
magick wave-small.png \( fade.png -alpha copy \) -compose DstIn -composite wave-faded.png
magick wave-faded.png -blur 0x8 glow.png
magick -size 700x280 radial-gradient:'#16233a'-'#04060b' background.png
magick background.png glow.png -geometry +24+40 -compose screen -composite \
    wave-faded.png -geometry +24+40 -compose over -composite \
    -font Newtown.ttf -fill white -pointsize 42 -gravity northwest \
    -annotate +384+66 "MASTER" -annotate +384+114 "RECORDINGS" \
    -fill "rgb(255,150,40)" -pointsize 21 \
    -annotate +386+184 "Ian Livingstone's" -annotate +386+212 "44.1 kHz masters" \
    -depth 8 -strip -define png:compression-level=9 mod.png
```
