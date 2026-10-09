# Cut Dreamcast Missions: sources

Restored cut missions found on the Dreamcast version of StarLancer. The mod puts back missions 12,
13, 17 and 22, which were cut from the campaign and whose files survive only on the Dreamcast disc.
The documents beside its files, `dreamcast_readme.md` and one for each mission, reconstruct each
mission: where it sits in the story, what the game's files say about it, every radio line with its
speaker, face and words, Enriquez's briefing and the debriefings, and how all of it was worked
out.

## The missions

`mission12.dte`, `mission13.dte`, `mission17.dte` and `mission22.dte` are the Dreamcast disc's, as
they are. The disc's `RESOURCE.HOG` uses the PC's archive format, so `sltool` takes them out:

```bash
sltool hog extract RESOURCE.HOG dreamcast
```

## The scripts

- `campaign.luau`, a load script, puts the four missions into the campaign's order
  (`records.campaign`): 12 and 13 after 11, 17 after 16, and 22 after 21. It gives each Enriquez's
  briefing, spoken over the briefing room since the game has no hologram for them, and the date the
  launch shows, which the game's text leaves as "aaaa", from the ITAC's table of mission dates
  (`records.missions`).
- `faces.luau`, run with all four missions, gives each speaker the pilot the PC's missions give the
  same person at that point of the story, and every other ship the pilot the PC's missions most
  often give a ship of its type. The Dreamcast's files number their pilots from an older pilot
  table, so most lines would show the wrong face, and other ships would fly as pilots who don't
  belong in them.
- `radio22.luau`, run with mission 22, voices the mission. Its script prints its draft radio as
  debug text and says nothing, so a `vm_command` hook on `print_debug_message` has the radio say
  the line that stands for each text (`openreliant.radio`), and sets the mission's objectives as it
  goes (`world.set_objective`), whose names `campaign.luau` gives. `radio22_lines.luau` holds the
  line, speaker and face for each text, by its place in the mission's file. `make_radio22.py`
  writes it from the mission's file and the document's radio table:

  ```bash
  python3 make_radio22.py mission22.dte sltool dreamcast_mission22.md radio22_lines.luau
  ```
- `yamato22.luau`, run with mission 22, is the mod's own ending, not the Dreamcast's: as the Yamato
  arrives, the convoy's ships whose engines still work jump out (`object.engines_intact`), and she
  picks off the big ships left behind, stopping once her guns reach each.
- `targets22.luau`, run with mission 22, is the mod's own help with its crowded last part: from the
  Badinov's on, each shield generator the player can hit becomes the target, and the primary
  target, in turn.
- `fixes22.luau`, run with mission 22, fixes flaws of its draft script, two of which leave it with
  no way to finish: the Hades bombers take no damage, a friendly torpedo that ends without hitting
  its target still destroys it, the convoy's count no longer misses a ship destroyed within two
  seconds of another, and the Badinov is disabled only once her jump is done.

## The voices

Each line is generated with [F5-TTS](https://github.com/SWivid/F5-TTS), from a reference clip of its
character's own recorded lines, then made to sound like the game's recordings. The scripts in
`voice` do it, in Python environments with `f5-tts`, `chatterbox-tts` and `openai-whisper`, from the game's speech
archive decoded to WAV files (`sltool speech extract ms_speech/msspeech.hog speech`):

1. `ref_select.py` picks each character's cleanest lines (the least clipped, the clearest to
   Whisper), joined into about nine seconds, with their words.
2. `render_f5.py` renders every line of the four documents' tables.
3. `retry_f5.py` renders a line again, with other seeds, until Whisper hears all its words. Lines
   named on its command line are rendered again whatever their score, for example after a change
   to their words or to how a name is said.
4. `render_spoken.py chatterbox:0.3:0.3` renders Enriquez's four briefings as
   `dreamcast_brief<mission>`, which she speaks over the briefing room, with
   [Chatterbox](https://github.com/resemble-ai/chatterbox) (`clone.py`). Its prompt is a clean
   stretch of her spoken briefing at the campaign's end (`enddebriefing`), and her speaker
   embedding the mean of all she says in person and in the briefing holograms. It renders a
   paragraph at a time, at a calm pace (exaggeration and pace 0.3), checks each with Whisper, trims
   each to its speech and joins them with her own pauses. A narrow notch takes out a faint 6 kHz
   tone Chatterbox's vocoder leaves between words. The same script renders with F5-TTS (`f5`),
   which sounded less natural.
5. `finish.py` matches each line to its character's recordings: an equalizer of its own, the same
   silence before and after, the same loudness under a limiter, then the game's speech codec, which
   it checks so that no line overshoots full scale more often than the game's own lines do. The
   briefings are matched to her spoken briefing at the campaign's end instead, without the radio's
   compression, and ship as MP3 recordings at 64 kbit/s (OpenReliant
   [#988](https://github.com/OpenReliant/openreliant/issues/988)), since the speech codec distorts
   long, clean speech.

`speech_text.py` holds the words both kinds of render share: the game's names, which Whisper can't
be expected to spell, and how the voices say some of them. Enriquez says "Berezhov" for the
Berijev class in her briefings, so the renders do too; names the game never says are spelled for
the voice model the usual way, such as "Gagarin" for the Gegarin.

`voices.py` lists which recorded lines each voice is cloned from. Four speakers with no lines of
their own in the game take a similar pilot's voice: Mayday takes Cutter's, Striker Juice's, and the
Maulers' and the Marauders' leaders take the Pumas' and the Buccaneers' leaders'.

## The thumbnail

`mod.png` is 700 by 280, the shape that fills the mods screen's box: the PAL Dreamcast box's front,
cropped to 4:3 from the top, over a blurred, darkened copy of it, with the mod's name in Newtown,
the public domain font built into OpenReliant (`deps/newtown/Newtown.ttf` in its repository). With
ImageMagick 7:

```bash
magick StarLancer_DC_EU_Box_Front.jpg -crop 1424x1068+0+0 +repage top.png
magick top.png -resize 700x -gravity center -crop 700x280+0+0 +repage -blur 0x12 \
    -fill black -colorize 55% background.png
magick top.png -filter Lanczos -resize x280 -unsharp 0x0.6 cover.png
magick cover.png \( +clone -background black -shadow 70x8+0+0 \) +swap -background none \
    -layers merge +repage shadowed.png
magick background.png shadowed.png -gravity west -geometry -12+0 -composite \
    -font Newtown.ttf -fill white -pointsize 40 -gravity northwest -annotate +392+62 "CUT" \
    -annotate +392+108 "DREAMCAST" -annotate +392+154 "MISSIONS" \
    -fill "rgb(255,150,40)" -pointsize 21 -annotate +394+212 "Missions 12, 13, 17 and 22" \
    -strip -define png:compression-level=9 mod.png
```
