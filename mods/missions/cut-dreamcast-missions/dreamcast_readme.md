# Cut Dreamcast Missions

Restored cut missions found on the Dreamcast version of StarLancer. Missions 12, 13, 17 and 22 were
cut from the campaign, and their files survive only on the Dreamcast disc. These documents
reconstruct each one for the mod that puts them back: where it sits in the story, what the game's
files say about it, Enriquez's briefing, every radio line with its speaker, face and words, and the
ITAC's debriefings. They ship with the mod.

| Mission | Document | Between | The story | Lines |
|---|---|---|---|---|
| 12 | [mission12.md](dreamcast_mission12.md) | 11 and 14 | The Black Guard ambush the Reliant; Nicolai Petrov gets away | 52 |
| 13 | [mission13.md](dreamcast_mission13.md) | 12 and 14 | Stahl's Marines raid the Kafelnikof, a cloaked base near Saturn | 51 |
| 17 | [mission17.md](dreamcast_mission17.md) | 16 and 18 | The Reliant baits the carrier Gegarin into an ambush | 53 |
| 22 | [mission22.md](dreamcast_mission22.md) | 21 and 23 | The Tigers and Ronin stop a convoy bound for Neptune | 134 |

`mooms1017`, Moose's "jump drive on-line", plays in all four, so the mod has 288 radio lines, and
Enriquez's four briefings.

## What the game's files give

- **Objectives:** the PC's executable names them for missions 12, 13 and 17 (strings 457, 596 to
  604, 605 to 610). String 632, "Destroy the Reliant's attackers", is used by no mission and fits
  mission 12.
- **Debriefings:** the PC's ITAC has mission 12's for every rating it can reach (strings 299 to
  315). Mission 13's success row repeats mission 15's, and the rest are placeholders.
- **Dates:** the date the launch shows is a placeholder, "aaaa", for all four missions, on the PC
  and the Dreamcast alike (texts 989, 990, 994 and 999). The ITAC's table of mission dates has
  theirs: February 2, 2161 for 12, February 21 for 13, June 6 for 17 and October 17 for 22. For the
  other missions, that table matches the launch's dates, except for mission 18's month and mission
  25's year. The mod's `campaign.luau` puts them in.
- **News:** the ITAC's news after mission 13 renames the squadron the 45th Tigers, after 17 reports
  the Gegarin destroyed, and after 22 reports a Coalition force stopped on its way to Neptune.
- **Faces:** the game's face table has faces made for these missions' speakers, some used by no PC
  mission: Nicolai Petrov, the Lueneberg's pilot, Stahl with his Marines, the Mitchell's bridge
  officer and the Pukov-class captain.
- **Radio words:** only mission 22's, as debug text. The game has no subtitles for its radio. The
  words of 12, 13 and 17 are written from their line names, speakers, triggers and objectives, and
  from the canon missions around them.

## How they were reconstructed

1. **The missions' files.** The four mission files come from the Dreamcast disc's `RESOURCE.HOG`,
   which uses the PC's archive format. They're standard `.DTE` missions, so OpenReliant flies them
   as they are, and `sltool dte` lists their ships, triggers and script parts, and disassembles their
   scripts.
2. **What each line is.** The scripts play their radio lines by file name, such as `ms_ban12_004`,
   with commands that name the ship or pilot speaking. The name gives the speaker (`ban` is Bandit,
   `rel` the Reliant, `pet` Petrov), and the routine that plays it gives the moment: a trigger such
   as "the Lueneberg destroyed", or a named script part such as "Kamovs_fire_lunen". The scripts'
   own variables, such as "Reliant torp hits" or "Petrov dead", show what each mission tracks and
   how it rates the player.
3. **The words.** No recording or text of these lines survives, except mission 22's, whose draft
   radio the file prints as debug text. The other words were written to fit each line's speaker and
   moment, the mission's objectives, and its debriefing where the game has one. Enriquez's briefings
   follow her own, transcribed from the holograms of the canon missions around them: how she opens,
   sets out the plan objective by objective, and closes.
4. **The canon around them.** The ITAC's news and debriefings, and the objectives of the canon
   missions before and after each, place every cut mission in the story: its date, which squadron
   name the 45th flies under, and what the news later reports of it.
5. **The faces.** The Dreamcast files number their pilots from an older pilot table, so most
   speakers would show the wrong face, and the other ships would fly, taunt and report as pilots
   who don't belong in them, such as Coalition fighters flown by the nanny's pilot. The mod's
   `faces.luau` gives each speaker the pilot the PC's missions give the same speaker at that point
   in the story, and every other ship the pilot the PC's missions most often give a ship of its
   type. The player's wing keeps the pilots the game gives it.
6. **The voices.** Each speaker's radio lines are voiced by a voice model, F5-TTS, cloned from
   that character's recorded lines in the game ([the cast](#the-cast)). A speech recognizer,
   Whisper, checks every line, and one with a word missing or repeated is rendered again.
