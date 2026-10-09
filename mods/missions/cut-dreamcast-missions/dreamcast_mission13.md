# Mission 13: the raid on the Kafelnikof

A reconstruction of the cut mission 13, whose file survives only on the Dreamcast disc. What comes
from the game's own files is marked as such. The rest, Enriquez's briefing, the debriefings and the
words of the radio lines, is written for the mod from that evidence, and is open to change.

## Where it sits

- **Dated February 21, 2161** in the ITAC's table of mission dates. The game's own launch date, text
  990, is the placeholder "aaaa", so the mod puts this date in its place.
- **After mission 12**, the Black Guard's attack on the Reliant, and **before mission 14**, the raid
  on the Stalag with the Ronin.
- **Flown as the 45th Volunteers.** The ITAC's news after this mission announces the new name, the
  45th Tigers (February 21, 2161). The same news says the Coalition is pulling its hunting packs back
  to regroup around Saturn.
- **The war around it.** Chapter 2's "Counterstrike": the Alliance is raiding Coalition supply lines
  with hit and run attacks, and the Coalition's forward fleet is falling back to Titan. Mission 11
  had a boarding party aboard the Czar, and mission 14 recovers fuel cells from the Stalag, a
  Coalition base that supplies their warp gates.

## What the files say

- **Objectives** (the PC's executable, strings 596 to 601):
  1. Kill the patrolling Kurgens
  2. Destroy the cloak generator
  3. Protect the boarding ship during drop-off and pick-up run
  4. Take out the service hatch
  5. Protect the boarding ship for second drop and pick-up run
  6. Return to base
- **Setting:** near Saturn and Titan. The Kafelnikof (a ship type of its own) is a Coalition base
  hidden under a cloak, with gun and missile satellites and a field of proximity mines around it.
- **The 45th:** the player in a Grendel, Bandit leading in a Patriot, Diceman in a Tempest, and
  wingmen in a Predator, a Crusader and a Grendel. Commander Stahl's Marines ride in a Limpet
  boarding ship.
- **The Coalition:** two Kurgen gunboats on patrol, then Basilisks that jump in twice while the
  boarding ship is docked, more of them in a network game.
- **How it goes:** the wing jumps to the base, kills the Kurgens, and destroys the cloak generator.
  The boarding ship docks and lands the Marines, who fight the garrison; Basilisks jump in, and the
  wing targets the base's comms tower. The boarding ship picks the first team up, the wing blows the
  service hatch, and the boarding ship docks again for a second run. More Basilisks jump in. When the
  second team is out, the Kafelnikof explodes, and the wing jumps home to the Reliant.
- **Rating** (the script's completion code): the boarding ship destroyed is a total failure. The
  base destroyed with every Basilisk shot down is a success with the bonus, the base destroyed a
  success, and coming home without it a partial success.
- **Debriefings:** the PC's ITAC has none of its own for mission 13. Its success row repeats mission
  15's debriefing about McGann, and the rest are the placeholder many missions share. So they're
  written below.
- **Enriquez's last word** exists on the PC (`enrbr_tag13`).

## The story

Coalition hunting packs have been striking from nowhere, and Intelligence has traced them to the
Kafelnikof, a supply base near Saturn that hides under a cloak. The Volunteers escort Commander
Stahl's Marines there. They take out the patrolling Kurgens, then knock out the cloak generator, and
the base appears. The Marines go in twice: the first team clears the garrison and takes the base's
data, and the second goes in through the service hatch to set charges in the reactor. Basilisks
arrive to defend it, and the base's comms tower has to come down before it can call more. When the
Marines are out, the Kafelnikof goes up, and the hunting packs lose their hiding place.

## Enriquez's briefing

Written for the mod.

> Let's get started, people. For weeks now, Coalition hunting packs have been hitting our convoys
> and vanishing without a trace. Intelligence have finally found out how. This is the Kafelnikof, a
> Coalition supply base near Saturn. It's hidden under a cloak, and it's been refuelling and rearming
> those packs right under our noses.
>
> Commander Stahl's Marines are going to take it apart, and you're going to get them there. Your
> first objective will be to take out the Kurgen gunboats on patrol, before they can raise the
> alarm. Next, destroy the cloak generator. That will bring the base out where we can see it.
>
> The boarding ship will then make two runs. The first team will take the garrison and download
> everything in the base's computers. When they're out, you'll blow the service hatch, so that the
> second team can reach the reactor and set their charges. The boarding ship is your priority. Lose
> it, and the mission is over. Everyone clear?

## The radio

In the order the lines play. The speaker is the one the line's name gives, with the face the PC's
missions give that speaker in the Volunteers' time.

| Line | Speaker (face) | When | Words |
|---|---|---|---|
| `ms_ban13_001` | Bandit (`45VolntrWL_Bandit`) | The launch | Form up on me, Volunteers. We're babysitting Marines today, so stay tight. |
| `ms_sta13_001` | Commander Stahl (`Stahl_BrdShip`) | The launch | Stahl here. My men are ready. You keep the sky clear, we'll do the dirty work. |
| `ms_ban13_002` | Bandit | The launch | Copy that, Commander. Jump on my mark. |
| `mooms1017` | Moose (`45Volntrs_Moose`) | Jump drive on-line | Jump drive's on-line. Let's go. |
| `ms_ban13_003` | Bandit | Arriving at the base | Nothing on scope, but Intel says the base is right in front of us, under that cloak. Watch for patrols. |
| `ms_ban13_004` | Bandit | The Kurgens attack | Kurgens! Take them out before they raise the alarm! |
| `ms_bshp13_001` | The boarding ship's pilot (`Marine_Leader`) | The Kurgens attack | Boarding ship holding back until you clear those gunboats. |
| `ms_ban13_005` | Bandit | The Kurgens destroyed | Kurgens down. Nice shooting. |
| `ms_dice13_001` | Diceman (`45Volntrs_Plt`) | The Kurgens destroyed | Bandit, I'm picking up a power source dead ahead. Has to be the cloak generator. |
| `ms_dice13_002` | Diceman | Four seconds later | There it is. Sending you the coordinates. |
| `ms_moo13_001` | Moose | After Diceman | So that's where they've been hiding. Let's go knock on the door. |
| `ms_ban13_006` | Bandit | After Moose | Target the cloak generator. Let's bring that base out where we can see it. |
| `ms_ban13_007` | Bandit | The base decloaks | There she is! Clear out those defense satellites so the boarding ship can get in. |
| `ms_ban13_008` | Bandit | The boarding ship moves in | Boarding ship, the way's clear. Take her in. |
| `ms_bshp13_002` | The boarding ship's pilot | The boarding ship moves in | Copy, Alpha Leader. Moving in to dock. Keep them off our backs. |
| `ms_bshp13_003` | The boarding ship's pilot | Docked, first run | We're docked. Marines going in. |
| `ms_dice13_003` | Diceman | The Basilisks arrive | Contacts jumping in! Basilisks, a whole wing of them! |
| `ms_ban13_009` | Bandit | The Basilisks arrive | They must have got a call out. Protect that boarding ship! |
| `ms_sta13_002` | Commander Stahl (`Stahl_Marines`) | The Basilisks arrive | We're inside. Heavy resistance, but we're pushing through. |
| `ms_ban13_010` | Bandit | The Basilisks arrive | Take out their comms tower. No more calls for help. |
| `ms_sta13_003` | Commander Stahl | The garrison destroyed | Garrison's neutralized. We're downloading their computers now. |
| `ms_sta13_004` | Commander Stahl | First pickup | We've got what we came for. First team ready for pickup. |
| `ms_sta13_005` | Commander Stahl | Five seconds later | Boarding ship, we're at the airlock. Where are you? |
| `ms_sta13_006` | Commander Stahl | Thirty seconds later | We can't hold this airlock forever. Get us out of here! |
| `ms_ban13_011` | Bandit | The boarding ship goes back | Boarding ship, go get them. We'll cover you. |
| `ms_bshp13_004` | The boarding ship's pilot | Undocked, first run | First team's aboard. Pulling away. |
| `ms_ban13_012` | Bandit | Blow the hatch | The second team needs another way in. Blow that service hatch! |
| `ms_ban13_013` | Bandit | The hatch gone | Hatch is gone. Stahl, you've got your door. |
| `ms_sta13_007` | Commander Stahl | The hatch gone | Nice shooting. Second team's ready to go. |
| `ms_ban13_014` | Bandit | The hatch gone | Boarding ship, you're clear for the second run. |
| `ms_bshp13_005` | The boarding ship's pilot | The hatch gone | Roger that. Coming around now. |
| `ms_ban13_015` | Bandit | The hatch gone | Stay close to her, Volunteers. |
| `ms_bshp13_200` | The boarding ship's pilot | The hatch gone | Second team standing by to deploy. |
| `ms_sta13_008` | Commander Stahl | The hatch gone | Marines, this is it. Set the charges on that reactor and get out fast. |
| `ms_ban13_016` | Bandit | The hatch gone | You heard the man. Let's make this quick. |
| `ms_ban13_017` | Bandit | Second run | The boarding ship's moving in. Cover her! |
| `ms_bshp13_006` | The boarding ship's pilot | Second run | Lining up on the service hatch. |
| `ms_bshp13_007` | The boarding ship's pilot | Docked, second run | We're docked. Second team's away. |
| `ms_dice13_004` | Diceman | More Basilisks | More Basilisks decloaking! |
| `ms_ban13_018` | Bandit | More Basilisks | Keep them off the boarding ship! |
| `ms_sta13_009` | Commander Stahl | Second pickup | Charges are set! We're coming out! |
| `ms_bshp13_008` | The boarding ship's pilot | Second pickup | Going in for the pickup. |
| `ms_ban13_019` | Bandit | Second pickup | Make it fast. This place is about to go up. |
| `ms_bshp13_009` | The boarding ship's pilot | Undocked, second run | Everybody's aboard! We're clear! |
| `ms_ban13_020` | Bandit | Leaving | All Volunteers, pull back! Now! |
| `ms _moo13_002` | Moose | The base explodes | Woo! Look at her go! |
| `ms _ban13_300` | Bandit | The base explodes | That's one less hole for them to hide in. Good work, Volunteers. |
| `ms_ban13_022` | Bandit | Arriving home | Reliant, this is Alpha Leader. We're back. Request landing clearance. |
| `ms_bshp13_010` | The boarding ship's pilot | The boarding ship under fire | We're taking fire! Get them off us! |
| `ms_bshp13_011` | The boarding ship's pilot | Under fire again | Hull's breached! We can't take much more of this! |
| `ms_ban13_021` | Bandit | The boarding ship destroyed | We've lost the boarding ship. It's over, Volunteers. Form up, we're going home. |

Two names, `ms _moo13_002` and `ms _ban13_300`, have a space after `ms` in the mission's file. The
game looks for the files by those names, so the mod's files keep the space.

## The debriefings

Written for the mod, for the ratings the mission can reach. The ITAC shows each as paragraphs.

- **Success with the bonus:**
  > Outstanding work, pilot. The Kafelnikof is gone, and so is every Basilisk the Coalition sent to
  > defend it.
  >
  > Commander Stahl's Marines brought back the base's records intact. Intelligence is already working
  > through them, and they tell us where the hunting packs have been striking from and when they
  > meant to strike again. Our convoys will be a lot safer for it.
  >
  > Commander Stahl asked me to pass on his thanks. He says he's never had better cover.
- **Success:**
  > Good work. The Kafelnikof has been destroyed, and Commander Stahl's Marines are back aboard
  > safely with the base's records.
  >
  > Some of the Basilisks got away, though, and they'll be back. Remember that the boarding ship's
  > safety and the enemy's fighters go hand in hand. Every fighter you leave alive is a threat to the
  > ships you're protecting.
- **Partial success:**
  > You brought the boarding party home, but the Kafelnikof is still out there.
  >
  > Without the base destroyed, the Coalition will simply move its hunting packs back in, and all we
  > have to show for today is a few computer records. Next time, see the job through.

## Open points for the mod

- **Faces:** the mission's comms give the wrong faces. The mod sets the speaking ships' pilots as
  the mission starts (the wing leader's Patriot to Bandit, the Tempest to Diceman, the boarding ship
  to the Marine leader, whose face and voice mission 11's boarding ship has), and maps the pilot
  numbers its comms commands use: 103 to Stahl, 102 to Moose.
- **Voices:** the 51 lines are voiced, and so is Enriquez's briefing, as `dreamcast_brief13`.
- **Debriefings and briefing hologram:** OpenReliant can't yet give a mod's mission its own
  debriefings and briefing speech ([#976](https://github.com/OpenReliant/openreliant/issues/976)).
