"""
Marktplaats search scraper.
Fetches listings from marktplaats.nl for given search queries.
"""
import re
import time
import requests


# Furniture > Kasten category on Marktplaats
SEARCH_API = "https://www.marktplaats.nl/lrp/api/search"
LISTING_BASE = "https://www.marktplaats.nl"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Accept-Language": "nl-NL,nl;q=0.9",
}

# Marktplaats category IDs: Huis en Inrichting > Meubels > Kasten
L1_CATEGORY = 1031  # Huis en Inrichting
L2_CATEGORY = 1032  # Meubels (kasten sub-category group)


def _api_search(query: str, limit: int = 30, offset: int = 0) -> list[dict]:
    """Call Marktplaats search API and return raw listing dicts."""
    params = {
        "query": query,
        "limit": limit,
        "offset": offset,
        "l1CategoryId": L1_CATEGORY,
        "sortBy": "SORT_INDEX",
        "sortOrder": "DECREASING",
    }
    try:
        resp = requests.get(SEARCH_API, params=params, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data.get("listings", [])
    except Exception as exc:
        print(f"[scraper] Warning: API call failed for '{query}': {exc}")
        return []


def _parse_price(listing: dict) -> float | None:
    """Extract price in euros from a listing dict."""
    price_info = listing.get("priceInfo", {})
    amount = price_info.get("priceCents")
    if amount is not None:
        return amount / 100
    return None


def _parse_listing(raw: dict) -> dict:
    """Normalise a raw API listing into a flat dict."""
    item_id = str(raw.get("itemId", raw.get("id", "")))
    title = raw.get("title", "")
    description = raw.get("description", "")
    price = _parse_price(raw)

    # Build URL
    link = raw.get("vipUrl", "")
    if link and not link.startswith("http"):
        link = LISTING_BASE + link

    location = ""
    seller = raw.get("sellerInformation", {})
    if isinstance(seller, dict):
        location = seller.get("cityName", "")

    date_str = raw.get("date", "")

    return {
        "id": item_id,
        "title": title,
        "description": description,
        "price": price,
        "url": link,
        "location": location,
        "date": date_str,
    }


def fetch_listings(queries: list[str], max_per_query: int = 30) -> list[dict]:
    """
    Run multiple search queries on Marktplaats and return deduplicated listings.
    """
    seen_ids: set[str] = set()
    results: list[dict] = []

    for query in queries:
        raw_listings = _api_search(query, limit=max_per_query)
        for raw in raw_listings:
            listing = _parse_listing(raw)
            if listing["id"] and listing["id"] not in seen_ids:
                seen_ids.add(listing["id"])
                results.append(listing)
        # Be polite to the server
        time.sleep(0.5)

    return results