7. **The radio sound.** Each radio line then gets the game's radio sound: an equalizer matches its
   tone to the character's recorded lines, and it's brought to their loudness and encoded in the
   game's speech format. A line that the format would clip more often than the game's own lines is
   made a little quieter.
8. **Enriquez's briefings.** The game has no hologram for these missions, so Enriquez speaks each
   briefing over the briefing room, as she does at the campaign's end, while another mission's
   hologram that fits plays on the screen without its sound. Her briefings are voiced by
   Chatterbox, from a clean stretch of that speech at the campaign's end, with her voice averaged
   over all she says in person and in the briefing holograms, a paragraph at a time, at a calm,
   measured pace. They pause as she does there, and match its tone and loudness without being
   compressed. Chatterbox's vocoder leaves a faint 6 kHz tone between words, which a narrow notch
   takes out. They ship as MP3 recordings at 64 kbit/s, since the game's speech format distorts
   long, clean speech; the WAV masters are kept with the mod's sources.
9. **Pronunciation.** The game's names are said as its own voices say them: Enriquez says
   "Berezhov" for the Berijev class. Names the game never says are said the usual way: the Gegarin
   as "Gagarin", Gurevich as "Gurevitch".

## The cast

Each speaker's lines across the four missions, and the game's recordings their voice is cloned
from. The faces are listed in each document.

| Speaker | Lines | By mission | Voice cloned from |
|---|---|---|---|
| Diceman | 62 | 12: 4, 13: 4, 17: 3, 22: 51 | Diceman's radio lines, `ms*_dice_*` |
| Bandit | 51 | 12: 13, 13: 23, 17: 15 | Bandit's radio lines, `ms*_ban_*` |
| The Reliant's bridge officer | 29 | 12: 14, 17: 15 | the bridge officer's radio lines, `ms*_rel_*`, `relbdg_*`, `ms18_reliant*` |
| Moose | 25 | 12: 12, 13: 3, 17: 1, 22: 9 | Moose's radio lines, `ms*_moo_*` |
| Stalker | 20 | 22: 20 | Stalker's wingman calls, `sta_*`, `staejt*`, `stadth*` |
| Enriquez | 17 | 22: 17 | Enriquez's radio lines, `ms*_enq_*`, `enrbr_tag*`; the briefings from the canon holograms, `brief*` |
| Hades' leader | 16 | 22: 16 | Gamma 2's lines, `ms*_gam2_*` |
| The boarding ship's pilot | 12 | 13: 12 | mission 11's boarding ship, `ms11_bshp_*` |
| The Ronin's leader | 12 | 22: 12 | the Ronin's lines, `ms*_ron_*`, `ms*_ronwl_*` |
| Commander Stahl | 9 | 13: 9 | Stahl's lines, `ms9_stal_*`, `ms28_stl_*` |
| The Cougars' leader | 7 | 17: 7 | the Cougars' lines, `ms*_cougwl_*`, `ms1_rtwo_*` |
| The Mitchell's bridge officer | 6 | 17: 6 | the Mitchell's lines, `ms*_mitch_*` |
| Nicolai Petrov | 4 | 12: 4 | Petrov's lines, `ms19_npet_*`, `ms*_nic_*`, `np_res*` |
| Gamma 1 | 4 | 17: 4 | Gamma 1's lines, `ms*_gam1_*` |
| Gamma's leader | 4 | 22: 4 | Gamma 1's lines, `ms*_gam1_*` |
| The nanny's pilot | 2 | 12: 2 | the nanny pilots' lines, `ms*_nan_*` |
| The Reliant's address system | 1 | 12: 1 | the Reliant's bridge officer, as above |
| The Lueneberg | 1 | 12: 1 | the Lueneberg's lines, `ms*_lun_*`, `ms1_luntwo_*` |
| The Yamato's bridge officer | 1 | 12: 1 | the bridge officer's lines, `ms*_yam_*`, `yambdg_*` |
| Gamma 2 | 1 | 17: 1 | Gamma 2's lines, `ms*_gam2_*` |
| The Gegarin's captain | 1 | 17: 1 | mission 27's `ms27_apet_*` |
| Frenchy | 1 | 22: 1 | Frenchy's wingman calls, `fre_*`, `freejt*`, `fredth*` |
| Mayday | 1 | 22: 1 | Cutter's wingman calls, `cut_*`, `cutejt*`: Mayday has no recordings |
| Striker | 1 | 22: 1 | Juice's wingman calls, `jui_*`, `juiejt*`: Striker has no recordings |
| The Maulers' leader | 1 | 22: 1 | the Pumas' leader, `ms15_tan_*` |
| The Marauders' leader | 1 | 22: 1 | the Buccaneers' leader, `ms18_buc_*`, `ms21_buc_*` |
