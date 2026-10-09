# Mission 22: the convoy bound for Neptune

A reconstruction of the cut mission 22, whose file survives only on the Dreamcast disc. Unlike the
other three, its file has its radio in words: the developers' draft lines, printed as debug text,
each led by its speaker's name. The script below keeps those words, cleaned up for voicing, beside
the draft. The briefing, the objectives and the debriefings are written for the mod.

## Where it sits

- **Dated October 17, 2161** in the ITAC's table of mission dates. The game's own launch date, text
  999, is the placeholder "aaaa", so the mod puts this date in its place.
- **After mission 21**, where the Tigers destroy an ion cannon near Titan, and **before mission 23**,
  the rescue of Klaus Steiner from a Coalition prison ship.
- **Flown as the 45th Tigers from the Yamato,** with the Ronin, after the Reliant's loss in mission
  18. Bandit isn't in it: Diceman leads.
- **The game's own news of it.** The ITAC's news listed after mission 22 (October 17, 2161): Alliance
  forces supporting the liberation of Titan were caught off guard when a Coalition force bypassed
  Saturn and tried a surprise attack on Alliance HQ around Neptune. The Tigers and Ronin, flying off
  the Yamato, cut the force off from Alliance Command and led the assault, destroying several enemy
  vessels and support craft, and the Coalition retreated to its own lines.
- **A campaign flag:** if the Krasnaya got away in mission 8, she sails with this convoy, and the
  Ronin go after her. If she didn't, two cruisers take her place.

## What the files say

- **Objectives:** the PC's executable has none for mission 22 (its row of the table is empty). The
  mod gives it these:
  1. Find the Coalition convoy
  2. Destroy the scouts before they warn the convoy
  3. Disable the Badinov: destroy its shield generator, then its engines
  4. Destroy the troop carriers
  5. Take down the Krasnaya's shields for the bombers
  6. Protect Gamma's bombers
  7. Land on the Yamato
- **The Alliance:** the Tigers, Diceman leading; the Ronin; Gamma wing's Hades torpedo bombers,
  waiting in an asteroid field; the Maulers and the Marauders, sent in if the Tigers are slow; the
  Yamato, with Enriquez on her bridge, and her Rippers for salvage.
- **The Coalition:** Lagg scouts; the convoy: the Badinov, a big gunship with a heavy gun, three
  troop carriers, the Krasnaya or two cruisers, Luda escorts, Kurgens and Sabers.
