# Mission 12: the Black Guard's attack on the Reliant

A reconstruction of the cut mission 12, whose file survives only on the Dreamcast disc. What comes
from the game's own files is marked as such. The rest, Enriquez's briefing and the words of the
radio lines, is written for the mod from that evidence, and is open to change.

## Where it sits

- **Dated February 2, 2161** in the ITAC's table of mission dates. The game's own launch date, text
  989, is the placeholder "aaaa", so the mod puts this date in its place.
- **After mission 11**, the raid on the Czar with Klaus Steiner's Vampires, which ends chapter 2.
- **Before mission 14**, the raid on the Stalag with the Ronin.
- **Flown as the 45th Volunteers.** The ITAC's news after mission 13 announces the new name, the 45th
  Tigers, after Steiner compares the squadron to the Flying Tigers. So missions 12 and 13 still use
  the Volunteers' faces, as mission 11 does.
- **The war around it.** Chapter 2's movie, "Counterstrike": Operation Shield has brought 45% of the
  Alliance Fleet to Triton, and the Alliance is striking Coalition supply lines with hit and run
  raids, so the Coalition's forward fleet pulls back to Titan. The news after 13 says the Coalition is
  pulling its hunting packs back to regroup around Saturn.
- **The Black Guard.** The Coalition's elite unit, led by Ivan "The Butcher" Petrov. Mission 12 brings
  in his brother Nicolai, the Black Guard's second in command, who is wanted for war crimes.

## What the files say

