"""
Keyword-based scorer for vintage Danish/Scandinavian cabinet listings.

Style profile based on loui.store vintage kasten:
- Era: 1950s–1970s mid-century modern
- Style: Danish / Scandinavian design
- Materials: teak, oak (eiken), rosewood (palissander)
- Brands: Pastoe, Topform, Eeka, Cees Braakman, Deense merken
- Types: ladekast, kledingkast, dressoir, highboard, lowboard,
         roldeurkast (tambour), papierkast, buffetkast, vitrinekast
"""

import re

# ---------------------------------------------------------------------------
# Scoring tables
# ---------------------------------------------------------------------------

# Each entry: (regex_pattern, score)
POSITIVE_RULES: list[tuple[str, int]] = [
    # Strong style indicators
    (r"\bteak\b", 5),
    (r"\bpastoe\b", 5),
    (r"\bdeens\b", 4),
    (r"\bdanish\b", 4),
    (r"\bscandinavisch\b", 4),
    (r"\bscandinavi[ae]\b", 4),
    (r"\bpalissander\b", 4),
    (r"\bcees braakman\b", 5),
    (r"\btopform\b", 4),
    (r"\beeka\b", 4),
    (r"\bnordic\b", 3),
    (r"\bmid.?century\b", 4),
    (r"\bmidcentury\b", 4),

    # Era keywords
    (r"\bjaren\s*['\u2019]?5[05]\b", 4),  # jaren 50 / jaren '50
    (r"\bjaren\s*['\u2019]?6[05]\b", 4),
    (r"\bjaren\s*['\u2019]?7[05]\b", 3),
    (r"\b195\d\b", 3),
    (r"\b196\d\b", 3),
    (r"\b197\d\b", 2),
    (r"\bretro\b", 2),
    (r"\bvintage\b", 2),

    # Materials
    (r"\beiken\b", 3),
    (r"\beikenhout\b", 3),
    (r"\bwalnoot\b", 2),
    (r"\btropisch\s+hout\b", 2),
    (r"\bfineer\b", 1),
    (r"\bmassief\s+hout\b", 2),

    # Furniture types (right kind of item)
    (r"\bladekast\b", 2),
    (r"\bdressoir\b", 2),
    (r"\bhighboard\b", 2),
    (r"\blowboard\b", 2),
    (r"\bsideboard\b", 2),
    (r"\bbuffetkast\b", 2),
    (r"\broldeurkast\b", 2),
    (r"\btambour\b", 2),
    (r"\bpapierkast\b", 2),
    (r"\bvitrinekast\b", 1),
    (r"\bkledingkast\b", 1),
    (r"\bdivisienkast\b", 2),

    # General quality signals
    (r"\bgerestaureerd\b", 1),
    (r"\bopgeknapt\b", 1),
    (r"\bgoede\s+staat\b", 1),
    (r"\bdesign\b", 1),
]

NEGATIVE_RULES: list[tuple[str, int]] = [
    # Wrong brand / style
    (r"\bikea\b", -10),
    (r"\bbilly\b", -5),
    (r"\bcallax\b", -5),
    (r"\bpax\b", -5),

    # Wrong materials
    (r"\bspaanplaat\b", -5),
    (r"\bmdf\b", -5),
    (r"\bmelamime\b", -3),
    (r"\bplastic\b", -4),

    # Completely different items
    (r"\bkoelkast\b", -20),
    (r"\bvrieskast\b", -20),
    (r"\bwijnklimaatkast\b", -10),
    (r"\bdrankkast\b", -5),
    (r"\bserverkast\b", -10),
    (r"\bgereedschapskast\b", -10),
    (r"\bkleedkast\b", -3),

    # Condition issues
    (r"\bdefect\b", -3),
    (r"\bbeschadigd\b", -2),
]

MIN_SCORE = 3  # minimum score to consider a listing a match


def _normalise(text: str) -> str:
    return text.lower()


def score_listing(listing: dict) -> int:
    """Return an integer match score for a listing. Higher = better match."""
    haystack = _normalise(
        f"{listing.get('title', '')} {listing.get('description', '')}"
    )

    total = 0
    for pattern, points in POSITIVE_RULES:
        if re.search(pattern, haystack):
            total += points
    for pattern, points in NEGATIVE_RULES:
        if re.search(pattern, haystack):
            total += points  # points are already negative

    return total


def is_match(listing: dict, min_score: int = MIN_SCORE) -> bool:
    return score_listing(listing) >= min_score


def filter_and_rank(listings: list[dict], min_score: int = MIN_SCORE) -> list[dict]:
    """Return listings that match, sorted best-first, with score attached."""
    scored = []
    for listing in listings:
        s = score_listing(listing)
        if s >= min_score:
            scored.append({**listing, "score": s})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored
