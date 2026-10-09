# Mission 17: the Gegarin ambush

A reconstruction of the cut mission 17, whose file survives only on the Dreamcast disc. What comes
from the game's own files is marked as such. The rest, Enriquez's briefing, the debriefings and the
words of the radio lines, is written for the mod from that evidence, and is open to change.

## Where it sits

- **Dated June 6, 2161** in the ITAC's table of mission dates. The game's own launch date, text
  994, is the placeholder "aaaa", so the mod puts this date in its place.
- **After mission 16**, where the Tigers escort Gamma wing's torpedo bombers to a Coalition warp
  gate and destroy its power cells, and **before mission 18**, Foster's last stand, where the
  Reliant rams the CS Volga and is lost, and the 45th moves to the Yamato.
- **Flown as the 45th Tigers.** It's the Reliant's last great fight before Foster's sacrifice.
- **The game's own news of it.** The ITAC's news item listed after mission 17 (June 6, 2161): the
  Alliance Fleet has achieved its greatest victory yet, destroying the Coalition Class-1 carrier
  Gegarin in a combined operation. It's a symbol to the Alliance, but the Coalition still has twice
  as many carriers.

## What the files say

- **Objectives** (the PC's executable, strings 605 to 610 and 641):
  1. Lure the CS Gegarin and its escort into pursuit of the Reliant
  2. Keep the fighters busy until the Mitchell can move into position
  3. Take out the Gegarin's fighter cover to allow the torpedo bombers to make their run
  4. Destroy the Gegarin's shield generator
  5. Protect the torpedo bombers on their approach run on the Gegarin
  6. Protect the torpedo bombers on their approach run on the Berijev
  7. Return to base
- **The Alliance:** the Reliant; the Mitchell, an Alliance warship with its own bridge officer's face
  in the game; Gamma wing's two Hades torpedo bombers; the Cougars' Hades bombers. The player flies a
  Predator, with Bandit leading in a Grendel.
- **The Coalition:** the Gegarin (a Pukov-class carrier), the Berijev, two escorts (the Gurevich and
  the Shavrov), Loki cargo ships, Sabers, Laggs, Kurgens, and later a backup group led by a Zakov.
- **How it goes:** the wing jumps to a Coalition depot, where Gamma's bombers torpedo the Gurevich
  and the Shavrov. The Reliant jumps in and shows herself to provoke the Gegarin, then jumps away to
  an asteroid field, and the Gegarin follows. In the asteroids, the Mitchell moves in behind it.
  Warnings come every 30 seconds while the Gegarin's fighters are still up. Once eleven are down,
  the wing knocks out the Gegarin's shield generator, and the Cougars make their torpedo run. With
  the Gegarin destroyed, the Berijev is next. If the bombers are all lost, Coalition reinforcements
  arrive and everyone jumps home.
- **Rating** (the script's completion code): the Gegarin and the Berijev both destroyed is a success
  with the bonus, the Gegarin alone a success, and neither a total failure.
- **Debriefings:** the PC's ITAC has none of its own for mission 17, only the placeholder. They're
  written below.
- **Enriquez's last word** exists on the PC (`enrbr_tag17`).

## The story

The Gegarin is the biggest carrier the Coalition has in the sector, and Command wants it gone. Too
strong to fight head on, it has to be drawn into a trap. The Tigers and Gamma wing hit a Coalition
supply depot to stir things up, and then the Reliant herself shows up as bait. When the Gegarin
comes after her, Captain Foster jumps away into an asteroid field, where the Mitchell is waiting.
The Tigers keep the Gegarin's fighters busy until the Mitchell is in position, strip away its
fighter cover and its shields, and cover the Cougars' torpedo run. If the Gegarin goes down, the
Berijev is next.

## Enriquez's briefing

Written for the mod.

> Okay, pay attention. Today we go after the Gegarin, a Class One Coalition carrier, and the biggest
> ship they've got in this sector. Taking her on head to head would be suicide, so we're going to
> bring her to us.
>
> The Tigers and Gamma Wing will jump in to a Coalition supply depot. Gamma will deal with the
> escorts, and you'll keep their fighters busy. That should bring the Gegarin running. When she
> arrives, the Reliant will jump in and let herself be seen. Captain Foster will then lead the
> Gegarin into the asteroid field at your second nav point, where the Mitchell is waiting to close
> the trap.
>
> Once the Mitchell is in position, your first objective will be to take out the Gegarin's fighter
> cover. Next, destroy her shield generator, and protect the Cougars' bombers on their run. If the
> Gegarin goes down, the Berijev is next. This is a big one, Tigers. Let's make it count.

## The radio

In the order the lines play. The speaker is the one the line's name gives, with the face the PC's
missions give that speaker in the Tigers' time.

| Line | Speaker (face) | When | Words |
|---|---|---|---|
| `ms_rel17_001` | The Reliant's bridge officer (`Rel_Brdge_Off`) | The launch | Tigers, you're clear. Good hunting. The Reliant will join you at the depot. |
| `ms_ban17_001` | Bandit (`45TigersWL_Bandit`) | The launch | Copy, Reliant. Tigers, form up and get ready to jump. |
| `mooms1017` | Moose (`45Tigers_Moose`) | Jump drive on-line | Jump drive's on-line. Let's go. |
| `ms_ban17_002` | Bandit | Arriving at the depot | There's the depot. Cargo ships, and two escorts. |
| `ms_1gam17_001` | Gamma 1 (`Gamma_Ldr`) | Arriving at the depot | Gamma one in position. Starting our run on the Shavrov. |
| `ms_2gam17_001` | Gamma 2 (`Gamma_Ldr`) | Arriving at the depot | Gamma two, lining up on the Gurevich. |
| `ms_ban17_003` | Bandit | Arriving at the depot | Tigers, keep those fighters off Gamma. |
| `ms_rel17_002` | The Reliant's bridge officer | The Reliant jumps in | Reliant on station. Moving into the open, let's see if they take the bait. |
| `ms_rel17_005` | The Reliant's bridge officer | The Reliant jumps in | We're broadcasting in the clear. If the Gegarin's out there, she knows we're here. |
| `ms_ban17_008` | Bandit | The Reliant jumps in | Stay close to the Reliant, Tigers. She's sticking her neck out for this. |
| `ms_rus17_002` | The Gegarin's captain (`Pukov_Cap`) | The Gurevich destroyed | You will pay for that, Alliance dogs! All fighters, destroy them! |
| `ms_1gam17_002` | Gamma 1 | The Gurevich destroyed | Gurevich is history. Gamma's pulling out. |
| `ms_ban17_004` | Bandit | The Gurevich destroyed | Nice work, Gamma. See you at the rendezvous. |
| `ms_dice17_001` | Diceman (`45Tigers_Plt`) | The Gegarin jumps in | Big contact jumping in! That's the Gegarin! |
| `ms_ban17_010` | Bandit | The Gegarin jumps in | And she's launching fighters. Here they come! |
| `ms_rel17_003` | The Reliant's bridge officer | The Reliant shows herself | The Gegarin's turning toward us. She's taken the bait. |
| `ms_ban17_006` | Bandit | The Reliant shows herself | Keep her interested, Reliant. Not too close. |
| `ms_rel17_004` | The Reliant's bridge officer | The Gegarin gives chase | She's coming after us. Jumping to the asteroid field now! |
| `ms_ban17_007` | Bandit | The Gegarin gives chase | Tigers, follow the Reliant in. Let's spring that trap. |
| `ms_rel17_006` | The Reliant's bridge officer | In the asteroid field | All ships, the Gegarin is jumping in behind us. The Mitchell is moving into position. |
| `ms_ban17_009` | Bandit | In the asteroid field | Keep her fighters busy, Tigers. Buy the Mitchell some time. |
| `ms_mit17_001` | The Mitchell's bridge officer (`Mitchel_Brdge_Off`) | The trap closes | This is the Mitchell. We're in position. The Gegarin has nowhere to run. |
| `ms_dice17_002` | Diceman | The trap closes | She's launching everything she's got! |
| `ms_rel17_007` | The Reliant's bridge officer | The trap closes | Tigers, take out that fighter cover so the bombers can get in. |
| `ms_mit17_002` | The Mitchell's bridge officer | 30 seconds | Tigers, we're taking fire. We need those fighters cleared out. |
| `ms_rel17_008` | The Reliant's bridge officer | 60 seconds | Tigers, the bombers are waiting on you. Clear those fighters! |
| `ms_cou17_001` | The Cougars' leader (`Couger_Plt`) | 90 seconds | Cougars to Tigers, we can't start our run with those fighters out there. |
| `ms_cou17_002` | The Cougars' leader | 120 seconds | Tigers, we're running out of time here. Clear us a path! |
| `ms_rel17_009` | The Reliant's bridge officer | 120 seconds | We can't hold her here much longer, Tigers! |
| `ms_mit17_003` | The Mitchell's bridge officer | Fighter cover down | Fighter cover's down. Now go for her shield generator. |
| `ms_ban17_011` | Bandit | Fighter cover down | You heard him. Target the shield generator! |
| `ms_ban17_005` | Bandit | The player hits the Gegarin | That's it, keep hitting her! |
| `ms_dice17_003` | Diceman | Shield generator destroyed | Her shields are down! |
| `ms_cou17_003` | The Cougars' leader | Shield generator destroyed | Cougars beginning our torpedo run. Keep them off us! |
| `ms_cou17_004` | The Cougars' leader | Their escort's attackers down | Thanks, Tigers. Torpedoes away! |
| `ms_ban17_012` | Bandit | Their escort's attackers down | Stay with the bombers, Tigers! |
| `ms_cou17_005` | The Cougars' leader | The Gegarin destroyed | Direct hit! The Gegarin is breaking up! |
| `ms_ban17_013` | Bandit | The Gegarin destroyed | Yee-ha! The Gegarin's going down! |
| `ms_1gam17_003` | Gamma 1 | The Gegarin destroyed | Gamma here. Saw the whole thing. Beautiful. |
| `ms_cou17_006` | The Cougars' leader | The Gegarin destroyed, bombers alive | Cougars rearming. Lining up on the Berijev. |
| `ms_ban17_015` | Bandit | The Berijev next | One more, Tigers. Cover the Cougars on the Berijev! |
| `ms_cou17_007` | The Cougars' leader | The Berijev next | Starting our run on the Berijev. |
| `ms_mit17_005` | The Mitchell's bridge officer | The bombers lost, the Gegarin alive | We've lost the bombers. There's nothing more we can do here. |
| `ms_1gam17_004` | Gamma 1 | The bombers lost, the Gegarin alive | Gamma's out of torpedoes. We're out of here. |
| `ms_rel17_999` | The Reliant's bridge officer | Coalition backup | Coalition reinforcements jumping in! All ships, jump out now! |
| `ms_mit17_004` | The Mitchell's bridge officer | The Gegarin destroyed, the bombers lost | The Gegarin's gone, but so are the bombers. The Berijev will have to wait. |
| `ms_mit17_006` | The Mitchell's bridge officer | The bombers lost after the Gegarin | We've lost the bombers. The Berijev will have to wait for another day. |
| `ms_rel17_010` | The Reliant's bridge officer | Pulling out | All ships, we're pulling out. Jump home. |
| `ms_ban17_014` | Bandit | Pulling out | You heard him, Tigers. Let's go home. |
| `ms_rel17_011` | The Reliant's bridge officer | The Berijev destroyed | The Berijev is destroyed! Outstanding work, all of you. Jump home. |
| `ms_rel17_013` | The Reliant's bridge officer | Home, both destroyed | Welcome home, Tigers. Two capital ships in one day. The Captain wants to buy you all a drink. |
| `ms_rel17_015` | The Reliant's bridge officer | Home, the Gegarin destroyed | Welcome home, Tigers. The Gegarin's gone. That's a big day for the Alliance. |
| `ms_rel17_014` | The Reliant's bridge officer | Home, neither destroyed | Tigers, you're cleared to land. We'll talk about this at the debriefing. |

## The debriefings

Written for the mod, for the ratings the mission can reach.

- **Success with the bonus:**
  > Outstanding, pilot. The Gegarin and the Berijev are both gone, and Command is calling it the
  > greatest victory of the war so far.
  >
  > The Gegarin was one of the Coalition's largest carriers, and losing her will hurt them badly. But
  > don't let it go to your head. The Coalition still has twice as many carriers as we do.
  >
  > Captain Foster took a big risk using the Reliant as bait, and you made it pay off. Well done.
- **Success:**
  > Good work. The Gegarin has been destroyed, and that's a heavy blow to the Coalition fleet.
  >
  > The Berijev got away, though. With better protection for the bombers, she would have gone down
  > too. Remember that next time.
- **Total failure** (the pilot's career ends): no debriefing.

## Open points for the mod

- **Faces:** the mission's comms give the wrong faces. The mod sets the speaking ships' pilots as
  the mission starts (the wing leader's Grendel to Bandit, the Reliant to its bridge officer, the
  Mitchell to its bridge officer, the Hades bombers to Gamma's and the Cougars' pilots, the Gegarin
  to its captain), and maps the pilot numbers its comms commands use: 8 to Diceman, 102 to Moose.
- **Voices:** the 53 lines are voiced, and so is Enriquez's briefing, as `dreamcast_brief17`.
- **Debriefings and briefing hologram:** OpenReliant can't yet give a mod's mission its own
  debriefings and briefing speech ([#976](https://github.com/OpenReliant/openreliant/issues/976)).