- **Rating** (the script's completion code): by how quickly the Tigers work. The mission runs three
  timers, and if none of them ran out it's a success with the bonus; as they run out, it falls to a
  success, a partial success and a failure.
- **How it goes:** Enriquez splits the search; the Tigers find Lagg scouts, which try to jump out
  and warn the convoy. At the convoy, the Tigers have to bring down the Badinov's shields and engines
  before it can jump, so that Gamma's bombers can finish it. If the Tigers take too long, the bombers
  come in against a fully armed Badinov, or it escapes. Then the troop carriers, and the Ronin's call
  for help against the Krasnaya's shields. When most of the convoy's defenses are gone, the Yamato
  jumps in.

## The story

Allied Intelligence has picked up a Coalition convoy slipping past Saturn, and it's heading for
Alliance HQ at Neptune with troops aboard. Enriquez splits the search: the Tigers take sector three,
the Ronin sector six, and Gamma's bombers wait in an asteroid field between them. The Tigers find
the convoy's scouts first, and have to stop them before they can warn the convoy. Then they run into
the convoy itself, escorted by the Badinov, whose heavy gun would tear the bombers apart. The Tigers
have to cripple her, shields first, then engines, before she can jump, and clear a path so the
bombers can finish her. With the Badinov gone, the troop carriers and the Krasnaya are next, and the
Yamato comes in to clean up.

## Enriquez's briefing

Written for the mod, from her own lines at the start of the mission.

> Heads up, pilots! Allied Intelligence have picked up a Coalition force that slipped past Saturn.
> We believe it's a convoy carrying troops, and it's heading for Alliance Headquarters around
> Neptune. If it gets there, we'll be fighting this war on our own doorstep.
>
> We have two possible locations for it. The Tigers will take sector three, and the Ronin sector
> six. Gamma Wing's bombers will wait, concealed in an asteroid field between the two, ready to jump
> in as soon as we know where the convoy is.
>
> The convoy's escort includes the Badinov. Her main gun can shred our bombers before they get close,
> so she's your primary target. Knock out her shield generators, then her engines, so she can't run,
> and let Gamma do the rest. After that, the troop carriers. Not one of them reaches Neptune. Good
> luck out there, Tigers.

## The radio

The words to voice, in the order the lines play, and the file's draft text beside them. The mission's
file names no speech files, so the lines take names in the game's style. The speakers' faces are
those the PC's missions give them in the Yamato's time.

| Line | Speaker (face) | When | Words | The file's draft |
|---|---|---|---|---|
| `ms_enq22_001` | Enriquez (`Enq_YamBridge`) | The start | Allied Intelligence has identified two possible locations for a main Coalition convoy. | Enriques_Allied inteligence has identified 2 possible locations for a main coalition Convoy |
| `ms_enq22_002` | Enriquez (`Enq_YamBridge`) | The start | Tigers, you take sector three. Gamma are concealed in a small asteroid field, at a midpoint between our suspected areas. | -Enriques_Tigers, You take sector 3, Gamma are concealed in an small asteroid field at a mid point  between our suspected areas |
| `ms_enq22_003` | Enriquez (`Enq_YamBridge`) | The start | Ronin, jump out to sector six. Keep an eye open for any signal traces, and keep us informed. Good luck. | -Enriques_Ronins ,jump out to Sector 6, keep an eye open for any signal traces, keep us informed, Good luck |
| `ms_ron22_001` | The Ronin's leader (`RoninWL_Plt`) | The start | Tigers, if you see them first, bag one for us. | Ronin WL_ Tigers, if u see them first , bag one for us |
| `ms_ron22_002` | The Ronin's leader (`RoninWL_Plt`) | The start | Ronin, ready to jump. | -Roni WL_Ready to jump |
| `ms_ron22_003` | The Ronin's leader (`RoninWL_Plt`) | The Ronin jump out | Good luck, Tigers. Catch you later. | Good Luck,,, Tigers,,, catch you later |
| `ms_moo22_001` | Moose (`45Tigers_Moose`) | The start | Prepare for jump, Tigers. | Moose_ Prepare for jump Tigers, |
| `ms_dice22_001` | Diceman (`45TigersWL_Diceman`) | The start | Let's do it. | Diceman_Lets do it |
| `ms_dice22_002` | Diceman (`45TigersWL_Diceman`) | Arriving at nav 1 | Good to see you ready and waiting, Gamma. | Diceman_Good to see u ready and waiting Gamma |
| `ms_gam22_001` | Gamma's leader (`Gamma_Ldr`) | Arriving at nav 1 | Standing by and armed. You've just got to find out where. Best of luck. | Gamma WL_Standing by and armed, you've just gotta find out where, best of luck |
| `ms_moo22_002` | Moose (`45Tigers_Moose`) | Arriving at nav 1 | Hey, I'm picking up traces on the scanners. | -Moose-Hey Im picking up traces on the scanners |
| `ms_enq22_004` | Enriquez (`Enq_YamBridge`) | Arriving at nav 1 | Vector confirmed. We're uploading their projected positions. Uploading the coordinates now. | -Enriques- Vector confirmed, we're uploading theirprojected positions, Uploading the coordinates |
| `ms_dice22_003` | Diceman (`45TigersWL_Diceman`) | Nav 1, fighters | A welcome party. How nice. | Diceman_  A welcome parrty ,,,, how nice |
| `ms_dice22_004` | Diceman (`45TigersWL_Diceman`) | Nav 1, fighters | Keep them away from Gamma. If any of that scum so much as goes near them, blast them out of the sky. | Diceman_ Keep them away from Gamma, if any of thoes scum so much as go near them , blast them out of the sky |
| `ms_fren22_001` | Frenchy (`45Tigers_Plt`) | Nav 1, fighters | Steady, Tigers. Fire when you can see their yellow bellies. | Frenchy_ Steady Tigers,,,,,,, fire when you can see theyre yellow bellies |
| `ms_moo22_003` | Moose (`45Tigers_Moose`) | Nav 1, fighters | Tigers, keep an eye on your radar. Some of them could be cloaked. Could be tricky. | -Moose- Tigers, keep an eye on your radar,,,,, some could be cloaked, could be tricky |
| `ms_dice22_005` | Diceman (`45TigersWL_Diceman`) | Nav 1, fighters | Be alert, Tigers. We can't lose any of you now. Stopping that convoy is A1 priority. | Diceman_ Be alert Tigers, we cant loose any of u now,,, stopping that Convoy is A1 priority |
| `ms_moo22_004` | Moose (`45Tigers_Moose`) | Nav 1, fighters | You know what to do. | -Moose- You know what to do |
| `ms_dice22_006` | Diceman (`45TigersWL_Diceman`) | The Laggs jump in | Looks like we have company. | Diceman _looks like we have company |
| `ms_dice22_007` | Diceman (`45TigersWL_Diceman`) | The Laggs jump out | Damn it, they're jumping out. No point hanging around. Prepare to jump. | -Diceman_SSSSssttttttt, they're jumping out, no point hanging arround, prepare to jump |
| `ms_moo22_005` | Moose (`45Tigers_Moose`) | The Laggs run | Looks like they're running. Tigers, lock on. | Moose_ Looks like they're running,,, Tigers ,,,, lock on |
| `ms_dice22_008` | Diceman (`45TigersWL_Diceman`) | The Laggs run | No mercy, Tigers. Wipe them out before they jump. We've already picked up their transmissions to the convoy. | Diceman_no mercy, Tigers, wipe them out before they jump, we've already picked up their transmissions to the Convoy, |
| `ms_dice22_009` | Diceman (`45TigersWL_Diceman`) | The Laggs run | We'll call you in, Hades, when we've got them squealing. | Diceman_ We'll call u in Hades when  we've got them squealing |
| `ms_enq22_005` | Enriquez (`Enq_YamBridge`) | The Laggs run | Passing on the coordinates to the Ronin. | Enriques_ Passing on coordinates to Ronin, |
| `ms_enq22_006` | Enriquez (`Enq_YamBridge`) | The Laggs run | See them off, Tigers. | Enriques_ See them off Tigers |
| `ms_moo22_006` | Moose (`45Tigers_Moose`) | Arriving at the convoy | She's in our sights, Tigers. | Moose_She's in our sights Tigers.......... |
| `ms_dice22_010` | Diceman (`45TigersWL_Diceman`) | Arriving at the convoy | Set for primary target, people. | Diceman_Set for Primary target men |
| `ms_may22_001` | Mayday (`45Tigers_Plt`) | Arriving at the convoy | Let's go raise some hell. | Mayday_ Lets go raise some hell |
| `ms_dice22_011` | Diceman (`45TigersWL_Diceman`) | Arriving at the convoy | Don't lose sight of the big picture. Immobilize the Badinov, and let Hades do the rest. You do your job, let Hades do theirs. | Diceman_dont loose sight of the big picture, IMMOBILISE, the Badenov, let Hades do the rest, U do your job , let Hades do theirs |
| `ms_stal22_001` | Stalker (`45Tigers_Plt`) | Arriving at the convoy | Alpha Two, take out the shield generator. That'll let us get to the engines, and then that big bazooka's going nowhere. Then we disarm her. | Stalker_Alpha2, take out the Shield generator, that'll let us get to the Engines, then, tthat big bazuka's going nowhere, then disarm her |
| `ms_dice22_012` | Diceman (`45TigersWL_Diceman`) | The Ronin arrive | Nice timing, Ronin. | Diceman_Nice timing Ronin |
| `ms_ron22_004` | The Ronin's leader (`RoninWL_Plt`) | The Ronin arrive (the Krasnaya escaped in mission 8) | Heard you needed some help, Tigers. You look after the Badinov, we'll see to the Krasnaya. | -Ronin-Heard U needed some help Tigers,,,,,, you look after Badinov,,,,,, we ll see to the Krasnaya |
| `ms_ron22_005` | The Ronin's leader (`RoninWL_Plt`) | The Ronin arrive (cruisers instead) | Heard you needed some help, Tigers. You look after the Badinov, we'll see to the cruisers. | -Ronin-Heard U needed some help Tigers,,,,,, you look after Badinov,,,,,, we ll see to the Cruisers |
| `ms_dice22_013` | Diceman (`45TigersWL_Diceman`) | The convoy splits | Convoy's splitting up, Tigers. | Diceman_ Convoy's   splitting up, Tigers |
| `ms_stal22_002` | Stalker (`45Tigers_Plt`) | The convoy splits | Yeah, we've got them running scared! | Stalker_YEAH, we got them running scared |
| `ms_dice22_014` | Diceman (`45TigersWL_Diceman`) | The Sabers attack | Looks like I spoke too soon. | Diceman,, looks like I spoke too soon |
| `ms_dice22_015` | Diceman (`45TigersWL_Diceman`) | The Sabers attack | Ronin, you take on the convoy. Tigers, show these Sabers a bad time. | Diceman_Ronin, U take on the convoy, Tigers, show these Sabres a bad time |
| `ms_dice22_016` | Diceman (`45TigersWL_Diceman`) | The Sabers attack | Clear these guys out of the way. Hades won't be coming in with these buzzing about. Get rid of them. | Diceman_Clear theses guys out'a the way, Hades wont be coming in with these buzzing about, get rid of them |
| `ms_stal22_003` | Stalker (`45Tigers_Plt`) | The Sabers attack | Come on, soldiers, get rid of these guys. | Stalker_Come on Soldiers get rid of these guys |
| `ms_dice22_017` | Diceman (`45TigersWL_Diceman`) | The Sabers destroyed | That's whipped them good. Tigers, prepare to jump. | Diceman_Thats whipped them good, Tigers, prepare to jump |
| `ms_stal22_004` | Stalker (`45Tigers_Plt`) | The Sabers destroyed | Yeah, let's knock them to hell! | Stalker_ TEAH, lets knock em to hell |
| `ms_dice22_018` | Diceman (`45TigersWL_Diceman`) | Shooting the Badinov with its shields up | No point shooting those till the shields are down. Go for the shields. | Diceman_no point shootin thoes till the  shields are down, go for the shields |
| `ms_dice22_019` | Diceman (`45TigersWL_Diceman`) | Near the Badinov | Alpha One, take out the shield generators. | Diceman_Alpha1 take out the shield generators |
| `ms_dice22_020` | Diceman (`45TigersWL_Diceman`) | The Badinov's shields down | The shields are down! Hades, are you in position? | Diceman_THE SHIELDS ARE DOWN,,,Hades are u in position? |
| `ms_moo22_007` | Moose (`45Tigers_Moose`) | The Badinov's shields down | Come on, Tigers, she's charging up her jump drive. It's now or never! | Moose_Come on tigers.... shes's charging up her jump drive,,,,, its now or never |
| `ms_stal22_005` | Stalker (`45Tigers_Plt`) | The Badinov's big engine destroyed | Well done, that's the big one. | Stalker_Well, done thats the big one |
| `ms_dice22_021` | Diceman (`45TigersWL_Diceman`) | The Badinov's small engines destroyed | She's limping now. That's the small one. | Diceman_ Shes limping now, thats the small one |
| `ms_dice22_022` | Diceman (`45TigersWL_Diceman`) | The Badinov's small engines destroyed | There goes the small engine. | Diceman_ There goes the small engine |
| `ms_stal22_006` | Stalker (`45Tigers_Plt`) | The wing hasn't touched the shields | What do you think you're doing, pilot? | Stalker_Whadda ya think your're doing, pilot ? |
| `ms_dice22_023` | Diceman (`45TigersWL_Diceman`) | The wing hasn't touched the shields | They've lost their nerve, they can't destroy it. We'll have to go in. | Diceman_Theyve lost their balls, they cant desroy it, we'll have to go in |
| `ms_dice22_024` | Diceman (`45TigersWL_Diceman`) | The wing hasn't touched the shields | Tigers, let's get that generator. | Diceman_Tigers, lets get that generator |
| `ms_stal22_007` | Stalker (`45Tigers_Plt`) | The Badinov's Kurgens | Come on, we've got to get rid of those Kurgens. They want to hurt Gamma bad. | Stalker_Come on, we gotta get rid of thoes Kurgens, they wanna hurt Gamma bad, |
| `ms_dice22_025` | Diceman (`45TigersWL_Diceman`) | The Badinov's Kurgens | Take them out, soldiers. | Diceman_Take em out soldiers, |
| `ms_stal22_008` | Stalker (`45Tigers_Plt`) | The Badinov's turrets | Soldiers, Hades would appreciate losing a couple of those turrets. | Stalker_Soldiers, Hades would appreciate loosing a couple of thoes turrets |
| `ms_dice22_026` | Diceman (`45TigersWL_Diceman`) | The Badinov's turrets | We're on it. | Diceman_We're on it |
| `ms_dice22_027` | Diceman (`45TigersWL_Diceman`) | The Badinov's engines destroyed | Wow, that big boy's going nowhere now. Tigers, it's a turkey shoot! | Diceman_Wow , that big boys going nowhere now, Tigers, turkey shoot, |
| `ms_dice22_028` | Diceman (`45TigersWL_Diceman`) | The Badinov's engines destroyed | Keep your head, Gamma One. We have to give you a clear run. | Diceman _Keep you head Gamma1, have to give u a clear run |
| `ms_dice22_029` | Diceman (`45TigersWL_Diceman`) | The Badinov's engines destroyed | Come on, pilots, Hades need a clear path. | Diceman _Come on pilots, Hades need a clear path |
| `ms_dice22_030` | Diceman (`45TigersWL_Diceman`) | The Badinov's engines destroyed | Clear for Gamma to hit, do you read? | Diceman_Clear for Gamma to hit, do u read? |
| `ms_had22_001` | Hades' leader (`Gamma_Ldr`) | Hades come in early, the Badinov armed | This is not going to look good at the debrief. The Badinov is fully armed, and we have to come in now. We can't risk waiting any longer. | Hades WL_This is not gonna look good at Debrief, the Badinov is fully armed, and we have to come in now, we cant risk waiting any longer |
| `ms_had22_002` | Hades' leader (`Gamma_Ldr`) | Hades come in early | Get your slack asses out of there. We'll have to chance an attack on her fully armed. | Hades WL_Git your slack asses outta threre, we'll have to chance an attack on her fully armed |
| `ms_had22_003` | Hades' leader (`Gamma_Ldr`) | Hades come in early | This is really not good, pilots. Hades, cover up, we're going in. Get out of the area, pilots, if you don't want to go up with the Badinov. | Hades WL_This is really not good pilots, Hades, cover up, we're going in. Get out the area pilots if u dont wanna go up with the Badinov |
| `ms_had22_004` | Hades' leader (`Gamma_Ldr`) | Hades come in | Suggest you clear the area. You want to see these fireworks from a distance. | Hades WL_Suggest U clear the area, u want to see theses fireworks from a distance |
| `ms_had22_005` | Hades' leader (`Gamma_Ldr`) | The Badinov jumped out | Nothing to do here. The bird has flown. Repeat, the bird has flown. | HadesWL_Nothing to do here, the bird has flown, Repeat , the bird has flown |
| `ms_had22_006` | Hades' leader (`Gamma_Ldr`) | The Badinov jumped out | We have lost the Badinov. Aborting launch. Wouldn't want to be any of you Tigers at the debrief. | HadesWL_We have lost the Badinov, aborting launch, wouldnt want to be any of u Tigers at debrief |
| `ms_had22_007` | Hades' leader (`Gamma_Ldr`) | Hades' first wave | Clear on out, boys. Gamma Two, stand by for the second wave. | HadesWL_Clear on out boys, Gamma 2, stand by for second wave |
| `ms_dice22_031` | Diceman (`45TigersWL_Diceman`) | Hades come in | You heard them, soldiers. Clear the area! Clear the area! Let's get out of here! | Diceman _You heard them Soldiers, Clear the area, , CLEAR THE AREA, lets get outa here |
| `ms_dice22_032` | Diceman (`45TigersWL_Diceman`) | Hades come in | OK, Gamma, put the baby to bed. Let them loose. | Diceman _Ok Gamma put the baby to bed, let them loose |
| `ms_dice22_033` | Diceman (`45TigersWL_Diceman`) | Hades come in | Read them and weep. | Diceman _Read em and weep |
| `ms_had22_008` | Hades' leader (`Gamma_Ldr`) | Hades' torpedoes away | Package delivered. Looking good. | HadesWL_Package delivered looking good |
| `ms_had22_009` | Hades' leader (`Gamma_Ldr`) | Hades' torpedoes away | OK, Gamma, let's clear the area. | HadesWL_OK Gamma lets clear the area |
| `ms_dice22_034` | Diceman (`45TigersWL_Diceman`) | The Badinov destroyed | They're feeling it now. Keep on them, they love it! | Diceman_They're feeling it now, keep on em, they love it! |
| `ms_moo22_008` | Moose (`45Tigers_Moose`) | The Badinov destroyed | What's left of that little group can still be pretty handy. Take out or disable what you can. | Moose_ Whats left of that little group, can still be pretty handy, take out or disable what you can |
| `ms_enq22_007` | Enriquez (`Enq_YamBridge`) | The Badinov destroyed | Don't get carried away, Tigers. What's left is mostly trash. Get rid of any troop carriers left, then see to the Krasnaya. | Enriques_Dont get carried away Tigers, whats left is mostly trash, get rid  of any troopcarriers left, then see to Krasnaya |
| `ms_dice22_035` | Diceman (`45TigersWL_Diceman`) | The Badinov destroyed | No worries about those, they're floating graveyards now. | Diceman_no worries about thoes, they're floating graveyards now |
| `ms_enq22_008` | Enriquez (`Enq_YamBridge`) | The Badinov destroyed | Good. Take out what you can, but be on hand for the Ronin. | Enriques_Good, take out what u can, but be on hand for ronin |
| `ms_dice22_036` | Diceman (`45TigersWL_Diceman`) | The Badinov destroyed | You heard her, Tigers. Move on in. Gold star from Enriquez for getting these. | Diceman_You heard Tigers, move on in, gold star from Enriquez for getting these |
| `ms_stal22_009` | Stalker (`45Tigers_Plt`) | The Badinov destroyed | We have to be quick. The Ronin may need us to help them finish off over there. | Stalker_We have to be quick, Ronin may need us to help them finish off over there |
| `ms_stal22_010` | Stalker (`45Tigers_Plt`) | The Badinov escapes | We're going to lose the Badinov! | Stalker_ We're going to loose the Badinov |
| `ms_dice22_037` | Diceman (`45TigersWL_Diceman`) | The Badinov escapes | She's leaving the convoy behind. Take out the troop carriers. | Diceman_She's leaving the convoy behind, take out the Troop carriers |
| `ms_enq22_009` | Enriquez (`Enq_YamBridge`) | The Badinov escapes | Don't get carried away. If the Ronin call, you run. The Krasnaya is our secondary priority. | Enriquez_dont get carried away, if Ronin calls, you run, Krasnaya is our secondary priority |
| `ms_dice22_038` | Diceman (`45TigersWL_Diceman`) | The Badinov escapes | The Coalition are showing their true colors, leaving their men behind. That's no way to treat soldiers. | Diceman_The Coalition are showing their true colours, leaving their men behind, thats now way to treat soldiers |
| `ms_stal22_011` | Stalker (`45Tigers_Plt`) | The Badinov escapes | Leaves them for us, that is. In your own time, Tigers. | Stalker_Leave them for us that is, in your own time Tigers, |
| `ms_dice22_039` | Diceman (`45TigersWL_Diceman`) | A troop carrier about to blow | Back off, Tiger, she's going to blow! | Diceman_Back off Tiger, she's gonna blow |
| `ms_stal22_012` | Stalker (`45Tigers_Plt`) | A troop carrier about to blow | Tigers, move it! | Stalker_Tigers,,,, moove it |
| `ms_stal22_013` | Stalker (`45Tigers_Plt`) | A troop carrier about to blow | Tigers, move it! She's toast! | Stalker_Tigers,,,, moove it, She's Toast |
| `ms_stal22_014` | Stalker (`45Tigers_Plt`) | A troop carrier about to blow | Get away from there, Tigers, she's a-blowin'! | Stalker_Get away from there Tigers, she's a Blowin' |
| `ms_enq22_010` | Enriquez (`Enq_YamBridge`) | The troop carriers destroyed | All the troops destroyed. Nice shooting, lads. | Enriquez_All the Troops destroyed, nice shooting lads |
| `ms_stri22_001` | Striker (`45Tigers_Plt`) | The Ronin call for help | Troop carriers are about to jump, Tigers! | Striker_Troopcarriers are about to jump Tigers |
| `ms_dice22_040` | Diceman (`45TigersWL_Diceman`) | The Ronin call for help | They're about to jump, Tigers. We'll have another chance. | Diceman_Theyre about to jump Tigers, we'll have another chance |
| `ms_enq22_011` | Enriquez (`Enq_YamBridge`) | The Ronin call for help | Looks like those troops are going to live to fight another day. | Enriquez_Looks like thoes troops are going to live to fight another day, |
| `ms_ron22_006` | The Ronin's leader (`RoninWL_Plt`) | The Ronin call for help | Hate to crash the party, boys, but we really could use some of your firepower here. | RoninWL_Hate to crash the party boys, but we really could use some of your firepower here |
| `ms_ron22_007` | The Ronin's leader (`RoninWL_Plt`) | The Ronin call for help | Hades are waiting. We're going to need some help taking out the shield generators. | RoninWL_Hades are waiting, were gonna need some help taking out the Shield Generators |
| `ms_dice22_041` | Diceman (`45TigersWL_Diceman`) | The Ronin call for help, the Badinov escaped | (Close to tears) We let her get out. Our asses are on the line now. | Diceman_(In Tears) We let her get out, our asses are on the line now,,, |
| `ms_ron22_008` | The Ronin's leader (`RoninWL_Plt`) | The Ronin call for help, again | Urgent request, Tigers. Lick your wounds later. We are dead meat if you don't get your asses over here now! | Ronin WL_urgent request, Tigers, Lick your wounds later,,, WE are dead meat is u dont get your asses over here NOW |
| `ms_ron22_009` | The Ronin's leader (`RoninWL_Plt`) | The Ronin call for help, again | We need you here now, Tigers. Hades need the shield generators taken out. | Ronin WL_We need you here now Tigers, Hades need the Shield generators taken out |
| `ms_mau22_001` | The Maulers' leader (`Mauler_Plt`) | The Maulers and Marauders arrive | We've been told to come on in and give you guys a hand. Heard you're taking it a bit easy. | MaulersWL_We've been told to come on in to give u guys a hand, heard u r  taking it a bit easy |
| `ms_mar22_001` | The Marauders' leader (`MarauderWL_Plt`) | The Maulers and Marauders arrive | Marauders coming in as well. You guys must be really slow. | Marauders WL_Marauders coming in aswell, you must really be slow U guys |
| `ms_ron22_010` | The Ronin's leader (`RoninWL_Plt`) | The Maulers and Marauders arrive | After the Badinov farce, I'd have thought you'd try to do your job properly. | Ronin Wl_After the Badinov farse, I'd've thought u'd try to do your job properly |
| `ms_ron22_011` | The Ronin's leader (`RoninWL_Plt`) | The Maulers and Marauders arrive | You may have come up trumps with the Badinov, but there's no room to rest on your laurels. | Ronin Wl_You may have hit trumps with the Badinov, but there's no room to rest an your laurels |
| `ms_ron22_012` | The Ronin's leader (`RoninWL_Plt`) | The Maulers and Marauders arrive | This is going to look really bad at the debrief. This is going to be hard with those shields up. | Ronin Wl_This is going to look really bad at the debrief, this is gonna be hard with thoes shields up |
| `ms_dice22_042` | Diceman (`45TigersWL_Diceman`) | The Krasnaya's shields down | OK, pilots, we've got to get those Kurgens out of the picture. Gamma want a clear path in. | Diceman_Ok pilots, we've got to get thoes Kurgens out of the picture, Gamma want a clear path in |
| `ms_stal22_015` | Stalker (`45Tigers_Plt`) | The Krasnaya's shields down, the Badinov escaped | No screwing up this time. The Badinov was a mistake you will not be repeating. | Stalker_No screwing up, this time, the Badinov was a mistake you WILL NOT BE repeating |
| `ms_stal22_016` | Stalker (`45Tigers_Plt`) | The Krasnaya's shields down | You've done us proud so far. Don't let up on them, though. Clear those Kurgens, wipe them out. | Stalker_Youve done us proud,so far, dont let up on 'em though, clear thoes Kurgens, wipe them out, |
| `ms_had22_010` | Hades' leader (`Gamma_Ldr`) | The Krasnaya's shields down | OK, we can take it from here, Tigers. Make some room. | Hades2WL_Ok_we can take it from here Tigers, make some room |
| `ms_dice22_043` | Diceman (`45TigersWL_Diceman`) | A cruiser's shields down | That should loosen up their resolve. Let's clear the way for the Hades boys. | Diceman_that should loose up their resolve, lets clear the way for Hades boys |
| `ms_stal22_017` | Stalker (`45Tigers_Plt`) | A cruiser's shields down | Come on, pilots, we nearly have it in the bag. No slacking off now. | Stalker_come on pilots, we nearly have it in the bag, so slacking off now |
| `ms_stal22_018` | Stalker (`45Tigers_Plt`) | A cruiser's shields down | Fast as possible. I want to get back and get some hard relaxing done. | Stalker_Fast as possible, I wanna get back and get some hard relaxing done |
| `ms_dice22_044` | Diceman (`45TigersWL_Diceman`) | The first cruiser's shields down | Nice work. Let's take out the other shields, then we can get Hades in. | Diceman_Nice work, lets take out the other shields, then we can get Hades in |
| `ms_dice22_045` | Diceman (`45TigersWL_Diceman`) | The second cruiser's shields down | Nice work. Let's take out the other shields. They'll be sitting ducks for Hades then. | Diceman_Nice work, lets take out the other shields, they'll be buns up for Hades then |
| `ms_dice22_046` | Diceman (`45TigersWL_Diceman`) | Shooting a cruiser with its shields up | This turkey's here for the duration. Go and get the Badinov, that is your primary target. | Diceman_This turkeys here for the duration,  go and get the Badinov, that is your primary target |
| `ms_had22_011` | Hades' leader (`Gamma_Ldr`) | Hades' second wave, the Tigers slow | You'd better get out of there. We have to come in now. You guys really know how to screw up a mission. | HadesWL_You'd better get out of there, we HAVE to come in now, you really know how to screw up a mission u guys |
| `ms_had22_012` | Hades' leader (`Gamma_Ldr`) | Hades' second wave | Come on, guys, make some space. We have to risk it. We need to come in now! | HadesWL_Come on guys make some space, we have to risk it, we need to come in NOW |
| `ms_stal22_019` | Stalker (`45Tigers_Plt`) | Hades' second wave | Hades, I hope you're ready to get to work, because we could do with your muscle right now. | Stalker_Hades, I hope yoour ready to get to work, cos we could do with your muscle right now |
| `ms_had22_013` | Hades' leader (`Gamma_Ldr`) | Hades' second wave | Make some room, pilots. Hades coming in. | HadesWL_Make some room pilots.. Hades coming in |
| `ms_gam22_002` | Gamma's leader (`Gamma_Ldr`) | Gamma waits to launch | Gamma Two, waiting on your every move. We're ready to launch. Got any gaps for us? | Gamma_ Gamma 2, waiting on your every move, we're ready to launch, got any gaps for us? |
| `ms_stal22_020` | Stalker (`45Tigers_Plt`) | Gamma waits to launch | Sorry to keep you hanging on there. Bring them in and let them loose. | Stalker_Sorry to keep u hanging on there, bring em in and let em loose |
| `ms_gam22_003` | Gamma's leader (`Gamma_Ldr`) | Gamma waits to launch | We read. Gamma, drop your load. | Gamma WL_We read, Gamma, drop yer load |
| `ms_dice22_047` | Diceman (`45TigersWL_Diceman`) | The escort's Kurgens destroyed | Get rid of those shields, pilot. Hades are waiting! | Diceman_Get RiD of those shields pilot, Hades are waiting! |
| `ms_gam22_004` | Gamma's leader (`Gamma_Ldr`) | Gamma under attack | Gamma One. Tigers, need a bit of muscle over here. Sabers coming in! | Gamma WL_Gamma1 Tigers Need a bit of mussle over here, Sabres coming in |
| `ms_had22_014` | Hades' leader (`Gamma_Ldr`) | Gamma 2 under attack | Tigers, we've got some dogs sniffing around Gamma Two! | HadesWl_Tigers, We've got some bitches sniffing round Gamma2 |
| `ms_had22_015` | Hades' leader (`Gamma_Ldr`) | The Krasnaya destroyed | OK, Gamma, clear out and wait for the Yamato. | Hades WL_ Ok Gamma , clear out and wait for the Yamato |
| `ms_had22_016` | Hades' leader (`Gamma_Ldr`) | The Krasnaya destroyed | Over and out. | Hades WL_ Over and out |
| `ms_enq22_012` | Enriquez (`Enq_YamBridge`) | Convoy ships still left | You're going to have to get rid of a few more of those convoy ships before the Yamato can jump in. | Enriquez_your'e gonna have to get rid of a few more of thoes convoy ships before Yamato can jump in |
| `ms_dice22_048` | Diceman (`45TigersWL_Diceman`) | Convoy ships still left | Clear the way, soldiers. Enriquez won't like it if we let these guys jump out. | Diceman_Clear the way soldiers, Enriques wont like it iif we let these guys jump out |
| `ms_moo22_009` | Moose (`45Tigers_Moose`) | Convoy ships still left | Alpha Two, clear these guys. We'll cover. | Moose_Alpha 2, clear these guys, we'll cover |
| `ms_enq22_013` | Enriquez (`Enq_YamBridge`) | The convoy's defenses destroyed | Nice work, pilots. The Yamato's coming in, mind your backs. | Enriques_Nice work pilots yamato coming in, mind y backs |
| `ms_enq22_014` | Enriquez (`Enq_YamBridge`) | The Yamato jumps in, a poor showing | You ought to be ashamed of yourselves. I know I'm ashamed of you. What did you think you were doing out there? | Enriquez_You aught to be ashamed of u're selve, I know I'm ashamed of u, what do u think u were doing out there? |
| `ms_enq22_015` | Enriquez (`Enq_YamBridge`) | The Yamato jumps in, a good showing | Nice work. I'm really proud of you, pilots. The Yamato's jumping in. | Enriquez_Nice work, real proud of u pilots, Yamato jumping in |
| `ms_dice22_049` | Diceman (`45TigersWL_Diceman`) | The Yamato jumps in | Whatever. You'll be a sight for very sore eyes, Enriquez. | Diceman_Whatever....you'll be a sight for very sore eyes Enriquez |
| `ms_dice22_050` | Diceman (`45TigersWL_Diceman`) | The Yamato jumps in | OK, there's a lot of salvage out here, Enriquez. We could do with some Rippers to clear up. | Diceman_ OK, there's a lot of salvage out here, Enriques, could do with some Rippers to clear up |
| `ms_enq22_016` | Enriquez (`Enq_YamBridge`) | The Yamato jumps in | We're on to it. Rippers launching now. | Enriquez_We're on to it, Rippers launching  now |
| `ms_enq22_017` | Enriquez (`Enq_YamBridge`) | The end | Tigers, Ronin, prepare to land. | Enriquez_Tigers, Ronin, prepare to land |
| `ms_dice22_051` | Diceman (`45TigersWL_Diceman`) | The end | Nothing more to be done here. Time to land. | Diceman_nothing more to be done here, time to land |

Some draft lines were toned down for voicing: "lost their balls" became "lost their nerve", "bitches
sniffing round Gamma2" became "dogs sniffing around Gamma Two", and "they'll be buns up" became
"they'll be sitting ducks". The rest keep their wording, swearing included, as the game's other
drafts do.

## The debriefings

Written for the mod, one for each rating the mission can give.

- **Success with the bonus:**
  > Outstanding work, Tigers. The convoy never got near Neptune. The Badinov is destroyed, the troop
  > carriers with her, and the Ronin report the Krasnaya won't trouble anyone again.
  >
  > Command is calling it the closest the Coalition has come to hitting Alliance HQ. You and the
  > Ronin cut them off and broke them up. Well done.
- **Success:**
  > Good work. The convoy has been broken up and the Coalition force has retreated to its own lines.
  >
  > Some of their ships got away, though, and we'll be seeing them again. Next time, finish the job.
- **Partial success:**
  > The convoy didn't reach Neptune, but too much of it got away.
  >
  > You lost sight of the big picture out there. The Badinov should have been crippled before it
  > could fight back, and the bombers paid for the delay.
- **Failure:**
  > That was a mess, pilots. The Badinov escaped, and with her most of the convoy.
  >
  > Command was counting on us to stop that force before it reached Neptune. It's only thanks to the
  > Ronin and the rest of the fleet that it was turned back at all. I expect much better from the
  > Tigers.

## Open points for the mod

The mod leaves the mission's file as the Dreamcast has it, and gives it what it lacks through
OpenReliant's scripting:

- **Saying the lines and the objectives:** mission 22 prints its radio as debug text and sets no
  objectives. The mod's `radio22.luau` hooks `print_debug_message`, and as the mission reaches each
  text, has the radio say the line that stands for it, with its speaker's face
  (`openreliant.radio`), and makes the moment's objective current (`world.set_objective`). The
  objectives' names come from `records.missions[22].objectives`.
- **The convoy's retreat, the mod's own:** once most of the convoy's defenses are down, the mission
  calls the Yamato in and tells the Tigers to land, and leaves the rest of the convoy fighting. The
  mod's `yamato22.luau` has the convoy's ships that can still fly jump out as she arrives, as the
  ITAC's news after the mission has it: the Coalition retreated to its own lines. A ship can fly if
  it has an engine that isn't destroyed, or no engines at all. The Yamato then picks off the big
  ships left behind, and stops once her guns reach each one. The Dreamcast's script has no such
  step.
- **Targeting help, the mod's own:** the last part of the mission is crowded, so the mod's
  `targets22.luau` picks the shield generators for the player. When the Tigers reach the convoy,
  the Badinov's shield generator becomes the target. Each time a shield generator goes down, the
  nearest one left that can be hit becomes the target. If none can be hit yet, such as the
  cruisers' before the Ronin call for help, the first one the mission makes hittable becomes the
  target. Each is also the primary target, so the PRIMARY TARGET key goes back to it.
- **Fixes to the draft script, the mod's own:** the mod's `fixes22.luau` works around flaws of the
  draft script. The first two leave the mission with no way to finish.
  - The script never checks whether the Hades bombers survive, and without their torpedoes the
    cruisers can't be destroyed. The mod makes both Hades invulnerable.
  - A torpedo hit is what destroys a cruiser, and the script counts a hit only on the cruiser that
    torpedo was aimed at. A torpedo can end some other way: from the Hades' jump-in point one
    cruiser stands in front of the other, so the second group of torpedoes can strike the first
    cruiser or its wreck, and the convoy's guns can shoot torpedoes down. The second cruiser is
    then never destroyed. In the mod, once a friendly torpedo is gone, its target explodes three
    seconds later unless it already has, as the script's own hit has it two seconds after the
    strike.
  - The Yamato comes once the script has counted six of the convoy's eight defence ships
    destroyed. Its two Shavrovs can't be destroyed by fighters: the Sharov's main body has 10000
    armour, which takes only hits of 500 or more from a crash or a heavy kind, so the player must
    destroy all six of the others. The script counts each in a trigger that waits two seconds
    after counting, and the game doesn't start a trigger again while its last run still runs, so a
    ship destroyed in those two seconds goes uncounted and the Yamato never comes. In the mod the
    trigger doesn't wait.
  - When the Badinov escapes, the script starts a camera on her, orders her to jump out, and
    disables her at once. A disabled ship isn't drawn, so the camera shows empty space. In the mod
    she is disabled once her jump is done, or after a minute, so the camera shows her leaving.
  - **Unverified:** in the campaign, when the Krasnaya escaped in mission 8, she takes the
    cruisers' place. The script then counts only the first torpedo group's hits on her and needs
    three, though that group holds two torpedoes. Whether the torpedoes' damage alone destroys her
    is not yet checked.
- **Pacing:** the script waits a second or two between texts, long enough to read one, and less
  than the voiced lines take to say. The mod's `radio22.luau` holds the script's wait after each
  voiced text while the radio is busy, so the mission goes on once the line is said, as the PC's
  missions wait for their speech.
- **Faces:** the script's one comms command, as the jump drive comes online, has Moose say
  `mooms1017` by the Dreamcast's pilot number 102, which the PC's pilot table gives Talon, a 45th
  Tigers pilot. The mod's `faces.luau` gives the line Moose, and Alpha 1, the Dreamcast's pilot 8,
  Diceman as the Tigers' leader. The file gives the Ronin, the Yamato and the Mammoths no pilot,
  which leaves them Bandit's: the mod gives them the Ronin, the Yamato's bridge officer and a
  Mammoth pilot, and the other ships their type's pilot (the README's step 5).
- **Voices:** the 134 lines are voiced, and so is Enriquez's briefing, as `dreamcast_brief22`. Stalker and Frenchy, 45th Tigers pilots with no mission lines
  on the PC, are cloned from their wingman calls. Mayday and Striker have no recordings at all, so
  they borrow Cutter's and Juice's voices.
- **Debriefings:** OpenReliant can't yet give a campaign mission debriefings of its own
  ([#984](https://github.com/OpenReliant/openreliant/issues/984)).
