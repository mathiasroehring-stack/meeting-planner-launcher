#!/usr/bin/env python3
"""Build timeanddate city ID dataset from worldclock URLs."""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "public" / "timeanddate-cities.json"

# Verified IDs when scraping fails or returns unrelated meeting-planner links.
VERIFIED_IDS: dict[str, int] = {
    "new-zealand/auckland": 22,
    "new-zealand/wellington": 264,
    "new-zealand/christchurch": 951,
    "india/delhi": 771,
}

# Curated worldclock paths (country/slug) — expand as needed
PATHS = [
    "new-zealand/auckland",
    "new-zealand/wellington",
    "new-zealand/christchurch",
    "new-zealand/dunedin",
    "new-zealand/hamilton-nz",
    "australia/sydney",
    "australia/melbourne",
    "australia/brisbane",
    "australia/perth",
    "australia/adelaide",
    "australia/canberra",
    "australia/hobart",
    "uk/london",
    "uk/edinburgh",
    "uk/manchester",
    "uk/birmingham",
    "usa/new-york",
    "usa/los-angeles",
    "usa/chicago",
    "usa/san-francisco",
    "usa/seattle",
    "usa/denver",
    "usa/houston",
    "usa/miami",
    "usa/boston",
    "usa/washington-dc",
    "usa/san-diego",
    "usa/phoenix",
    "usa/atlanta",
    "usa/dallas",
    "usa/minneapolis",
    "usa/detroit",
    "usa/portland-or",
    "usa/austin",
    "canada/toronto",
    "canada/vancouver",
    "canada/montreal",
    "canada/calgary",
    "canada/ottawa",
    "germany/berlin",
    "germany/munich",
    "germany/frankfurt",
    "germany/hamburg",
    "france/paris",
    "france/lyon",
    "france/marseille",
    "netherlands/amsterdam",
    "belgium/brussels",
    "switzerland/zurich",
    "switzerland/geneva",
    "austria/vienna",
    "spain/madrid",
    "spain/barcelona",
    "italy/rome",
    "italy/milan",
    "portugal/lisbon",
    "sweden/stockholm",
    "norway/oslo",
    "denmark/copenhagen",
    "finland/helsinki",
    "poland/warsaw",
    "czech-republic/prague",
    "hungary/budapest",
    "greece/athens",
    "turkey/istanbul",
    "russia/moscow",
    "russia/saint-petersburg",
    "ukraine/kyiv",
    "israel/jerusalem",
    "israel/tel-aviv",
    "uae/dubai",
    "saudi-arabia/riyadh",
    "india/mumbai",
    "india/delhi",
    "india/bangalore",
    "india/chennai",
    "india/kolkata",
    "india/hyderabad",
    "india/pune",
    "china/beijing",
    "china/shanghai",
    "china/hong-kong",
    "china/shenzhen",
    "china/guangzhou",
    "japan/tokyo",
    "japan/osaka",
    "south-korea/seoul",
    "taiwan/taipei",
    "singapore/singapore",
    "malaysia/kuala-lumpur",
    "indonesia/jakarta",
    "thailand/bangkok",
    "vietnam/ho-chi-minh",
    "philippines/manila",
    "australia/sydney",
    "south-africa/johannesburg",
    "south-africa/cape-town",
    "egypt/cairo",
    "nigeria/lagos",
    "kenya/nairobi",
    "brazil/sao-paulo",
    "brazil/rio-de-janeiro",
    "argentina/buenos-aires",
    "chile/santiago",
    "colombia/bogota",
    "mexico/mexico-city",
    "mexico/monterrey",
    "ireland/dublin",
    "iceland/reykjavik",
    "romania/bucharest",
    "serbia/belgrade",
    "croatia/zagreb",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch(path: str) -> str | None:
    url = f"https://www.timeanddate.com/worldclock/{path}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError:
        return None


def parse_city(html: str, path: str) -> dict | None:
    ids = re.findall(r"[?&]p1=(\d+)", html)
    if not ids:
        return None
    title = re.search(r"<title>Current Local Time in ([^,|<]+)", html)
    name = title.group(1).strip() if title else path.split("/")[-1].replace("-", " ").title()
    lat = re.search(r'"latitude"\s*:\s*(-?\d+\.?\d*)', html)
    lng = re.search(r'"longitude"\s*:\s*(-?\d+\.?\d*)', html)
    return {
        "id": int(ids[0]),
        "name": name,
        "path": path,
        "lat": float(lat.group(1)) if lat else None,
        "lng": float(lng.group(1)) if lng else None,
    }


def enrich_coords(city: dict) -> dict:
    if city.get("lat") is not None:
        return city
    query = urllib.parse.quote(f"{city['name']}")
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
    req = urllib.request.Request(url, headers={"User-Agent": "MeetingPlannerTool/1.0"})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=30).read())
        if data:
            city["lat"] = float(data[0]["lat"])
            city["lng"] = float(data[0]["lon"])
    except Exception:
        pass
    time.sleep(1.1)
    return city


def main() -> None:
    import urllib.parse

    cities: list[dict] = []
    seen: set[int] = set()
    for path in PATHS:
        html = fetch(path)
        if not html:
            print("skip", path)
            time.sleep(0.5)
            continue
        parsed = parse_city(html, path)
        if not parsed:
            continue
        if path in VERIFIED_IDS:
            parsed["id"] = VERIFIED_IDS[path]
        if parsed["id"] in seen:
            continue
        seen.add(parsed["id"])
        cities.append(enrich_coords(parsed))
        print("ok", parsed["id"], parsed["name"])
        time.sleep(0.4)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cities, indent=2), encoding="utf-8")
    print(f"Wrote {len(cities)} cities to {OUT}")


if __name__ == "__main__":
    main()
