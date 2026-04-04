"""
Marktplaats vintage kast monitor.

Usage:
    python -m scraper.main              # check for new matches, show results
    python -m scraper.main --all        # show all matches (ignore seen list)
    python -m scraper.main --reset      # clear seen-listings history and exit
    python -m scraper.main --max-price 500   # only show listings below €500
    python -m scraper.main --min-score 5     # stricter matching
"""
import argparse
import sys

from scraper.marktplaats import fetch_listings
from scraper.matcher import filter_and_rank
from scraper import storage

# ---------------------------------------------------------------------------
# Search queries – cast a wide net, the matcher will filter
# ---------------------------------------------------------------------------
SEARCH_QUERIES = [
    "vintage kast teak",
    "vintage kast deens design",
    "vintage ladekast",
    "vintage dressoir teak",
    "scandinavisch vintage kast",
    "deens design kast",
    "pastoe kast",
    "jaren 60 kast",
    "jaren 50 kast",
    "mid century kast",
]


def format_price(price: float | None) -> str:
    if price is None:
        return "prijs onbekend"
    return f"€{price:,.0f}".replace(",", ".")


def print_listing(listing: dict, index: int) -> None:
    score = listing.get("score", "?")
    price = format_price(listing.get("price"))
    title = listing.get("title", "(geen titel)")
    url = listing.get("url", "")
    location = listing.get("location", "")
    date = listing.get("date", "")

    print(f"\n{'─' * 60}")
    print(f"#{index}  [{score} punten]  {price}")
    print(f"   {title}")
    if location:
        print(f"   📍 {location}  {date}")
    print(f"   {url}")


def run(args: argparse.Namespace) -> None:
    if args.reset:
        storage.reset()
        print("Geziene advertenties gewist.")
        return

    print(f"Zoeken op Marktplaats ({len(SEARCH_QUERIES)} zoekopdrachten)...")
    all_listings = fetch_listings(SEARCH_QUERIES, max_per_query=30)
    print(f"  {len(all_listings)} unieke advertenties gevonden.")

    # Filter on minimum score
    matches = filter_and_rank(all_listings, min_score=args.min_score)
    print(f"  {len(matches)} advertenties matchen het stijlprofiel.")

    # Filter on price
    if args.max_price is not None:
        matches = [m for m in matches if m.get("price") is None or m["price"] <= args.max_price]
        print(f"  {len(matches)} advertenties onder €{args.max_price:,.0f}.")

    # Filter out already-seen listings (unless --all)
    if not args.all:
        matches = storage.filter_new(matches)
        print(f"  {len(matches)} nieuwe advertenties (nog niet eerder gezien).")

    if not matches:
        print("\nGeen nieuwe matches gevonden. Probeer het later opnieuw.")
        return

    print(f"\n{'=' * 60}")
    print(f"  {len(matches)} nieuwe vintage kasten gevonden!")
    print(f"{'=' * 60}")

    for i, listing in enumerate(matches, start=1):
        print_listing(listing, i)

    print(f"\n{'─' * 60}")
    print(f"Klaar. Sla de URLs op die je interessant vindt!")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Marktplaats vintage kast monitor"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Toon alle matches, ook al eerder geziene advertenties",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Wis de lijst van eerder geziene advertenties",
    )
    parser.add_argument(
        "--max-price",
        type=float,
        default=None,
        metavar="EURO",
        help="Maximale prijs in euro (bijv. 500)",
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=3,
        metavar="N",
        help="Minimale matchscore (standaard: 3)",
    )
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