- **Objective** (the PC's executable, string 457): Protect the Reliant.
- **Setting:** the Reliant holds station in a nebula with the German ship Lueneberg (its own ship
  type). A nanny ship is on station for rearming. The Yamato is far away, and only comes in if the
  Reliant is lost.
- **The 45th:** the player in a Phoenix, Bandit leading in a Patriot, wingmen in a Predator and a
  Naginata.
- **The Coalition:** waves of Kossacs, a Kurgen gunboat, Sabers, two Kamov torpedo bombers with
  seven torpedoes, and the Black Guard's five Basilisks with Nicolai Petrov's own Basilisk.
- **Petrov can't be killed.** The script makes his Basilisk invulnerable as the mission starts, and
  nothing lifts it, so he always gets away. That fits the canon: Nicolai Petrov speaks again in
  mission 19. The bonus rating, which needs him dead, can't happen.
- **Rating** (the script's completion code): Petrov dead with the Reliant alive is a success with
  the bonus; otherwise one torpedo hit or none on the Reliant is a success, two a partial success,
  three a partial failure, and a fourth destroys the Reliant, a total failure.
- **Campaign flags:** if mission 3's fixed gate still stands, Sabers warp in through it for a
  surprise attack, and a second Black Guard group follows. The later waves grow with the number of
  players in a network game.
- **Debriefings:** the PC's ITAC already holds mission 12's debriefings for every rating it can
  reach (below).

## The story

The Reliant is resupplying in a nebula, with the Lueneberg alongside, when the alarm sounds: a
Coalition strike group has found her. The 45th scrambles and meets a first wave of Kossacs, while
Nicolai Petrov's Basilisk makes straight for the carrier and taunts the pilots. Once the first wave
is down, the pilots rearm at the nanny ship if it survived. Then the real attack comes: the Black
Guard jump in, and two Kamov torpedo bombers move on the Lueneberg. The Lueneberg puts herself between
the bombers and the Reliant, and takes the first torpedo meant for the carrier. The Kamovs then
launch at the Reliant, a torpedo every ten seconds, and the 45th has to shoot them down. Four hits
break the Reliant's back. If she survives, the Black Guard are beaten and Petrov escapes again.
If she's lost, the Volunteers jump to the Yamato.

## Enriquez's briefing

Written for the mod. The mission starts with a scramble, so the briefing sets up the alert duty that
the attack interrupts.

> Okay, settle down and listen up. The Czar raid has put the Reliant at the top of the Coalition's
> list, so Command wants us out of sight for a while. We're holding station inside this nebula while
> we take on supplies from the German ship Lueneberg. The Yamato is on her way to join us, but until
> she gets here, we're on our own.
>
> Intelligence have picked up Coalition hunting packs moving through this sector, and there are
> reports that the Black Guard have been seen near the front, led by Nicolai Petrov, the Butcher's
> brother.
>
> Your wing is on alert duty. If anything comes for the Reliant, you'll be the first to meet it. A
> nanny ship will be standing by to rearm you. Your orders are simple: protect the Reliant. Nothing
> gets through. Stay sharp, Volunteers.

Her last word: the game has none for mission 12 (`enrbr_tag12` doesn't exist on either platform).

## The radio

In the order the lines play. The speaker is the one the line's name gives, with the face the PC's
missions give that speaker in the Volunteers' time. "When" names the script's part or trigger.

| Line | Speaker (face) | When | Words |
|---|---|---|---|
| `ms_scram12_001` | The Reliant's address system (no face) | The launch | Scramble, scramble! All pilots to your fighters! The Reliant is under attack! |
| `ms_rel12_001` | The Reliant's bridge officer (`Rel_Brdge_Off`) | First wave | Forty-fifth, multiple Coalition fighters inbound on the Reliant. Keep them off us! |
| `ms_ban12_001` | Bandit (`45VolntrWL_Bandit`) | First wave | You heard him, Volunteers. Break and engage. Nobody touches the Reliant. |
| `ms_moo12_001` | Moose (`45Volntrs_Moose`) | First wave | Kossacs, a whole pack of them. Plenty to go around! |
| `ms_pet12_001` | Nicolai Petrov (`BlckGrdNP_Plt`) | 35 seconds in, while his escort lives | Alliance pilots. I am Nicolai Petrov of the Black Guard. Your carrier dies today. |
| `ms_moo12_002` | Moose | After Petrov | Petrov? Bandit, that's the Butcher's brother! |
| `ms_pet12_002` | Nicolai Petrov | His escort destroyed | You fly well, for colonists. Let us see how you do against my Black Guard. |
| `ms_moo12_003` | Moose | After Petrov | He's falling back to his friends. Here they come. |
| `ms_dice12_001` | Diceman (`45Volntrs_Plt`) | First wave down | First wave's down. Bandit, I'm running low. Any chance of a rearm? |
| `ms_rel12_002` | The Reliant's bridge officer | The nanny alive | Copy, Forty-fifth. The nanny's on station off our bow. Rearm while you can, there's more coming. |
| `ms_rel12_013` | The Reliant's bridge officer | The nanny lost | Sorry guys, the nanny's been taken out. You'll have to go without a rearm. *(These words are the game's: with three or four players, the script prints them as text instead.)* |
| `ms_ban12_002` | Bandit | After the Reliant | Make it quick, Volunteers. Re-arm and get back on station. |
| `ms_rel12_014` | The Reliant's bridge officer | Surprise warp attack (mission 3's gate stands) | Warp signature! Coalition fighters warping in right on top of us! |
| `ms_ban12_102` | Bandit | Surprise warp attack | Sabers. They came through that gate. Break and engage! |
| `ms_rel12_003` | The Reliant's bridge officer | The Black Guard jump in | New contacts jumping in. Basilisks, with Black Guard markings. |
| `ms_ban12_003` | Bandit | The Black Guard | This is the real fight, Volunteers. Stay sharp and stay together. |
| `ms_moo12_004` | Moose | The Black Guard | I've been waiting for a crack at these guys. |
| `ms_rel12_200` | The Reliant's bridge officer | The Black Guard, if the gate stands | More Coalition ships coming through that gate. Second group right behind them! |
| `ms_rel12_004` | The Reliant's bridge officer | The Kamovs move on the Lueneberg | Kamov bombers closing on the Lueneberg! Intercept, Forty-fifth! |
| `ms_ban12_004` | Bandit | The Kamovs | Two Kamovs. Get on them before they launch! |
| `ms_rel12_005` | The Reliant's bridge officer | The first torpedo | Torpedo away! It's heading for the Lueneberg! |
| `ms_moo12_005` | Moose | The first torpedo | I see it. Going after the fish! |
| `ms_dice12_003` | Diceman | The first torpedo | Kill the torpedo first, the bombers can wait! |
| `ms_ban12_005` | Bandit | The first torpedo | Negative, they're carrying more. Take out those bombers! |
| `ms_rel12_006` | The Reliant's bridge officer | The Lueneberg moves | Lueneberg, this is the Reliant. Move clear, we'll cover you. |
| `ms_lun12_001` | The Lueneberg (`Mammoth_Plt_01`, "LUENEBERG PILOT") | The Lueneberg moves | Negative, Reliant. We're putting ourselves between you and those bombers. Lueneberg out. |
| `ms_dice12_002` | Diceman | The Kamovs launch at the Reliant | They're launching at the Reliant! Torpedoes inbound, shoot them down! |
| `ms_rel12_007` | The Reliant's bridge officer | First torpedo hit | We've been hit! Damage on decks four through seven! |
| `ms_rel12_008` | The Reliant's bridge officer | Second hit | Second hit! Hull breaches amidships. We can't take much more of this! |
| `ms_moo12_006` | Moose | Second hit | Come on, people, keep those torpedoes off her! |
| `ms_rel12_009` | The Reliant's bridge officer | Third hit | We've lost main power! One more hit and she'll break her back! |
| `ms_moo12_007` | Moose | Third hit | Not on my watch. Nothing else gets through! |
| `ms_ban12_006` | Bandit | The Lueneberg destroyed | We've lost the Lueneberg. Damn it, they took that hit for us. |
| `ms_rel12_012` | The Reliant's bridge officer | The Kamovs destroyed | Kamovs destroyed. Good work, Forty-fifth. Now clear out that Black Guard. |
| `ms_nan12_001` | The nanny's pilot (`Nanny_Ldr`) | The nanny under fire | Nanny one taking fire! I need cover over here! |
| `ms_ban12_100` | Bandit | The nanny under fire | Get those fighters off the nanny! |
| `ms_nan12_002` | The nanny's pilot, dying | The nanny destroyed | I'm hit, I'm going down! |
| `ms_ban12_101` | Bandit | The nanny destroyed | We've lost the nanny. No more rearms, make every missile count. |
| `ms_pet12_004` | Nicolai Petrov, dying | Petrov destroyed (can't happen) | No! No... Ivan... avenge me! |
| `ms_moo12_009` | Moose | Petrov destroyed (can't happen) | Nicolai Petrov is down! That one was for the Alliance! |
| `ms_ban12_009` | Bandit | Victory | That's the last of them. Reliant, the area is clear. |
| `ms_moo12_010` | Moose | Victory | Tell the Black Guard they can come back anytime! |
| `ms_rel12_010` | The Reliant's bridge officer, dying | The Reliant destroyed | Abandon ship! All hands, abandon ship! She's breaking up! |
| `ms_ban12_007` | Bandit | The Reliant destroyed | The Reliant... she's gone. |
| `ms_dice12_004` | Diceman | The Reliant destroyed | More Black Guard jumping in! Bandit, what do we do? |
| `ms_ban12_008` | Bandit | The Reliant destroyed, Petrov alive | We can't win this one. Form up on me. |
| `ms_pet12_003` | Nicolai Petrov | The Reliant destroyed | Run home, little Volunteers. Tell your Alliance what the Black Guard has done. |
| `ms_moo12_008` | Moose | The Reliant destroyed | This isn't over, Petrov. You hear me? This isn't over! |
| `ms_moo12_099` | Moose | 30 seconds later | Bandit, there's nothing left to defend. We have to get out of here. |
| `ms_ban12_099` | Bandit | 30 seconds later | Agreed. All Volunteers, plot a jump to the Yamato's position. |
| `mooms1017` | Moose | Jump drive on-line | Jump drive's on-line. Let's go. *(The same line plays in missions 13, 17 and 22.)* |
| `ms_yam12_001` | The Yamato's bridge officer (`Yam_Brdge_Off`) | The jump to the Yamato | Forty-fifth, this is the Yamato. We have you. Come aboard, we'll take care of you. |

## The debriefings

The PC's ITAC holds these already (strings 299 to 315). The failure row is the placeholder that many
missions share, but mission 12 can't be rated a failure: a lost Reliant is a total failure, and that
ends the pilot's career instead.

- **Success with the bonus** (can't happen while Petrov can't be killed): "Today has been a good
  day. You have turned a surprise attack by the Coalition into a victory for the Alliance and her
  people." Petrov's death, his crimes, and Ivan's revenge to come.
- **Success:** the attack repelled with little damage to the Reliant, the Black Guard beaten, and
  "Unfortunately Nicholai Petrov managed to get away again."
- **Partial success:** the Reliant took moderate damage, and Petrov got away.
- **Partial failure:** "one more torpedo hit would have probably broken the spine of the ship", a
  warning to keep the torpedoes off, and Petrov got away.

## Open points for the mod

- **Faces:** the Dreamcast file gives most speakers the wrong face (an older pilot table). The mod
  sets the speaking ships' pilots as the mission starts, and maps the pilot numbers its comms
  commands use: 4 to Bandit, 102 to Moose, 8 to Diceman, 116 to the Reliant's bridge officer, 63 to
  Nicolai Petrov, 115 to the nanny's pilot.
- **Voices:** the 52 lines are voiced, and so is Enriquez's briefing, as `dreamcast_brief12`.
- **Briefing hologram:** OpenReliant can't yet give a mod's mission its own briefing speech
  ([#976](https://github.com/OpenReliant/openreliant/issues/976)).
