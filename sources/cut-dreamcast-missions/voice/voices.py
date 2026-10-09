"""The cast: each voice of the cut missions, and the PC's recorded lines it is cloned from.

The speaker names are those of the reconstruction documents' tables.
"""

import glob
import os
import re

# Voice: the regular expression that picks its recorded lines in the decoded speech archive.
references = {
    "bandit": r"^ms\d+_ban_\d+\.wav$",
    "moose": r"^ms\d+_moo_\d+\.wav$",
    "diceman": r"^ms\d+_dice_\d+\.wav$",
    "enriquez": r"^ms\d+_enq_\d+\.wav$|^enrbr_tag\d+\.wav$",
    # Her briefings' narration, from the holograms of the canon missions (brief<mission>.wav, the
    # movies' sound beside the speech archive's lines).
    "enriquez_brief": r"^brief\d+\.wav$",
    # Her words in person, in the briefing room: the campaign's end and her last words, which the
    # game plays as speech files, as the mod's spoken briefings are.
    "enriquez_room": r"^enddebriefing\.wav$|^enrbr_tag\d+\.wav$",
    # Her spoken briefing at the campaign's end alone, which the mod's spoken briefings are matched
    # to: her last words are mastered much louder.
    "enriquez_spoken": r"^enddebriefing\.wav$",
    "reliant": r"^ms\d+_rel_\d+\.wav$|relbdg|^ms18_reliant",
    "yamato": r"^ms\d+_yam_\d+\.wav$|yambdg",
    "nicolai": r"npet|^ms\d+_nic_|np_res",
    "lueneberg": r"^ms\d+_lun_|luntwo",
    "nanny": r"^ms\d+_nan_\d+\.wav$",
    "stahl": r"stal_|_stl_",
    "boarding": r"^ms11_bshp_",
    "gamma1": r"^ms\d+_gam1_",
    "gamma2": r"^ms\d+_gam2_",
    "cougars": r"cougwl|rtwo",
    "mitchell": r"mitch",
    "pukov": r"apet",
    "ronin": r"ronwl|^ms\d+_ron_",
    "stalker": r"^sta_|staejt|stadth",
    "frenchy": r"^fre_|freejt|fredth",
    "mayday": r"^cut_|cutejt",
    "striker": r"^jui_|juiejt",
    "maulers": r"_tan_",
    "marauders": r"^ms\d+_buc_",
}

# The documents' speaker names, as each table writes them, to the voice that says the line.
speakers = {
    "Bandit": "bandit",
    "Moose": "moose",
    "Diceman": "diceman",
    "Enriquez": "enriquez",
    "The Reliant's bridge officer": "reliant",
    "The Reliant's address system": "reliant",
    "The Yamato's bridge officer": "yamato",
    "Nicolai Petrov": "nicolai",
    "The Lueneberg": "lueneberg",
    "The nanny's pilot": "nanny",
    "Commander Stahl": "stahl",
    "The boarding ship's pilot": "boarding",
    "Gamma 1": "gamma1",
    "Gamma 2": "gamma2",
    "Gamma's leader": "gamma1",
    "Hades' leader": "gamma2",
    "The Cougars' leader": "cougars",
    "The Mitchell's bridge officer": "mitchell",
    "The Gegarin's captain": "pukov",
    "The Ronin's leader": "ronin",
    "Stalker": "stalker",
    "Frenchy": "frenchy",
    "Mayday": "mayday",
    "Striker": "striker",
    "The Maulers' leader": "maulers",
    "The Marauders' leader": "marauders",
}


def files_of(speech_dir, voice):
    """The recorded lines a voice is cloned from."""
    pattern = re.compile(references[voice], re.I)
    return sorted(f for f in glob.glob(os.path.join(speech_dir, "*.wav")) if pattern.search(os.path.basename(f)))
