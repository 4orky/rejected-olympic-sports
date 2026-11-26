#!/usr/bin/env python3
"""Rejected Olympic Sports — make.fun bounty
u-motasimfuad-rejected-olympic-sports-9d83e7da

Writes one made-up Olympic sport the Games turned down to
/output/entry.txt: a single line, 1-200 characters, in the voice of a
broadcaster who has to read it out with a straight face.

How the line was chosen: twelve original one-liners were drafted by
hand and marked out of ten on the five things the house judge weighs,
in its order — how funny the rejected sport is, whether the joke lands
in a single read with the twist before the line ends, whether it sounds
like a real event a broadcaster would have to explain, whether every
word earns its place, and whether it is quotable. The highest total
wins; a tie goes to the shorter line. The winning line was then
reworked once more (see the note on WINNER) before it was frozen.
"""

# (line, funny, one-read twist, broadcast voice, tight, quotable)
DRAFTS = [
    ("Competitive Hide and Seek: the final was abandoned after eleven "
     "days \u2014 nobody could find the defending champion.",
     9, 9, 9, 9, 9),
    ("Synchronised Procrastination: first scheduled for 2016, then 2020, "
     "then 2024; the athletes still have not started.",
     9, 9, 8, 9, 7),
    ("Synchronised Queueing: four athletes stand in line for four hours; "
     "gold goes to whoever complains the least.",
     8, 7, 8, 8, 8),
    ("Marathon Apologising: athletes say sorry for 26 miles straight; "
     "disqualified if any apology sounds sincere.",
     8, 8, 7, 8, 7),
    ("Synchronised Eye-Rolling: judged on height, rotation and contempt; "
     "the 2016 final ended in a staring contest.",
     8, 8, 7, 8, 7),
    ("Synchronised Sighing: teams of four sigh in perfect unison; points "
     "deducted for any sigh that sounds rehearsed.",
     8, 7, 8, 8, 7),
    ("Extreme Ironing: competitors press shirts on a cliff edge in a "
     "gale; points deducted for every crease and every fall.",
     8, 7, 8, 8, 7),
    ("Extreme Sitting: competitors sit perfectly still for six hours; "
     "the first to check their phone loses the gold.",
     7, 7, 8, 8, 8),
    ("Competitive Dog-Walking: athletes walk twelve dogs at once; gold "
     "goes to whoever is still holding all twelve leads.",
     7, 7, 8, 8, 8),
    ("Competitive Umbrella Folding: athletes fold a wet umbrella "
     "one-handed in a storm; the crowd goes silent for the final click.",
     7, 7, 8, 7, 8),
    ("Speed Tax Returns: athletes file a full return in under ten "
     "minutes; the winner is whoever cries last.",
     7, 8, 7, 8, 7),
    ("Competitive Napping: athletes sleep for eight hours while judges "
     "score their snoring for style, rhythm and commitment.",
     7, 7, 8, 7, 7),
]

# The winning line, frozen after its second pass. First draft: "the
# final lasted eleven days because nobody could find the defending
# champion." That version was flat — "lasted" reports nothing going
# wrong, and "because" explains the joke instead of landing it. The
# rework swaps in the broadcaster's verdict for a failed event, "was
# abandoned", and puts a dash-beat before the punch, so the punch word
# "champion" still closes the line. 112 characters.
WINNER = DRAFTS[0][0]

# SHA-256 of WINNER, pinned as a constant so the output check does not
# grade its own homework: if the table above were corrupted, the hash
# would catch it instead of agreeing with it.
WINNER_SHA256 = "68f6681a37f4798b328d27f34d5bc7922ff7453d302711a716488c09c7054586"

# Worn-out angles the judge's brief warns against; none of the twelve
# drafts is built on one of them.
TIRED_WORDS = ("traffic", "gravity", "weather")


def total_marks(draft):
    """Add up a draft's five marks; the line itself is element zero."""
    return sum(draft[1:])


def choose(drafts):
    """Return the strongest draft: highest total, then shortest line."""
    best_line = None
    best_key = None
    for draft in drafts:
        line = draft[0]
        if not 1 <= len(line) <= 200:
            raise ValueError(f"draft breaks the 200-character gate: {line!r}")
        if "\n" in line or not line.strip():
            raise ValueError(f"draft is not one clean line: {line!r}")
        if any(word in line.lower() for word in TIRED_WORDS):
            raise ValueError(f"draft leans on a tired angle: {line!r}")
        key = (total_marks(draft), -len(line))
        if best_key is None or key > best_key:
            best_key, best_line = key, line
    return best_line


def write_entry(line):
    """Write the line to /output/entry.txt and prove it landed intact."""
    import hashlib
    import os
    import sys

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(line)
    with open("/output/entry.txt", "rb") as handle:
        raw = handle.read()
    if raw.decode("utf-8") != line:
        print("error: entry.txt came back different from the chosen line",
              file=sys.stderr)
        sys.exit(1)
    if hashlib.sha256(raw).hexdigest() != WINNER_SHA256:
        print("error: entry.txt hash does not match the frozen winner",
              file=sys.stderr)
        sys.exit(1)
    if not 1 <= len(line) <= 200:
        print(f"error: entry is {len(line)} characters, gate is 1-200",
              file=sys.stderr)
        sys.exit(1)
    print(line)


if __name__ == "__main__":
    picked = choose(DRAFTS)
    if picked != WINNER:
        raise SystemExit("error: chooser and frozen winner disagree")
    write_entry(picked)
