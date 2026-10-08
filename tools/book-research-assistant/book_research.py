#!/usr/bin/env python3
"""Fetch public bibliographic metadata from Open Library; never reads paid book content."""
import argparse
import csv
import json
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://openlibrary.org/search.json"
FIELDS = "key,title,author_name,first_publish_year"
COLUMNS = ["query", "title", "authors", "first_publish_year", "open_library_url", "status", "notes"]

def search_books(query, limit=5, fetcher=urlopen):
    if not query.strip():
        raise ValueError("Please provide a search query")
    if not 1 <= limit <= 10:
        raise ValueError("Limit must be between 1 and 10")
    url = API + "?" + urlencode({"q": query, "fields": FIELDS, "limit": limit})
    req = Request(url, headers={"User-Agent": "FalahMousaBookResearch/1.0 (https://falahmousa.com)"})
    with fetcher(req, timeout=12) as response:
        data = json.load(response)
    items = []
    for doc in data.get("docs", []):
        key = doc.get("key", "")
        if not key.startswith("/works/"):
            continue
        items.append({
            "query": query,
            "title": doc.get("title", ""),
            "authors": "; ".join(doc.get("author_name", [])[:3]),
            "first_publish_year": doc.get("first_publish_year", ""),
            "open_library_url": "https://openlibrary.org" + key,
            "status": "Unverified",
            "notes": "Metadata only. Confirm publisher, edition and any factual claims independently.",
        })
    return items

def save_csv(records, target):
    with Path(target).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(records)

def main(argv=None):
    parser = argparse.ArgumentParser(description="Public book metadata lookup; not a summary service")
    parser.add_argument("query", nargs="?")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--csv", help="Write metadata to CSV")
    parser.add_argument("--blank-template", help="Create offline claim-review worksheet")
    args = parser.parse_args(argv)
    if args.blank_template:
        with Path(args.blank_template).open("w", encoding="utf-8", newline="") as stream:
            csv.writer(stream).writerow(["claim","source_title","source_url","published_date","status","supporting_evidence","limitations","reviewer"])
        print("Blank claim-review worksheet created")
        return 0
    if not args.query:
        parser.error("A query is required unless --blank-template is specified")
    try:
        records = search_books(args.query, args.limit)
        if args.csv:
            save_csv(records, args.csv)
            print("Saved " + str(len(records)) + " records; bibliographic metadata is not fact-checked")
        else:
            for item in records:
                print(item["title"] + " — " + item["authors"] + " (" + str(item["first_publish_year"]) + ")")
                print(item["open_library_url"])
            if not records:
                print("No matching catalogue records.")
        return 0
    except (ValueError, OSError, json.JSONDecodeError, KeyError) as exc:
        print("Lookup failed: " + str(exc), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
