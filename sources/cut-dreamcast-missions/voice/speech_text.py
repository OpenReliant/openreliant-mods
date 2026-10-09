"""How the lines' words are spoken and checked: the game's names, as its voices say them, and how
much of a line's words Whisper hears."""

import re

NAMES = {
    "gegarin", "berijev", "lueneberg", "kurgens", "kurgen", "basilisks", "basilisk", "badinov", "cougars",
    "shavrov", "gurevich", "kafelnikof", "ronin", "hades", "gamma", "rippers", "yamato", "petrov", "nicolai",
    "ivan", "kamov", "kamovs", "kossacs", "sabers", "laggs", "lagg", "krasnaya", "reliant", "mitchell",
    "stahl", "enriquez", "diceman", "bandit", "moose", "tigers", "volunteers", "fortyfifth", "luda",
}


# How the game's voices say some names, spelled for the voice model: Enriquez's briefings say
# "Berezhov" for the Berijev class and "Pukoff" for the Pukov, and the Gegarin is named for
# Gagarin.
SAY = {"Gegarin": "Gagarin", "Berijev": "Berezhov", "Badinov": "Badanov", "Gurevich": "Gurevitch"}


def spoken(text):
    for written, said in SAY.items():
        text = text.replace(written, said)
    return text


def words_of(text):
    return re.sub(r"[^a-z0-9' ]", " ", text.lower().replace("-", "")).replace("'", "").split()


def heard_share(heard, wanted):
    want = [w for w in words_of(wanted) if w not in NAMES]
    if not want:
        return 1.0
    got = set(words_of(heard))
    return sum(1 for w in want if w in got) / len(want)


# Words Whisper writes its own way: digits, "OK", and the Czar as "Tsar".
WRITTEN = {"1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight",
           "9": "nine", "ok": "okay", "tsar": "czar"}
# The game's names, as written and as spoken, which Whisper may spell its own way.
SPOKEN_NAMES = NAMES | {w for said in SAY.values() for w in words_of(said)} | {"czar", "kafelnikof", "kurgen"}


def normal(word):
    """A word as compared: Whisper's spelling made the briefings', and doubled letters single, so
    that "refuelling" and "refueling" match."""
    return re.sub(r"(.)\1", r"\1", WRITTEN.get(word, word))


def is_name(word):
    return word in SPOKEN_NAMES or (word.endswith("s") and word[:-1] in SPOKEN_NAMES)


def score(heard, piece):
    """How right a piece sounds, best first: the share of its words heard, other than names,
    whether its first word is among the first heard, and how far the count of words is off, which
    a dropped or repeated word shows."""
    spaced = [normal(w) for w in words_of(heard.replace("-", " "))]
    got = set(spaced) | {normal(w) for w in words_of(heard)}
    written = words_of(spoken(piece).replace("-", " "))
    want = [normal(w) for w in written if not is_name(w)]
    share = sum(1 for w in want if w in got) / len(want) if want else 1.0
    first = is_name(written[0]) or normal(written[0]) in spaced[:3]
    # Hyphens joined and split, either way: "re-arm" is one word or two.
    counts = (len(spaced), len(words_of(heard))), (len(written), len(words_of(spoken(piece))))
    off = min(abs(h - w) for h in counts[0] for w in counts[1])
    return share, first, -off


def right(mark):
    share, first, off = mark
    return share == 1 and first and off == 0
