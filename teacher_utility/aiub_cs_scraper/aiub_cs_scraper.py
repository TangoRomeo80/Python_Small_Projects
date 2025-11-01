#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AIUB News & Events image scraper (CS + ICCA/ICCIT + AJSE) with per-event subfolders

- Crawls https://www.aiub.edu/category/news-events (via ?pageNo=&pageSize=)
- Opens each post, extracts:
    Title, Event Date (Events Date + Year), Organized By, all <img> sources
- Filters to last N years and "relevant" posts:
    * Department of Computer Science / Computer Science
    * Conferences like ICCA / ICCIT (names in organizer or page text)
    * AIUB Journal of Science and Engineering (AJSE)
    * Broader engineering/CS conference/journal signals (configurable below)
- Downloads images to aiub_cs_event_images/<YYYY-MM-DD_Title>_<hash>/...
- Appends rows into aiub_cs_event_images/metadata.csv
"""

import os
import re
import csv
import time
import hashlib
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# ---------------- Basic settings ----------------
BASE = "https://www.aiub.edu"
LIST_URL = f"{BASE}/category/news-events"
HEADERS = {
    "User-Agent": "Rahat-CS-Event-Scraper/1.2 (+contact: your.email@example.com)"
}
OUT_DIR = "aiub_cs_event_images"
META_CSV = os.path.join(OUT_DIR, "metadata.csv")

YEARS_BACK = 5
CUTOFF_DATE = datetime.now() - timedelta(days=365 * YEARS_BACK)
PAGE_SIZE = 50                 # reduce total requests
SLEEP_BETWEEN_REQUESTS = 0.8   # be polite
TIMEOUT = 20                   # seconds
# -------------------------------------------------

# ---------- WIDER FILTER CONFIG ----------
# Relevant if EITHER "Organized By" matches below OR page text matches below.
INCLUDE_ORGANIZER_PATTERNS = [
    r"\bDepartment of Computer Science\b",
    r"\bComputer\s*Science\b",
    r"\bFaculty of Engineering\b",
    r"\bDepartment of EEE\b",
    r"\bEEE\b",
    r"\bIEEE\s+AIUB\b",
    r"\bAIUB Journal of Science and Engineering\b",
    r"\bAJSE\b",
    r"\bICCA\b",  # International Conference on Computing Advancements
    r"\bInternational Conference on Computing Advancements\b",
    r"\bICCIT\b",
    r"\bInternational Conference on Computer and Information Technology\b",
]

INCLUDE_TEXT_PATTERNS = [
    r"\bICCA\b",
    r"\bInternational Conference on Computing Advancements\b",
    r"\bICCIT\b",
    r"\bInternational Conference on Computer and Information Technology\b",
    r"\bAJSE\b",
    r"\bAIUB Journal of Science and Engineering\b",
    r"\bjournal\b",
    r"\bcall for papers\b",
    r"\bspecial issue\b",
    r"\bconference\b",
    r"\bsymposium\b",
    r"\bworkshop\b",
    r"\bCSE\b",
    r"\bComputer\s*Science\b",
    r"\bEngineering\b",
]
# ----------------------------------------


def any_match(patterns, text):
    """Return True if any regex in `patterns` matches `text` (case-insensitive)."""
    if not text:
        return False
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return True
    return False


def get_soup(url):
    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "lxml")


def normalize_url(src):
    if not src:
        return None
    return urljoin(BASE, src.strip())


def unique_name_from_url(url):
    """Create a stable short-ish filename from the URL."""
    h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
    path = urlparse(url).path
    base = os.path.basename(path) or "image"
    base = re.sub(r"[^A-Za-z0-9._-]+", "_", base)
    return f"{h}_{base}"


def event_subfolder_for(data):
    """
    Create a unique, readable folder name per event:
    <YYYY-MM-DD>_<sanitized title>_<8-char hash of post URL>
    """
    date_part = data["event_dt"].strftime("%Y-%m-%d") if data["event_dt"] else "undated"
    safe_title = re.sub(r"[^A-Za-z0-9._ -]+", "_", data["title"]).strip("_ ")[:80] or "event"
    short = hashlib.sha1(data["url"].encode("utf-8")).hexdigest()[:8]
    folder = f"{date_part}_{safe_title}_{short}"
    return os.path.join(OUT_DIR, folder)


def _find_value_after_label(soup, label):
    """
    Find a textual value appearing after a label like 'Events Date' or 'Year'.
    Heuristic to handle AIUB's layout variations.
    """
    lab = soup.find(string=re.compile(rf"^\s*{label}\s*:?\s*$", re.IGNORECASE))
    if not lab:
        return None
    node = lab.parent
    for _ in range(8):
        node = node.find_next(string=True)
        if not node:
            break
        val = node.strip()
        if val and not re.match(rf"^\s*{label}\s*:?\s*$", val, re.IGNORECASE):
            return val
    return None


def _parse_event_datetime(soup):
    """
    Try to parse a concrete datetime for the event.
    Preferred: "Events Date" + "Year"
    Fallback: a 'Published Date' cluster with day Month Year
    """
    events_date_str = _find_value_after_label(soup, "Events Date")
    year_str = _find_value_after_label(soup, "Year")

    if events_date_str and year_str and year_str.isdigit():
        m = re.match(r"([A-Za-z]+)\s+(\d{1,2})", events_date_str)
        if m:
            month_name, day_str = m.group(1), m.group(2)
            for fmt in ("%d %B %Y", "%d %b %Y"):
                try:
                    return datetime.strptime(f"{day_str} {month_name} {year_str}", fmt)
                except ValueError:
                    pass

    published_block = soup.find(string=re.compile(r"Published Date", re.IGNORECASE))
    if published_block:
        around = published_block.parent.get_text(" ", strip=True)
        m = re.search(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", around)
        if m:
            d, mon, y = m.groups()
            for fmt in ("%d %B %Y", "%d %b %Y"):
                try:
                    return datetime.strptime(f"{d} {mon} {y}", fmt)
                except ValueError:
                    pass
    return None


def parse_post(url):
    """
    Parse a single post page.
    Returns: dict(title, url, organized_by, event_dt, page_text, images[list])
    """
    soup = get_soup(url)

    h1 = soup.find(["h1", "h2"])
    title = (h1.get_text(strip=True) if h1 else "").strip()

    organized_by = _find_value_after_label(soup, "Organized By") or ""

    event_dt = _parse_event_datetime(soup)

    page_text = soup.get_text(" ", strip=True)

    img_urls = set()
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or img.get("data-original")
        url_abs = normalize_url(src)
        if url_abs and url_abs.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
            img_urls.add(url_abs)

    return {
        "title": title,
        "url": url,
        "organized_by": organized_by,
        "event_dt": event_dt,
        "page_text": page_text,
        "images": sorted(img_urls),
    }


def iter_listing_pages():
    """
    Iterate over listing pages and yield a list of post URLs per page.
    Uses a heuristic for links: accepts top-level '/slug' post paths,
    skips category/faculty/notice/etc.
    """
    page_no = 1
    while True:
        list_url = f"{LIST_URL}?pageNo={page_no}&pageSize={PAGE_SIZE}"
        soup = get_soup(list_url)

        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith("/") and href.count("/") == 1 and len(href) > 2:
                if any(skip in href for skip in ("/category/", "/faculties/", "/notice", "/notices", "/newsletter")):
                    continue
                links.append(urljoin(BASE, href))

        seen = set()
        unique_links = []
        for u in links:
            if u not in seen:
                seen.add(u)
                unique_links.append(u)

        if not unique_links:
            break

        yield unique_links
        page_no += 1
        time.sleep(SLEEP_BETWEEN_REQUESTS)


def download(url, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    name = unique_name_from_url(url)
    path = os.path.join(dest_dir, name)
    if os.path.exists(path):
        return path
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, stream=True)
    r.raise_for_status()
    with open(path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
    return path


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    write_header = not os.path.exists(META_CSV)
    fcsv = open(META_CSV, "a", newline="", encoding="utf-8")
    w = csv.writer(fcsv)
    if write_header:
        w.writerow(["title", "url", "organized_by", "event_date_iso", "image_path"])

    cutoff = CUTOFF_DATE
    print(f"Cutoff (last {YEARS_BACK} years): {cutoff.date()}")

    for links in iter_listing_pages():
        for post_url in links:
            try:
                data = parse_post(post_url)
            except Exception as e:
                print(f"[WARN] Failed to parse {post_url}: {e}")
                time.sleep(SLEEP_BETWEEN_REQUESTS)
                continue

            # --- Date filter ---
            if data["event_dt"] and data["event_dt"] < cutoff:
                continue

            # --- Relevance filter (broadened) ---
            org_text = data.get("organized_by", "")
            page_text = data.get("page_text", "")
            is_relevant = (
                any_match(INCLUDE_ORGANIZER_PATTERNS, org_text) or
                any_match(INCLUDE_TEXT_PATTERNS, page_text)
            )
            if not is_relevant:
                continue

            # --- Per-event subfolder (unique) ---
            event_dir = event_subfolder_for(data)

            # --- Download images + write metadata ---
            if not data["images"]:
                print(f"[INFO] No images in: {data['title']}")

            for img_url in data["images"]:
                try:
                    saved = download(img_url, event_dir)
                    w.writerow([
                        data["title"], data["url"], data["organized_by"],
                        data["event_dt"].date().isoformat() if data["event_dt"] else "",
                        saved,
                    ])
                except Exception as e:
                    print(f"[WARN] Image failed ({img_url}): {e}")

            time.sleep(SLEEP_BETWEEN_REQUESTS)

    fcsv.close()
    print("Done. Images and metadata saved under:", OUT_DIR)


if __name__ == "__main__":
    main()
